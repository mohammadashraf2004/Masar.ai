'use client'
import Link from 'next/link'
import { ArrowRight, Compass, Languages, Target } from 'lucide-react'
import { AppShell } from '@/components/layout/AppShell'
import { Logo } from '@/components/layout/Logo'
import { PageHeader } from '@/components/layout/PageHeader'
import { LegalLinks } from '@/components/legal/LegalLinks'
import { YourMasarCard } from '@/components/learning/YourMasarCard'
import { buttonStyles } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/index'
import { LanguageSwitcher } from '@/components/ui/LanguageSwitcher'
import { useI18n } from '@/lib/i18n'
import { useAuthStore } from '@/lib/store'

/**
 * `/` is two pages. A signed-in learner gets a compact home: their roadmap, one
 * tap from continuing. Everyone else gets the marketing page. Which one is
 * decided by the stored session, after it has hydrated — never before, so a
 * signed-in learner is not flashed the sales page (nor a visitor a spinner
 * that never resolves).
 */
export default function Home() {
  const hydrated = useAuthStore((s) => s._hasHydrated)
  const token = useAuthStore((s) => s.token)

  if (!hydrated) {
    return <div className="flex min-h-dvh items-center justify-center bg-void"><Spinner announce className="h-6 w-6" /></div>
  }
  return token ? <MemberHome /> : <Landing />
}

function MemberHome() {
  const { t, tf } = useI18n()
  const user = useAuthStore((s) => s.user)
  const first = user?.full_name?.split(' ')[0] ?? ''

  return (
    <AppShell>
      <PageHeader title={first ? tf('home.welcome', { name: first }) : t('home.title')} wrapTitle />
      <div className="flex-1 space-y-6 overflow-y-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl space-y-4">
          <YourMasarCard variant="home" />
          <Link href="/dashboard" className={buttonStyles({ variant: 'ghost', size: 'sm' })}>
            {t('home.dashboard')} <ArrowRight size={12} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </AppShell>
  )
}

function Landing() {
  const { t } = useI18n()
  const features = [
    { icon: Target, title: t('landing.f1.title'), body: t('landing.f1.body') },
    { icon: Languages, title: t('landing.f2.title'), body: t('landing.f2.body') },
    { icon: Compass, title: t('landing.f3.title'), body: t('landing.f3.body') },
  ]
  return (
    <div className="flex min-h-dvh flex-col bg-void px-4 py-6 sm:px-6">
      <header className="mx-auto flex w-full max-w-5xl items-center justify-between">
        <Logo size={28} wordmarkClassName="text-sm" />
        <div className="flex items-center gap-3">
          <LanguageSwitcher />
          <Link href="/auth/login" className="inline-flex min-h-[44px] items-center text-sm text-soft hover:text-bright lg:min-h-0">
            {t('landing.signIn')}
          </Link>
        </div>
      </header>

      <main className="mx-auto w-full max-w-5xl flex-1 py-16 sm:py-24">
        <p className="text-xs font-medium uppercase tracking-widest text-amber-text">{t('landing.tagline')}</p>
        <h1 className="mt-3 max-w-2xl font-display text-4xl font-bold leading-tight text-white sm:text-5xl">
          {t('reg.title')}
        </h1>
        <p className="mt-4 max-w-xl text-base leading-relaxed text-soft">{t('landing.body')}</p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link href="/auth/register" className={buttonStyles({ size: 'lg' })}>
            {t('landing.signUp')} <ArrowRight size={14} className="rtl:rotate-180" aria-hidden="true" />
          </Link>
          <Link href="/auth/login" className={buttonStyles({ size: 'lg', variant: 'ghost' })}>
            {t('landing.signIn')}
          </Link>
        </div>

        <ul className="mt-16 grid gap-4 sm:grid-cols-3">
          {features.map(({ icon: Icon, title, body }) => (
            <li key={title} className="rounded-lg border border-border bg-panel p-5">
              <Icon size={18} className="text-amber-text" aria-hidden="true" />
              <h2 className="mt-3 text-sm font-semibold text-bright">{title}</h2>
              <p className="mt-1.5 text-sm leading-relaxed text-soft">{body}</p>
            </li>
          ))}
        </ul>
      </main>

      <footer className="mx-auto flex w-full max-w-5xl items-center justify-between border-t border-border pt-4">
        <span className="text-xs text-soft">Masar · مسار</span>
        <LegalLinks />
      </footer>
    </div>
  )
}
