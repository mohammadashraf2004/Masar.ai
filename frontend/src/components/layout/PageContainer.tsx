import type { HTMLAttributes } from 'react'
import { LegalFooter } from '@/components/layout/LegalFooter'
import { cn } from '@/lib/utils'

/**
 * The one horizontal rule for a page: how wide it may get, and the side padding
 * it keeps at each breakpoint. A page's header and its content both take it, so
 * the title's edge is the content's edge at every width - the dashboard is the
 * reference (it always lined up), and /tracks, /tools and /learn each used to
 * narrow their own content column (`max-w-4xl`, `-5xl`, `-3xl`) under a header
 * that did not, which left the title hanging past the cards.
 *
 * 1400px is wider than the main pane at any laptop width (1440 wide leaves
 * 1192 beside the sidebar), so it only takes effect on a large monitor, where
 * it stops the page stretching edge to edge and centres it instead.
 */
export const PAGE_CONTAINER = 'mx-auto w-full max-w-[1400px] px-4 sm:px-6 lg:px-8'

export function PageContainer({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn(PAGE_CONTAINER, className)} {...props} />
}

/**
 * What sits under a `<PageHeader contained>`: the scroll region, with the page's
 * content inside the same container the header uses. The pane scrolls on its own
 * (the header stays put above it), which is why it is a separate element from the
 * container rather than one div doing both jobs.
 */
export function PageBody({
  className,
  children,
  footer = true,
}: {
  className?: string
  children: React.ReactNode
  /** Full-height focus views keep their pinned controls instead of a site footer. */
  footer?: boolean
}) {
  return (
    <div className="flex-1 overflow-y-auto">
      <PageContainer className="flex min-h-full flex-col pt-6 pb-[calc(1.25rem+env(safe-area-inset-bottom))]">
        <div className={cn('flex-1', className)}>{children}</div>
        {footer && <LegalFooter />}
      </PageContainer>
    </div>
  )
}
