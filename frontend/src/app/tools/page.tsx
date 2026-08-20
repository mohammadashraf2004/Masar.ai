'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, Spinner, ProgressBar } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { ToolCourseSummary, ToolEnrollment } from '@/types'
import { ArrowRight, CheckCircle, Layers, Boxes, Server, Database } from 'lucide-react'

const CATEGORY_META: Record<string, { icon: React.ElementType; color: string }> = {
  'LLM & AI Application Layer': { icon: Layers, color: 'amber' },
  'Vector Databases':           { icon: Database, color: 'sky' },
  'MLOps & Infrastructure':     { icon: Server, color: 'emerald' },
  'Data Tools':                 { icon: Boxes, color: 'violet' },
}
const CATEGORY_ORDER = Object.keys(CATEGORY_META)

export default function ToolsPage() {
  const { isLoading: authLoading } = useAuth()
  const [courses, setCourses] = useState<ToolCourseSummary[]>([])
  const [enrollments, setEnrollments] = useState<ToolEnrollment[]>([])
  const [loading, setLoading] = useState(true)
  const [enrollingId, setEnrollingId] = useState<number | null>(null)

  useEffect(() => {
    if (authLoading) return
    async function load() {
      try {
        const [c, e] = await Promise.all([api.listToolCourses(), api.getMyToolEnrollments()])
        setCourses(c)
        setEnrollments(e)
      } catch {}
      setLoading(false)
    }
    load()
  }, [authLoading])

  async function handleEnroll(course: ToolCourseSummary) {
    setEnrollingId(course.id)
    try {
      const enr = await api.enrollToolCourse(course.id)
      setEnrollments(prev => [...prev.filter(e => e.tool_course_id !== course.id), enr])
    } catch {}
    setEnrollingId(null)
  }

  if (authLoading || loading) return (
    <div className="min-h-screen bg-void flex items-center justify-center">
      <Spinner className="w-6 h-6" />
    </div>
  )

  const enrMap = new Map(enrollments.map(e => [e.tool_course_id, e]))
  const byCategory = new Map<string, ToolCourseSummary[]>()
  for (const c of courses) {
    const key = c.category ?? 'Other'
    if (!byCategory.has(key)) byCategory.set(key, [])
    byCategory.get(key)!.push(c)
  }
  const orderedCategories = [
    ...CATEGORY_ORDER.filter(c => byCategory.has(c)),
    ...Array.from(byCategory.keys()).filter(c => !CATEGORY_ORDER.includes(c)),
  ]

  return (
    <AppShell>
      <PageHeader
        title="Tools & frameworks"
        subtitle="No prerequisites, no tracks — pick any tool and start. Great alongside or independent of a career track."
      />

      <div className="flex-1 overflow-y-auto px-8 py-6">
        <div className="max-w-5xl mx-auto space-y-10">
          {orderedCategories.map(category => {
            const meta = CATEGORY_META[category] ?? { icon: Boxes, color: 'ghost' }
            const Icon = meta.icon
            return (
              <div key={category}>
                <div className="flex items-center gap-2 mb-4">
                  <Icon size={15} className={`text-${meta.color}`} />
                  <h2 className="text-sm font-medium text-bright">{category}</h2>
                  <span className="text-xs text-ghost">{byCategory.get(category)!.length} tools</span>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  {byCategory.get(category)!.map(course => {
                    const enr = enrMap.get(course.id)
                    return (
                      <Card key={course.id} className="p-5 flex flex-col">
                        <div className="flex items-start justify-between mb-3">
                          <span className="text-2xl">{course.icon}</span>
                          <Badge variant={course.difficulty}>{course.difficulty}</Badge>
                        </div>
                        <h3 className="font-medium text-bright text-sm mb-1.5">{course.title}</h3>
                        <p className="text-xs text-ghost leading-relaxed mb-4 flex-1">{course.description}</p>

                        {enr ? (
                          <div className="mb-3">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-xs text-ghost">{enr.progress_pct >= 100 ? 'Completed' : 'In progress'}</span>
                              <span className="text-xs font-mono text-amber">{Math.round(enr.progress_pct)}%</span>
                            </div>
                            <ProgressBar value={enr.progress_pct} size="sm" color={enr.progress_pct >= 100 ? 'emerald' : 'amber'} />
                          </div>
                        ) : (
                          <div className="flex items-center gap-3 mb-3 text-xs text-ghost">
                            {course.estimated_hours && <span>{course.estimated_hours}h</span>}
                            {course.topic_count > 0 && <span>{course.topic_count} topics</span>}
                          </div>
                        )}

                        {enr ? (
                          <Link href={`/tools/${course.slug}`}>
                            <Button size="sm" variant={enr.progress_pct >= 100 ? 'ghost' : 'amber'} className="w-full">
                              {enr.progress_pct >= 100
                                ? <><CheckCircle size={12} /> Review</>
                                : <>Continue <ArrowRight size={12} /></>}
                            </Button>
                          </Link>
                        ) : (
                          <Button
                            size="sm"
                            variant="outline"
                            className="w-full"
                            loading={enrollingId === course.id}
                            onClick={() => handleEnroll(course)}
                          >
                            Start learning
                          </Button>
                        )}
                      </Card>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </AppShell>
  )
}
