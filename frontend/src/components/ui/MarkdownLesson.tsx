'use client'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'
import { Lightbulb } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useI18n } from '@/lib/i18n'
import { TermAnnotationScope, useTermAnnotation } from './TermAnnotator'

interface MarkdownLessonProps {
  content: string
  /**
   * Direction of the prose. Defaults to the reader's UI language, but a
   * lesson that is still English-only can force `ltr` even for an Arabic
   * reader — the text itself decides, not the preference.
   */
  dir?: 'rtl' | 'ltr'
  /**
   * Tighter typography for prose inside a card — an exercise brief or a
   * project brief, which are structured markdown (numbered steps, fenced
   * snippets) but must not be typeset at full lesson scale.
   */
  compact?: boolean
}

const HIGHLIGHTABLE: Record<string, unknown> = {
  python: languages.python,
  py: languages.python,
  bash: languages.bash,
  sh: languages.bash,
  shell: languages.bash,
  json: languages.json,
}

/** Renders lesson markdown with a voice that matches the rest of the
 * product instead of default browser typography — the underlying text
 * is untouched, only how it's presented. Real code samples get the same
 * Prism theme as the interactive CodeCell; plain-text diagrams (common in
 * these lessons — ASCII arrows sketching a pipeline) get their own
 * distinct "diagram" framing instead of being mistaken for runnable code.
 *
 * Prose additionally runs through term annotation (the first-mention rule,
 * see TermAnnotator). Code does not: the `code` renderer below never calls
 * the annotator, so identifiers, commands and package names are rendered
 * exactly as authored regardless of language settings. */
function MarkdownBody({
  content,
  dir,
  compact,
}: {
  content: string
  dir: 'rtl' | 'ltr'
  compact: boolean
}) {
  const annotate = useTermAnnotation()

  return (
    <div className={cn('lesson-content', compact && 'lesson-content--compact')} dir={dir}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // The lesson's own h1 duplicates the collapsible card title
          // that's already shown above it — render it as a small eyebrow
          // instead of a second giant heading.
          h1: ({ children }) => (
            <p className="text-xs font-medium text-amber uppercase tracking-widest mb-4">
              {annotate(children)}
            </p>
          ),
          h2: ({ children }) => (
            <h2 className={cn('flex items-center gap-2.5 mb-3 first:mt-0', compact ? 'mt-5' : 'mt-8')}>
              <span className={cn('w-1 rounded-full bg-amber shrink-0', compact ? 'h-4' : 'h-5')} />
              <span
                className={cn(
                  'font-display font-bold text-bright',
                  compact ? 'text-sm' : 'text-lg'
                )}
              >
                {annotate(children)}
              </span>
            </h2>
          ),
          h3: ({ children }) => (
            <h3
              className={cn(
                'font-display font-semibold text-amber mb-2',
                compact ? 'text-sm mt-4' : 'text-base mt-6'
              )}
            >
              {annotate(children)}
            </h3>
          ),
          p: ({ children }) => (
            <p
              className={cn(
                'text-soft',
                compact ? 'text-sm leading-relaxed mb-3' : 'text-[15px] leading-[1.8] mb-4'
              )}
            >
              {annotate(children)}
            </p>
          ),
          strong: ({ children }) => (
            <strong className="text-amber2 font-semibold">{annotate(children)}</strong>
          ),
          em: ({ children }) => <em className="text-dim">{annotate(children)}</em>,
          ul: ({ children }) => (
            <ul className={cn('list-disc list-outside ps-5', compact ? 'space-y-1.5 my-3' : 'space-y-2 my-4')}>
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol
              className={cn(
                'list-decimal list-outside ps-5',
                compact ? 'space-y-1.5 my-3' : 'space-y-2.5 my-4'
              )}
            >
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li
              className={cn(
                'text-soft marker:text-amber marker:font-mono',
                compact ? 'text-sm leading-relaxed' : 'text-[15px] leading-[1.75]'
              )}
            >
              {annotate(children)}
            </li>
          ),
          blockquote: ({ children }) => (
            <div className="flex gap-3 my-5 px-4 py-3.5 rounded-lg bg-amber/5 border border-amber/20">
              <Lightbulb size={16} className="text-amber shrink-0 mt-0.5" />
              <div className="text-sm text-soft leading-relaxed [&>p]:mb-0">{children}</div>
            </div>
          ),
          hr: () => <div className={cn('border-t border-border', compact ? 'my-5' : 'my-8')} />,
          a: ({ children, href }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="text-amber hover:text-amber2 underline decoration-amber/30 underline-offset-2 transition-colors">
              {children}
            </a>
          ),
          code: ({ className, children }) => {
            const raw = String(children).replace(/\n$/, '')
            const lang = /language-(\w+)/.exec(className ?? '')?.[1]

            // Inline code (no fenced block) — a single word/expression in
            // running prose, e.g. `model.invoke()`. Always LTR: an
            // identifier does not flip direction because the surrounding
            // sentence is Arabic.
            if (!className) {
              return <code className="prism-inline-code" dir="ltr">{raw}</code>
            }

            const grammar = lang ? HIGHLIGHTABLE[lang] : undefined
            if (grammar) {
              const html = highlight(raw, grammar, lang!)
              return (
                <pre
                  dir="ltr"
                  className="prism-code bg-void border border-border rounded-lg p-4 overflow-x-auto text-[13px] leading-relaxed text-start"
                >
                  {/*
                    The ONLY dangerouslySetInnerHTML in the app, and the
                    one place it is justified: `html` is Prism's own
                    output, produced from `raw` by highlight(). Prism
                    HTML-escapes the source text it wraps, so the markup
                    here is Prism's <span class="token …"> scaffolding
                    around escaped content — never caller-authored HTML.
                    Anything else rendered by this component goes through
                    react-markdown, which does not render raw HTML (no
                    rehype-raw) and strips javascript: URLs from links.
                    Do not pass anything but highlight() output here.
                  */}
                  {/* eslint-disable-next-line react/no-danger */}
                  <code dangerouslySetInnerHTML={{ __html: html }} />
                </pre>
              )
            }

            // No recognized language — these lessons use plain fenced
            // blocks for ASCII pipeline diagrams, not runnable code.
            // Framing them as a "diagram" instead of highlighting them as
            // code avoids implying syntax that isn't there.
            return (
              <pre
                dir="ltr"
                className="my-4 px-4 py-3.5 rounded-lg bg-surface border border-dashed border-border text-[13px] leading-relaxed text-dim font-mono overflow-x-auto text-start"
              >
                <code>{raw}</code>
              </pre>
            )
          },
          // GFM tables get the same treatment the code renderer above already
          // gives fenced blocks: the overflow is the table's own problem to
          // solve, inside its own scroll container, instead of the whole page
          // scrolling sideways to accommodate one wide row.
          //
          // The wrapper, not `table { width: 100% }`, is what fixes this —
          // a percentage width never stops content forcing a min-content
          // width wider than the viewport. Desktop is unaffected: the
          // container only scrolls when there is something to scroll.
          table: ({ children }) => (
            <div className="overflow-x-auto">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

export function MarkdownLesson({ content, dir, compact = false }: MarkdownLessonProps) {
  const { language, annotateTerms } = useI18n()
  const resolvedDir = dir ?? (language === 'ar' ? 'rtl' : 'ltr')

  return (
    // A fresh scope per lesson: the first-mention rule is per lesson, not
    // per session, so every lesson re-introduces the terms it uses.
    <TermAnnotationScope key={content} enabled={annotateTerms}>
      <MarkdownBody content={content} dir={resolvedDir} compact={compact} />
    </TermAnnotationScope>
  )
}
