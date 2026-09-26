'use client'
import { usePathname } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { FIRST_ROADMAP_INTRO, WHATS_NEW } from '@/lib/releases'
import { SkillGapIntroDialog } from './SkillGapIntroDialog'
import { WhatsNewDialog } from './WhatsNewDialog'

/**
 * Where an announcement may interrupt: the places a learner lands (home, the
 * dashboard) and the roadmap it points at - never a lesson, an exam, a payment
 * or a sign-in page. Elsewhere it simply waits for the next visit.
 */
const PLACES = new Set(['/', '/dashboard', '/learn', '/learn/masar'])

/**
 * Shows the announcement the server says this account has yet to see, if any.
 *
 * Which one is the server's decision (`user.pending_updates`, first entry): an
 * existing account is told what is new; a new one meets the feature in its
 * first roadmap. Nothing here decides who is new, and nothing is shown while the
 * Terms are waiting to be accepted - those come first, and a session that predates
 * this field is refreshed by LegalGate, whose answer carries it.
 */
export function UpdateGate() {
  const token = useAuthStore((s) => s.token)
  const user = useAuthStore((s) => s.user)
  const pathname = usePathname()

  if (!token || !user || user.requires_legal_acceptance !== false) return null
  if (!PLACES.has(pathname)) return null

  switch (user.pending_updates?.[0]) {
    case WHATS_NEW: return <WhatsNewDialog />
    case FIRST_ROADMAP_INTRO: return <SkillGapIntroDialog />
    default: return null   // none due, or one a later build knows how to draw
  }
}
