'use client'
import { useId, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useGuest } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { api } from '@/lib/api'
import { useI18n } from '@/lib/i18n'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { LegalLinks } from '@/components/legal/LegalLinks'
import { getErrorMessage } from '@/lib/utils'
import { ArrowRight } from 'lucide-react'
import { Logo } from '@/components/layout/Logo'

export default function RegisterPage() {
  useGuest()
  const router = useRouter()
  const { t } = useI18n()
  const setAuth = useAuthStore(s => s.setAuth)
  // The level is asked once, in the learning onboarding that follows, where it
  // sits beside the questions it belongs with. (The API still defaults the
  // legacy field, and saving the learning profile keeps it in step.)
  const [form, setForm] = useState({ full_name: '', email: '', password: '' })
  // Unchecked by default, and account creation stays disabled until it is
  // ticked. This is a courtesy: the server refuses a registration that does not
  // carry the agreement, whatever this page did.
  const [accepted, setAccepted] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const legalId = useId()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!accepted) return
    setError('')
    setLoading(true)
    try {
      // Only the agreement is sent. Which version of each document that means is
      // decided by the server, never by this page.
      const data = await api.register({ ...form, accept_terms: true, accept_privacy: true })
      setAuth(data.access_token, data.user, data.expires_in)
      router.replace('/onboarding/quick')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  const link = 'text-amber-text underline underline-offset-2 hover:text-amber-text2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring'

  return (
    <div className="min-h-dvh bg-void flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <div className="mb-8 flex items-center justify-between">
          <Logo size={28} wordmarkClassName="text-sm" />
          <LanguageSwitcher />
        </div>

        <h1 className="font-display font-bold text-2xl text-white mb-1">{t('reg.title')}</h1>
        <p className="text-sm text-soft mb-8">{t('reg.subtitle')}</p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label={t('reg.name')}
            placeholder={t('reg.namePlaceholder')}
            value={form.full_name}
            onChange={e => setForm(p => ({ ...p, full_name: e.target.value }))}
            autoComplete="name"
            required
          />
          <Input
            label={t('reg.email')}
            type="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
            autoComplete="email"
            required
          />
          <Input
            label={t('reg.password')}
            type="password"
            placeholder={t('reg.passwordPlaceholder')}
            value={form.password}
            onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
            autoComplete="new-password"
            minLength={10}
            maxLength={72}
            required
          />

          {/* A real checkbox with its own label; the label is the only place the agreement
              is stated. (A second line under it used to say the same thing again, as the
              reason the button was disabled - the checkbox is that reason, and `required`
              tells a screen reader so.) The two documents open in a new tab so the form
              (and what was typed into it) is not lost. */}
          <div className="flex items-start gap-3">
            <input
              id={legalId}
              type="checkbox"
              checked={accepted}
              onChange={e => setAccepted(e.target.checked)}
              required
              className="mt-0.5 h-5 w-5 shrink-0 cursor-pointer rounded border-border accent-amber focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            />
            <label htmlFor={legalId} className="min-h-[44px] flex-1 cursor-pointer py-0.5 text-sm leading-relaxed text-soft">
              {t('legal.agree.prefix')}
              <Link href="/terms" target="_blank" rel="noopener noreferrer" className={link}>{t('legal.terms')}</Link>
              {t('legal.agree.and')}
              <Link href="/privacy" target="_blank" rel="noopener noreferrer" className={link}>{t('legal.privacy')}</Link>
              {t('legal.agree.suffix')}
            </label>
          </div>
          {error && (
            <div role="alert" className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
              {error}
            </div>
          )}

          <Button type="submit" className="w-full" size="lg" loading={loading} disabled={!accepted}>
            {t('reg.submit')} <ArrowRight size={14} className="rtl:rotate-180" />
          </Button>
        </form>

        <p className="text-center text-sm text-soft mt-6">
          {t('reg.haveAccount')}{' '}
          <Link href="/auth/login" className="text-amber-text hover:text-amber-text2 transition-colors">
            {t('reg.signIn')}
          </Link>
        </p>
        <LegalLinks className="mt-4 justify-center" />
      </div>
    </div>
  )
}
