/** @type {import('next').NextConfig} */

// The API URL is needed in connect-src so the browser will let the SPA
// talk to the backend at all under CSP.
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
const API_ORIGIN = (() => {
  try {
    return new URL(API_URL).origin
  } catch {
    return 'http://localhost:8000'
  }
})()

const isProd = process.env.NODE_ENV === 'production'

// Notes on the two loose directives:
//  - 'unsafe-inline' in script-src: tried and reverted a nonce-based
//    replacement during the 2026-09 security audit (see SECURITY.md). The
//    per-request nonce a middleware/proxy hook mints DOES reach Next's own
//    inline hydration/RSC-bootstrap scripts (`self.__next_f.push(...)`) —
//    but ONLY on a route that renders dynamically, because that HTML has
//    to be generated per-request for a per-request nonce to land in it at
//    all. Verified empirically: on a build where every page stayed
//    statically prerendered (the current architecture — most routes below
//    show as `○ Static` in `next build`'s output), zero inline scripts
//    carried the nonce and a strict CSP would have blocked Next's own
//    hydration on every one of them, i.e. broken the app for every visitor.
//    Making it work required forcing the root layout to read
//    `headers()`, which converts EVERY route in the app from static to
//    dynamically rendered (confirmed: `next build`'s route list flips from
//    mostly `○` to all `ƒ`) — trading away edge caching and static TTFB
//    app-wide to remove one CSP directive. That trade is a product/infra
//    call, not a "clearly safe" security fix, so it was not made
//    unilaterally; see SECURITY.md for the recommendation left for a
//    deliberate decision (nonce + force-dynamic, a hash-based CSP for the
//    static bundle's scripts, or keep this as documented residual risk).
//  - 'unsafe-inline' in style-src: Next.js injects inline <style> tags for
//    its CSS, and Tailwind's runtime-generated styles land the same way.
//    Nonce'ing style tags has the same static-vs-dynamic problem as above,
//    plus React inline `style` props and styled-jsx don't carry a nonce at
//    all today — not attempted.
//  - 'unsafe-eval' in dev only: the dev-mode React refresh runtime needs it.
//    It is absent from production builds.
const csp = [
  "default-src 'self'",
  `script-src 'self' 'unsafe-inline'${isProd ? '' : " 'unsafe-eval'"}`,
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data: blob: https:",
  // Every typeface is committed under src/fonts and served from
  // /_next/static/media by next/font/local, so 'self' is the whole policy —
  // no fonts.googleapis.com in style-src, no fonts.gstatic.com here. That
  // pairing was what broke the fonts in production before they were
  // self-hosted; do not re-add the origins to fix a missing face.
  "font-src 'self' data:",
  `connect-src 'self' ${API_ORIGIN}`,
  // No plugins, no embedding, no <base> hijacking, and forms may only
  // post back to us — this is what actually limits an injected payload.
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  ...(isProd ? ['upgrade-insecure-requests'] : []),
].join('; ')

const securityHeaders = [
  { key: 'Content-Security-Policy', value: csp },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  // Referrer would otherwise carry app paths (which include ids) to any
  // third-party host the user navigates to.
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  {
    key: 'Permissions-Policy',
    // camera=(self) is deliberate: exam proctoring uses the webcam.
    value: 'accelerometer=(), camera=(self), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()',
  },
]

if (isProd) {
  securityHeaders.push({
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains; preload',
  })
}

const nextConfig = {
  output: 'standalone',
  // Version disclosure in a response header is free reconnaissance.
  poweredByHeader: false,
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: API_URL,
  },
  async headers() {
    return [{ source: '/:path*', headers: securityHeaders }]
  },
}

module.exports = nextConfig
