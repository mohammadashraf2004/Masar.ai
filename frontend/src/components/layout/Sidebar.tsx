'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/lib/store'
import { useI18n } from '@/lib/i18n'
import { AltWordmark, LogoMark, Wordmark } from '@/components/layout/Logo'
import { Avatar } from '@/components/layout/AccountMenu'
import { LOW_CREDITS, useCreditBalance } from '@/components/layout/WalletContext'
import { isActive, navFor } from '@/components/layout/nav'

/** The wallet: what is left to spend, and the way to add to it. */
function WalletCard() {
  const { t } = useI18n()
  const balance = useCreditBalance()
  const low = balance !== null && balance < LOW_CREDITS

  return (
    <div className="flex flex-col gap-2 rounded-[10px] border border-border bg-surface p-3.5">
      <span className="text-xs text-dim">{t('nav.wallet')}</span>
      <div className="flex items-baseline gap-1.5">
        <span className={cn('font-mono text-[22px] font-medium', low ? 'text-rose' : 'text-white')}>
          {balance === null ? '—' : balance.toLocaleString('en-US')}
        </span>
        <span className="text-xs text-dim">{t('nav.credits')}</span>
      </div>
      <Link href="/billing" className="text-xs text-amber-text hover:underline">
        {t('nav.topUp')}
      </Link>
    </div>
  )
}

/** Who is signed in, and the way to their profile. */
function UserRow() {
  const user = useAuthStore((s) => s.user)
  if (!user) return null
  return (
    <Link
      href="/profile"
      className="flex items-center gap-2.5 rounded-lg px-1 py-1 transition-colors hover:bg-panel"
    >
      <Avatar name={user.full_name} size={32} />
      <span className="flex min-w-0 flex-col gap-0.5">
        <span className="truncate text-[13px] font-semibold text-white">{user.full_name}</span>
        <span className="truncate text-[11px] capitalize text-ghost">{user.experience_level}</span>
      </span>
    </Link>
  )
}

/**
 * The desktop sidebar (from `lg` up; below that the same destinations are in
 * the mobile menu): the brand, the navigation, then the wallet and the account.
 *
 * The nav scrolls on its own. Without `min-h-0` a flex child refuses to shrink
 * below its content, so on a short viewport the wallet and account below it
 * were pushed out of the clipped shell.
 */
export function Sidebar() {
  const pathname = usePathname()
  const role = useAuthStore((s) => s.user?.role)
  const { t } = useI18n()
  const items = navFor(role)

  return (
    <aside className="hidden w-[248px] shrink-0 flex-col gap-7 border-e border-border bg-ink px-4 py-5 lg:flex">
      {/* Brand: the name in the reader's script leads; the other script sits at the far end. */}
      <Link href="/dashboard" className="flex shrink-0 items-center gap-2.5 px-1.5">
        <LogoMark size={28} label={null} />
        <Wordmark className="text-[17px] text-white" />
        <AltWordmark className="ms-auto text-[17px] text-ghost" />
      </Link>

      <nav aria-label={t('nav.menu')} className="min-h-0 flex-1 overflow-y-auto">
        <ul className="flex flex-col gap-1">
          {items.map(({ href, icon: Icon, label, tour }) => {
            const active = isActive(pathname, href)
            return (
              <li key={href}>
                <Link
                  href={href}
                  data-tour={tour}
                  aria-current={active ? 'page' : undefined}
                  className={cn(
                    'flex items-center gap-3 rounded-lg border px-3 py-2.5 text-sm transition-colors',
                    active
                      ? 'border-border bg-panel font-semibold text-white'
                      : 'border-transparent text-dim hover:bg-panel/60 hover:text-bright',
                  )}
                >
                  <Icon size={18} strokeWidth={1.8} className="shrink-0" />
                  <span className="min-w-0 flex-1">{t(label)}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="flex shrink-0 flex-col gap-3.5">
        <WalletCard />
        <UserRow />
      </div>

    </aside>
  )
}
