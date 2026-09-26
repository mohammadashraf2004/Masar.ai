'use client'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { MentorCodeBlock } from '@/components/mentor/MentorCodeBlock'
import { splitFences } from '@/lib/mentor/fences'

/**
 * A mentor reply, rendered from markdown, with fenced code drawn as `MentorCodeBlock`.
 *
 * Inline code versus a fenced block is told apart the way MarkdownLesson does it, and for the
 * same reason: an untagged fence arrives with no `language-` class, so the class alone cannot
 * say; a newline in the text can (an inline span never has one).
 */
export function MentorMarkdown({ children }: { children: string }) {
  return (
    <div className="prose-dark text-sm [&_ol]:ms-0 [&_ol]:ps-5 [&_p]:whitespace-pre-wrap [&_ul]:ms-0 [&_ul]:ps-5 [&>*:last-child]:mb-0 [&>*:first-child]:mt-0">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ children: label, href }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="text-amber-text underline underline-offset-2">
              {label}
            </a>
          ),
          // The `code` renderer returns the block itself, so the default wrapping <pre> is dropped.
          pre: ({ children: inner }) => <>{inner}</>,
          code: ({ className, children: text }) => {
            const raw = String(text)
            if (!className && !raw.includes('\n')) {
              return <code dir="ltr" className="prism-inline-code">{raw}</code>
            }
            const lang = /language-([\w+#.-]+)/.exec(className ?? '')?.[1]
            return <MentorCodeBlock code={raw.replace(/\n$/, '')} lang={lang} />
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  )
}

/** A learner's message: their words as typed (line breaks kept), with any fenced code as a block. */
export function UserMessageBody({ text }: { text: string }) {
  return (
    <>
      {splitFences(text).map((segment, i) =>
        segment.type === 'code' ? (
          <MentorCodeBlock key={i} code={segment.code} lang={segment.lang} />
        ) : (
          <p key={i} className="whitespace-pre-wrap">{segment.text}</p>
        ),
      )}
    </>
  )
}
