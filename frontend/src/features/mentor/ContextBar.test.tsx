import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { ContextBar } from './ContextBar'

const courses = [
  { courseId: 'ml', title: 'Machine Learning', lessonsDone: 2, lessonsTotal: 7 },
  { courseId: 'rag', title: 'RAG Systems', lessonsDone: 0, lessonsTotal: 9 },
]

describe('ContextBar', () => {
  it('offers only the enrolled courses and General, and says when the whole course is attached', async () => {
    const onSelect = vi.fn()
    render(<ContextBar course={{ options: courses, selected: 'ml', enrolled: true, onSelect }} />)
    expect(screen.getByText('The mentor sees:')).toBeInTheDocument()
    const picker = screen.getByRole('combobox', { name: 'Course to ask about' })
    expect(Array.from((picker as HTMLSelectElement).options).map((o) => o.text)).toEqual([
      'General (no course)', 'Machine Learning · 2/7', 'RAG Systems · 0/9',
    ])
    expect(screen.getByText('The whole course')).toBeInTheDocument()
    expect(screen.queryByText(/Nothing\./)).toBeNull()
    await userEvent.selectOptions(picker, 'rag')
    expect(onSelect).toHaveBeenLastCalledWith('rag')
    await userEvent.selectOptions(picker, '')
    expect(onSelect).toHaveBeenLastCalledWith(null)
  })

  it('has nothing to attach or remove: no lesson or code chips, and no attach button', () => {
    render(<ContextBar course={{ options: courses, selected: 'ml', enrolled: true, onSelect: () => {} }} />)
    expect(document.querySelectorAll('[data-chip]')).toHaveLength(1)
    expect(document.querySelector('[data-chip="course"]')).toHaveTextContent('The whole course')
    expect(screen.queryAllByRole('button')).toHaveLength(0)
    expect(screen.queryByText(/Attach/)).toBeNull()
  })

  it('says the mentor will answer in general for General', () => {
    render(<ContextBar course={{ options: courses, selected: null, enrolled: false, onSelect: () => {} }} />)
    expect(screen.getByText(/Nothing\. The mentor will answer in general/)).toBeInTheDocument()
    expect(screen.queryByText('The whole course')).toBeNull()
  })

  it('names the course when the course list could not be read', () => {
    render(<ContextBar courseTitle="Machine Learning" />)
    expect(screen.queryByRole('combobox')).toBeNull()
    expect(document.querySelector('[data-chip="course"]')).toHaveTextContent('Machine Learning')
  })

  it('points a learner with no enrolment to the catalogue', () => {
    render(<ContextBar course={{ options: [], selected: null, enrolled: false, onSelect: () => {} }} />)
    expect(screen.getByText(/Enrol in a course to ask the mentor about it/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Browse courses' })).toHaveAttribute('href', '/explore')
    expect(screen.getByText(/Nothing\./)).toBeInTheDocument()
  })
})
