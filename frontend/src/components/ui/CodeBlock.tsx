'use client'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'
import { cn } from '@/lib/utils'

const GRAMMARS: Record<string, unknown> = {
  python: languages.python,
  py: languages.python,
  bash: languages.bash,
  sh: languages.bash,
  shell: languages.bash,
  json: languages.json,
}

/**
 * Read-only code, highlighted with the same Prism theme as lesson code
 * blocks and the interactive CodeCell.
 *
 * Exists because starter code was rendered as a bare `<pre>` — plain grey
 * monospace, while the identical snippet three lines up in the lesson was
 * fully highlighted. Same code, two different treatments, and the flat one
 * landed on the screen where the student is supposed to start working.
 *
 * Always LTR and left-aligned: a Python snippet does not change direction
 * because the sentence around it is Arabic.
 */
export function CodeBlock({
  code,
  language = 'python',
  className,
}: {
  code: string
  language?: string
  className?: string
}) {
  const grammar = GRAMMARS[language]
  const body = code.replace(/\n$/, '')

  if (!grammar) {
    return (
      <pre
        dir="ltr"
        className={cn(
          'bg-void border border-border rounded-lg p-4 overflow-x-auto',
          'text-[13px] leading-relaxed font-mono text-soft text-start',
          className
        )}
      >
        <code>{body}</code>
      </pre>
    )
  }

  const html = highlight(body, grammar, language)

  return (
    <pre
      dir="ltr"
      className={cn(
        'prism-code bg-void border border-border rounded-lg p-4 overflow-x-auto',
        'text-[13px] leading-relaxed text-start',
        className
      )}
    >
      {/*
        Prism's own output, produced from `body` by highlight() — Prism
        HTML-escapes the source text it wraps, so this is token markup around
        escaped content, never caller-authored HTML. Same reasoning, and the
        same constraint, as the code renderer in MarkdownLesson: do not pass
        anything but highlight() output here.
      */}
      {/* eslint-disable-next-line react/no-danger */}
      <code dangerouslySetInnerHTML={{ __html: html }} />
    </pre>
  )
}
