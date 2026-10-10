'use client'
import { MobileNavProvider } from '@/components/layout/MobileNavContext'
import { LegalGate } from '@/components/layout/LegalGate'
import { AuthPromptDialog } from '@/components/auth/AuthPrompt'
import { MobileMenu } from '@/components/layout/MobileMenu'
import { ShellHeader } from '@/components/layout/ShellHeader'
import { Sidebar } from '@/components/layout/Sidebar'
import { WalletProvider } from '@/components/layout/WalletContext'
import { TourProvider } from '@/features/tours/TourProvider'

/**
 * The frame every signed-in page sits in: the sidebar (from `lg`), the header,
 * the mobile menu (below `lg`) and the page itself.
 *
 * Direction is never decided here. Everything below uses logical properties
 * (`start`/`end`, `ms-`/`me-`, `border-e`), so the sidebar sits on the right in
 * Arabic and on the left in English without a line of direction logic.
 */
export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <MobileNavProvider>
      <WalletProvider>
        {/* Walkthroughs: starts the one that is due on this page, and offers "Replay tour" to the Help menus. */}
        <TourProvider>
          <AppShellFrame>{children}</AppShellFrame>
        </TourProvider>
      </WalletProvider>
    </MobileNavProvider>
  )
}

function AppShellFrame({ children }: { children: React.ReactNode }) {
  return (
    // Below lg the document scrolls normally: a locked `h-screen` shell stops
    // mobile browsers retracting their URL bar and buries whatever sits at the
    // bottom of the page behind it. `dvh` rather than `vh` for the same
    // reason — `100vh` is the *largest* viewport height on iOS, not the
    // current one. From lg up the fixed-pane desktop layout is unchanged.
    <div className="flex min-h-dvh bg-void lg:h-dvh lg:overflow-hidden">
      {/* Asks for acceptance of the current Terms and Privacy Policy when the
          account has not given it; renders nothing otherwise. */}
      <LegalGate />

      <Sidebar />

      {/* `min-w-0` is what lets this column actually shrink: without it a flex
          child floors at its content's intrinsic width, and any wide child (a
          table, a code block, a long title) pushes the whole page sideways. */}
      <div className="flex min-w-0 flex-1 flex-col lg:overflow-hidden">
        <ShellHeader />
        <MobileMenu />
        <main className="flex min-h-0 flex-1 flex-col lg:overflow-hidden">
          {children}
        </main>
      </div>

      {/* "Sign in to continue", for a signed-out visitor who reaches for something
          that needs an account. Last, so it stacks above the page's own dialogs. */}
      <AuthPromptDialog />
    </div>
  )
}
