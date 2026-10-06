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
import type { LessonBlock } from '@/types'
import { LessonImage } from './LessonImage'
import { TermAnnotationScope, useTermAnnotation } from './TermAnnotator'

interface MarkdownLessonProps {
  content: string
  /**
   * The body as ordered blocks (text runs, figures, author notes), when the lesson
   * holds authoring syntax. They are rendered in the order given, inside the one
   * term-annotation scope, so the first-mention rule is still per lesson and not per
   * text run. An empty list renders nothing (never the raw `content`). Without blocks
   * (null) the body is `content`, exactly as before.
   */
  blocks?: LessonBlock[] | null
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

// Fenced blocks in these lessons don't always carry a language tag — a lot
// of it is Python simply fenced as plain ```, indistinguishable at the
// parser level from an ASCII pipeline diagram fenced the same way. Treat a
// block as code only when it contains unambiguous code syntax AND no
// diagram connector; verified against every untagged block in the actual
// lesson content (2034 blocks: 95 reclassified as code, 0 blocks matched
// both a code and a diagram signal). When both would somehow match, the
// diagram reading wins — misrendering a real diagram as broken code looks
// worse than leaving a rare mistagged snippet unhighlighted.
const PY_CODE_SIGNALS = [
  /^\s*(def|class)\s+\w+/m,
  /^\s*(import|from)\s+[\w.]+/m,
  /^\s*@\w+/m,
  /^\s*(elif\b|while\s+.+:|for\s+\w+\s+in\s+.+:)\s*$/m,
  /^\s*return\b/m,
  /^\s*self\./m,
]
const DIAGRAM_SIGNALS = /[┌┐└┘├┤┬┴┼─│═║╔╗╚╝╠╣▼▶◀▲►◄]|-{2,}>|=+>|→|⇒|⟶|↓|↑|←|↔|↕|↖|↗|↘|↙/

function detectFallbackLanguage(raw: string): string | undefined {
  if (DIAGRAM_SIGNALS.test(raw)) return undefined
  return PY_CODE_SIGNALS.some((re) => re.test(raw)) ? 'python' : undefined
}

// Highlights arrow/connector runs (→, -->, single- and double-line
// box-drawing corners and rules, the four diagonals...) in the accent color
// so a multi-step pipeline reads at a glance, leaving node labels in the
// body text color. Purely cosmetic — this only ever runs on text already
// routed away from Prism because it isn't recognized as code. Every
// character matched here is covered by the self-hosted
// 'JetBrains Mono Diagrams' face declared in globals.css — verified
// against every diagram block in the real lesson content, not guessed —
// so it renders at the same cell width as the surrounding text instead of
// falling back to a mismatched system font and drifting out of alignment.
const DIAGRAM_CONNECTOR =
  /(-{2,}>|=+>|<-{2,}|[─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣]+|[→⇒⟶↓↑←↔↕↖↗↘↙▼▶◀▲►◄])/

function renderDiagram(raw: string) {
  return raw
    .split(DIAGRAM_CONNECTOR)
    .map((part, i) => (i % 2 === 1 ? <span key={i} className="text-amber-text2">{part}</span> : part))
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
          //
          // Sizes, line-heights and gaps for headings, paragraphs, lists,
          // code and tables come from the `.lesson-content` rules in
          // globals.css (the --lc-* tokens); the classes here are colour and
          // structure only, so a size cannot be set in two places.
          h1: ({ children }) => (
            <p className="text-lc-label font-medium text-amber-text uppercase tracking-widest">
              {annotate(children)}
            </p>
          ),
          h2: ({ children }) => (
            <h2 className="flex items-start gap-3">
              <span className="w-1 self-stretch my-[0.2em] rounded-full bg-amber shrink-0" />
              <span className="min-w-0 font-display font-bold text-bright">
                {annotate(children)}
              </span>
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="font-display font-semibold text-amber-text">
              {annotate(children)}
            </h3>
          ),
          p: ({ children }) => <p className="text-soft">{annotate(children)}</p>,
          strong: ({ children }) => (
            <strong className="text-amber-text2 font-semibold">{annotate(children)}</strong>
          ),
          em: ({ children }) => <em className="text-dim">{annotate(children)}</em>,
          ul: ({ children }) => <ul className="list-disc list-outside">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-outside">{children}</ol>,
          li: ({ children }) => (
            <li className="text-soft marker:text-amber-text marker:font-mono">{annotate(children)}</li>
          ),
          blockquote: ({ children }) => (
            <div className="lesson-callout flex gap-3 px-4 py-3 rounded-lg bg-amber/5 border border-amber/20">
              {/* One line box tall, so the icon centres on the first line at
                  any body size or script. */}
              <span className="flex h-[1lh] shrink-0 items-center text-amber-text">
                <Lightbulb size={16} />
              </span>
              <div className="min-w-0 text-soft">{children}</div>
            </div>
          ),
          hr: () => <hr className="border-0 border-t border-border" />,
          a: ({ children, href }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="text-amber-text hover:text-amber-text2 underline decoration-amber/30 underline-offset-2 transition-colors">
              {children}
            </a>
          ),
          // The `code` renderer below returns its own <pre> for blocks;
          // react-markdown's default wraps that in another one, which left an
          // unstyled outer <pre> around the styled inner one (invalid
          // nesting, and the outer box took the spacing instead of the block).
          pre: ({ children }) => <>{children}</>,
          code: ({ className, children }) => {
            const untrimmed = String(children)
            const raw = untrimmed.replace(/\n$/, '')
            const explicitLang = /language-(\w+)/.exec(className ?? '')?.[1]

            // Inline vs. fenced can't be told apart by className alone:
            // react-markdown/rehype only sets `language-xxx` when the fence
            // actually names a language, so an untagged fenced block (most
            // of the diagrams and a fair amount of code in these lessons)
            // arrives with no className too — indistinguishable from real
            // inline code by that check alone, which every earlier version
            // of this function got wrong. The reliable signal is a literal
            // newline: CommonMark defines inline code spans as normalizing
            // any line ending to a single space, so `children` here can
            // never contain "\n" for genuine inline code, while any fenced
            // block — tagged or not — always has at least the one trailing
            // its content, before the closing fence. Checked on the
            // untrimmed string since a one-line fenced block would lose
            // its only newline to the trim below.
            const isInline = !className && !untrimmed.includes('\n')

            // Inline code (no fenced block) — a single word/expression in
            // running prose, e.g. `model.invoke()`. Always LTR: an
            // identifier does not flip direction because the surrounding
            // sentence is Arabic.
            if (isInline) {
              return <code className="prism-inline-code" dir="ltr">{raw}</code>
            }

            const lang = explicitLang && HIGHLIGHTABLE[explicitLang]
              ? explicitLang
              : detectFallbackLanguage(raw)
            const grammar = lang ? HIGHLIGHTABLE[lang] : undefined
            if (grammar) {
              const html = highlight(raw, grammar, lang!)
              return (
                <pre
                  dir="ltr"
                  className="prism-code bg-void border border-border rounded-lg text-start"
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

            // No recognized language, and no code syntax detected either —
            // these lessons use plain fenced blocks for ASCII pipeline
            // diagrams. Framed distinctly from code (no syntax highlighting,
            // since there is no syntax) with arrows and connectors picked
            // out in the accent color, so a multi-step pipeline reads at a
            // glance instead of as one undifferentiated block of text.
            return (
              <pre
                dir="ltr"
                className="rounded-lg bg-surface border border-border border-s-2 border-s-amber/40 text-soft font-mono text-start"
              >
                <code>{renderDiagram(raw)}</code>
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
            <div className="lesson-table-wrap">
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

/**
 * A lesson places an image the course does not have (removed after the lesson was imported).
 * Validation stops this at import, so it is rare; when it happens the gap is visible: a learner
 * sees that a figure is unavailable, and outside production the note names the key.
 */
function MissingImage({ assetKey }: { assetKey: string }) {
  const { t } = useI18n()
  return (
    <div
      role="note"
      data-missing-image={process.env.NODE_ENV !== 'production' ? assetKey : undefined}
      className="mx-auto my-4 max-w-full rounded-lg border border-dashed border-border bg-surface px-4 py-6 text-center text-sm text-soft"
    >
      {t('lesson.figureUnavailable')}
      {process.env.NODE_ENV !== 'production' && (
        <code className="mt-1 block text-xs" dir="ltr">{`image "${assetKey}" - no such image in this course`}</code>
      )}
    </div>
  )
}

/**
 * Authoring notes (an unresolved image request, an exercise marker with no exercise behind it). The API sends
 * them outside production only; a production build of the app drops them as well, so nothing here can reach a
 * published lesson even if a development API is pointed at it.
 */
function AuthorNote({ kind, children }: { kind: string; children: React.ReactNode }) {
  if (process.env.NODE_ENV === 'production') return null
  return (
    <div
      role="note"
      data-author-note={kind}
      dir="auto"
      className="mx-auto max-w-[var(--lc-measure)] rounded-md border border-dashed border-border px-3 py-1.5 text-center text-xs text-ghost"
    >
      {children}
    </div>
  )
}

export function MarkdownLesson({ content, blocks, dir, compact = false }: MarkdownLessonProps) {
  const { language, annotateTerms } = useI18n()
  const resolvedDir = dir ?? (language === 'ar' ? 'rtl' : 'ltr')

  return (
    // A fresh scope per lesson: the first-mention rule is per lesson, not
    // per session, so every lesson re-introduces the terms it uses.
    <TermAnnotationScope key={content} enabled={annotateTerms}>
      {blocks ? (
        <div className="lesson-blocks" dir={resolvedDir}>
          {blocks.map((block, i) =>
            block.type === 'image' ? (
              <LessonImage key={`${i}-${block.asset_key}`} block={block} />
            ) : block.type === 'image_missing' ? (
              <MissingImage key={`${i}-${block.asset_key}`} assetKey={block.asset_key} />
            ) : block.type === 'markdown' ? (
              <MarkdownBody key={i} content={block.content} dir={resolvedDir} compact={compact} />
            ) : block.type === 'author_marker' ? (
              <AuthorNote key={i} kind={block.kind}>Image needed{block.title ? `: ${block.title}` : ''}</AuthorNote>
            ) : block.type === 'exercise_missing' ? (
              <AuthorNote key={i} kind="exercise_missing">Exercise {block.exercise_id} not found for this lesson</AuthorNote>
            ) : null,
          )}
        </div>
      ) : (
        <MarkdownBody content={content} dir={resolvedDir} compact={compact} />
      )}
    </TermAnnotationScope>
  )
}
