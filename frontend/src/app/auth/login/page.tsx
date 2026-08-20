'use client'
import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { useGuest } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { getErrorMessage } from '@/lib/utils'
import { Cpu, ArrowRight, CheckCircle, XCircle } from 'lucide-react'

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
  const params = useSearchParams()
  const setAuth = useAuthStore(s => s.setAuth)

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
      setAuth(data.access_token, data.user)
      router.replace('/dashboard')
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
      setMessage('Password reset — please log in with your new password.')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-void flex">
      {/* Left decorative panel */}
      <div className="hidden lg:flex w-1/2 bg-ink border-r border-border flex-col justify-between p-12 relative overflow-hidden">
        <div
          className="absolute inset-0 opacity-30"
          style={{
            backgroundImage: 'linear-gradient(rgba(30,37,53,0.6) 1px, transparent 1px), linear-gradient(90deg, rgba(30,37,53,0.6) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-amber/5 blur-3xl pointer-events-none" />

        <div className="relative flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber flex items-center justify-center">
            <Cpu size={16} className="text-void" />
          </div>
          <span className="font-display font-bold text-bright text-base">AI Career Platform</span>
        </div>

        <div className="relative space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber/10 border border-amber/20">
            <span className="w-1.5 h-1.5 rounded-full bg-amber animate-pulse" />
            <span className="text-xs text-amber font-medium">For AI engineers in MENA</span>
          </div>
          <h2 className="font-display font-bold text-3xl text-white leading-tight">
            From student<br />to job-ready<br />
            <span className="text-amber">AI engineer.</span>
          </h2>
          <p className="text-sm text-dim leading-relaxed max-w-xs">
            Personalized roadmaps, an AI mentor that actually understands your
            curriculum, real projects, and career-focused evaluation.
          </p>
        </div>

        <div className="relative flex gap-8 text-sm">
          {[['5', 'Levels'], ['24', 'Weeks'], ['100%', 'Project-based']].map(([n, l]) => (
            <div key={l}>
              <div className="text-2xl font-display font-bold text-amber">{n}</div>
              <div className="text-ghost text-xs mt-0.5">{l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Right: form */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="w-full max-w-sm">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6 lg:hidden">
              <div className="w-7 h-7 rounded-md bg-amber flex items-center justify-center">
                <Cpu size={13} className="text-void" />
              </div>
              <span className="font-display font-bold text-bright text-sm">AI Career Platform</span>
            </div>
            <h1 className="font-display font-bold text-2xl text-white mb-1">
              {mode === 'forgot' ? 'Reset your password' : mode === 'reset' ? 'Choose a new password' : 'Welcome back'}
            </h1>
            {mode === 'login' && <p className="text-sm text-ghost">Sign in to continue your learning journey.</p>}
            {mode === 'forgot' && <p className="text-sm text-ghost">We&apos;ll email you a link to reset it.</p>}
            {mode === 'reset' && <p className="text-sm text-ghost">This link is single-use and expires in an hour.</p>}
          </div>

          {verifyStatus && (
            <div className={`mb-5 flex items-center gap-2 px-3 py-2.5 rounded-lg border text-xs ${
              verifyStatus === 'ok' ? 'bg-emerald/10 border-emerald/20 text-emerald' :
              verifyStatus === 'failed' ? 'bg-rose/10 border-rose/20 text-rose' :
              'bg-amber/10 border-amber/20 text-amber'
            }`}>
              {verifyStatus === 'ok' && <><CheckCircle size={13} /> Email verified — you&apos;re all set.</>}
              {verifyStatus === 'failed' && <><XCircle size={13} /> That verification link is invalid or expired.</>}
              {verifyStatus === 'checking' && 'Verifying your email…'}
            </div>
          )}

          {message && (
            <div className="mb-5 px-3 py-2.5 rounded-lg bg-emerald/10 border border-emerald/20 text-xs text-emerald">
              {message}
            </div>
          )}

          {mode === 'login' && (
            <>
              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  label="Email"
                  type="email"
                  placeholder="you@example.com"
                  value={form.email}
                  onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
                  autoComplete="email"
                  required
                />
                <Input
                  label="Password"
                  type="password"
                  placeholder="••••••••"
                  value={form.password}
                  onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
                  autoComplete="current-password"
                  required
                />

                {error && (
                  <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}

                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  Sign in <ArrowRight size={14} />
                </Button>
              </form>

              <p className="text-center text-sm text-ghost mt-4">
                <button onClick={() => { setMode('forgot'); setError(''); setMessage('') }} className="text-ghost hover:text-soft underline decoration-dotted underline-offset-2">
                  Forgot your password?
                </button>
              </p>

              <p className="text-center text-sm text-ghost mt-2">
                No account?{' '}
                <Link href="/auth/register" className="text-amber hover:text-amber2 transition-colors">
                  Create one
                </Link>
              </p>
            </>
          )}

          {mode === 'forgot' && (
            <>
              <form onSubmit={handleForgotSubmit} className="space-y-4">
                <Input
                  label="Email"
                  type="email"
                  placeholder="you@example.com"
                  value={forgotEmail}
                  onChange={e => setForgotEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
                {error && (
                  <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}
                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  Send reset link
                </Button>
              </form>
              <p className="text-center text-sm text-ghost mt-4">
                <button onClick={() => { setMode('login'); setError(''); setMessage('') }} className="text-ghost hover:text-soft underline decoration-dotted underline-offset-2">
                  Back to sign in
                </button>
              </p>
            </>
          )}

          {mode === 'reset' && (
            <>
              <form onSubmit={handleResetSubmit} className="space-y-4">
                <Input
                  label="New password"
                  type="password"
                  placeholder="At least 8 characters"
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                  autoComplete="new-password"
                  minLength={8}
                  required
                />
                {error && (
                  <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                    {error}
                  </div>
                )}
                <Button type="submit" className="w-full" size="lg" loading={loading}>
                  Set new password
                </Button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
