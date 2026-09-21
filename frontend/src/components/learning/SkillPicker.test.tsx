import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useState } from 'react'
import { describe, expect, it, vi } from 'vitest'
import { SkillPicker, groupSkillOptions } from '@/components/learning/SkillPicker'
import { useLanguageStore } from '@/lib/language'
import { NLP, SKILL_OPTIONS, VISION, ref } from '@/test/fixtures'
import type { SkillOption } from '@/types'

function Harness({ options = SKILL_OPTIONS, initial = [] as string[], onChange = vi.fn() }) {
  const [value, setValue] = useState<string[]>(initial)
  return (
    <SkillPicker
      options={options}
      value={value}
      onChange={(next) => {
        setValue(next)
        onChange(next)
      }}
    />
  )
}

const option = (over: Partial<SkillOption>): SkillOption => ({
  slug: 'x', name: 'X', name_ar: null, kind: 'skill', group: null, is_required: false, course_count: 1, ...over,
})

describe('grouping — derived from what the catalogue sent, never named here', () => {
  it('files a skill under its field, tools together, and the rest under General', () => {
    const groups = groupSkillOptions(SKILL_OPTIONS)
    expect(groups.map((g) => [g.kind, g.options.map((o) => o.slug)])).toEqual([
      ['general', ['evaluation']],
      ['field', ['llms', 'rag', 'embeddings']],
      ['tools', ['langchain', 'fastapi']],
    ])
  })

  it('creates a section for a field it has never heard of', () => {
    const robotics = { slug: 'robotics', name: 'Robotics', name_ar: 'الروبوتات', icon: 'cpu' }
    const groups = groupSkillOptions([option({ slug: 'slam', name: 'SLAM', group: robotics })])
    expect(groups).toHaveLength(1)
    expect(groups[0].field?.slug).toBe('robotics')
  })

  it('keeps a group at the position of its first member, in the server\'s order', () => {
    const groups = groupSkillOptions([
      option({ slug: 'a', group: ref(VISION) }), option({ slug: 'b', group: ref(NLP) }), option({ slug: 'c', group: ref(VISION) }),
    ])
    expect(groups.map((g) => g.field?.slug)).toEqual(['computer-vision', 'nlp'])
    expect(groups[0].options.map((o) => o.slug)).toEqual(['a', 'c'])
  })

  it('never puts a tool under a field, even if the server attached one', () => {
    const groups = groupSkillOptions([option({ slug: 'lc', kind: 'tool', group: ref(NLP) })])
    expect(groups[0].kind).toBe('tools')
  })
})

describe('the checkboxes', () => {
  it('are native checkboxes, each with an associated label', () => {
    render(<Harness />)
    for (const input of screen.getAllByRole('checkbox')) {
      expect(input.tagName).toBe('INPUT')
      expect(input).toHaveAttribute('type', 'checkbox')
      const label = document.querySelector(`label[for="${input.id}"]`)
      expect(label).not.toBeNull()
      // The label's text is the input's name (a "needed for this goal" badge may follow it).
      expect(input).toHaveAccessibleName(new RegExp(`^${label!.querySelector('bdi')!.textContent}`))
    }
  })

  it('give every option its own id, so labels never point at the wrong box', () => {
    render(<Harness />)
    const ids = screen.getAllByRole('checkbox').map((c) => c.id)
    expect(new Set(ids).size).toBe(ids.length)
  })

  it('toggle from the keyboard and by tapping the row', async () => {
    const user = userEvent.setup()
    render(<Harness />)
    const rag = screen.getByRole('checkbox', { name: /RAG/ })
    rag.focus()
    await user.keyboard(' ')
    expect(rag).toBeChecked()
    await user.click(rag.closest('label') as HTMLElement)
    expect(rag).not.toBeChecked()
  })

  it('have a visible focus state and a touch-sized row', () => {
    render(<Harness />)
    const label = screen.getByRole('checkbox', { name: /RAG/ }).closest('label') as HTMLElement
    expect(label.className).toContain('has-[:focus-visible]:outline')
    expect(label.className).toContain('min-h-[44px]')
  })

  it('show what is checked by more than colour: a tick, and the checked state', async () => {
    const user = userEvent.setup()
    render(<Harness />)
    const rag = screen.getByRole('checkbox', { name: /RAG/ })
    const label = rag.closest('label') as HTMLElement
    expect(label.querySelector('svg')).toBeNull()
    await user.click(label)
    expect(label.querySelector('svg')).not.toBeNull()
    expect(rag).toBeChecked()
  })

  it('reports the whole selection on every change', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    render(<Harness onChange={onChange} />)
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    await user.click(screen.getByRole('checkbox', { name: /Embeddings/ }))
    expect(onChange).toHaveBeenLastCalledWith(['rag', 'embeddings'])
    await user.click(screen.getByRole('checkbox', { name: /RAG/ }))
    expect(onChange).toHaveBeenLastCalledWith(['embeddings'])
  })
})

