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
import { ArrowRight, Check } from 'lucide-react'
import { Logo } from '@/components/layout/Logo'

const LEVELS = [
  { value: 'beginner',     label: 'Beginner',     desc: 'New to programming' },
  { value: 'intermediate', label: 'Intermediate',  desc: 'Some Python & ML knowledge' },
  { value: 'advanced',     label: 'Advanced',      desc: 'Comfortable with ML basics' },
]

export default function RegisterPage() {
  useGuest()
  const router = useRouter()
  const setAuth = useAuthStore(s => s.setAuth)
  const [form, setForm] = useState({
    full_name: '', email: '', password: '', experience_level: 'beginner'
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await api.register(form)
      setAuth(data.access_token, data.user, data.expires_in)
      router.replace('/dashboard')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-dvh bg-void flex items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <Logo size={28} className="mb-8" wordmarkClassName="text-sm" />

        <h1 className="font-display font-bold text-2xl text-white mb-1">Start your journey</h1>
        <p className="text-sm text-ghost mb-8">Create your account and get a personalized AI engineer roadmap.</p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label="Full name"
            placeholder="Ahmed Hassan"
            value={form.full_name}
            onChange={e => setForm(p => ({ ...p, full_name: e.target.value }))}
            required
          />
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
            placeholder="At least 10 characters"
            value={form.password}
            onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
            minLength={10}
            maxLength={72}
            required
          />

          {/* Experience level */}
          <div>
            <label className="text-xs font-medium text-soft tracking-wide uppercase block mb-2">
              Experience level
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {LEVELS.map(({ value, label, desc }) => {
                const active = form.experience_level === value
                return (
                  <button
                    key={value}
                    type="button"
                    onClick={() => setForm(p => ({ ...p, experience_level: value }))}
                    className={`
                      relative text-start p-3 rounded border transition-all
                      ${active
                        ? 'bg-amber/10 border-amber/40 text-amber'
                        : 'bg-surface border-border text-ghost hover:border-muted hover:text-soft'
                      }
                    `}
                  >
                    {active && (
                      <Check size={10} className="absolute top-2 end-2 text-amber" />
                    )}
                    <div className="text-xs font-medium">{label}</div>
                    <div className="text-xs mt-0.5 opacity-70">{desc}</div>
                  </button>
                )
              })}
            </div>
          </div>

          {error && (
            <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
              {error}
            </div>
          )}

          <Button type="submit" className="w-full" size="lg" loading={loading}>
            Create account <ArrowRight size={14} />
          </Button>
        </form>

        <p className="text-center text-sm text-ghost mt-6">
          Already have an account?{' '}
          <Link href="/auth/login" className="text-amber hover:text-amber2 transition-colors">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
