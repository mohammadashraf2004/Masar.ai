import type { Metadata } from 'next'
import './globals.css'
import { LanguageProvider } from '@/components/layout/LanguageProvider'
import { fontVariables } from '@/fonts'

export const metadata: Metadata = {
  // Both scripts in the tab title: the browser tab is the one surface that
  // cannot follow the reader's language preference, since it is rendered
  // before the client store has hydrated.
  title: {
    default: 'Masar مسار',
    template: '%s · Masar',
  },
  description: 'Arabic-first AI engineering. From student to job-ready AI engineer.',
  applicationName: 'Masar',
  // Needed for the OpenGraph image URL to resolve absolutely. Set
  // NEXT_PUBLIC_SITE_URL in production or link previews point at localhost.
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'http://localhost:3000'),
  openGraph: {
    siteName: 'Masar',
    locale: 'ar_AR',
    alternateLocale: 'en_US',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // Arabic-first is the default posture, so the document starts in
    // Arabic/RTL; LanguageProvider flips it for readers who choose English.
    <html lang="ar" dir="rtl" className={fontVariables}>
      <body className="bg-void text-bright antialiased">
        <LanguageProvider>{children}</LanguageProvider>
      </body>
    </html>
  )
}
