import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { useLanguageStore } from '@/lib/language'
import { TrackCard } from './TrackCard'
import type { CareerTrackSummary, TrackCatalogueStatus } from '@/types'

function track(status: TrackCatalogueStatus): CareerTrackSummary {
  return {
    id: 5, slug: 'ai-engineer', title: 'AI Engineer', title_en: 'AI Engineer',
    title_ar: 'مهندس ذكاء اصطناعي', description: 'Canonical course workflow.',
    description_ar: 'سير عمل الدورات الأساسي.', estimated_weeks: 15,
    course_count: 7, hours: 120,
    progress: status === 'done' ? 100 : status === 'current' ? 46 : 0,
    status,
  }
}

describe('TrackCard localization and routing', () => {
  it.each([
    ['done', 'Completed'],
    ['current', 'Your current track'],
    ['open', 'Available'],
  ] as const)('renders the %s state and an explicit Explore Track action', (status, pill) => {
    render(<TrackCard track={track(status)} index={4} />)
    expect(screen.getByText(pill)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Explore Track' })).toHaveAttribute('href', '/tracks/ai-engineer')
    expect(screen.getByRole('link', { name: 'Explore AI Engineer' })).toHaveAttribute('href', '/tracks/ai-engineer')
    expect(screen.getByText('Canonical course workflow.')).toBeInTheDocument()
  })

  it('uses the Arabic title, description, status, and action in Arabic mode', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<TrackCard track={track('open')} index={0} />)
    expect(screen.getByText('مهندس ذكاء اصطناعي')).toBeInTheDocument()
    expect(screen.getByText('سير عمل الدورات الأساسي.')).toBeInTheDocument()
    expect(screen.getByText('متاح')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'استكشف المسار' })).toHaveAttribute('href', '/tracks/ai-engineer')
  })
})
