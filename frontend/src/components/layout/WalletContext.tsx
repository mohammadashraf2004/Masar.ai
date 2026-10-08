'use client'
import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

/**
 * The reader's credit balance, fetched once per page for everything in the
 * shell that shows it: the header pill and the sidebar's wallet card. Two
 * components each asking the API would be two requests for one number.
 *
 * `null` means "not known" — still loading, or the request failed — and the
 * pieces that show it render nothing (the pill) or a dash (the card) rather than
 * a made-up zero.
 */
const WalletContext = createContext<number | null>(null)

export function WalletProvider({ children }: { children: React.ReactNode }) {
  const [balance, setBalance] = useState<number | null>(null)
  const token = useAuthStore(state => state.token)

  useEffect(() => {
    if (!token) return
    let live = true
    api.getWallet()
      .then((wallet) => { if (live) setBalance(wallet.credit_balance) })
      .catch(() => {})
    return () => { live = false }
  }, [token])

  return <WalletContext.Provider value={token ? balance : null}>{children}</WalletContext.Provider>
}

export function useCreditBalance(): number | null {
  return useContext(WalletContext)
}

/** Below this the pill and the wallet card turn to a warning. */
export const LOW_CREDITS = 20
