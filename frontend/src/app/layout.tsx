'use client'
import './globals.css'
import type { Metadata } from 'next'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="noise">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-void text-bright antialiased">
        {children}
      </body>
    </html>
  )
}
