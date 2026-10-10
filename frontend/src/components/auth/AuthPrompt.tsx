'use client'
import { forwardRef, useCallback, useRef, type ComponentProps, type MouseEvent } from 'react'
import Link from 'next/link'
import { LogIn } from 'lucide-react'
import { create } from 'zustand'
import { Modal } from '@/components/ui/Modal'
import { buttonStyles } from '@/components/ui/Button'
import { authHref, currentPath, needsAccount, safeNext } from '@/lib/authRedirect'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'

/**
 * "Sign in to continue": what a signed-out visitor meets when they reach for
 * something that needs an account — a lesson, enrolling, joining a challenge,
 * the mentor. Browsing never opens it; only a deliberate action does.
 *
 * It offers Sign in and Create free account, both carrying where the visitor
 * was headed (`?next=`), so they land back on it afterwards. It decides
 * nothing about access: the server still answers every request, and a signed-in
 * learner keeps exactly the Free/Pro rules their account has.
 */

interface PromptState {
  open: boolean
  next: string | null
  show: (next: string) => void
  hide: () => void
}

export const useAuthPrompt = create<PromptState>((set) => ({
  open: false,
  next: null,
  show: (next) => set({ open: true, next: safeNext(next) }),
  hide: () => set({ open: false }),
}))

/**
 * `requireAuth(next?)`: true when someone is signed in; otherwise opens the
 * dialog (returning to `next`, or to this page) and returns false.
 */
export function useRequireAuth() {
  const token = useAuthStore((s) => s.token)
  const show = useAuthPrompt((s) => s.show)
  return useCallback(
    (next?: string) => {
      if (token) return true
      show(next ?? currentPath())
      return false
    },
    [token, show],
  )
}

/**
 * A link that may lead somewhere needing an account. Signed in, or pointing at
 * a page anyone may browse, it is an ordinary link; signed out and pointing at
 * an account page (a lesson, the mentor, Your Masar), a plain click opens the
 * dialog instead. A modified click still goes to the address, where the page's
 * own guard sends the visitor to sign in.
 */
export const GatedLink = forwardRef<HTMLAnchorElement, ComponentProps<typeof Link>>(function GatedLink(
  { href, onClick, ...props },
  ref,
) {
  const requireAuth = useRequireAuth()
  return (
    <Link
      ref={ref}
      href={href}
      {...props}
      onClick={(e: MouseEvent<HTMLAnchorElement>) => {
        onClick?.(e)
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
        if (typeof href !== 'string' || !needsAccount(href)) return
        if (!requireAuth(href)) e.preventDefault()
      }}
    />
  )
})

/** Rendered once by the shell. Nothing while closed or once signed in. */
export function AuthPromptDialog() {
  const { t } = useI18n()
  const open = useAuthPrompt((s) => s.open)
  const next = useAuthPrompt((s) => s.next)
  const hide = useAuthPrompt((s) => s.hide)
  const token = useAuthStore((s) => s.token)
  const primary = useRef<HTMLAnchorElement>(null)

  if (!open || token) return null
  return (
    <Modal
      title={t('gate.title')}
      description={t('gate.body')}
      icon={<LogIn size={16} />}
      onClose={hide}
      initialFocus={primary}
      className="max-w-md"
      footer={
        <>
          <Link ref={primary} href={authHref('login', next)} onClick={hide} className={buttonStyles({ variant: 'amber' })}>
            {t('gate.signIn')}
          </Link>
          <Link href={authHref('register', next)} onClick={hide} className={buttonStyles({ variant: 'ghost' })}>
            {t('gate.signUp')}
          </Link>
        </>
      }
    />
  )
}
