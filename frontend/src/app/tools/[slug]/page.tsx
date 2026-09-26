'use client'
import { useParams } from 'next/navigation'
import { CourseViewer } from '@/components/course/CourseViewer'

export default function ToolCoursePage() {
  const { slug } = useParams() as { slug: string }
  return <CourseViewer slug={slug} />
}
