'use client'
import { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { api } from '@/lib/api'
import { getErrorMessage } from '@/lib/utils'
import { User, Github, Linkedin, Save, CheckCircle } from 'lucide-react'

export default function ProfilePage() {
  const { user } = useAuth()
  const { setAuth, token } = useAuthStore()
  const [form, setForm] = useState({
    full_name: user?.full_name ?? '',
    bio: user?.bio ?? '',
    github_url: user?.github_url ?? '',
    linkedin_url: user?.linkedin_url ?? '',
    experience_level: user?.experience_level ?? 'beginner',
  })
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      const updated = await api.updateMe(form)
      if (token) setAuth(token, updated)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (err) {
      setError(getErrorMessage(err))
    }
    setSaving(false)
  }

  if (!user) return null

  return (
    <AppShell>
      <PageHeader title="Profile" subtitle="Manage your account and preferences." />

      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-2xl space-y-6">

          {/* Avatar + stats */}
          <Card className="p-6">
            <div className="flex items-center gap-5">
              <div className="w-16 h-16 rounded-full bg-amber/10 border-2 border-amber/30 flex items-center justify-center shrink-0">
                <span className="text-2xl font-display font-700 text-amber">
                  {user.full_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <h2 className="font-display font-700 text-white text-lg">{user.full_name}</h2>
                <p className="text-sm text-ghost">{user.email}</p>
                <div className="flex items-center gap-3 mt-1.5">
                  <span className="text-xs px-2 py-0.5 rounded bg-amber/10 border border-amber/20 text-amber capitalize">
                    {user.experience_level}
                  </span>
                  <span className="text-xs text-ghost capitalize">{user.role}</span>
                </div>
              </div>
              <div className="ml-auto text-right">
                <div className="text-3xl font-display font-700 text-amber">
                  {user.overall_readiness_score.toFixed(0)}%
                </div>
                <div className="text-xs text-ghost">Readiness score</div>
              </div>
            </div>
          </Card>

          {/* Edit form */}
          <Card className="p-6">
            <h3 className="font-medium text-bright mb-5 flex items-center gap-2">
              <User size={15} className="text-ghost" />
              Edit profile
            </h3>

            <form onSubmit={handleSave} className="space-y-4">
              <Input
                label="Full name"
                value={form.full_name}
                onChange={e => setForm(p => ({ ...p, full_name: e.target.value }))}
              />

              <div>
                <label className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">Bio</label>
                <textarea
                  className="w-full bg-surface border border-border rounded px-3 py-2.5 text-sm text-bright placeholder:text-ghost focus:outline-none focus:border-amber/50 min-h-24 resize-none"
                  placeholder="Tell us about yourself and your goals…"
                  value={form.bio}
                  onChange={e => setForm(p => ({ ...p, bio: e.target.value }))}
                />
              </div>

              <div>
                <label className="text-xs font-medium text-soft tracking-wide uppercase block mb-1.5">
                  Experience level
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {(['beginner', 'intermediate', 'advanced'] as const).map(level => (
                    <button
                      key={level}
                      type="button"
                      onClick={() => setForm(p => ({ ...p, experience_level: level }))}
                      className={`
                        py-2 rounded border text-sm transition-all capitalize
                        ${form.experience_level === level
                          ? 'bg-amber/10 border-amber/40 text-amber'
                          : 'bg-surface border-border text-ghost hover:border-muted hover:text-soft'
                        }
                      `}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Input
                  label="GitHub URL"
                  placeholder="https://github.com/username"
                  value={form.github_url}
                  onChange={e => setForm(p => ({ ...p, github_url: e.target.value }))}
                />
                <Input
                  label="LinkedIn URL"
                  placeholder="https://linkedin.com/in/username"
                  value={form.linkedin_url}
                  onChange={e => setForm(p => ({ ...p, linkedin_url: e.target.value }))}
                />
              </div>

              {error && (
                <div className="px-3 py-2.5 rounded bg-rose/10 border border-rose/20 text-xs text-rose">
                  {error}
                </div>
              )}

              <Button type="submit" loading={saving} variant={saved ? 'ghost' : 'amber'}>
                {saved ? (
                  <><CheckCircle size={13} className="text-emerald" /> Saved</>
                ) : (
                  <><Save size={13} /> Save changes</>
                )}
              </Button>
            </form>
          </Card>

          {/* Account info */}
          <Card className="p-6">
            <h3 className="font-medium text-bright mb-4 text-sm">Account</h3>
            <div className="space-y-3 text-sm">
              <div className="flex items-center justify-between py-2 border-b border-border">
                <span className="text-ghost">Email</span>
                <span className="text-soft">{user.email}</span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-border">
                <span className="text-ghost">Member since</span>
                <span className="text-soft">{new Date(user.created_at).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="text-ghost">Role</span>
                <span className="text-soft capitalize">{user.role}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  )
}
