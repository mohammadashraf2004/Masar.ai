'use client'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { ProjectLabPage } from '@/features/project-lab/ProjectLabPage'

/** Challenges › Projects › one project's overview (and, once submitted, its completion summary). */
export default function ChallengeProjectPage() {
  const { slug } = useParams() as { slug: string }
  return (
    <AppShell>
      <ProjectLabPage slug={slug} />
    </AppShell>
  )
}
