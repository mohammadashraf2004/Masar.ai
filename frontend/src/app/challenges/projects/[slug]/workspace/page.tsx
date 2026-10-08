'use client'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { ProjectWorkspacePage } from '@/features/project-lab/ProjectLabPage'

/** Challenges › Projects › one project's workspace (the lab). */
export default function ChallengeProjectWorkspacePage() {
  const { slug } = useParams() as { slug: string }
  return (
    <AppShell>
      <ProjectWorkspacePage slug={slug} />
    </AppShell>
  )
}
