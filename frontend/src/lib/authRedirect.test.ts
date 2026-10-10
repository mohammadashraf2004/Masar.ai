import { describe, expect, it } from 'vitest'
import { authHref, needsAccount, safeNext } from '@/lib/authRedirect'

describe('safeNext: only a path on this site is ever followed after signing in', () => {
  it.each([
    ['/courses/course-007', '/courses/course-007'],
    ['/courses/course-007/lessons/12?tab=x#top', '/courses/course-007/lessons/12?tab=x#top'],
    ['/challenges?challenge=clean-sales', '/challenges?challenge=clean-sales'],
    ['  /tracks  ', '/tracks'],
  ])('keeps %j', (raw, expected) => {
    expect(safeNext(raw)).toBe(expected)
  })

  it.each([
    null, undefined, '', 'courses', 'https://evil.example/x', '//evil.example/x', '/\\evil.example',
    '\\\\evil.example', '/\tevil', 'javascript:alert(1)', '/auth/login', '/auth/register?next=/x', '/auth',
  ])('drops %j', (raw) => {
    expect(safeNext(raw as string | null | undefined)).toBeNull()
  })
})

describe('authHref', () => {
  it('carries a safe destination and drops an unsafe one', () => {
    expect(authHref('login', '/courses/a')).toBe('/auth/login?next=%2Fcourses%2Fa')
    expect(authHref('register', '/challenges?challenge=x')).toBe('/auth/register?next=%2Fchallenges%3Fchallenge%3Dx')
    expect(authHref('login', '//evil.example')).toBe('/auth/login')
    expect(authHref('register')).toBe('/auth/register')
  })
})

describe('needsAccount: which pages are the learning itself or an account', () => {
  it.each([
    '/dashboard', '/learn/masar', '/mentor', '/mentor/interview/new', '/profile', '/community',
    '/certificates', '/onboarding/quick', '/exam/3', '/billing/orders', '/billing/success?invoice=1',
    '/courses/course-007/learn', '/courses/course-007/lessons/12', '/tools/langchain',
    '/challenges/projects/masar-commerce/workspace', '/admin/analytics',
  ])('%s needs an account', (href) => {
    expect(needsAccount(href)).toBe(true)
  })

  it.each([
    '/', '/explore', '/tracks', '/tracks/ai-engineer', '/roadmaps/ai-engineer', '/courses/course-007',
    '/challenges', '/challenges?challenge=x', '/challenges/projects/masar-commerce', '/tools', '/glossary',
    '/billing', '/terms', '/privacy', '/refund-policy', '/verify/abc', '/learning-path',
  ])('%s can be browsed', (href) => {
    expect(needsAccount(href)).toBe(false)
  })
})
