import { describe, expect, it } from 'vitest'
import { STRINGS, type StringKey } from '@/lib/i18n'
import { TOURS, copyFor, homeRoute, routeMatches, targetFor, tourById } from './registry'

describe('the tour list', () => {
  it('has the four tours, in the order they are offered', () => {
    expect(TOURS.map((t) => [t.id, t.kind, t.steps.length])).toEqual([
      ['onboarding', 'onboarding', 4],
      ['mentor', 'feature', 6],
      ['mentor-interview', 'feature', 2],
      ['language', 'feature', 3],
    ])
  })

  it('walks the mentor hub from choosing a course to its other tabs, before the interview tour', () => {
    expect(tourById('mentor').steps.map((s) => s.target)).toEqual([
      'mentor-course', 'mentor-context', 'mentor-actions', 'mentor-composer', 'mentor-learner',
      { desktop: 'mentor-tabs', mobile: 'mentor-tabs-phone' },
    ])
    expect(routeMatches(tourById('mentor'), '/mentor')).toBe(true)
    expect(TOURS.findIndex((t) => t.id === 'mentor')).toBeLessThan(TOURS.findIndex((t) => t.id === 'mentor-interview'))
  })

  it('points the onboarding at the four things the handoff names', () => {
    const steps = tourById('onboarding').steps
    expect(steps.map((s) => s.target)).toEqual([
      'path',
      'learn',
      { desktop: 'nav-practice', mobile: 'practice' },
      { desktop: 'nav-mentor', mobile: 'mentor' },
    ])
    // The two that live in the nav rail put the card beside it.
    expect(steps.map((s) => s.placement)).toEqual([undefined, undefined, 'side', 'side'])
  })

  it('points the mock-interview tour at the tab and the credit line', () => {
    expect(tourById('mentor-interview').steps.map((s) => s.target)).toEqual(['interview-tab', 'credits'])
  })

  it('points the language tour at the switch, the first term and the mentor rows', () => {
    const steps = tourById('language').steps
    expect(steps.map((s) => [s.target, s.placement])).toEqual([
      [{ desktop: 'lang-switch', mobile: 'menu-button' }, 'bottom'],
      ['lesson-terms', undefined],
      ['mentor-lang', 'side'],
    ])
  })
})

describe('per-device targets', () => {
  const [path, , practice, mentor] = tourById('onboarding').steps

  it('uses one id for both devices when the step names one', () => {
    expect(targetFor(path, 'desktop')).toBe('path')
    expect(targetFor(path, 'mobile')).toBe('path')
  })

  it('uses the sidebar item on desktop and the on-page element on mobile', () => {
    expect(targetFor(practice, 'desktop')).toBe('nav-practice')
    expect(targetFor(practice, 'mobile')).toBe('practice')
    expect(targetFor(mentor, 'desktop')).toBe('nav-mentor')
    expect(targetFor(mentor, 'mobile')).toBe('mentor')
  })
})

describe('the language switch on a phone', () => {
  const [switchStep, terms] = tourById('language').steps

  it('points at the desktop header\'s switch on a desktop and at the menu button on a phone', () => {
    expect(targetFor(switchStep, 'desktop')).toBe('lang-switch')
    expect(targetFor(switchStep, 'mobile')).toBe('menu-button')
  })

  it('says "from the menu" on a phone and keeps the same title', () => {
    expect(copyFor(switchStep, 'desktop')).toEqual({ titleKey: 'tour.language.switch.title', bodyKey: 'tour.language.switch.body' })
    expect(copyFor(switchStep, 'mobile')).toEqual({ titleKey: 'tour.language.switch.title', bodyKey: 'tour.language.switch.mobile.body' })
    expect(STRINGS.en['tour.language.switch.mobile.body']).toBe('Switch the interface language from the menu anytime; your progress stays the same.')
    expect(STRINGS.ar['tour.language.switch.mobile.body']).toBe('بدّل لغة الواجهة من القائمة في أي وقت، وسيبقى تقدّمك كما هو.')
    expect(STRINGS.ar['tour.language.switch.mobile.body']).toMatch(/[؀-ۿ]/)
  })

  it('uses the same words on both devices for a step with no phone copy', () => {
    expect(copyFor(terms, 'mobile')).toEqual(copyFor(terms, 'desktop'))
  })
})

