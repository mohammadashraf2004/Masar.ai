import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { GlobalSearch } from '@/components/layout/GlobalSearch'
import { useLanguageStore } from '@/lib/language'
import { useAuthStore } from '@/lib/store'
import { useAuthPrompt } from '@/components/auth/AuthPrompt'
import { router } from '@/test/nav'
import type { SearchHit, SearchResults } from '@/types'

vi.mock('@/lib/api', () => ({ api: { search: vi.fn() } }))
import { api } from '@/lib/api'

const hit = (over: Partial<SearchHit> & Pick<SearchHit, 'id' | 'title' | 'href'>): SearchHit => ({
  kind: 'tool_course', title_ar: null, parent_title: null, score: 1, matched_terms: [], ...over,
})
const results = (hits: SearchHit[]): SearchResults => ({ query: 'q', expanded: [], matched_terms: [], hits })

const LANGGRAPH = hit({ id: 1, title: 'LangGraph', title_ar: 'لانج جراف', href: '/tools/langgraph' })
const LANGCHAIN = hit({ id: 2, kind: 'lesson', title: 'LangChain basics', href: '/tools/langchain', parent_title: 'LangChain' })

// By role only: the accessible name is language-dependent, and is asserted where it matters.
const field = () => screen.getByRole('combobox')

