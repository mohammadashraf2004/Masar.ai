'use client'
import { CheckCircle, FileText, ListChecks, Wrench } from 'lucide-react'
import { Badge } from '@/components/ui/index'
import { MarkdownLesson } from '@/components/ui/MarkdownLesson'
import { useI18n } from '@/lib/i18n'
import { pickText } from '@/lib/content-language'
import { safeUrl, cn } from '@/lib/utils'
import type { Project } from '@/types'

/**
 * A project brief, in the same shape as an exercise brief: labelled bands
 * for what it is, what it must do, and what it is built with.
 *
 * Same two defects as the exercise card had — the description was rendered
 * in a plain `<p>` (so any structure in it collapsed), and the tool-course
 * reader dropped `objectives` entirely, which is precisely the "what you
 * have to deliver" list. Track and tool readers now show the same brief.
 *
 * `footer` carries whatever submission flow the host page has; the track
 * reader passes its AI-review form, the tool reader passes nothing.
 */
export function ProjectCard({
  project,
  footer,
}: {
  project: Project
  footer?: React.ReactNode
}) {
  const { t, language } = useI18n()

  const title = pickText(project.title, project.title_ar, language)
  const brief = pickText(project.description, project.description_ar, language)

  return (
    <div className="bg-panel border border-border rounded-lg overflow-hidden">
      {/* ── Header ── */}
      <div className="px-5 pt-4 pb-3.5 border-b border-border">
        <div className="flex items-start justify-between gap-3 mb-1.5">
          <span className="text-[11px] font-mono text-ghost uppercase tracking-wider">
            {t('project.label')}
          </span>
          <Badge variant={project.difficulty}>{project.difficulty}</Badge>
        </div>

        <h3
          className="font-display font-bold text-bright text-base leading-snug"
          dir={title.shownIn === 'ar' ? 'rtl' : 'ltr'}
        >
          {title.text}
        </h3>

        <div className="flex items-center gap-3 mt-2.5">
          <Badge variant="ghost">{project.estimated_hours}h</Badge>
          {project.starter_repo_url && (
            <a
              href={safeUrl(project.starter_repo_url)}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-amber hover:text-amber2 transition-colors"
            >
              Starter repo →
            </a>
          )}
        </div>
      </div>

      {/* ── Brief ── */}
      <Band icon={<FileText size={13} />} label={t('project.brief')}>
        <MarkdownLesson
          content={brief.text}
          dir={brief.shownIn === 'ar' ? 'rtl' : 'ltr'}
          compact
        />
      </Band>

      {/* ── Acceptance criteria — the actual deliverable ── */}
      {project.objectives.length > 0 && (
        <Band icon={<ListChecks size={13} />} label={t('project.objectives')}>
          <ul className="space-y-1.5">
            {project.objectives.map((objective, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-soft leading-relaxed">
                <CheckCircle size={12} className="text-emerald mt-1 shrink-0" />
                <span>{objective}</span>
              </li>
            ))}
          </ul>
        </Band>
      )}

      {/* ── Stack: proper nouns, never translated ── */}
      {project.tech_stack.length > 0 && (
        <Band icon={<Wrench size={13} />} label={t('project.stack')} last={!footer}>
          <div className="flex flex-wrap gap-1.5">
            {project.tech_stack.map((tool) => (
              <span
                key={tool}
                className="px-2 py-0.5 rounded bg-surface border border-border text-xs font-mono text-dim"
                dir="ltr"
              >
                {tool}
              </span>
            ))}
          </div>
        </Band>
      )}

      {footer && <div className="px-5 py-4">{footer}</div>}
    </div>
  )
}

function Band({
  icon,
  label,
  children,
  last,
}: {
  icon: React.ReactNode
  label: string
  children: React.ReactNode
  last?: boolean
}) {
  return (
    <div className={cn('px-5 py-4', !last && 'border-b border-border')}>
      <div className="flex items-center gap-1.5 mb-2.5 text-amber">
        {icon}
        <span className="text-[11px] font-medium uppercase tracking-wider">{label}</span>
      </div>
      {children}
    </div>
  )
}
