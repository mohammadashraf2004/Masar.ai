'use client'
import Editor from 'react-simple-code-editor'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-python'

interface CodeCellProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  minHeight?: number
  autoFocus?: boolean
}

/** An editable, syntax-highlighted code cell — DataCamp-style — for
 * writing Python solutions to coding exercises. This edits and displays
 * code; it doesn't execute it. Grading happens conversationally via
 * AnswerChat once submitted (see app/services/mentor/answer_evaluator_service.py). */
export function CodeCell({ value, onChange, placeholder, minHeight = 140, autoFocus }: CodeCellProps) {
  return (
    <div
      className="prism-code bg-void border border-border rounded-lg overflow-y-auto focus-within:border-amber/50 transition-colors"
      style={{ maxHeight: 320 }}
    >
      <Editor
        value={value}
        onValueChange={onChange}
        highlight={code => highlight(code, languages.python, 'python')}
        padding={12}
        autoFocus={autoFocus}
        placeholder={placeholder}
        textareaClassName="code-cell-textarea"
        style={{
          fontSize: 13,
          minHeight,
          color: '#E2E8F0',
        }}
      />
    </div>
  )
}
