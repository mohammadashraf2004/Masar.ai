import { describe, expect, it } from 'vitest'
import { buildContext, wholeCourse } from './context'
import { scopeOf } from './threadStore'

const ON = { lesson: true, code: true }

describe('what a request carries', () => {
  it('sends the lesson with its course while the lesson chip is on', () => {
    const context = buildContext({ courseId: 'ml', courseEnrolled: true, lessonId: '7' }, ON)
    expect(context).toEqual({ courseId: 'ml', lessonId: '7' })
    expect(scopeOf(context)).toBe('lesson:7')
  })

  it('keeps the chosen course, as a conversation about the whole course, when the lesson is removed', () => {
    const context = buildContext({ courseId: 'ml', courseEnrolled: true, lessonId: '7' }, { lesson: false, code: true })
    expect(context).toEqual({ courseId: 'ml' })
    expect(scopeOf(context)).toBe('course:ml')
  })

  it('never makes a course the learner is not enrolled in the subject of a conversation', () => {
    // A lesson link into a course they only preview: the lesson can be attached, the course alone cannot.
    expect(buildContext({ courseId: 'ml', courseEnrolled: false, lessonId: '7' }, ON)).toEqual({ courseId: 'ml', lessonId: '7' })
    const context = buildContext({ courseId: 'ml', courseEnrolled: false, lessonId: '7' }, { lesson: false, code: true })
    expect(context).toEqual({})
    expect(scopeOf(context)).toBe('general')
  })

  it('attaches nothing for General', () => {
    expect(buildContext({}, ON)).toEqual({})
  })
})

describe('the mentor hub', () => {
  // What the server resolves for the learner's most active course (or a lesson link): its next lesson.
  const resolved = {
    courseId: 'ml', courseTitle: 'Machine Learning', courseEnrolled: true,
    lessonId: '7', lessonTitle: 'Loss functions', lessonNumber: 7, lessonTotal: 12,
    exerciseId: '9007', exerciseTitle: 'loss.py',
  }

  it('talks about the whole course by default, never the lesson or the code the server resolved', () => {
    const base = wholeCourse(resolved)
    expect(base).toEqual({ courseId: 'ml', courseTitle: 'Machine Learning', courseEnrolled: true })
    const context = buildContext(base, ON)
    expect(context).toEqual({ courseId: 'ml' })
    expect(scopeOf(context)).toBe('course:ml')
  })

  it('answers in general for a course the learner is not enrolled in', () => {
    expect(buildContext(wholeCourse({ ...resolved, courseEnrolled: false }), ON)).toEqual({})
  })
})
