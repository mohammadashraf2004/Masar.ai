'use client'

import { useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ImageOff } from 'lucide-react'
import { useLabI18n } from './strings'
import type { LabArtifact } from './types'

/** Rendered view of a workspace Markdown file (the report, the plan, the README).
 *
 *  Images resolve ONLY to charts this learner's code generated (saved artifacts, as data: URLs);
 *  any other image source — including external URLs — is shown as a labelled placeholder and never
 *  fetched. The prose follows the reader's direction; code stays LTR. */
export function MarkdownPreview({ markdown, artifacts, artifactData, loadArtifact }: {
  markdown: string
  artifacts: LabArtifact[]
  artifactData: Record<string, string>
  loadArtifact: (artifact: LabArtifact) => void
}) {
  const { t, tf } = useLabI18n()
  const byPath = new Map(artifacts.map(artifact => [artifact.path, artifact]))
  const referenced = Array.from(markdown.matchAll(/!\[[^\]]*\]\(\s*<?([^)\s>]+)/g), match => match[1].replace(/^\.\//, ''))
  const key = referenced.join('|')

  useEffect(() => {
    for (const path of key.split('|')) {
      const artifact = byPath.get(path)
      if (artifact) loadArtifact(artifact)
    }
    // byPath is rebuilt every render; the paths and the artifact list are what matter.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, artifacts, loadArtifact])

  return (
    <div
      data-testid="lab-markdown-preview"
      className="lab-markdown min-h-0 flex-1 space-y-3 overflow-auto bg-void p-5 text-sm leading-relaxed text-soft [&_code]:rounded [&_code]:bg-surface [&_code]:px-1 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-bright [&_h1]:mt-6 [&_h1]:border-b [&_h1]:border-border [&_h1]:pb-1 [&_h1]:font-display [&_h1]:text-lg [&_h1]:font-bold [&_h1]:text-bright [&_h1:first-child]:mt-0 [&_h2]:mt-5 [&_h2]:text-base [&_h2]:font-semibold [&_h2]:text-bright [&_li]:ms-5 [&_ol]:list-decimal [&_pre]:overflow-x-auto [&_pre]:rounded-lg [&_pre]:bg-surface [&_pre]:p-3 [&_strong]:text-bright [&_table]:w-full [&_table]:text-xs [&_td]:border [&_td]:border-border [&_td]:p-1.5 [&_th]:border [&_th]:border-border [&_th]:p-1.5 [&_th]:text-start [&_ul]:list-disc"
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          // Each block takes its direction from its own text: an English report reads correctly
          // in the Arabic interface (and the reverse), punctuation included.
          p: ({ children }) => <p dir="auto">{children}</p>,
          h1: ({ children }) => <h1 dir="auto">{children}</h1>,
          h2: ({ children }) => <h2 dir="auto">{children}</h2>,
          h3: ({ children }) => <h3 dir="auto">{children}</h3>,
          li: ({ children }) => <li dir="auto">{children}</li>,
          td: ({ children }) => <td dir="auto">{children}</td>,
          th: ({ children }) => <th dir="auto">{children}</th>,
          pre: ({ children }) => <pre dir="ltr">{children}</pre>,
          img: ({ src, alt }) => {
            const path = typeof src === 'string' ? src.replace(/^\.\//, '') : ''
            const artifact = byPath.get(path)
            const data = artifact ? artifactData[artifact.sha256] : undefined
            if (data) {
              // eslint-disable-next-line @next/next/no-img-element -- a data: URL of a chart this learner generated
              return <img src={data} alt={alt ?? path} className="my-2 max-w-full rounded-lg border border-border bg-white" />
            }
            return (
              <span role="img" aria-label={alt || path}
                className="my-2 flex items-center gap-2 rounded-lg border border-dashed border-border px-3 py-4 text-xs text-ghost">
                <ImageOff size={14} aria-hidden="true" />
                <span>
                  {path.startsWith('charts/')
                    ? (artifact ? t('lab.preview.loading') : tf('lab.preview.missingChart', { file: path }))
                    : t('lab.preview.externalImage')}
                </span>
              </span>
            )
          },
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  )
}
