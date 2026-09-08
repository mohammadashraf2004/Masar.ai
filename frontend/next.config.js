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
//  - 'unsafe-inline' in style-src: Next.js injects inline <style> tags for
//    its CSS, and Tailwind's runtime-generated styles land the same way.
//    Removing it needs a nonce-based setup (a custom Document + middleware),
//    which is the documented next step, not something to switch on blind.
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
