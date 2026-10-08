import { redirect } from 'next/navigation'

const TRACK_SLUGS = new Set([
  'data-analyst',
  'ml-engineer',
  'ai-developer',
  'mlops-engineer',
  'ai-engineer',
])

/** Preserve reliable legacy URLs; generated/specialized paths have no 1:1 track. */
export default async function LegacyPathPage({ params }: { params: Promise<{ slug: string }> }): Promise<never> {
  const { slug } = await params
  return redirect(TRACK_SLUGS.has(slug) ? `/tracks/${slug}` : '/tracks')
}
