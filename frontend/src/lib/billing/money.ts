import { useI18n } from '@/lib/i18n'
import { formatAmount } from '@/lib/billing/pricing'
import type { UiLanguage } from '@/lib/language'

/**
 * How a currency reads in each language. A code the table does not know is shown as it is, so
 * a catalog in another currency still renders correctly (as "EGP 99") before anyone translates it.
 */
const CURRENCY_LABELS: Record<string, Record<UiLanguage, string>> = {
  SAR: { en: 'SAR', ar: 'ر.س' },
}

export function currencyLabel(currency: string, language: UiLanguage): string {
  return CURRENCY_LABELS[currency]?.[language] ?? currency
}

/** "SAR 1,234.56" in English, "1,234.56 ر.س" in Arabic: the number first, as Arabic writes it. */
export function formatMoney(amount: number, currency: string, language: UiLanguage): string {
  const label = currencyLabel(currency, language)
  return language === 'ar' ? `${formatAmount(amount)} ${label}` : `${label} ${formatAmount(amount)}`
}

/** `money(n)` for the reader's language, in the catalog's currency. */
export function useMoney(currency: string) {
  const { language } = useI18n()
  return {
    money: (amount: number) => formatMoney(amount, currency, language),
    label: currencyLabel(currency, language),
  }
}
