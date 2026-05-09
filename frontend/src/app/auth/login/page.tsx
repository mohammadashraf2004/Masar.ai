'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useGuest } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { getErrorMessage } from '@/lib/utils'
import { Cpu, ArrowRight } from 'lucide-react'

export default function LoginPage() {
  useGuest()
  const router = useRouter()
  const setAuth = useAuthStore(s => s.setAuth)
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

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

  return (
    <div className="min-h-screen bg-void flex">
      {/* Left panel — decorative */}
      <div className="hidden lg:flex w-1/2 bg-ink border-r border-border flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-30" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-amber/5 blur-3xl" />

        <div className="relative flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-amber flex items-center justify-center">
            <Cpu size={16} className="text-void" />
          </div>
          <span className="font-display font-700 text-bright text-base">AI Career Platform</span>
        </div>

        <div className="relative space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber/10 border border-amber/20">
            <span className="w-1.5 h-1.5 rounded-full bg-amber animate-pulse" />
            <span className="text-xs text-amber font-medium">For AI engineers in MENA</span>
          </div>
          <h2 className="font-display font-700 text-3xl text-white leading-tight">
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
              <div className="text-2xl font-display font-700 text-amber">{n}</div>
              <div className="text-ghost text-xs mt-0.5">{l}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex items-center justify-center px-8">
        <div className="w-full max-w-sm">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6 lg:hidden">
              <div className="w-7 h-7 rounded-md bg-amber flex items-center justify-center">
                <Cpu size={13} className="text-void" />
              </div>
              <span className="font-display font-700 text-bright text-sm">AI Career Platform</span>
            </div>
            <h1 className="font-display font-700 text-2xl text-white mb-1">Welcome back</h1>
            <p className="text-sm text-ghost">Sign in to continue your learning journey.</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
              required
            />
            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={form.password}
              onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
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

          <p className="text-center text-sm text-ghost mt-6">
            No account?{' '}
            <Link href="/auth/register" className="text-amber hover:text-amber2 transition-colors">
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
