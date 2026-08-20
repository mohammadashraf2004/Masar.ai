'use client'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { AppShell } from '@/components/layout/AppShell'
import { PageHeader } from '@/components/layout/PageHeader'
import { Card, Badge, ProgressBar, Spinner } from '@/components/ui/index'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import type { ToolCourse, ToolTopic, ToolEnrollment } from '@/types'
import { cn } from '@/lib/utils'
import {
  ChevronDown, ChevronRight, BookOpen, Code, FolderKanban, HelpCircle,
  CheckCircle, Circle, Play, Layers,
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function ToolCoursePage() {
  useAuth()
  const { slug } = useParams() as { slug: string }
  const [course, setCourse] = useState<ToolCourse | null>(null)
  const [enrollment, setEnrollment] = useState<ToolEnrollment | null>(null)
  const [activeTopic, setActiveTopic] = useState<ToolTopic | null>(null)
  const [activeTab, setActiveTab] = useState<'lesson' | 'exercise' | 'quiz' | 'project'>('lesson')
  const [loading, setLoading] = useState(true)
  const [enrolling, setEnrolling] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const [c, enrs] = await Promise.all([api.getToolCourse(slug), api.getMyToolEnrollments()])
        setCourse(c)
        const enr = enrs.find(e => e.tool_course.slug === slug)
        if (enr) setEnrollment(enr)
        if (c.topics?.[0]) setActiveTopic(c.topics[0])
      } catch {}
      setLoading(false)
    }
    load()
  }, [slug])

  async function handleEnroll() {
    if (!course) return
    setEnrolling(true)
    try {
      const enr = await api.enrollToolCourse(course.id)
      setEnrollment(enr)
    } catch {}
    setEnrolling(false)
  }

  if (loading) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center">
        <Spinner className="w-6 h-6" />
      </div>
    </AppShell>
  )

  if (!course) return (
    <AppShell>
      <div className="flex-1 flex items-center justify-center text-ghost">Tool course not found.</div>
    </AppShell>
  )

  return (
    <AppShell>
      <PageHeader
        title={`${course.icon ?? ''} ${course.title}`}
        subtitle={course.description ?? ''}
        action={
          enrollment ? (
            <div className="flex items-center gap-2">
              <span className="text-xs text-emerald">Enrolled</span>
              <ProgressBar value={enrollment.progress_pct} className="w-24" />
            </div>
          ) : (
            <Button onClick={handleEnroll} loading={enrolling} size="sm">
              Start learning
            </Button>
          )
        }
      />

      <div className="flex-1 flex overflow-hidden">
        {/* ── Topics sidebar (flat — no levels) ── */}
        <div className="w-72 shrink-0 border-r border-border overflow-y-auto bg-ink py-4">
          {course.topics.length === 0 ? (
            <div className="px-4 py-8 text-center">
              <Layers size={24} className="text-muted mx-auto mb-2" />
              <p className="text-xs text-ghost leading-relaxed">
                Content for {course.title} is being drafted. Check back soon.
              </p>
            </div>
          ) : (
            <div className="px-2">
              {course.topics.map(topic => {
                const active = activeTopic?.id === topic.id
                return (
                  <button
                    key={topic.id}
                    className={cn(
                      'w-full text-left px-3 py-2 rounded text-sm transition-all my-0.5',
                      active
                        ? 'bg-amber/10 text-amber border border-amber/20'
                        : 'text-dim hover:text-bright hover:bg-surface border border-transparent'
                    )}
                    onClick={() => setActiveTopic(topic)}
                  >
                    <div className="flex items-center gap-2">
                      <Circle size={8} className={active ? 'text-amber' : 'text-ghost'} />
                      <span className="flex-1">{topic.title}</span>
                    </div>
                    <div className="flex items-center gap-2 mt-1 ml-3.5">
                      <Badge variant={topic.difficulty} className="text-[10px] py-0">
                        {topic.difficulty}
                      </Badge>
                      <span className="text-xs text-ghost">{topic.estimated_hours}h</span>
                    </div>
                  </button>
                )
              })}
            </div>
          )}
        </div>

        {/* ── Topic content ── */}
        {activeTopic ? (
          <div className="flex-1 flex flex-col overflow-hidden">
            <div className="px-8 py-5 border-b border-border shrink-0">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="font-display font-700 text-white text-lg mb-2">{activeTopic.title}</h2>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge variant={activeTopic.difficulty}>{activeTopic.difficulty}</Badge>
                    <Badge variant="ghost">{activeTopic.estimated_hours}h estimated</Badge>
                    {activeTopic.skill_tags.map(tag => (
                      <Badge key={tag} variant="ghost">{tag}</Badge>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-1 mt-4">
                {[
                  { key: 'lesson', icon: BookOpen, label: 'Lessons', count: activeTopic.lessons.length },
                  { key: 'exercise', icon: Code, label: 'Exercises', count: activeTopic.exercises.length },
                  { key: 'quiz', icon: HelpCircle, label: 'Quiz', count: activeTopic.quizzes.length },
                  { key: 'project', icon: FolderKanban, label: 'Project', count: activeTopic.projects.length },
                ].map(({ key, icon: Icon, label, count }) => (
                  <button
                    key={key}
                    onClick={() => setActiveTab(key as typeof activeTab)}
                    className={cn(
                      'flex items-center gap-2 px-4 py-2 rounded text-sm transition-all',
                      activeTab === key
                        ? 'bg-amber/10 text-amber border border-amber/20'
                        : 'text-ghost hover:text-soft border border-transparent'
                    )}
                  >
                    <Icon size={13} />
                    {label}
                    <span className={cn(
                      'text-xs px-1.5 py-0.5 rounded',
                      activeTab === key ? 'bg-amber/20 text-amber' : 'bg-muted text-ghost'
                    )}>
                      {count}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex-1 overflow-y-auto px-8 py-6">
              {activeTab === 'lesson' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.lessons.length === 0 ? (
                    <p className="text-ghost text-sm">No lessons for this topic yet.</p>
                  ) : activeTopic.lessons.map((lesson, i) => (
                    <LessonCard key={lesson.id} lesson={lesson} index={i} topicId={activeTopic.id} />
                  ))}
                </div>
              )}

              {activeTab === 'exercise' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.exercises.length === 0 ? (
                    <p className="text-ghost text-sm">No exercises for this topic yet.</p>
                  ) : activeTopic.exercises.map(ex => (
                    <Card key={ex.id} className="p-5">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-medium text-bright">{ex.title}</h3>
                        <Badge variant={ex.difficulty as 'beginner' | 'intermediate' | 'advanced'}>
                          {ex.difficulty}
                        </Badge>
                      </div>
                      <p className="text-sm text-soft leading-relaxed mb-4">{ex.description}</p>
                      {ex.starter_code && (
                        <pre className="bg-ink border border-border rounded p-4 text-xs font-mono text-soft overflow-x-auto">
                          {ex.starter_code}
                        </pre>
                      )}
                      <div className="flex gap-2 flex-wrap mt-3">
                        {ex.skill_tested.map(s => (
                          <Badge key={s} variant="ghost">{s}</Badge>
                        ))}
                      </div>
                    </Card>
                  ))}
                </div>
              )}

              {activeTab === 'quiz' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.quizzes.length === 0 ? (
                    <p className="text-ghost text-sm">No quiz for this topic yet.</p>
                  ) : activeTopic.quizzes.map(quiz => (
                    <Card key={quiz.id} className="p-5">
                      <h3 className="font-medium text-bright mb-1">{quiz.title}</h3>
                      <p className="text-xs text-ghost">{quiz.questions.length} questions · pass at {quiz.passing_score}%</p>
                    </Card>
                  ))}
                </div>
              )}

              {activeTab === 'project' && (
                <div className="space-y-4 max-w-3xl">
                  {activeTopic.projects.length === 0 ? (
                    <p className="text-ghost text-sm">No project for this topic yet.</p>
                  ) : activeTopic.projects.map(proj => (
                    <Card key={proj.id} className="p-6">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-medium text-bright text-base">{proj.title}</h3>
                        <Badge variant={proj.difficulty as 'beginner' | 'intermediate' | 'advanced'}>
                          {proj.difficulty}
                        </Badge>
                      </div>
                      <p className="text-sm text-soft leading-relaxed mb-4">{proj.description}</p>
                      <div className="flex flex-wrap gap-1.5 mb-2">
                        {proj.tech_stack.map(t => (
                          <span key={t} className="px-2 py-0.5 rounded bg-surface border border-border text-xs font-mono text-dim">
                            {t}
                          </span>
                        ))}
                      </div>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-ghost flex-col gap-2">
            <BookOpen size={32} className="text-muted" />
            <p className="text-sm">
              {course.topics.length === 0 ? 'Content coming soon.' : 'Select a topic from the left to start.'}
            </p>
          </div>
        )}
      </div>
    </AppShell>
  )
}

function LessonCard({ lesson, index, topicId }: {
  lesson: { id: number; title: string; content: string; estimated_minutes: number }
  index: number
  topicId: number
}) {
  const [expanded, setExpanded] = useState(index === 0)
  const [marking, setMarking] = useState(false)
  const [done, setDone] = useState(false)

  async function markComplete() {
    setMarking(true)
    try {
      await api.updateToolTopicProgress(topicId, { lesson_id: lesson.id })
      setDone(true)
    } catch {}
    setMarking(false)
  }

  return (
    <Card className={cn('overflow-hidden transition-all', expanded ? 'border-amber/20' : '')}>
      <button
        className="w-full flex items-center gap-4 p-5 text-left hover:bg-surface/50 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="w-7 h-7 rounded bg-amber/10 border border-amber/20 flex items-center justify-center shrink-0">
          <Play size={11} className="text-amber" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium text-bright text-sm">{lesson.title}</p>
          <p className="text-xs text-ghost mt-0.5">{lesson.estimated_minutes} min read</p>
        </div>
        {expanded
          ? <ChevronDown size={14} className="text-ghost shrink-0" />
          : <ChevronRight size={14} className="text-ghost shrink-0" />
        }
      </button>

      {expanded && (
        <div className="px-5 pb-6 border-t border-border">
          <div className="prose-dark mt-4 text-sm">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {lesson.content}
            </ReactMarkdown>
          </div>
          <div className="mt-4 pt-4 border-t border-border">
            {done ? (
              <span className="flex items-center gap-1.5 text-xs text-emerald">
                <CheckCircle size={13} /> Marked complete
              </span>
            ) : (
              <Button size="sm" variant="outline" loading={marking} onClick={markComplete}>
                Mark as complete
              </Button>
            )}
          </div>
        </div>
      )}
    </Card>
  )
}