describe('routes', () => {
  it('matches an exact path, with or without a trailing slash', () => {
    expect(routeMatches(tourById('onboarding'), '/dashboard')).toBe(true)
    expect(routeMatches(tourById('onboarding'), '/dashboard/')).toBe(true)
    expect(routeMatches(tourById('onboarding'), '/dashboard/extra')).toBe(false)
    expect(routeMatches(tourById('mentor-interview'), '/mentor')).toBe(true)
    expect(routeMatches(tourById('mentor-interview'), '/mentor/interview/new')).toBe(false)
  })

  it('matches a lesson or the mentor for the language tour, and nothing else', () => {
    const language = tourById('language')
    expect(routeMatches(language, '/courses/langgraph/learn')).toBe(true)
    expect(routeMatches(language, '/tools/qdrant')).toBe(true)
    expect(routeMatches(language, '/mentor')).toBe(true)
    expect(routeMatches(language, '/tools')).toBe(false)
    expect(routeMatches(language, '/courses/langgraph')).toBe(false)
    expect(routeMatches(language, '/dashboard')).toBe(false)
  })

  it('sends a replay to the first of a tour\'s routes', () => {
    expect(homeRoute(tourById('onboarding'))).toBe('/dashboard')
    expect(homeRoute(tourById('language'))).toBe('/courses/*/learn')
  })
})

describe('copy', () => {
  const keys = TOURS.flatMap((t) => t.steps.flatMap((s) => [s.titleKey, s.bodyKey]))

  it('has every step\'s title and body in both languages', () => {
    for (const key of keys) {
      expect(STRINGS.en[key], `en ${key}`).toBeTruthy()
      expect(STRINGS.ar[key], `ar ${key}`).toBeTruthy()
    }
    expect(new Set(keys).size).toBe(keys.length)
  })

  it('has Arabic that is Arabic, and English that is not', () => {
    const arabic = /[؀-ۿ]/
    for (const key of keys) {
      expect(STRINGS.ar[key], key).toMatch(arabic)
      expect(STRINGS.en[key], key).not.toMatch(arabic)
    }
  })

  it('says what the handoff says', () => {
    expect(STRINGS.en['tour.onboarding.path.title']).toBe('Your path starts here')
    expect(STRINGS.ar['tour.onboarding.path.title']).toBe('مسارك يبدأ من هنا')
    expect(STRINGS.en['tour.interview.tab.title']).toBe('New: mock interviews')
    expect(STRINGS.ar['tour.interview.credits.title']).toBe('تكلفة واضحة لكل خطوة')
    expect(STRINGS.en['tour.language.switch.title']).toBe('Arabic first, English anytime')
    expect(STRINGS.ar['tour.language.switch.title']).toBe('عربي أولاً، وبالإنجليزية متى شئت')
    expect(STRINGS.en['tour.language.mentor.title']).toBe('Choose how your mentor talks')
    expect(STRINGS.ar['tour.language.terms.title']).toBe('الشرح بالعربية، والمصطلحات كما في سوق العمل')
  })

  it('has the card\'s own strings in both languages', () => {
    const chrome: StringKey[] = ['tour.stepOf', 'tour.new', 'tour.skip', 'tour.back', 'tour.next', 'tour.start', 'tour.got', 'tour.done', 'tour.replay']
    const pairs = Object.fromEntries(chrome.map((k) => [k, [STRINGS.en[k], STRINGS.ar[k]]]))
    expect(pairs).toEqual({
      'tour.stepOf': ['{n} of {total}', '{n} من {total}'],
      'tour.new': ['New', 'جديد'],
      'tour.skip': ['Skip tour', 'تخطّي الجولة'],
      'tour.back': ['Back', 'السابق'],
      'tour.next': ['Next', 'التالي'],
      'tour.start': ['Get started', 'ابدأ الآن'],
      'tour.got': ['Got it', 'فهمت'],
      'tour.done': ['You can replay this tour anytime from Help.', 'يمكنك إعادة الجولة في أي وقت من قائمة المساعدة.'],
      'tour.replay': ['Replay tour', 'إعادة الجولة'],
    })
  })
})
