'use client'
import { useParams } from 'next/navigation'
import { LessonPage } from '@/features/lessons/LessonPage'

/**
 * One lesson on its own page: its content, then its graded exercise below
 * it. Reached from the module aside, the course outline's "continue" and
 * the catalogue once a course links a specific lesson.
 */
export default function LessonRoute() {
  const { slug, lesson } = useParams() as { slug: string; lesson: string }
  return <LessonPage courseSlug={slug} lessonParam={lesson} />
}
