'use client'
import { useParams } from 'next/navigation'
import { AppShell } from '@/components/layout/AppShell'
import { useAuth } from '@/hooks/useAuth'
import { ProjectWorkspacePage } from '@/features/project-lab/ProjectLabPage'

/** Challenges › Projects › one project's workspace (the lab). */
export default function ChallengeProjectWorkspacePage() {
  // The workspace is the learning itself: signed-out visitors are sent to sign
  // in and brought back here.
  useAuth()
  const { slug } = useParams() as { slug: string }
  return (
    <AppShell>
      <ProjectWorkspacePage slug={slug} />
    </AppShell>
  )
}
