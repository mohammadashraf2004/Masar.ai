import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

/**
 * Language and terminology preferences.
 *
 * Kept in its own store (and its own localStorage key) rather than folded
 * into the auth store: these are device preferences, they must survive a
 * logout, and nothing here is a credential.
 *
 * Two independent axes, deliberately:
 *
 *   `language`  — which language the *explanations* and the UI chrome are in.
 *   `mode`      — how much English terminology the explanations carry.
 *
 * Neither ever affects code. Code samples, framework names, CLI commands and
 * identifiers are the same in every setting; see
 * docs/content/ARABIC_FIRST_GUIDELINES.md.
 */

export type UiLanguage = 'ar' | 'en'

/**
 * The Industry Mode ladder. A student starts with mostly-Arabic explanations
 * and works up to the phrasing used in English documentation and interviews.
 */
export type TerminologyMode = 'arabic_first' | 'industry' | 'english_technical'

export const TERMINOLOGY_MODES: TerminologyMode[] = [
  'arabic_first',
  'industry',
  'english_technical',
]

interface LanguageState {
  language: UiLanguage
  mode: TerminologyMode
  /** Whether inline terms in lessons render as annotated, clickable chips. */
  annotateTerms: boolean
  _hasHydrated: boolean

  setLanguage: (language: UiLanguage) => void
  setMode: (mode: TerminologyMode) => void
  setAnnotateTerms: (annotate: boolean) => void
  setHasHydrated: (value: boolean) => void
}

export const useLanguageStore = create<LanguageState>()(
  persist(
    (set) => ({
      // Arabic-first is the product's default posture, not a fallback.
      language: 'ar',
      mode: 'arabic_first',
      annotateTerms: true,
      _hasHydrated: false,

      setLanguage: (language) => set({ language }),
      setMode: (mode) => set({ mode }),
      setAnnotateTerms: (annotateTerms) => set({ annotateTerms }),
      setHasHydrated: (value) => set({ _hasHydrated: value }),
    }),
    {
      name: 'language-prefs',
      storage: createJSONStorage(() =>
        typeof window !== 'undefined'
          ? localStorage
          : { getItem: () => null, setItem: () => {}, removeItem: () => {} }
      ),
      partialize: (s) => ({
        language: s.language,
        mode: s.mode,
        annotateTerms: s.annotateTerms,
      }),
      onRehydrateStorage: () => (state) => state?.setHasHydrated(true),
    }
  )
)

export function directionFor(language: UiLanguage): 'rtl' | 'ltr' {
  return language === 'ar' ? 'rtl' : 'ltr'
}
