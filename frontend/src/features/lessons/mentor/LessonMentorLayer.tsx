'use client'
import { useEffect, type RefObject } from 'react'
import { LessonMentorPanel } from './LessonMentorPanel'
import { SelectionToolbar } from './SelectionToolbar'
import { useLessonMentor } from './useLessonMentor'

/**
 * Everything the lesson page needs for the mentor, as one element: the selection toolbar (over the
 * article) and, once a question is asked, the fixed side panel. The parent is told when it opens so
 * wide lesson layouts can reserve the same amount of inline-end space.
 */
export function LessonMentorLayer({
  articleRef,
  courseId,
  lessonId,
  lessonNumber,
  onOpenChange,
}: {
  articleRef: RefObject<HTMLElement>
  courseId: string
  lessonId: string
  lessonNumber: number
  onOpenChange?: (open: boolean) => void
}) {
  const mentor = useLessonMentor({ courseId, lessonId })
  useEffect(() => onOpenChange?.(mentor.open), [mentor.open, onOpenChange])
  return (
    <>
      <SelectionToolbar
        articleRef={articleRef}
        onAsk={(intent, selected, label) => void mentor.ask(label, intent, selected)}
      />
      {mentor.open && (
        <LessonMentorPanel
          lessonNumber={lessonNumber}
          courseId={courseId}
          lessonId={lessonId}
          exchanges={mentor.exchanges}
          loading={mentor.loading}
          failed={mentor.failed}
          onClose={() => mentor.setOpen(false)}
          onRetry={mentor.retry}
          onFollowUp={(answer) => void mentor.ask(answer, null, null)}
        />
      )}
    </>
  )
}
