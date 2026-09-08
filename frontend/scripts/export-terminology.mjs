/**
 * Exports the terminology dictionary to the backend.
 *
 *     npm run terminology:export
 *
 * The dictionary is authored once, in TypeScript, at
 * `src/content/terminology/*.ts` — that is where the types, the docs and the
 * review live. The backend needs the same data for three things it cannot do
 * from the client: bilingual course search, the AI tutor's language policy,
 * and the content linter. Rather than maintain a second hand-written copy
 * (which would drift the moment someone adds a term), this writes a
 * generated JSON snapshot to `backend/app/content/ai_terms.json`.
 *
 * Why it evaluates the source instead of importing it: Node cannot import a
 * `.ts` module without a loader, and adding a TypeScript runtime as a
 * dependency just to move ~70 rows of data is not worth it. The three
 * declarations below are plain data literals — no imports, no calls, no
 * template strings — so the script slices each literal out of its own
 * first-party source file and evaluates it in isolation.
 *
 * The generated file is committed. CI does not regenerate it; if you edit the
 * dictionary and forget to run this, `pytest tests/test_terminology.py` fails
 * on the count check that the backend and frontend disagree.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const termsDir = join(here, '..', 'src', 'content', 'terminology')
const outFile = resolve(here, '..', '..', 'backend', 'app', 'content', 'ai_terms.json')

/** Slice a `export const NAME<...> = <literal>` data literal out of a source file. */
function extractLiteral(source, name, open, close) {
  const declaration = source.indexOf(`export const ${name}`)
  if (declaration === -1) throw new Error(`${name} not found`)

  // Start after the `=`, not after the name: the type annotation in
  // `export const TECH_NAMES: string[] = [...]` contains the opening
  // bracket too, and matching it would yield an empty array.
  const assignment = source.indexOf('=', declaration)
  if (assignment === -1) throw new Error(`${name}: no assignment`)

  const start = source.indexOf(open, assignment)
  if (start === -1) throw new Error(`${name}: no opening ${open}`)

  let depth = 0
  let inString = null
  for (let i = start; i < source.length; i++) {
    const char = source[i]
    if (inString) {
      if (char === '\\') i++
      else if (char === inString) inString = null
      continue
    }
    if (char === "'" || char === '"' || char === '`') {
      inString = char
      continue
    }
    if (char === open) depth++
    else if (char === close) {
      depth--
      if (depth === 0) {
        // A first-party data literal from our own source tree — no
        // identifiers, no calls, nothing to resolve at evaluation time.
        return new Function(`return ${source.slice(start, i + 1)}`)()
      }
    }
  }
  throw new Error(`${name}: unbalanced ${open}${close}`)
}

const terms = extractLiteral(
  readFileSync(join(termsDir, 'ai-terms.ts'), 'utf8'),
  'AI_TERMS',
  '{',
  '}'
)
const techNames = extractLiteral(
  readFileSync(join(termsDir, 'tech-names.ts'), 'utf8'),
  'TECH_NAMES',
  '[',
  ']'
)
const roles = extractLiteral(
  readFileSync(join(termsDir, 'job-roles.ts'), 'utf8'),
  'JOB_ROLES',
  '[',
  ']'
)

const payload = {
  _generated: 'npm run terminology:export — edit frontend/src/content/terminology/*.ts instead',
  version: 1,
  terms,
  tech_names: techNames,
  job_roles: roles,
}

mkdirSync(dirname(outFile), { recursive: true })
writeFileSync(outFile, `${JSON.stringify(payload, null, 2)}\n`, 'utf8')

console.log(
  `terminology → ${outFile}\n  ${Object.keys(terms).length} terms, ` +
    `${techNames.length} technology names, ${roles.length} job roles`
)
