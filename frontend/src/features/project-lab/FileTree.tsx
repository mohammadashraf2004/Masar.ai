'use client'

import { Database, FileCode2, FileText, Folder, Lock } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useLabI18n } from './strings'
import type { LabWorkspace, LabWorkspaceEntry } from './types'

function FileIcon({ entry }: { entry: LabWorkspaceEntry }) {
  if (entry.language === 'csv') return <Database size={14} aria-hidden="true" className="shrink-0 text-sky" />
  if (entry.language === 'python' || entry.language === 'sql')
    return <FileCode2 size={14} aria-hidden="true" className="shrink-0 text-amber-text" />
  return <FileText size={14} aria-hidden="true" className="shrink-0 text-soft" />
}

/** The workspace as a tree. File names are code (always LTR); the chrome follows the page. */
export function FileTree({ workspace, selectedPath, dirtyPaths, onSelect }: {
  workspace: LabWorkspace
  selectedPath: string | null
  dirtyPaths: string[]
  onSelect: (path: string) => void
}) {
  const { t } = useLabI18n()
  const dirs = workspace.entries.filter(e => e.kind === 'dir').map(e => e.path)
  const topFiles = workspace.entries.filter(e => e.kind === 'file' && !e.path.includes('/'))

  const renderFile = (entry: LabWorkspaceEntry, depth: number) => {
    const name = entry.path.split('/').pop()
    const selected = entry.path === selectedPath
    const dirty = dirtyPaths.includes(entry.path)
    return (
      <li key={entry.path}>
        <button
          type="button"
          onClick={() => onSelect(entry.path)}
          aria-current={selected ? 'true' : undefined}
          className={cn(
            'flex min-h-[36px] w-full items-center gap-2 rounded-md pe-2 text-start font-mono text-xs transition-colors lg:min-h-[30px]',
            selected ? 'bg-amber/10 text-bright' : 'text-soft hover:bg-surface hover:text-bright',
          )}
          style={{ paddingInlineStart: `${0.5 + depth * 0.9}rem` }}
        >
          <FileIcon entry={entry} />
          {/* The name sits beside its icon in both directions; markers go to the far end. */}
          <span className="min-w-0 truncate" dir="ltr">{name}</span>
          <span className="ms-auto flex shrink-0 items-center gap-1.5">
            {!entry.editable && <Lock size={12} className="text-ghost" aria-label={t('lab.files.readOnly')} />}
            {(dirty || entry.modified) && (
              <span
                className={cn('size-1.5 rounded-full', dirty ? 'bg-amber' : 'bg-soft/60')}
                aria-label={dirty ? t('lab.editor.unsaved') : t('lab.files.modified')}
                role="img"
              />
            )}
          </span>
        </button>
      </li>
    )
  }

  return (
    <nav aria-label={t('lab.files')} className="min-h-0 overflow-y-auto p-2">
      <p className="px-2 pb-2 font-mono text-[11px] uppercase tracking-wide text-ghost" dir="ltr">{workspace.root}/</p>
      <ul className="space-y-0.5">
        {dirs.map(dir => {
          const children = workspace.entries.filter(e => e.kind === 'file' && e.path.startsWith(`${dir}/`)
            && !e.path.slice(dir.length + 1).includes('/'))
          const depth = dir.split('/').length - 1
          return (
            <li key={dir}>
              <div
                className="flex min-h-[30px] items-center gap-2 font-mono text-xs text-ghost"
                style={{ paddingInlineStart: `${0.5 + depth * 0.9}rem` }}
              >
                <Folder size={14} aria-hidden="true" className="shrink-0" />
                <span dir="ltr">{dir.split('/').pop()}/</span>
              </div>
              {children.length > 0 && <ul className="space-y-0.5">{children.map(entry => renderFile(entry, depth + 1))}</ul>}
            </li>
          )
        })}
        {topFiles.map(entry => renderFile(entry, 0))}
      </ul>
    </nav>
  )
}
