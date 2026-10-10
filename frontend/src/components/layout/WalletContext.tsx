'use client'
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { api, type WalletInfo } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

/**
 * The reader's credit wallet, fetched once per page for everything in the shell that
 * shows it: the header pill and the sidebar's wallet card. Two components each asking the
 * API would be two requests for one number.
 *
 * `null` means "not known" - still loading, or the request failed - and the pieces that
 * show it render nothing (the pill) or a dash (the card) rather than a made-up zero.
 *
 * `refresh()` asks again: the Buy Credits page calls it once a purchase is confirmed, so
 * the header and the page agree with the server straight away.
 */
interface WalletState {
  wallet: WalletInfo | null
  refresh: () => Promise<void>
}

const WalletContext = createContext<WalletState>({ wallet: null, refresh: async () => {} })

export function WalletProvider({ children }: { children: React.ReactNode }) {
  const [wallet, setWallet] = useState<WalletInfo | null>(null)
  const token = useAuthStore(state => state.token)

  const refresh = useCallback(async () => {
    if (!token) return
    try {
      setWallet(await api.getWallet())
    } catch {
      // Keep whatever was last known: a failed refresh is not a zero balance.
    }
  }, [token])

  useEffect(() => {
    if (!token) return
    let live = true
    api.getWallet()
      .then((next) => { if (live) setWallet(next) })
      .catch(() => {})
    return () => { live = false }
  }, [token])

  const value = useMemo(() => ({ wallet: token ? wallet : null, refresh }), [token, wallet, refresh])
  return <WalletContext.Provider value={value}>{children}</WalletContext.Provider>
}

export function useCreditBalance(): number | null {
  return useContext(WalletContext).wallet?.credit_balance ?? null
}

/** The whole wallet (balance split into purchased and included credits) and a way to reload it. */
export function useWallet(): WalletState {
  return useContext(WalletContext)
}

/** Below this the pill and the wallet card turn to a warning. */
export const LOW_CREDITS = 20
