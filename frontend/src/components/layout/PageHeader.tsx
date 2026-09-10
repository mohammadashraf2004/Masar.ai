'use client'
import { useEffect, useState, useRef } from 'react'
import Link from 'next/link'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { useI18n } from '@/lib/i18n'
import { useMobileNav } from '@/components/layout/MobileNavContext'
import { Zap, AlertTriangle, User, LogOut, Settings, Menu } from 'lucide-react'

// ── Mobile drawer toggle ──────────────────────────────────────────────────────
/**
 * The only entry point to navigation below `lg`, where AppShell's sidebar is
 * hidden. Renders nothing when no AppShell wraps the page — the exam runner
 * builds its own shell and has no drawer to open.
 */
function MobileNavToggle() {
  const { open, setOpen, available } = useMobileNav()
  const { t } = useI18n()

  if (!available) return null

  return (
    <button
      type="button"
      onClick={() => setOpen(!open)}
      aria-label={t('nav.openMenu')}
      aria-expanded={open}
      className="lg:hidden -ms-1 flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-border text-soft hover:text-bright hover:border-amber/30 transition-colors"
    >
      <Menu size={18} />
    </button>
  )
}

interface PageHeaderProps {
  title: string
  subtitle?: string
  action?: React.ReactNode
  className?: string
}

// ── Credits badge ─────────────────────────────────────────────────────────────
function CreditsBadge() {
  const [balance, setBalance] = useState<number | null>(null)

  useEffect(() => {
    api.getWallet().then(w => setBalance(w.credit_balance)).catch(() => {})
  }, [])

  if (balance === null) return null

  const low = balance < 20

  return (
    <Link
      href="/profile"
      className={cn(
        'flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono font-semibold transition-all',
        low
          ? 'bg-rose/10 border-rose/30 text-rose hover:bg-rose/20'
          : 'bg-amber/10 border-amber/20 text-amber hover:bg-amber/20'
      )}
      title={low ? 'Low credits — click to top up' : 'Your credit balance'}
    >
      {low
        ? <AlertTriangle size={11} className="flex-shrink-0" />
        : <Zap size={11} className="flex-shrink-0" />
      }
      {/* The word costs ~45px the mobile header does not have. The number and
          the icon still say what this is, and the title needs the room. */}
      <span>{balance}</span>
      <span className="hidden sm:inline">credits</span>
    </Link>
  )
}

// ── Profile avatar + dropdown ─────────────────────────────────────────────────
function ProfileMenu() {
  const { user, logout } = useAuthStore()
  const [open, setOpen]  = useState(false)
  const ref              = useRef<HTMLDivElement>(null)

  // Close on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  if (!user) return null

  return (
    <div className="relative" ref={ref}>
      {/* Avatar button */}
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 group"
        title="Profile menu"
      >
        <div className={cn(
          'w-8 h-8 rounded-full bg-amber/20 border flex items-center justify-center transition-colors',
          open ? 'border-amber/60' : 'border-amber/30 group-hover:border-amber/60'
        )}>
          <span className="text-xs font-semibold text-amber">
            {user.full_name.charAt(0).toUpperCase()}
          </span>
        </div>
        <div className="hidden sm:block text-start">
          <p className="text-xs font-medium text-bright leading-none">{user.full_name.split(' ')[0]}</p>
          <p className="text-xs text-ghost capitalize leading-none mt-0.5">{user.experience_level}</p>
        </div>
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute end-0 top-full mt-2 w-52 max-w-[calc(100vw-2rem)] bg-ink border border-border rounded-xl shadow-2xl z-50 overflow-hidden">
          {/* User info */}
          <div className="px-4 py-3 border-b border-border">
            <p className="text-xs font-semibold text-bright truncate">{user.full_name}</p>
            <p className="text-xs text-ghost truncate">{user.email}</p>
          </div>

          {/* Menu items */}
          <div className="py-1.5">
            <Link
              href="/profile"
              onClick={() => setOpen(false)}
              className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft hover:text-bright hover:bg-surface transition-colors"
            >
              <User size={13} className="text-ghost" />
              Profile & Scorecard
            </Link>
            <Link
              href="/profile"
              onClick={() => setOpen(false)}
              className="flex items-center gap-2.5 px-4 py-2 text-xs text-soft hover:text-bright hover:bg-surface transition-colors"
            >
              <Zap size={13} className="text-ghost" />
              Buy Credits
            </Link>
          </div>

          {/* Sign out */}
          <div className="border-t border-border py-1.5">
            <button
              onClick={() => { setOpen(false); logout() }}
              className="w-full flex items-center gap-2.5 px-4 py-2 text-xs text-ghost hover:text-rose hover:bg-rose/5 transition-colors"
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

// ── PageHeader ────────────────────────────────────────────────────────────────
export function PageHeader({ title, subtitle, action, className }: PageHeaderProps) {
  return (
    <div className={cn(
      'flex flex-wrap items-center gap-x-3 gap-y-2.5 border-b border-border shrink-0',
      'px-4 sm:px-6 lg:px-8 py-4 sm:py-5',
      className
    )}>
      <MobileNavToggle />

      {/* Left: title + subtitle. `min-w-0` lets it shrink instead of forcing
          the controls off the edge; the subtitle wraps to two lines on a
          phone rather than being cut off at the first word. */}
      <div className="min-w-0 flex-1">
        <h1 className="font-display font-bold text-lg sm:text-xl text-white tracking-tight truncate">{title}</h1>
        {subtitle && (
          <p className="text-xs sm:text-sm text-ghost mt-0.5 line-clamp-2 sm:truncate">{subtitle}</p>
        )}
      </div>

      {/* Page action. Below sm it wraps to its own row rather than competing
          with the title for a share of ~150px; `order-last` puts it after the
          controls on that second row, and DOM order takes over again from sm
          so the desktop arrangement is unchanged. */}
      {action && (
        <div className="order-last sm:order-none w-full sm:w-auto shrink-0">{action}</div>
      )}

      {/* Right: language + credits + profile.
          The language control sits in the header rather than buried in
          settings: switching between Arabic explanations and industry
          terminology is something a student does mid-lesson, not once. */}
      <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0 ms-auto sm:ms-0">
        <LanguageSwitcher />
        <CreditsBadge />
        <ProfileMenu />
      </div>
    </div>
  )
}