import { cn } from '@/lib/utils'
import { PAGE_CONTAINER } from '@/components/layout/PageContainer'

interface PageHeaderProps {
  title: string
  subtitle?: string
  action?: React.ReactNode
  className?: string
  /** Keep a sentence-length title - a greeting - on up to two lines at every
   *  width. Any title already wraps on a phone; this also stops it being cut
   *  to one line from `sm` up. */
  wrapTitle?: boolean
  /** Take the page container (`PageContainer`) so the header lines up with a
   *  `PageBody` beneath it. Without it the header spans the pane, as it always did. */
  contained?: boolean
  /** The title and subtitle come from content data, in whichever language the
   *  content was written: each picks its own direction from its first strong
   *  character instead of inheriting the page's. Without this an English course
   *  title on an Arabic page renders as "?What is LangChain". */
  dirAuto?: boolean
}

/**
 * A page's title, its one-line description and, optionally, its main action.
 *
 * It used to carry the language switcher, the credit balance and the account
 * menu as well. Those are the shell's now (ShellHeader), which means they no
 * longer depend on which page is open, and a page's header is only about the page.
 *
 * Deliberately not scrolled away with the content: the pages below it own the
 * scroll region, and their padding is what this is aligned to.
 */
export function PageHeader({ title, subtitle, action, className, wrapTitle, contained, dirAuto }: PageHeaderProps) {
  const dir = dirAuto ? 'auto' : undefined
  return (
    <div className={cn(
      'flex flex-wrap items-center gap-x-3 gap-y-2.5 shrink-0',
      contained ? PAGE_CONTAINER : 'px-4 sm:px-6 lg:px-8',
      'pb-4 pt-5 lg:pb-5 lg:pt-7',
      className
    )}>
      {/* Below `sm` the title block is guaranteed 10rem, so the action (which
          drops to its own row there) cannot squeeze it to "Care…" and it wraps
          instead. From `sm` up `min-w-0` lets it shrink and the title is a
          single truncated line, as it always was. The subtitle wraps to two
          lines rather than being cut off at the first word. */}
      <div className="min-w-[10rem] flex-1 sm:min-w-0">
        <h1 dir={dir} className={cn('ui-page-title break-words', wrapTitle ? 'line-clamp-2' : 'sm:truncate')}>{title}</h1>
        {subtitle && (
          <p dir={dir} className="ui-description mt-1.5 line-clamp-2">{subtitle}</p>
        )}
      </div>

      {/* Page action. Below sm it wraps to its own row rather than competing
          with the title for a share of ~150px; `order-last` puts it after the
          title on that second row, and DOM order takes over again from sm
          so the desktop arrangement is unchanged. */}
      {action && (
        <div className="order-last sm:order-none w-full sm:w-auto shrink-0">{action}</div>
      )}
    </div>
  )
}
