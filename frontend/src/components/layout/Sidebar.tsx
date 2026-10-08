'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/lib/store'
import { useI18n } from '@/lib/i18n'
import { LogoMark, Wordmark } from '@/components/layout/Logo'
import { Avatar } from '@/components/layout/AccountMenu'
import { isActive, navFor } from '@/components/layout/nav'

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
  const { t, language } = useI18n()
  const items = navFor(role)

  return (
    <aside className="hidden w-[248px] shrink-0 flex-col gap-7 border-e border-border bg-ink px-4 py-5 lg:flex">
      {/* The locale-aware wordmark shows Masar in English and مسار in Arabic. */}
      <Link
        href="/"
        aria-label={language === 'ar' ? 'مسار' : 'Masar'}
        className="flex shrink-0 items-center gap-2.5 px-1.5"
      >
        <LogoMark size={28} label={null} />
        <Wordmark className="text-[17px] text-white" />
      </Link>

      <nav aria-label={t('nav.menu')} className="min-h-0 flex-1 overflow-y-auto">
        <ul className="flex flex-col gap-1">
          {items.map(({ href, icon: Icon, label, tour, groupStart }) => {
            const active = isActive(pathname, href)
            return (
              <li key={href} className={groupStart ? 'mt-3 border-t border-border pt-3' : undefined}>
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

      <UserRow />

    </aside>
  )
}
