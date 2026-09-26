/** 754 seconds is "12:34". Minutes are not capped at 59: a 45-minute interview reads "45:00". */
export function formatClock(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000))
  const minutes = Math.floor(total / 60)
  const seconds = total % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

/** "22 September" / "22 سبتمبر", in Latin digits like the rest of the app. */
export function formatShortDate(iso: string, language: 'ar' | 'en'): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return ''
  return date.toLocaleDateString(language === 'ar' ? 'ar-u-nu-latn-ca-gregory' : 'en-GB', {
    day: 'numeric',
    month: 'long',
  })
}
