import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import { ExerciseBrief, splitBrief } from './ExerciseBrief'

const ENGLISH = [
  'Train a decision tree on the iris data.',
  '',
  '**Instructions**',
  '',
  '1. Create the model.',
  '2. Fit it on `X_train, y_train`.',
  '',
  '**Expected output**',
  '',
  'An accuracy above 0.9.',
  '',
  '**Think about it**',
  '',
  'Why does a deeper tree overfit?',
].join('\n')

const ARABIC = [
  'درّب شجرة قرار على بيانات iris.',
  '',
  '**التعليمات**',
  '',
  '1. أنشئ الـ model.',
  '2. درّبه على `X_train, y_train`.',
  '',
  '**المخرَج المتوقع**',
  '',
  'دقة أعلى من 0.9.',
].join('\n')

beforeEach(() => {
  useLanguageStore.setState({ language: 'en', mode: 'arabic_first', annotateTerms: true })
})

describe('splitBrief', () => {
  it('splits an English brief into goal, steps, expected output and reflection', () => {
    expect(splitBrief(ENGLISH)).toEqual({
      goal: 'Train a decision tree on the iris data.',
      steps: '1. Create the model.\n2. Fit it on `X_train, y_train`.',
      expected: 'An accuracy above 0.9.',
      reflect: 'Why does a deeper tree overfit?',
    })
  })

  it('recognises the Arabic headings and keeps code untouched', () => {
    const brief = splitBrief(ARABIC)
    expect(brief.goal).toBe('درّب شجرة قرار على بيانات iris.')
    expect(brief.steps).toContain('`X_train, y_train`')
    expect(brief.expected).toBe('دقة أعلى من 0.9.')
    expect(brief.reflect).toBe('')
  })
})

describe('ExerciseBrief', () => {
  it('shows the goal and numbered steps above everything else, and marks reflection as ungraded', () => {
    render(<ExerciseBrief content={ENGLISH} dir="ltr" />)
    const headings = screen.getAllByRole('heading', { level: 3 }).map(h => h.textContent)
    expect(headings).toEqual(['Goal', 'Steps', 'Expected output', 'Think about it'])
    expect(screen.getByText('· Not graded')).toBeInTheDocument()
    expect(screen.getAllByRole('listitem').map(item => item.textContent)).toEqual([
      'Create the model.', 'Fit it on X_train, y_train.',
    ])
  })

  it('labels an Arabic brief in Arabic and lays it out right to left', () => {
    useLanguageStore.setState({ language: 'ar' })
    const { container } = render(<ExerciseBrief content={ARABIC} dir="rtl" />)
    expect(screen.getAllByRole('heading', { level: 3 }).map(h => h.textContent)).toEqual([
      'الهدف', 'الخطوات', 'المخرَج المتوقع',
    ])
    expect(container.firstElementChild).toHaveAttribute('dir', 'rtl')
    expect(screen.getByText('X_train, y_train')).toBeInTheDocument()
  })

  it('shows an unstructured brief whole', () => {
    const { container } = render(<ExerciseBrief content="Explain overfitting in two sentences." dir="ltr" />)
    expect(screen.getAllByRole('heading', { level: 3 })).toHaveLength(1)
    // Glossary terms are annotated inline, so match the text, not one node.
    expect(container).toHaveTextContent(/Explain overfitting.*in two sentences\./i)
  })
})
