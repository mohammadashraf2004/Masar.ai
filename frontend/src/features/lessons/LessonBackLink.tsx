'use client'

import Link from 'next/link'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import { useI18n } from '@/lib/i18n'

export function LessonBackLink({ href, label }: { href: string; label: string }) {
  const { isRtl } = useI18n()
  const Arrow = isRtl ? ArrowRight : ArrowLeft
  return (
    <Link
      href={href}
      aria-label={`${isRtl ? 'العودة إلى' : 'Back to'} ${label}`}
      className="inline-flex items-center gap-1.5 text-sm text-dim transition-colors hover:text-bright"
    >
      <Arrow size={16} aria-hidden="true" />
      <span>{label}</span>
    </Link>
  )
}
