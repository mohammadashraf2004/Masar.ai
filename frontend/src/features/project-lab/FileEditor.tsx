'use client'

import { useId } from 'react'
import Editor from 'react-simple-code-editor'
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-clike'
import 'prismjs/components/prism-markup'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-sql'
import 'prismjs/components/prism-markdown'
import { codeEditorStyle } from '@/features/exercises/CodeCell/codeCellTheme'
import { useLabI18n } from './strings'
import type { LabFile, LabLanguage, LabTable } from './types'

const GRAMMAR: Partial<Record<LabLanguage, string>> = { python: 'python', sql: 'sql', markdown: 'markdown' }

function highlighted(code: string, language: LabLanguage): string {
  const grammar = GRAMMAR[language]
  if (grammar && languages[grammar]) return highlight(code, languages[grammar], grammar)
  return code.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c] as string)
}

/** The editor surface for one workspace file.
 *
 *  Uses the editor Masar already ships (react-simple-code-editor + Prism) rather than adding
 *  Monaco: same look as the lesson code cells, no runtime CDN loading (which the app's CSP would
 *  block), and it works in tests. `.py`, `.sql` and `.md` get syntax highlighting; a CSV dataset
 *  is shown as a read-only table; anything read-only cannot be typed into. */
export function FileEditor({ file, value, onChange }: {
  file: LabFile
  value: string
  onChange: (content: string) => void
}) {
  const { t, tf } = useLabI18n()
  const textareaId = useId()

  if (file.language === 'csv' && file.table) return <CsvTable path={file.path} table={file.table} />

  const lineCount = Math.max(1, value.split('\n').length)
  return (
    <div className="prism-code relative min-h-0 flex-1 overflow-auto" dir="ltr">
      <label htmlFor={textareaId} className="sr-only">
        {tf('lab.editor.label', { file: file.path })}{file.editable ? '' : ` — ${t('lab.editor.readOnly')}`}
      </label>
      <div className="flex min-w-max items-stretch py-3">
        <div
          aria-hidden="true"
          className="w-11 shrink-0 select-none border-e border-white/5 pe-3 text-end font-mono text-[12.5px] leading-[1.75] text-[#3A4456]"
        >
          {Array.from({ length: lineCount }, (_, index) => <span key={index} className="block">{index + 1}</span>)}
        </div>
        <Editor
          value={value}
          onValueChange={onChange}
          highlight={code => highlighted(code, file.language)}
          padding="0 16px"
          readOnly={!file.editable}
          textareaId={textareaId}
          spellCheck={false}
          textareaClassName="code-cell-textarea"
          style={{ ...codeEditorStyle, minHeight: 320 }}
        />
      </div>
    </div>
  )
}

function CsvTable({ path, table }: { path: string; table: LabTable }) {
  const { tf } = useLabI18n()
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <p className="border-b border-border px-4 py-2 text-xs text-ghost" dir="auto">
        {tf('lab.csv.rows', { shown: table.rows.length, total: table.row_count })}
      </p>
      <div className="min-h-0 flex-1 overflow-auto" dir="ltr">
        <table className="w-full border-collapse font-mono text-xs" aria-label={path}>
          <thead className="sticky top-0 bg-surface">
            <tr>
              {table.columns.map(column => (
                <th key={column} scope="col" className="border-b border-border px-3 py-2 text-start font-semibold text-bright">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row, index) => (
              <tr key={index} className="odd:bg-surface/40">
                {row.map((cell, column) => (
                  <td key={column} className="whitespace-nowrap border-b border-border/60 px-3 py-1.5 text-soft">
                    {cell === null || cell === '' ? <span className="text-ghost">—</span> : String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export { CsvTable }
