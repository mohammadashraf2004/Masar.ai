'use client'
import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { BarChart3, CircleHelp, CreditCard, LogOut, ReceiptText, User, Zap } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/lib/store'
import { useI18n } from '@/lib/i18n'
import { useTours } from '@/features/tours/TourProvider'

/** The account's initial in a neutral 34px circle (the handoff's avatar). */
export function Avatar({ name, size = 34, className }: { name: string; size?: number; className?: string }) {
  return (
    <span
      aria-hidden="true"
      style={{ width: size, height: size }}
      className={cn(
        'grid shrink-0 place-items-center rounded-full border border-border bg-panel text-[13px] font-semibold text-white',
        className,
      )}
    >
      {name.charAt(0).toUpperCase()}
    </span>
  )
}

/**
 * The avatar in the header and the menu behind it: profile, credits, sign out
 * (and, for an admin, the analytics page). Below `lg` the same things are in
 * the mobile menu instead.
 */
export function AccountMenu({ className }: { className?: string }) {
  const { user, logout } = useAuthStore()
  const { t } = useI18n()
  const tours = useTours()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const trigger = useRef<HTMLButtonElement>(null)

  // Close on outside click, or on Escape (handing focus back to the avatar)
  useEffect(() => {
    if (!open) return
    const onMouseDown = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return
      setOpen(false)
      trigger.current?.focus()
    }
    document.addEventListener('mousedown', onMouseDown)
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('mousedown', onMouseDown)
      document.removeEventListener('keydown', onKeyDown)
    }
  }, [open])

  if (!user) return null

  return (
    <div className={cn('relative', className)} ref={ref}>
      <button
        ref={trigger}
        type="button"
        onClick={() => setOpen(o => !o)}
        className={cn(
          'flex min-h-[44px] min-w-[44px] items-center justify-center rounded-full lg:min-h-0 lg:min-w-0',
          open && 'ring-2 ring-amber/40',
        )}
        aria-expanded={open}
        aria-label={`${t('nav.profileMenu')}: ${user.full_name}`}
      >
        <Avatar name={user.full_name} />
      </button>

      {open && (
        <div className="absolute end-0 top-full z-50 mt-2 w-52 max-w-[calc(100vw-2rem)] overflow-hidden rounded-xl border border-border bg-ink shadow-2xl">
          <div className="border-b border-border px-4 py-3">
            <p className="truncate text-xs font-semibold text-bright">{user.full_name}</p>
            <p className="truncate text-xs text-ghost">{user.email}</p>
          </div>

          <div className="py-1.5">
            <Link
              href="/billing"
              onClick={() => setOpen(false)}
              className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
            >
              <User size={13} className="text-ghost" />
              Profile & Scorecard
            </Link>
            <Link
              href="/profile"
              onClick={() => setOpen(false)}
              className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
            >
              <Zap size={13} className="text-ghost" />
              Buy Credits
            </Link>
            <Link
              href="/billing/orders"
              onClick={() => setOpen(false)}
              className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
            >
              <ReceiptText size={13} className="text-ghost" />
              Billing &amp; payments
            </Link>

            {/* Admins only. The account menu is where someone looks for
                "the things I can do because of who I am", which is why the
                link lives here as well as in the sidebar. */}
            {user.role === 'admin' && (
              <>
                <Link
                  href="/admin/analytics"
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
                >
                  <BarChart3 size={13} className="text-amber-text" />
                  Admin analytics
                </Link>
                <Link
                  href="/admin/billing"
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
                >
                  <CreditCard size={13} className="text-amber-text" />
                  Admin billing
                </Link>
              </>
            )}
          </div>

          {/* The help menu: for now, the walkthrough. */}
          {tours && (
            <div role="group" aria-label={t('nav.help')} className="border-t border-border py-1.5">
              <p className="px-4 pb-1 pt-1.5 text-[11px] font-medium text-ghost">{t('nav.help')}</p>
              <button
                type="button"
                onClick={() => { setOpen(false); tours.replay() }}
                className="flex w-full items-center gap-2.5 px-4 py-2 text-xs text-soft transition-colors hover:bg-surface hover:text-bright"
              >
                <CircleHelp size={13} className="text-ghost" aria-hidden="true" />
                {t('tour.replay')}
              </button>
            </div>
          )}

          <div className="border-t border-border py-1.5">
            <button
              onClick={() => { setOpen(false); logout() }}
              className="flex w-full items-center gap-2.5 px-4 py-2 text-xs text-ghost transition-colors hover:bg-rose/5 hover:text-rose"
            >
              <LogOut size={13} />
              Sign out
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
