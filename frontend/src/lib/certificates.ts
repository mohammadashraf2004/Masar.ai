/**
 * Small helpers for certificates that belong to no one component: the public
 * link, the LinkedIn share URL, the date as the certificate prints it, and the
 * "download as PDF" step.
 */

/** Where a certificate can be checked by anyone holding the link. */
export function verifyUrlFor(certificateId: string): string {
  // NEXT_PUBLIC_SITE_URL is the public origin in production (layout.tsx uses it for the
  // OpenGraph image too); in development the address in the bar is the right one.
  const configured = process.env.NEXT_PUBLIC_SITE_URL
  const origin = configured || (typeof window !== 'undefined' ? window.location.origin : '')
  return `${origin.replace(/\/$/, '')}/verify/${encodeURIComponent(certificateId)}`
}

export function linkedInShareUrl(verifyUrl: string): string {
  return `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(verifyUrl)}`
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

/**
 * "18 Sep 2026". The certificate is English-only whatever the page language is,
 * and the date is read in UTC so the same certificate says the same day to a
 * reader in Riyadh and one in Casablanca (and to the server that rendered it).
 * Built by hand rather than with `toLocaleDateString`: the locale data spells
 * September "Sept" in en-GB on some engines and "Sep" on others, and a certificate
 * has to print the same thing wherever it is opened.
 */
export function formatIssued(iso: string): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return ''
  return `${date.getUTCDate()} ${MONTHS[date.getUTCMonth()]} ${date.getUTCFullYear()}`
}

/**
 * Print only the certificate, on A4 landscape with no margin, so "Save as PDF" in
 * the print dialog produces the certificate at full size. The certificate sizes
 * everything in container units, so it fills 297mm x 210mm without a separate
 * print layout; the rules that hide the rest of the page are in globals.css and
 * apply only while `body.printing-certificate` is set.
 */
export function printCertificate(): void {
  const page = document.createElement('style')
  page.textContent = '@page { size: A4 landscape; margin: 0 }'
  document.head.appendChild(page)
  document.body.classList.add('printing-certificate')

  const cleanup = () => {
    document.body.classList.remove('printing-certificate')
    page.remove()
    window.removeEventListener('afterprint', cleanup)
  }
  window.addEventListener('afterprint', cleanup)
  try {
    window.print()
  } catch {
    cleanup()
  }
}
