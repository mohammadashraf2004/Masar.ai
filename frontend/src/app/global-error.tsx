'use client'
import './globals.css'
import { buttonStyles } from '@/components/ui/Button'
import { THEME_INIT_SCRIPT } from '@/lib/theme'

/**
 * The last resort: it renders only when the root layout itself failed, so it has to
 * bring its own <html> and <body> and can lean on nothing the layout provides - no
 * language store, no shell, no self-hosted fonts and no client router (plain anchors, and a
 * reload rather than a re-render). The font classes are avoided on purpose: `--font-body`
 * is built from the self-hosted faces' variables, which do not exist here, and a stack built
 * on an undefined variable is dropped whole - the page would come out in the browser's
 * default serif. The stacks are set directly instead.
 *
 * Because it cannot know which language the reader chose, it says the message in both,
 * Arabic first like the rest of the product. It still takes the saved theme, and the
 * same tokens as everything else, so it does not flash a white page at a dark-mode reader.
 */
export default function GlobalError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <html lang="ar" dir="rtl" suppressHydrationWarning>
      <head>
        {/* A constant string from lib/theme, not anything a user supplies (as in layout.tsx). */}
        {/* eslint-disable-next-line react/no-danger */}
        <script dangerouslySetInnerHTML={{ __html: THEME_INIT_SCRIPT }} />
      </head>
      <body className="bg-void text-bright antialiased" style={{ fontFamily: 'system-ui, sans-serif' }}>
        <main className="flex min-h-dvh flex-col items-center justify-center gap-6 px-4 py-16 text-center">
          <p
            aria-hidden="true"
            dir="ltr"
            className="select-none text-[96px] font-medium leading-none text-ghost sm:text-[128px]"
            style={{ fontFamily: 'ui-monospace, monospace' }}
          >
            500
          </p>
          <div className="max-w-md space-y-3">
            <h1 className="text-2xl font-bold text-white">حدث خطأ ما</h1>
            <p className="text-sm leading-relaxed text-dim">تعذّر تحميل مسار. حاول مرة أخرى بعد قليل.</p>
            <p dir="ltr" lang="en" className="text-sm leading-relaxed text-dim">
              Something went wrong. Please try again in a moment.
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            <button type="button" onClick={() => reset()} className={buttonStyles()}>
              حاول مرة أخرى · Try again
            </button>
            <a href="/dashboard" className={buttonStyles({ variant: 'ghost' })}>لوحة التحكم · Dashboard</a>
          </div>
        </main>
      </body>
    </html>
  )
}
