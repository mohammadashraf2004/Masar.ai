'use client'

import { useId, useRef } from 'react'
import Editor from 'react-simple-code-editor'
import { codeCellColors, codeEditorStyle, highlightedCode } from './codeCellTheme'

export function CodeEditor({
  value,
  onChange,
  readOnly = false,
  highlightLines = [],
  ariaLabel,
  language = 'python',
}: {
  value: string
  onChange: (value: string) => void
  readOnly?: boolean
  highlightLines?: number[]
  ariaLabel: string
  language?: string
}) {
  const textareaId = useId()
  const surfaceRef = useRef<HTMLDivElement>(null)
  const highlighted = new Set(highlightLines)
  const lineCount = Math.max(1, value.split('\n').length)

  function focusEditor(event: React.MouseEvent<HTMLDivElement>) {
    if (readOnly || event.target instanceof HTMLTextAreaElement) return
    const textarea = surfaceRef.current?.querySelector<HTMLTextAreaElement>('textarea')
    if (!textarea) return
    event.preventDefault()
    textarea.focus()
  }

  return (
    <div className="relative">
      <label htmlFor={textareaId} className="sr-only">{ariaLabel}</label>
      <div
        ref={surfaceRef}
        onMouseDown={focusEditor}
        className="flex min-w-max items-stretch py-3.5 [&_.code-cell-line--highlighted_*]:!text-[#E2E8F0] [&_.token.comment]:!text-[#5C6678] [&_.token.keyword]:!text-[#F59E0B]"
        style={{ background: codeCellColors.background }}
      >
      <div
        aria-hidden="true"
        className="w-11 shrink-0 select-none border-e border-[#151B27] pe-3.5 text-end font-mono text-[12.5px] leading-[1.75] text-[#3A4456]"
      >
        {Array.from({ length: lineCount }, (_, index) => (
          <span key={index} className="block">{index + 1}</span>
        ))}
      </div>
        <Editor
          value={value}
          onValueChange={onChange}
          highlight={code => highlightedCode(code, language, highlighted)}
          padding="0 16px"
          readOnly={readOnly}
          textareaId={textareaId}
          spellCheck={false}
          textareaClassName="code-cell-textarea"
          style={codeEditorStyle}
        />
      </div>
    </div>
  )
}
