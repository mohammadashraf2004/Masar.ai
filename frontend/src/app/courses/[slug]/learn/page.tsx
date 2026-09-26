'use client'
import { useParams } from 'next/navigation'
import { CourseViewer } from '@/components/course/CourseViewer'

/**
 * The lessons of a curriculum course, at the address the catalogue gives them
 * (`/courses/course-001/learn`). Independent of any track: enrolment here is the
 * course's own, and the server still decides who may read which lesson.
 */
export default function CourseLearnPage() {
  const { slug } = useParams() as { slug: string }
  return <CourseViewer slug={slug} curriculum />
}
