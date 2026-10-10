'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { useGuest, useNextParam } from '@/hooks/useAuth'
import { authHref } from '@/lib/authRedirect'
import { useAuthStore } from '@/lib/store'
import { api } from '@/lib/api'
import { useI18n, type StringKey } from '@/lib/i18n'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { getErrorMessage } from '@/lib/utils'
import { ArrowRight, CheckCircle, XCircle, BookOpen, Brain, ShieldCheck } from 'lucide-react'
import { Logo } from '@/components/layout/Logo'
import { LegalFooter } from '@/components/layout/LegalFooter'

// What the panel promises has to be something the product actually does —
// each of these maps to a shipped feature, not a projected number.
const HIGHLIGHTS: Array<{ icon: React.ElementType; label: StringKey }> = [
  { icon: BookOpen,    label: 'login.hl.lessons' },
  { icon: Brain,       label: 'login.hl.graded' },
  { icon: ShieldCheck, label: 'login.hl.exams' },
]

export default function LoginPage() {
  return (
    <Suspense fallback={null}>
      <LoginPageInner />
    </Suspense>
  )
}

type Mode = 'login' | 'forgot' | 'reset'

function LoginPageInner() {
  useGuest()
  const router = useRouter()
  const { t } = useI18n()
  const params = useSearchParams()
  const setAuth = useAuthStore(s => s.setAuth)
  // Where a "sign in to continue" sent them from; followed only if it is a path on this site.
  const next = useNextParam()

  const verifyToken = params.get('verify_token')
  const resetToken = params.get('reset_token')

  const [mode, setMode] = useState<Mode>(resetToken ? 'reset' : 'login')
  const [form, setForm] = useState({ email: '', password: '' })
  const [forgotEmail, setForgotEmail] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [verifyStatus, setVerifyStatus] = useState<'checking' | 'ok' | 'failed' | null>(verifyToken ? 'checking' : null)

  useEffect(() => {
    if (!verifyToken) return
    api.verifyEmail(verifyToken)
      .then(() => setVerifyStatus('ok'))
      .catch(() => setVerifyStatus('failed'))
  }, [verifyToken])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await api.login(form.email, form.password)
      setAuth(data.access_token, data.user, data.expires_in)
      router.replace(next ?? '/dashboard')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  async function handleForgotSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setMessage('')
    setLoading(true)
    try {
      const res = await api.forgotPassword(forgotEmail)
      setMessage(res.message)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  async function handleResetSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await api.resetPassword(resetToken!, newPassword)
      setMode('login')
      setMessage(t('login.resetDone'))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-dvh bg-void flex">
      {/* Left decorative panel */}
      <div className="hidden lg:flex w-1/2 bg-ink border-e border-border flex-col justify-between p-12 relative overflow-hidden">
        <div
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: 'linear-gradient(rgb(var(--line) / 0.6) 1px, transparent 1px), linear-gradient(90deg, rgb(var(--line) / 0.6) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-amber/5 blur-3xl pointer-events-none" />

        <Logo size={32} className="relative gap-3" wordmarkClassName="text-base" />

        <div className="relative space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber/10 border border-amber/20">
            <span className="w-1.5 h-1.5 rounded-full bg-amber animate-pulse" />
            <span className="text-xs text-amber-text font-medium">{t('login.panel.badge')}</span>
          </div>
          <h2 className="font-display font-bold text-3xl text-white leading-tight">
            {t('login.panel.lead')}<br />
            <span className="text-amber-text">{t('login.panel.accent')}</span>
          </h2>
          <p className="text-sm text-dim leading-relaxed max-w-xs">{t('login.panel.body')}</p>
        </div>

        <div className="relative space-y-3">
          {HIGHLIGHTS.map(({ icon: Icon, label }) => (
            <div key={label} className="flex items-center gap-2.5">
              <Icon size={14} className="text-amber-text shrink-0" />
              <span className="text-xs text-dim">{t(label)}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Right: form */}
      <div className="flex min-w-0 flex-1 flex-col overflow-y-auto px-4 pb-[calc(1.25rem+env(safe-area-inset-bottom))] sm:px-8">
        <div className="flex flex-1 items-center justify-center py-12">
          <div className="w-full max-w-sm">
          <div className="mb-8">
            {/* The language can be changed here, not only after signing in: Arabic is the
                default, and this is the first page a visitor who reads English lands on. */}
            <div className="mb-6 flex items-center justify-between gap-3">
              <Logo size={28} className="lg:hidden" wordmarkClassName="text-sm" />
              <LanguageSwitcher className="ms-auto" />
            </div>
            <h1 className="ui-page-title mb-1">
              {mode === 'forgot' ? t('login.forgot.title') : mode === 'reset' ? t('login.reset.title') : t('login.title')}
            </h1>
            {mode === 'login' && <p className="ui-description">{t('login.subtitle')}</p>}
            {mode === 'forgot' && <p className="ui-description">{t('login.forgot.subtitle')}</p>}
            {mode === 'reset' && <p className="ui-description">{t('login.reset.subtitle')}</p>}
          </div>

          {verifyStatus && (
            <div role={verifyStatus === 'failed' ? 'alert' : 'status'} className={`mb-5 flex items-center gap-2 px-3 py-2.5 rounded-lg border text-xs ${
              verifyStatus === 'ok' ? 'bg-emerald/10 border-emerald/20 text-emerald' :
              verifyStatus === 'failed' ? 'bg-rose/10 border-rose/20 text-rose' :
              'bg-amber/10 border-amber/20 text-amber-text'
            }`}>
              {verifyStatus === 'ok' && <><CheckCircle size={13} /> {t('login.verified')}</>}
              {verifyStatus === 'failed' && <><XCircle size={13} /> {t('login.verifyFailed')}</>}
              {verifyStatus === 'checking' && t('login.verifying')}
            </div>
          )}

          {message && (
            <div dir="auto" className="mb-5 px-3 py-2.5 rounded-lg bg-emerald/10 border border-emerald/20 text-xs text-emerald">
              {message}
            </div>
          )}

          {mode === 'login' && (
            <>
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  label={t('login.email')}
                  type="email"
                  placeholder="you@example.com"
                  value={form.email}
                  onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
                  autoComplete="email"
                  required
                />
                <Input
                  label={t('login.password')}
                  type="password"
                  placeholder="••••••••"
                  value={form.password}
                  onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
                  autoComplete="current-password"
                  required
                />

                {error && (
                  <div role="alert" dir="auto" className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}

                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  {t('login.submit')} <ArrowRight size={14} className="rtl:rotate-180" />
                </Button>
              </form>

              <p className="text-center text-sm text-ghost mt-4">
                <button onClick={() => { setMode('forgot'); setError(''); setMessage('') }} className="inline-flex min-h-[44px] items-center text-ghost hover:text-soft underline decoration-dotted underline-offset-2 lg:min-h-0">
                  {t('login.forgot')}
                </button>
              </p>

              <p className="text-center text-sm text-ghost mt-2">
                {t('login.noAccount')}{' '}
                <Link href={authHref('register', next)} className="text-amber-text hover:text-amber-text2 transition-colors">
                  {t('login.createOne')}
                </Link>
              </p>
            </>
          )}

          {mode === 'forgot' && (
            <>
              <form onSubmit={handleForgotSubmit} className="space-y-4">
                <Input
                  label={t('login.email')}
                  type="email"
                  placeholder="you@example.com"
                  value={forgotEmail}
                  onChange={e => setForgotEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
                {error && (
                  <div role="alert" dir="auto" className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}
                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  {t('login.sendReset')}
                </Button>
              </form>
              <p className="text-center text-sm text-ghost mt-4">
                <button onClick={() => { setMode('login'); setError(''); setMessage('') }} className="inline-flex min-h-[44px] items-center text-ghost hover:text-soft underline decoration-dotted underline-offset-2 lg:min-h-0">
                  {t('login.back')}
                </button>
              </p>
            </>
          )}

          {mode === 'reset' && (
            <>
              <form onSubmit={handleResetSubmit} className="space-y-4">
                <Input
                  label={t('login.newPassword')}
                  type="password"
                  placeholder={t('login.newPasswordPlaceholder')}
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  autoComplete="new-password"
                  minLength={8}
                  required
                />
                {error && (
                  <div role="alert" dir="auto" className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}
                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  {t('login.setPassword')}
                </Button>
              </form>
            </>
          )}
          </div>
        </div>
        <LegalFooter className="mx-auto w-full max-w-sm" />
      </div>
    </div>
  )
}
