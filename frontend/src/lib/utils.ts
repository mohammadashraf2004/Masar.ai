import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

export function formatRelative(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return formatDate(iso)
}

export function difficultyColor(d: string) {
  return { beginner: 'text-emerald', intermediate: 'text-amber', advanced: 'text-rose' }[d] ?? 'text-soft'
}

export function difficultyBg(d: string) {
  return {
    beginner: 'bg-emerald/10 text-emerald border-emerald/20',
    intermediate: 'bg-amber/10 text-amber border-amber/20',
    advanced: 'bg-rose/10 text-rose border-rose/20',
  }[d] ?? 'bg-muted text-soft'
}

export function scoreColor(score: number) {
  if (score >= 75) return 'text-emerald'
  if (score >= 50) return 'text-amber'
  return 'text-rose'
}

export function scoreGradient(score: number) {
  if (score >= 75) return 'from-emerald to-emerald/50'
  if (score >= 50) return 'from-amber to-amber/50'
  return 'from-rose to-rose/50'
}

export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const resp = (error as { response?: { data?: { detail?: string } } }).response
    return resp?.data?.detail || 'An error occurred'
  }
  return 'An unexpected error occurred'
}
