import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import { SkillGapSummary } from '@/components/learning/SkillGapSummary'
import { useLanguageStore } from '@/lib/language'

const props = { known: 4, partial: 2, missing: 6, total: 12, coveragePct: 33.3, immediate: 3 }

describe('SkillGapSummary', () => {
  it('shows the server\'s coverage, rounded, and the counts it was given', () => {
    render(<SkillGapSummary {...props} />)
    expect(screen.getByText('33%')).toBeInTheDocument()
    expect(screen.getByRole('progressbar', { name: 'Skill coverage' })).toHaveAttribute('aria-valuenow', '33')
    expect(screen.getByText('You know 4 of 12 skills')).toBeInTheDocument()
    expect(screen.getByText('4 known')).toBeInTheDocument()
    expect(screen.getByText('2 in progress')).toBeInTheDocument()
    expect(screen.getByText('6 to gain')).toBeInTheDocument()
    expect(screen.getByText('3 needed right now')).toBeInTheDocument()
  })

  it('computes nothing: the percentage is whatever the server reported, even if the counts disagree with it', () => {
    render(<SkillGapSummary {...props} coveragePct={80} />)
    expect(screen.getByText('80%')).toBeInTheDocument()          // 4/12 would be 33% - the component does not check
  })

  it('leaves out the in-progress and immediate figures when there are none', () => {
    render(<SkillGapSummary {...props} partial={0} immediate={0} />)
    expect(screen.queryByText(/in progress/)).toBeNull()
    expect(screen.queryByText(/needed right now/)).toBeNull()
  })

  it('shows 0% for a learner who knows nothing yet, not an empty state', () => {
    render(<SkillGapSummary known={0} partial={0} missing={5} total={5} coveragePct={0} />)
    expect(screen.getByText('0%')).toBeInTheDocument()
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '0')
  })

  it('says there is nothing to measure — not 0% — when no skill is relevant', () => {
    render(<SkillGapSummary known={0} partial={0} missing={0} total={0} coveragePct={null} />)
    expect(screen.getByText('There are no skills to measure yet.')).toBeInTheDocument()
    expect(screen.queryByRole('progressbar')).toBeNull()
    expect(screen.queryByText('0%')).toBeNull()
  })

  it('reads in Arabic, with the percentage kept left-to-right', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<SkillGapSummary {...props} />)
    expect(screen.getByText('تعرف 4 من 12 مهارة')).toBeInTheDocument()
    expect(screen.getByText('4 تعرفها')).toBeInTheDocument()
    expect(screen.getByText('6 ستكتسبها')).toBeInTheDocument()
    expect(screen.getByText('33%')).toHaveAttribute('dir', 'ltr')
    expect(screen.getByRole('progressbar', { name: 'تغطية المهارات' })).toBeInTheDocument()
  })
})

beforeEach(() => useLanguageStore.setState({ language: 'en' }))
