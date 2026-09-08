'use client'
import { Children, createContext, useContext, type ReactNode } from 'react'
import { matchTermsInText } from '@/content/terminology'
import { TechnicalTerm } from './TechnicalTerm'

/**
 * Applies the first-mention rule to lesson prose.
 *
 * The first time a lesson mentions a term it renders as
 * `Embeddings (التضمينات)`; every later mention renders as `Embeddings`
 * alone, clickable for the definition. That is the whole point of the
 * policy — introduce the Arabic meaning once, then keep using the English
 * term the industry uses.
 *
 * Safety property: this only ever transforms *string* children. Anything
 * already rendered into an element — most importantly the `code` renderer's
 * output — is passed through untouched, so no code sample, identifier, CLI
 * command or package name can be rewritten by term annotation.
 */

interface TermScope {
  /** Term ids already introduced in this lesson. */
  seen: Set<string>
  enabled: boolean
}

const TermScopeContext = createContext<TermScope | null>(null)

export function TermAnnotationScope({
  children,
  enabled = true,
}: {
  children: ReactNode
  enabled?: boolean
}) {
  // A fresh scope object per render pass, deliberately: "first mention" is
  // then decided in document order every time the lesson renders, instead of
  // drifting as terms accumulate across re-renders.
  const scope: TermScope = { seen: new Set(), enabled }
  return <TermScopeContext.Provider value={scope}>{children}</TermScopeContext.Provider>
}

function annotateString(text: string, scope: TermScope): ReactNode {
  const matches = matchTermsInText(text)
  if (matches.length === 0) return text

  const out: ReactNode[] = []
  let cursor = 0

  matches.forEach((match, i) => {
    if (match.start < cursor) return // overlapping match, already consumed
    if (match.start > cursor) out.push(text.slice(cursor, match.start))

    const isFirst = !scope.seen.has(match.term.id)
    scope.seen.add(match.term.id)

    out.push(
      <TechnicalTerm
        key={`${match.term.id}-${match.start}-${i}`}
        term={match.term.id}
        firstMention={isFirst}
      />
    )
    cursor = match.end
  })

  if (cursor < text.length) out.push(text.slice(cursor))
  return out
}

/**
 * Returns a mapper for a text-bearing renderer's children. Call it from `p`,
 * `li`, headings, `strong`, `em`, table cells — never from `code`.
 */
export function useTermAnnotation(): (children: ReactNode) => ReactNode {
  const scope = useContext(TermScopeContext)

  return (children: ReactNode) => {
    if (!scope || !scope.enabled) return children
    return Children.map(children, (child) =>
      typeof child === 'string' ? annotateString(child, scope) : child
    )
  }
}