describe('select all and clear', () => {
  it('selects every skill on screen and reports the count', async () => {
    const user = userEvent.setup()
    render(<Harness />)
    await user.click(screen.getByRole('button', { name: 'Select all' }))
    expect(screen.getAllByRole('checkbox').every((c) => (c as HTMLInputElement).checked)).toBe(true)
    expect(screen.getByRole('status')).toHaveTextContent(`${SKILL_OPTIONS.length} selected`)
  })

  it('clears every skill on screen', async () => {
    const user = userEvent.setup()
    render(<Harness initial={['rag', 'llms']} />)
    expect(screen.getByRole('status')).toHaveTextContent('2 selected')
    await user.click(screen.getByRole('button', { name: 'Clear all' }))
    expect(screen.getByRole('status')).toHaveTextContent('0 selected')
  })

  it('leaves alone a skill the learner declared that this route does not list', async () => {
    const user = userEvent.setup()
    const onChange = vi.fn()
    render(<Harness initial={['rag', 'telepathy']} onChange={onChange} />)
    expect(screen.getByRole('status')).toHaveTextContent('1 selected') // only what is on screen is counted
    await user.click(screen.getByRole('button', { name: 'Clear all' }))
    expect(onChange).toHaveBeenLastCalledWith(['telepathy'])            // ...and only that is cleared
    await user.click(screen.getByRole('button', { name: 'Select all' }))
    expect(onChange).toHaveBeenLastCalledWith(expect.arrayContaining(['telepathy', 'rag', 'llms']))
  })

  it('cannot clear when nothing is selected', () => {
    render(<Harness />)
    expect(screen.getByRole('button', { name: 'Clear all' })).toBeDisabled()
  })
})

describe('what it shows', () => {
  it('marks the skills the goal needs', () => {
    render(<Harness />)
    const evaluation = screen.getByRole('checkbox', { name: /Evaluation/ }).closest('label') as HTMLElement
    expect(within(evaluation).getByText('Needed for this goal')).toBeInTheDocument()
    const rag = screen.getByRole('checkbox', { name: /RAG/ }).closest('label') as HTMLElement
    expect(within(rag).queryByText('Needed for this goal')).toBeNull()
  })

  it('separates tools from skills and says a tool is not the skill', () => {
    render(<Harness />)
    const tools = screen.getByRole('group', { name: 'Tools & frameworks' })
    expect(within(tools).getByText(/Knowing a tool is not the same as knowing the skill/)).toBeInTheDocument()
    expect(within(screen.getByRole('group', { name: /NLP & LLMs/ })).queryByText(/Knowing a tool/)).toBeNull()
  })

  it('has no "Tools" heading when there are no tools', () => {
    render(<Harness options={SKILL_OPTIONS.filter((o) => o.kind !== 'tool')} />)
    expect(screen.queryByRole('group', { name: 'Tools & frameworks' })).toBeNull()
  })
})

describe('Arabic (RTL)', () => {
  it('reads in Arabic, with English skill names kept left-to-right', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    render(<Harness />)
    expect(screen.getByRole('button', { name: 'اختر الكل' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'إلغاء الكل' })).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('تم اختيار 0')
    expect(screen.getByRole('group', { name: 'الأدوات والأطر' })).toBeInTheDocument()
    const rag = screen.getByRole('checkbox', { name: /RAG/ }).closest('label') as HTMLElement
    expect(rag.querySelector('bdi')).toHaveAttribute('dir', 'ltr')
    const evaluation = screen.getByRole('checkbox', { name: /Evaluation/ }).closest('label') as HTMLElement
    expect(within(evaluation).getByText('مطلوبة لهذا الهدف')).toBeInTheDocument()
  })

  it('uses only logical (start/end) spacing, so the checkbox sits on the reading side', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    const { container } = render(<Harness />)
    expect(container.innerHTML).not.toMatch(/\b(?:ml|mr|pl|pr)-\d|text-left|text-right/)
  })
})
