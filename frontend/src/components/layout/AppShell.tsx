'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard, BookOpen, Brain, User,
  LogOut, Cpu, ChevronRight, Zap
} from 'lucide-react'

const NAV = [
  { href: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { href: '/tracks',    icon: BookOpen,         label: 'Learning tracks' },
  { href: '/mentor',   icon: Brain,             label: 'AI mentor' },
  { href: '/profile',  icon: User,              label: 'Profile' },
]

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const { user, logout } = useAuthStore()

  return (
    <div className="flex h-screen bg-void overflow-hidden">

      {/* ── Sidebar ── */}
      <aside className="w-56 shrink-0 flex flex-col bg-ink border-r border-border">

        {/* Brand */}
        <div className="px-5 py-5 flex items-center gap-2.5 border-b border-border">
          <div className="w-7 h-7 rounded-md bg-amber flex items-center justify-center">
            <Cpu size={14} className="text-void" />
          </div>
          <span className="font-display font-700 text-bright text-sm tracking-tight">
            AI Career
          </span>
        </div>

        {/* Readiness pill */}
        {user && (
          <div className="mx-3 mt-4 px-3 py-2 rounded bg-surface border border-border">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs text-ghost">Readiness</span>
              <span className="text-xs font-mono text-amber">
                {user.overall_readiness_score.toFixed(0)}%
              </span>
            </div>
            <div className="h-1 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-amber to-amber2 rounded-full transition-all duration-700"
                style={{ width: `${user.overall_readiness_score}%` }}
              />
            </div>
          </div>
        )}

        {/* Nav */}
        <nav className="flex-1 px-3 mt-4 space-y-0.5">
          {NAV.map(({ href, icon: Icon, label }) => {
            const active = pathname === href || pathname.startsWith(href + '/')
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded text-sm transition-all duration-150 group',
                  active
                    ? 'bg-amber/10 text-amber border border-amber/20'
                    : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                )}
              >
                <Icon size={15} className={cn(active ? 'text-amber' : 'text-ghost group-hover:text-soft')} />
                <span className="flex-1">{label}</span>
                {active && <ChevronRight size={12} className="text-amber/60" />}
              </Link>
            )
          })}
        </nav>

        {/* Quick actions */}
        <div className="mx-3 mb-3 px-3 py-2.5 rounded bg-surface border border-border">
          <div className="flex items-center gap-2 mb-1">
            <Zap size={12} className="text-amber" />
            <span className="text-xs text-amber font-medium">Quick action</span>
          </div>
          <Link href="/mentor" className="text-xs text-ghost hover:text-soft transition-colors">
            Ask your AI mentor →
          </Link>
        </div>

        {/* User footer */}
        {user && (
          <div className="px-3 pb-4 border-t border-border pt-3">
            <div className="flex items-center gap-2.5 px-2 mb-1">
              <div className="w-7 h-7 rounded-full bg-amber/20 border border-amber/30 flex items-center justify-center shrink-0">
                <span className="text-xs font-medium text-amber">
                  {user.full_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="min-w-0">
                <p className="text-xs font-medium text-bright truncate">{user.full_name}</p>
                <p className="text-xs text-ghost truncate">{user.experience_level}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="w-full flex items-center gap-2 px-2 py-1.5 mt-1 rounded text-xs text-ghost hover:text-rose hover:bg-rose/5 transition-colors"
            >
              <LogOut size={12} />
              Sign out
            </button>
          </div>
        )}
      </aside>

      {/* ── Main content ── */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {children}
      </main>
    </div>
  )
}
