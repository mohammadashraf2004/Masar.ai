'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { CircleHelp, LogOut } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/lib/store'
import { useI18n } from '@/lib/i18n'
import { Avatar } from '@/components/layout/AccountMenu'
import { useMobileNav } from '@/components/layout/MobileNavContext'
import { ThemeToggle } from '@/components/layout/ThemeToggle'
import { isActive, navFor } from '@/components/layout/nav'
import { LegalLinks } from '@/components/legal/LegalLinks'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { useTours } from '@/features/tours/TourProvider'

/** What the header's menu button controls. */
export const MOBILE_MENU_ID = 'mobile-menu'

/**
 * Navigation below `lg`: a panel that drops from the header over a dimmed page.
 *
 * The same destinations as the sidebar, as 48px rows. The account, the theme
 * and the language live in its footer, because the header has no room for
 * them. Choosing a route closes it (and so does a tap on the dimmed page,
 * Escape, and any route change — MobileNavProvider owns that).
 *
 * It is a disclosure, not a modal: it opens where its button is, focus stays
 * on the button, and the next Tab lands on the first row.
 */
export function MobileMenu() {
  const { open, setOpen } = useMobileNav()
  const pathname = usePathname()
  const { user, logout } = useAuthStore()
  const { t } = useI18n()
  const tours = useTours()

  if (!open) return null
  const close = () => setOpen(false)

  return (
    <>
      {/* The dimmed page. Tapping it closes the menu. */}
      <div
        className="fixed inset-x-0 bottom-0 top-14 z-30 bg-scrim/50 lg:hidden"
        onClick={close}
        aria-hidden="true"
      />
      {/* The height cap (header 3.5rem + a 4rem strip) is deliberate: with every
          destination in it the panel would otherwise fill the screen, leaving no
          dimmed page to tap and no sign that it is an overlay. It scrolls inside. */}
      <nav
        id={MOBILE_MENU_ID}
        aria-label={t('nav.menu')}
        className="fixed inset-x-0 top-14 z-40 max-h-[calc(100dvh-7.5rem)] overflow-y-auto border-b border-border bg-ink px-4 pb-[18px] pt-2.5 lg:hidden"
      >
        <ul className="flex flex-col gap-1">
          {navFor(user?.role).map(({ href, icon: Icon, label }) => {
            const active = isActive(pathname, href)
            return (
              <li key={href}>
                <Link
                  href={href}
                  onClick={close}
                  aria-current={active ? 'page' : undefined}
                  className={cn(
                    'flex min-h-[48px] items-center gap-3 rounded-lg px-3 text-base transition-colors',
                    active ? 'bg-panel font-bold text-white' : 'text-dim hover:bg-panel/60 hover:text-bright',
                  )}
                >
                  <Icon size={18} strokeWidth={1.8} className="shrink-0" />
                  <span className="min-w-0 flex-1">{t(label)}</span>
                </Link>
              </li>
            )
          })}
        </ul>

        <div className="mt-2.5 flex flex-col gap-2 border-t border-border pt-3.5">
          <div className="flex items-center justify-between gap-3">
            {user ? (
              <Link href="/profile" onClick={close} className="flex min-h-[44px] min-w-0 items-center gap-2.5">
                <Avatar name={user.full_name} size={32} />
                <span className="truncate text-sm font-semibold text-white">{user.full_name}</span>
              </Link>
            ) : <span />}
            <ThemeToggle />
          </div>

          <div className="flex items-center justify-between gap-3">
            {/* Opens upward: this row is at the bottom of a scrolling panel. */}
            <LanguageSwitcher placement="up" align="start" />
            {user && (
              <button
                type="button"
                onClick={() => { close(); logout() }}
                className="inline-flex min-h-[44px] items-center gap-2 px-2 text-sm text-ghost transition-colors hover:text-rose"
              >
                <LogOut size={14} className="shrink-0" aria-hidden="true" />
                {t('nav.signOut')}
              </button>
            )}
          </div>

          {/* The help menu: for now, the walkthrough. */}
          {tours && (
            <button
              type="button"
              onClick={() => { close(); tours.replay() }}
              className="inline-flex min-h-[44px] items-center gap-2 self-start px-2 text-sm text-soft transition-colors hover:text-bright"
            >
              <CircleHelp size={14} className="shrink-0" aria-hidden="true" />
              {t('tour.replay')}
            </button>
          )}

          <LegalLinks />
        </div>
      </nav>
    </>
  )
}