beforeEach(() => {
  vi.mocked(api.search).mockResolvedValue(results([LANGGRAPH, LANGCHAIN]))
  // A signed-in learner; the signed-out case is asserted on its own below.
  useAuthStore.setState({ token: 'tok', _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
})

describe('GlobalSearch — the field', () => {
  it('is a labelled combobox that says what it searches, with the Ctrl K hint hidden from assistive technology', () => {
    render(<GlobalSearch />)
    expect(screen.getByRole('combobox', { name: 'Search' })).toBeInTheDocument()
    expect(field()).toHaveAttribute('placeholder', 'Search a course, tool or lesson…')
    expect(field()).toHaveAttribute('aria-autocomplete', 'list')
    expect(field()).toHaveAttribute('aria-expanded', 'false')
    const hint = screen.getByText('Ctrl K')
    expect(hint.closest('[aria-hidden="true"]')).not.toBeNull()
  })

  it('is in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<GlobalSearch />)
    expect(screen.getByRole('combobox', { name: 'بحث' })).toHaveAttribute('placeholder', 'ابحث عن دورة، أداة، أو درس…')
  })

  it('drops the shortcut hint once something is typed', async () => {
    const user = userEvent.setup()
    render(<GlobalSearch />)
    await user.type(field(), 'a')
    expect(screen.queryByText('Ctrl K')).toBeNull()
  })

  it.each([['Control'], ['Meta']])('is focused by %s+K from anywhere', (modifier) => {
    render(<div><GlobalSearch /><p>page</p></div>)
    expect(field()).not.toHaveFocus()
    fireEvent.keyDown(document.body, { key: 'k', ...(modifier === 'Control' ? { ctrlKey: true } : { metaKey: true }) })
    expect(field()).toHaveFocus()
  })
})

describe('GlobalSearch — asking', () => {
  it('waits for two characters before asking the server anything', async () => {
    const user = userEvent.setup()
    render(<GlobalSearch />)
    await user.type(field(), 'l')
    await act(() => new Promise((r) => setTimeout(r, 400)))
    expect(api.search).not.toHaveBeenCalled()
    expect(screen.queryByRole('listbox')).toBeNull()
  })

  it('asks once for a burst of typing, not once per key', async () => {
    const user = userEvent.setup()
    render(<GlobalSearch />)
    await user.type(field(), 'lang')
    expect(await screen.findByRole('listbox')).toBeInTheDocument()
    expect(api.search).toHaveBeenCalledTimes(1)
    expect(api.search).toHaveBeenCalledWith('lang')
  })

  it('lists what came back, each with its kind and its parent', async () => {
    const user = userEvent.setup()
    render(<GlobalSearch />)
    await user.type(field(), 'lang')
    const options = await screen.findAllByRole('option')
    expect(options).toHaveLength(2)
    expect(options[0]).toHaveAttribute('href', '/tools/langgraph')
    expect(options[0]).toHaveTextContent('Course')
    expect(options[0]).toHaveTextContent('LangGraph')
    expect(options[1]).toHaveTextContent('Lesson')
    expect(options[1]).toHaveTextContent('LangChain basics')
    expect(options[1]).toHaveTextContent('LangChain') // parent
    expect(field()).toHaveAttribute('aria-expanded', 'true')
    expect(field()).toHaveAttribute('aria-controls', screen.getByRole('listbox').id)
  })

  it('shows the Arabic title for an Arabic reader, and the kind in Arabic', async () => {
    useLanguageStore.setState({ language: 'ar' })
    const user = userEvent.setup()
    render(<GlobalSearch />)
    await user.type(field(), 'لانج')
    const first = (await screen.findAllByRole('option'))[0]
    expect(first).toHaveTextContent('دورة')
    expect(first).toHaveTextContent('لانج جراف')
  })

  it('says so when nothing matches, and when the request fails', async () => {
    const user = userEvent.setup()
    vi.mocked(api.search).mockResolvedValueOnce(results([]))
    const { unmount } = render(<GlobalSearch />)
    await user.type(field(), 'zzz')
    expect(await screen.findByText('Nothing matches that.')).toBeInTheDocument()
    unmount()

    vi.mocked(api.search).mockRejectedValueOnce(new Error('network'))
    render(<GlobalSearch />)
    await user.type(field(), 'zzz')
    expect(await screen.findByText('Nothing matches that.')).toBeInTheDocument()
  })

  it('never lets a slow answer to an earlier query replace the answer to the current one', async () => {
    const slow = { resolve: (_: SearchResults) => {} }
    vi.mocked(api.search)
      .mockImplementationOnce(() => new Promise<SearchResults>((r) => { slow.resolve = r }))
      .mockResolvedValueOnce(results([hit({ id: 9, title: 'Second answer', href: '/tools/second' })]))
    const user = userEvent.setup()
    render(<GlobalSearch />)

    await user.type(field(), 'ab')
    await waitFor(() => expect(api.search).toHaveBeenCalledTimes(1))
    await user.type(field(), 'c')
    expect(await screen.findByRole('option', { name: /Second answer/ })).toBeInTheDocument()

    // The first request finally answers — after the second already has.
    await act(async () => { slow.resolve(results([hit({ id: 8, title: 'First answer', href: '/tools/first' })])) })
    expect(screen.queryByRole('option', { name: /First answer/ })).toBeNull()
    expect(screen.getByRole('option', { name: /Second answer/ })).toBeInTheDocument()
  })
})

describe('GlobalSearch — the keyboard', () => {
  async function typeAndWait(user: ReturnType<typeof userEvent.setup>) {
    render(<GlobalSearch />)
    await user.type(field(), 'lang')
    await screen.findAllByRole('option')
  }

  it('moves through the results with the arrow keys, wrapping at both ends, and tells the screen reader which is current', async () => {
    const user = userEvent.setup()
    await typeAndWait(user)
    const [first, second] = screen.getAllByRole('option')
    expect(first).toHaveAttribute('aria-selected', 'false')

    await user.keyboard('{ArrowDown}')
    expect(first).toHaveAttribute('aria-selected', 'true')
    expect(field()).toHaveAttribute('aria-activedescendant', first.id)

    await user.keyboard('{ArrowDown}')
    expect(second).toHaveAttribute('aria-selected', 'true')
    expect(first).toHaveAttribute('aria-selected', 'false')

    await user.keyboard('{ArrowDown}') // wraps to the first
    expect(first).toHaveAttribute('aria-selected', 'true')
    await user.keyboard('{ArrowUp}') // and back to the last
    expect(second).toHaveAttribute('aria-selected', 'true')
    // focus never leaves the field: the highlight is aria-activedescendant, not focus
    expect(field()).toHaveFocus()
  })

  it('opens the highlighted result on Enter, and empties and closes the search', async () => {
    const user = userEvent.setup()
    await typeAndWait(user)
    await user.keyboard('{ArrowDown}{Enter}')
    expect(router.push).toHaveBeenCalledWith('/tools/langgraph')
    expect(field()).toHaveValue('')
    expect(screen.queryByRole('listbox')).toBeNull()
  })

  it('signed out, Enter on a course that needs an account asks them to sign in instead', async () => {
    useAuthStore.setState({ token: null })
    const user = userEvent.setup()
    await typeAndWait(user)
    await user.keyboard('{ArrowDown}{Enter}')
    expect(router.push).not.toHaveBeenCalledWith('/tools/langgraph')
    expect(useAuthPrompt.getState()).toMatchObject({ open: true, next: '/tools/langgraph' })
  })

  it('does nothing on Enter when no result is highlighted', async () => {
    const user = userEvent.setup()
    await typeAndWait(user)
    await user.keyboard('{Enter}')
    expect(router.push).not.toHaveBeenCalled()
    expect(screen.getByRole('listbox')).toBeInTheDocument()
  })

  it('closes the list on Escape and keeps what was typed', async () => {
    const user = userEvent.setup()
    await typeAndWait(user)
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('listbox')).toBeNull()
    expect(field()).toHaveValue('lang')
    expect(field()).toHaveAttribute('aria-expanded', 'false')
  })

  it('closes the list when the pointer goes elsewhere', async () => {
    const user = userEvent.setup()
    render(<div><GlobalSearch /><p>elsewhere</p></div>)
    await user.type(field(), 'lang')
    await screen.findAllByRole('option')
    await user.click(screen.getByText('elsewhere'))
    expect(screen.queryByRole('listbox')).toBeNull()
  })

  it('a click on a result lets the link navigate (no second router push) and closes the search', async () => {
    const user = userEvent.setup()
    // jsdom does not implement following a link; stop the click there.
    document.addEventListener('click', (e) => e.preventDefault(), { once: true, capture: true })
    await typeAndWait(user)
    await user.click(screen.getAllByRole('option')[1])
    expect(router.push).not.toHaveBeenCalled()
    expect(screen.queryByRole('listbox')).toBeNull()
    expect(field()).toHaveValue('')
  })
})
