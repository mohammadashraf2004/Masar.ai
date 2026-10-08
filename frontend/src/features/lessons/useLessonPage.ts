import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import type { Exercise, Lesson } from '@/types'
import {
  DEMO_COURSE, DEMO_COURSE_SLUG, DEMO_EXERCISE, DEMO_EXERCISE_INDEX, DEMO_EXERCISE_TOTAL,
  DEMO_LESSON, DEMO_LESSON_NUMBER, DEMO_LESSON_TOTAL, DEMO_MODULE_LESSONS, DEMO_NEXT_LESSON_ID,
  DEMO_TRACK, DEMO_CREDITS,
} from './mockLesson'
import type { ModuleLessonRow } from './mockLesson'

export type LessonPageState = 'loading' | 'ready' | 'missing'

export interface NamedRef {
  slug: string
  title: string
  title_ar: string
}

export interface LessonPageData {
  state: LessonPageState
  track: NamedRef | null
  course: NamedRef
  lessonNumber: number
  lessonTotal: number
  lesson: Lesson
  moduleLessons: ModuleLessonRow[]
  exercises: Exercise[]
  exerciseIndex: number
  exerciseTotal: number
  credits: number
  /** Needed to call the progress API — null for the design fixture, which has
   *  nothing real to persist against. */
  topicId: number | null
  previousLessonId: number | null
  nextLessonId: number | null
  isCompleted: boolean
  isMock: boolean
}

const LOADING: LessonPageData = {
  state: 'loading', track: null, course: { slug: '', title: '', title_ar: '' },
  lessonNumber: 0, lessonTotal: 0, lesson: DEMO_LESSON, moduleLessons: [], exercises: [],
  exerciseIndex: 0, exerciseTotal: 0, credits: 0, topicId: null,
  previousLessonId: null, nextLessonId: null, isCompleted: false, isMock: false,
}

function statusFor(
  lessonId: number,
  currentId: number,
  locked: boolean | undefined,
  completedIds: Set<number>,
): ModuleLessonRow['status'] {
  if (lessonId === currentId) return 'current'
  if (completedIds.has(lessonId)) return 'done'
  if (locked) return 'locked'
  return 'upcoming'
}

/**
 * Resolves everything a lesson page needs to render, from either of two
 * sources: the one design fixture (`DEMO_COURSE_SLUG`, entirely
 * frontend-only — see mockLesson.ts for why) or the real catalogue, via the
 * same `getToolCourse` call the all-lessons viewer already uses.
 *
 * A lesson's number and the course's total are computed by flattening every
 * topic's lessons in order — the API has no separate "lesson N of M" field.
 * The sidebar's module list, though, stays scoped to the lesson's own topic,
 * matching what the design shows (5 rows, not the whole course).
 */
export function useLessonPage(courseSlug: string, lessonParam: string, enabled = true): LessonPageData {
  const [data, setData] = useState<LessonPageData>(LOADING)

  useEffect(() => {
    // API lesson bodies require authentication. Wait for the persisted auth
    // store to hydrate so the first request cannot race ahead without a token.
    if (!enabled) return

    let cancelled = false
    const lessonId = Number(lessonParam)

    async function loadMock() {
      const currentIndex = DEMO_MODULE_LESSONS.findIndex(row => row.status === 'current')
      setData({
        state: 'ready',
        track: DEMO_TRACK,
        course: DEMO_COURSE,
        lessonNumber: DEMO_LESSON_NUMBER,
        lessonTotal: DEMO_LESSON_TOTAL,
        lesson: DEMO_LESSON,
        moduleLessons: DEMO_MODULE_LESSONS,
        exercises: [DEMO_EXERCISE],
        exerciseIndex: DEMO_EXERCISE_INDEX,
        exerciseTotal: DEMO_EXERCISE_TOTAL,
        credits: DEMO_CREDITS,
        topicId: null,
        previousLessonId: DEMO_MODULE_LESSONS[currentIndex - 1]?.id ?? null,
        nextLessonId: currentIndex >= 0 ? DEMO_NEXT_LESSON_ID : null,
        isCompleted: false,
        isMock: true,
      })
    }

    async function loadReal() {
      if (!Number.isFinite(lessonId)) {
        setData(d => ({ ...d, state: 'missing' }))
        return
      }
      try {
        const course = await api.getToolCourse(courseSlug)
        const topics = course.topics ?? []
        const topic = topics.find(tp => tp.lessons.some(l => l.id === lessonId))
        const lesson = topic?.lessons.find(l => l.id === lessonId)
        if (!topic || !lesson) {
          if (!cancelled) setData(d => ({ ...d, state: 'missing' }))
          return
        }

        const flat = [...topics]
          .sort((a, b) => a.order - b.order)
          .flatMap(tp => [...tp.lessons].sort((a, b) => a.order - b.order))
        const positionInCourse = flat.findIndex(l => l.id === lessonId)
        const lessonNumber = positionInCourse + 1

        let completedIds = new Set<number>()
        try {
          const progress = await api.getToolTopicProgress(topic.id) as { lessons_completed?: number[] }
          completedIds = new Set(progress.lessons_completed ?? [])
        } catch { /* no progress recorded yet */ }

        const moduleLessons: ModuleLessonRow[] = [...topic.lessons]
          .sort((a, b) => a.order - b.order)
          .map(l => ({
            id: l.id,
            order: l.order,
            title: l.title,
            title_ar: l.title_ar ?? l.title,
            status: statusFor(l.id, lessonId, l.is_locked, completedIds),
          }))
        const sortedTopicLessons = [...topic.lessons].sort((a, b) => a.order - b.order)
        // Lesson navigation follows the whole course, not only the current
        // module. The last lesson in one module therefore continues to the
        // first lesson in the next module (and Previous works across the same
        // boundary in reverse).
        const previousLessonId = positionInCourse > 0 ? flat[positionInCourse - 1].id : null
        const nextLessonId = positionInCourse >= 0 && positionInCourse + 1 < flat.length
          ? flat[positionInCourse + 1].id
          : null

        const exercises = topic.exercises.filter(e => e.lesson_id === lessonId)

        if (!cancelled) {
          setData({
            state: 'ready',
            track: null,
            course: { slug: course.slug, title: course.title, title_ar: course.title_ar ?? course.title },
            lessonNumber,
            lessonTotal: flat.length,
            lesson,
            moduleLessons,
            exercises,
            exerciseIndex: 0,
            exerciseTotal: exercises.length,
            credits: 0,
            topicId: topic.id,
            previousLessonId,
            nextLessonId,
            isCompleted: completedIds.has(lessonId),
            isMock: false,
          })
        }
      } catch {
        if (!cancelled) setData(d => ({ ...d, state: 'missing' }))
      }
    }

    if (courseSlug === DEMO_COURSE_SLUG) loadMock()
    else loadReal()

    return () => { cancelled = true }
  }, [courseSlug, lessonParam, enabled])

  return data
}
