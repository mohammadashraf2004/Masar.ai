import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { PageHeader } from '@/components/layout/PageHeader'
import { PAGE_CONTAINER, PageBody } from '@/components/layout/PageContainer'

// jsdom has no layout, so what is pinned here is the structure that lets the
// title wrap; that it really does at 320px is checked in a real browser.
describe('PageHeader', () => {
  const LONG_EN = 'Career tracks and the learning paths that lead to a job you want'
  const LONG_AR = 'مسارات مهنية وخطط تعلم تقودك إلى الوظيفة التي تريدها'

  it.each([['English', 'Career tracks'], ['Arabic', 'المسارات المهنية'], ['a long English title', LONG_EN], ['a long Arabic title', LONG_AR]])(
    'lets %s wrap on a phone and truncates it to one line from sm up',
    (_label, title) => {
      render(<PageHeader title={title} />)
      const h1 = screen.getByRole('heading', { level: 1 })
      // Below sm there is no truncation: the only truncate utility is behind sm:
      expect(h1.className.split(/\s+/)).not.toContain('truncate')
      expect(h1).toHaveClass('break-words', 'sm:truncate')
      expect(h1).not.toHaveClass('line-clamp-2')
    },
  )

  it('gives every title room on a phone by letting the action move to its own row', () => {
    render(<PageHeader title="Career tracks" />)
    const block = screen.getByRole('heading', { level: 1 }).parentElement as HTMLElement
    expect(block).toHaveClass('min-w-[10rem]', 'sm:min-w-0', 'flex-1')
    expect(block.parentElement).toHaveClass('flex-wrap')
  })

  it('does not change the desktop structure: one row, title first, the action after it, no clamp', () => {
    render(<PageHeader title="Explore" action={<button type="button">Go</button>} />)
    const h1 = screen.getByRole('heading', { level: 1 })
    const block = h1.parentElement as HTMLElement
    const row = block.parentElement as HTMLElement
    expect(row).toHaveClass('flex')
    expect(block).toHaveClass('sm:min-w-0')
    // the action only leaves DOM order below sm
    const action = screen.getByRole('button', { name: 'Go' }).parentElement as HTMLElement
    expect(action).toHaveClass('order-last', 'sm:order-none', 'w-full', 'sm:w-auto')
  })

  it('lets a sentence-length title wrap onto two lines at every width', () => {
    render(<PageHeader title="Good afternoon, Amira" wrapTitle />)
    const h1 = screen.getByRole('heading', { level: 1 })
    expect(h1).toHaveClass('line-clamp-2', 'break-words')
    expect(h1.className.split(/\s+/)).not.toContain('sm:truncate')
  })

  it('keeps the page action in the header on a phone', () => {
    render(<PageHeader title="Career tracks" action={<button type="button">New</button>} />)
    expect(screen.getByRole('button', { name: 'New' })).toBeInTheDocument()
  })

  it('lets a long subtitle wrap onto two lines at every width instead of cutting it off on a desktop', () => {
    render(<PageHeader title="Career tracks" subtitle="The curriculum libraries behind your Masar. Browse and enrol in the ones with published lessons." />)
    const sub = screen.getByText(/curriculum libraries/)
    expect(sub).toHaveClass('line-clamp-2')
    expect(sub.className).not.toMatch(/truncate/)
  })

  // The header and the content under it share ONE container, so the title's edge is the
  // content's edge at every width (they used to differ on /tracks, /tools and /learn).
  describe('contained', () => {
    it('takes the same container as a PageBody, class for class', () => {
      render(
        <>
          <PageHeader title="Career tracks" contained />
          <PageBody><p>the content</p></PageBody>
        </>,
      )
      const header = screen.getByRole('heading', { level: 1 }).parentElement!.parentElement!
      const content = screen.getByText('the content').parentElement!.parentElement!
      for (const cls of PAGE_CONTAINER.split(' ')) {
        expect(header).toHaveClass(cls)
        expect(content).toHaveClass(cls)
      }
    })

    it('scrolls the content on its own, under a header that stays put', () => {
      render(<PageBody><p>the content</p></PageBody>)
      const scroller = screen.getByText('the content').parentElement!.parentElement!.parentElement!
      expect(scroller).toHaveClass('flex-1', 'overflow-y-auto')
    })

    it('leaves a header that did not ask for it spanning the pane, as before', () => {
      render(<PageHeader title="Explore" />)
      const header = screen.getByRole('heading', { level: 1 }).parentElement!.parentElement!
      expect(header).not.toHaveClass('max-w-[1400px]')
      expect(header).toHaveClass('px-4', 'sm:px-6', 'lg:px-8')
    })
  })

  describe('dirAuto', () => {
    it('lets a title and subtitle that come from content data pick their own direction', () => {
      render(<PageHeader title="What is LangChain?" subtitle="Build LLM pipelines." dirAuto />)
      expect(screen.getByRole('heading', { level: 1 })).toHaveAttribute('dir', 'auto')
      expect(screen.getByText('Build LLM pipelines.')).toHaveAttribute('dir', 'auto')
    })

    it("does not force a direction on a title that is the app's own text", () => {
      render(<PageHeader title="Career tracks" subtitle="Browse." />)
      expect(screen.getByRole('heading', { level: 1 })).not.toHaveAttribute('dir')
    })
  })

  // The language switcher, credit balance and account menu used to live here, and
  // so followed whichever page was open. They are the shell's now (ShellHeader).
  it('is only the title block: no language switcher, credits or account menu of its own', () => {
    render(<PageHeader title="Explore" />)
    expect(screen.queryByRole('button')).toBeNull()
    expect(screen.queryByRole('link')).toBeNull()
  })
})
