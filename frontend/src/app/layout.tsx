import type { Metadata } from 'next'
import './globals.css'
import { LanguageProvider } from '@/components/layout/LanguageProvider'
import { fontVariables } from '@/fonts'
import { THEME_INIT_SCRIPT } from '@/lib/theme'

const TITLE = 'Masar · مسار'
const DESCRIPTION = 'From student to job-ready AI engineer.'

export const metadata: Metadata = {
  // Both scripts in the tab title: the browser tab is the one surface that
  // cannot follow the reader's language preference, since it is rendered
  // before the client store has hydrated.
  title: {
    default: TITLE,
    template: '%s · Masar',
  },
  description: DESCRIPTION,
  applicationName: 'Masar',
  // Needed for the OpenGraph image URL to resolve absolutely. Set
  // NEXT_PUBLIC_SITE_URL in production or link previews point at localhost.
  // `||`, not `??`: the Docker build passes an empty string when it is unset.
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
  // The brand files live in public/ (favicon.ico, icon.svg, apple-touch-icon.png,
  // og.png), so nothing under app/ may use the icon / apple-icon /
  // opengraph-image file conventions: Next serves those at the same URLs and
  // they take precedence over this object.
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/icon.svg', type: 'image/svg+xml' },
    ],
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    title: TITLE,
    description: DESCRIPTION,
    siteName: 'Masar',
    images: [
      {
        url: '/og.png',
        width: 1200,
        height: 630,
        alt: 'Masar — Arabic-first AI engineering. From student to job-ready AI engineer.',
      },
    ],
    locale: 'ar_SA',
    alternateLocale: 'en_US',
    type: 'website',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // Arabic-first is the default posture, so the document starts in
    // Arabic/RTL; LanguageProvider flips it for readers who choose English.
    //
    // suppressHydrationWarning: the theme script below sets `data-theme` on
    // this element before React hydrates, so the server markup and the DOM
    // differ by that one attribute on purpose. It silences only this element.
    <html lang="ar" dir="rtl" className={fontVariables} suppressHydrationWarning>
      <head>
        {/* Applies a saved light theme before first paint, so a reader who chose
            it never sees the dark page flash. A plain inline script rather than
            next/script: `beforeInteractive` inline scripts are queued and run
            after Next's bootstrap, which is too late. The content is a constant
            string from lib/theme, not anything a user supplies, and script-src
            already allows inline scripts (next.config.js). */}
        {/* eslint-disable-next-line react/no-danger */}
        <script dangerouslySetInnerHTML={{ __html: THEME_INIT_SCRIPT }} />
      </head>
      <body className="bg-void text-bright antialiased">
        <LanguageProvider>{children}</LanguageProvider>
      </body>
    </html>
  )
}
