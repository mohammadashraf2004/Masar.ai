import { useState } from 'react'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { ContextBar } from './ContextBar'

function Harness({ lesson = 'LangGraph · Lesson 7', code = 'agent.py · exercise 3' }: { lesson?: string | null; code?: string | null }) {
  const [lessonOn, setLessonOn] = useState(true)
  const [codeOn, setCodeOn] = useState(true)
  return (
    <ContextBar
      lessonLabel={lesson}
      codeLabel={code}
      lessonOn={lessonOn}
      codeOn={codeOn}
      onToggleLesson={setLessonOn}
      onToggleCode={setCodeOn}
      onRestore={() => { setLessonOn(true); setCodeOn(true) }}
    />
  )
}

describe('ContextBar', () => {
  it('shows the lesson and the code the mentor will see, the code left to right in mono', () => {
    render(<Harness />)
    expect(screen.getByText('The mentor sees:')).toBeInTheDocument()
    expect(screen.getByText('LangGraph · Lesson 7')).toBeInTheDocument()
    const code = document.querySelector('[data-chip="code"]') as HTMLElement
    expect(code).toHaveAttribute('dir', 'ltr')
    expect(code.className).toContain('font-mono')
    expect(screen.queryByText(/Nothing\./)).toBeNull()
  })

  it('removes one chip at a time and keeps the other', async () => {
    render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: 'Remove LangGraph · Lesson 7' }))
    expect(screen.queryByText('LangGraph · Lesson 7')).toBeNull()
    expect(screen.getByText('agent.py · exercise 3')).toBeInTheDocument()
    expect(screen.queryByText(/Nothing\./)).toBeNull()
  })

  it('says the mentor will answer in general when both are removed, and attaching restores both', async () => {
    render(<Harness />)
    await userEvent.click(screen.getByRole('button', { name: 'Remove LangGraph · Lesson 7' }))
    await userEvent.click(screen.getByRole('button', { name: 'Remove agent.py · exercise 3' }))
    expect(screen.getByText(/Nothing\. The mentor will answer in general/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('button', { name: '+ Attach context' }))
    expect(screen.getByText('LangGraph · Lesson 7')).toBeInTheDocument()
    expect(screen.getByText('agent.py · exercise 3')).toBeInTheDocument()
  })

  it('has no attach button when nothing was removed, and none when there was nothing to attach', () => {
    const { unmount } = render(<Harness />)
    expect(screen.queryByRole('button', { name: '+ Attach context' })).toBeNull()
    unmount()
    render(<Harness lesson={null} code={null} />)
    expect(screen.queryByRole('button', { name: '+ Attach context' })).toBeNull()
    expect(screen.getByText(/Nothing\./)).toBeInTheDocument()
  })
})
