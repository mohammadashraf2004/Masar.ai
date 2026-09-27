'use client'
import { useEffect, useRef } from 'react'
import Link from 'next/link'
import { Menu, X } from 'lucide-react'
import { useI18n } from '@/lib/i18n'
import { AccountMenu } from '@/components/layout/AccountMenu'
import { CreditsBadge } from '@/components/layout/CreditsBadge'
import { GlobalSearch } from '@/components/layout/GlobalSearch'
import { LogoMark, Wordmark } from '@/components/layout/Logo'
import { MOBILE_MENU_ID } from '@/components/layout/MobileMenu'
import { useMobileNav } from '@/components/layout/MobileNavContext'
import { ThemeToggle } from '@/components/layout/ThemeToggle'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'

/**
 * The bar across the top of every signed-in page. One element, two layouts.
 *
 * From `lg` it is 64px: search on the left, and at the far end the language,
 * the credit pill, the theme toggle and the avatar. Below `lg` it is a 56px
 * site header — the mark and name, the credit pill, and the menu button — that
 * stays on screen as the page scrolls (below `lg` the document scrolls, so
 * without `sticky` the button that opens navigation would scroll away with it).
 * Whatever does not fit the phone bar is in the menu it opens.
 */
export function ShellHeader() {
  const { t } = useI18n()
  const { open, setOpen } = useMobileNav()
  const button = useRef<HTMLButtonElement>(null)

  // MobileNavProvider closes the menu on Escape; this puts focus back on the
  // button that opened it, as the account menu does for its avatar.
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') button.current?.focus() }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open])

  return (
    <header className="sticky top-0 z-50 flex h-14 shrink-0 items-center gap-3 border-b border-border bg-ink px-4 lg:static lg:h-16 lg:bg-transparent lg:px-8">
      <Link href="/dashboard" className="flex min-h-[44px] items-center gap-2 lg:hidden">
        <LogoMark size={28} label={null} />
        <Wordmark className="text-base text-white" />
      </Link>

      <GlobalSearch className="hidden min-w-0 flex-1 lg:block lg:max-w-[420px]" />

      <div className="ms-auto flex items-center gap-2 lg:gap-3">
        <LanguageSwitcher className="hidden lg:block" />
        <CreditsBadge />
        <ThemeToggle className="hidden lg:flex" />
        <AccountMenu className="hidden lg:block" />
        <button
          ref={button}
          type="button"
          onClick={() => setOpen(!open)}
          aria-label={open ? t('nav.closeMenu') : t('nav.openMenu')}
          aria-expanded={open}
          aria-controls={MOBILE_MENU_ID}
          data-tour="menu-button"
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-border bg-surface text-white transition-colors hover:border-amber/30 lg:hidden"
        >
          {open ? <X size={18} aria-hidden="true" /> : <Menu size={18} aria-hidden="true" />}
        </button>
      </div>
    </header>
  )
}
