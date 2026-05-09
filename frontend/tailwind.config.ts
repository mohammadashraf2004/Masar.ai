import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Base palette — near-black system
        void:    '#080A0E',
        ink:     '#0D1117',
        surface: '#111620',
        panel:   '#161C28',
        border:  '#1E2535',
        muted:   '#2A3347',
        // Text
        ghost:   '#4A5568',
        dim:     '#718096',
        soft:    '#A0AEC0',
        bright:  '#E2E8F0',
        white:   '#F7FAFC',
        // Accent — amber/gold
        amber:   '#F59E0B',
        amber2:  '#FBBF24',
        amberDim:'#92610A',
        // Status
        emerald: '#10B981',
        rose:    '#F43F5E',
        sky:     '#38BDF8',
        violet:  '#8B5CF6',
      },
      fontFamily: {
        sans:  ['var(--font-dm-sans)', 'sans-serif'],
        mono:  ['var(--font-jetbrains)', 'monospace'],
        display: ['var(--font-syne)', 'sans-serif'],
      },
      backgroundImage: {
        'grid-pattern': `
          linear-gradient(rgba(30,37,53,0.6) 1px, transparent 1px),
          linear-gradient(90deg, rgba(30,37,53,0.6) 1px, transparent 1px)
        `,
      },
      backgroundSize: {
        'grid': '40px 40px',
      },
      animation: {
        'fade-up':   'fadeUp 0.5s ease forwards',
        'fade-in':   'fadeIn 0.3s ease forwards',
        'pulse-slow':'pulse 3s ease-in-out infinite',
        'scan':      'scan 2s linear infinite',
        'glow':      'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeUp:  { from: { opacity: '0', transform: 'translateY(16px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeIn:  { from: { opacity: '0' }, to: { opacity: '1' } },
        scan:    { from: { transform: 'translateY(-100%)' }, to: { transform: 'translateY(100vh)' } },
        glow:    { from: { boxShadow: '0 0 4px #F59E0B40' }, to: { boxShadow: '0 0 16px #F59E0B80' } },
      },
    },
  },
  plugins: [],
}
export default config
