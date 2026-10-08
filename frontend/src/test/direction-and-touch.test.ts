import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { describe, expect, it } from 'vitest'

/**
 * Static guards for two things jsdom cannot measure.
 *
 * jsdom has no layout engine, so it cannot show that a screen *looks* right in
 * right-to-left or on a phone. What it can do is stop the common ways of getting
 * that wrong from being written: a physical `ml-4` / `text-left` silently breaks
 * RTL (the arrow ends up on the wrong side, the padding on the wrong edge), and
 * a control without a touch-sized target is unusable on a phone. The real
 * rendering is checked in a browser against the running app.
 */
const SRC = join(__dirname, '..')

function sourceFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((entry) => {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) return sourceFiles(full)
    return /\.tsx$/.test(entry) && !/\.test\.tsx$/.test(entry) ? [full] : []
  })
}

// Every screen and component of the learning experience.
const NEW_SURFACES = [
  ...sourceFiles(join(SRC, 'components', 'learning')),
  ...['learn', 'explore', 'paths', 'courses', 'onboarding', 'roadmaps'].flatMap((d) => sourceFiles(join(SRC, 'app', d))),
  join(SRC, 'app', 'profile', 'learning', 'page.tsx'),
  // Sign-up, the legal documents, the home page and the acceptance dialog.
  ...sourceFiles(join(SRC, 'components', 'legal')),
  ...['terms', 'privacy'].flatMap((d) => sourceFiles(join(SRC, 'app', d))),
  join(SRC, 'app', 'page.tsx'),
  join(SRC, 'app', 'auth', 'register', 'page.tsx'),
  join(SRC, 'components', 'layout', 'LegalGate.tsx'),
  // The shell every signed-in page sits in: the sidebar sits on the right in Arabic and the
  // left in English only because none of this says "left" or "right".
  ...['AppShell', 'Sidebar', 'ShellHeader', 'MobileMenu', 'AccountMenu', 'CreditsBadge', 'GlobalSearch', 'PageHeader', 'ThemeToggle', 'LegalFooter']
    .map((name) => join(SRC, 'components', 'layout', `${name}.tsx`)),
  join(SRC, 'components', 'brand', 'MasarMark.tsx'),
]

// Physical-direction utilities. The logical twins (ms-/me-/ps-/pe-/start-/end-/
// text-start/text-end/border-s/rounded-s) flip with the reading direction; these
// do not.
const PHYSICAL = [
  /(?:^|[\s"'`:])-?(?:ml|mr|pl|pr)-(?:\d|\[|px|auto)/,
  /(?:^|[\s"'`:])-?(?:left|right)-(?:\d|\[|0\b|full|1\/2)/,
  /(?:^|[\s"'`:])text-(?:left|right)\b/,
  /(?:^|[\s"'`:])(?:rounded|border)-(?:l|r|tl|tr|bl|br)(?:-|\s|"|'|`)/,
  /(?:^|[\s"'`:])float-(?:left|right)\b/,
]

describe('right-to-left safety of the learning screens', () => {
  it('covers the files it claims to (guards against the scan silently matching nothing)', () => {
    const names = NEW_SURFACES.map((f) => relative(SRC, f).replace(/\\/g, '/'))
    expect(names).toEqual(expect.arrayContaining([
      'components/learning/OnboardingFlow.tsx',
      'components/learning/CourseCard.tsx', 'components/learning/Pickers.tsx',
      'app/learn/page.tsx', 'app/explore/page.tsx', 'app/paths/page.tsx', 'app/paths/[slug]/page.tsx',
      'app/courses/[slug]/page.tsx', 'app/onboarding/learning-profile/page.tsx', 'app/profile/learning/page.tsx',
      'components/learning/SkillPicker.tsx', 'components/learning/SkillsStep.tsx', 'components/learning/MySkills.tsx',
      'components/learning/YourMasarCard.tsx', 'components/legal/LegalDocumentPage.tsx',
      'components/layout/LegalFooter.tsx', 'components/layout/LegalGate.tsx',
      'app/page.tsx', 'app/auth/register/page.tsx', 'app/terms/page.tsx', 'app/privacy/page.tsx',
      'components/layout/Sidebar.tsx', 'components/layout/ShellHeader.tsx', 'components/layout/MobileMenu.tsx',
      'components/layout/GlobalSearch.tsx',
    ]))
  })

  it('has a scan that can actually fail', () => {
    // Seeds the failure it is meant to catch, so a broken regex cannot pass silently.
    for (const bad of ['className="ml-4"', "'pr-2 text-left'", 'className="absolute left-0"', 'className="rounded-l-lg"']) {
      expect(PHYSICAL.some((re) => re.test(bad)), bad).toBe(true)
    }
    for (const good of ['className="ms-4 pe-2 text-start"', 'className="start-0 border-s"', 'className="ps-10 rounded-s-lg"']) {
      expect(PHYSICAL.some((re) => re.test(good)), good).toBe(false)
    }
  })

  for (const file of NEW_SURFACES) {
    it(`${relative(SRC, file).replace(/\\/g, '/')} uses only logical (start/end) direction utilities`, () => {
      const offending = readFileSync(file, 'utf-8').split('\n')
        .map((line, i) => ({ line: line.trim(), n: i + 1 }))
        .filter(({ line }) => !line.startsWith('//') && !line.startsWith('*') && PHYSICAL.some((re) => re.test(line)))
      expect(offending).toEqual([])
    })
  }
})

describe('touch targets on the learning screens', () => {
  it('every control that is not the shared Button carries the touch-sized minimum', () => {
    // Shared <Button> bakes in min-h-[44px]; a hand-rolled <button> must do the same.
    const offenders: string[] = []
    for (const file of NEW_SURFACES) {
      const source = readFileSync(file, 'utf-8')
      // Array.from, not `for…of`: the project targets es5, where iterating the
      // matchAll iterator directly needs downlevelIteration.
      for (const match of Array.from(source.matchAll(/<button\b[\s\S]*?>/g))) {
        const tag = match[0]
        if (!/className=/.test(tag)) continue
        // A card-sized control is tall by construction (padding on multi-line content).
        if (/\bp-4\b|\bpx-4\b/.test(tag)) continue
        if (!/min-h-\[44px\]/.test(tag)) offenders.push(`${relative(SRC, file)}: ${tag.replace(/\s+/g, ' ').slice(0, 90)}`)
      }
    }
    expect(offenders).toEqual([])
  })
})
