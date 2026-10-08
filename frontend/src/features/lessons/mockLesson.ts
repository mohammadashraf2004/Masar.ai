import type { Exercise, Lesson } from '@/types'

/**
 * A single design fixture for the lesson page: no "AI Engineer / LangGraph"
 * course exists in the real curriculum yet, so this course/lesson pair is
 * frontend-only and never touches the API. `DEMO_COURSE_SLUG` is the one
 * route this data answers; every other `/courses/[course]/lessons/[lesson]`
 * request goes through `useLessonPage`'s real-data path.
 *
 * The lesson body is plain Markdown through the same `MarkdownLesson`
 * renderer every real lesson uses — no separate block schema. Two
 * simplifications from how the design brief described the body, both
 * because the real renderer has no equivalent and this fixture must not
 * invent one:
 *   - the "flow" diagram is a plain fenced block (```), which the renderer
 *     already treats as an arrow-highlighted diagram, not a chip row.
 *   - the code sample has no per-token highlighting: the renderer has no
 *     line/token-highlight syntax to key off.
 */
export const DEMO_COURSE_SLUG = 'langgraph-agent-memory'
export const DEMO_LESSON_ID = 1007

export const DEMO_TRACK = { slug: 'ai-engineer', title: 'AI Engineer', title_ar: 'مهندس ذكاء اصطناعي' }
export const DEMO_COURSE = { slug: DEMO_COURSE_SLUG, title: 'LangGraph', title_ar: 'LangGraph' }

export const DEMO_LESSON_NUMBER = 7
export const DEMO_LESSON_TOTAL = 12
export const DEMO_CREDITS = 40

const CONTENT_AR = `كل استدعاء لـ graph.invoke يبدأ من حالة فارغة، فالوكيل لا يتذكّر ما قيل قبل رسالة واحدة. في هذا الدرس نضيف طبقة ذاكرة تحفظ الحالة بعد كل خطوة وتستعيدها عند الاستدعاء التالي.

## ١. ما هو الـ Checkpointer؟

الـ Checkpointer يلتقط لقطة من حالة الـ graph بعد كل عقدة ويخزّنها تحت مفتاح اسمه thread_id. عندما تستدعي الـ graph بنفس المفتاح، يُكمل من آخر لقطة بدل أن يبدأ من الصفر.

\`\`\`
invoke(msg, thread_id) → load state → agent node → save checkpoint
\`\`\`

## ٢. سطران يكفيان

تمرّر الـ checkpointer عند compile، ثم تمرّر thread_id داخل config في كل استدعاء:

\`\`\`python
graph = builder.compile(checkpointer=MemorySaver())
graph.invoke(state, {"configurable": {"thread_id": "user-42"}})
\`\`\`

> **انتبه**
>
> MemorySaver يحفظ في الذاكرة فقط؛ إذا أُعيد تشغيل الخادم تضيع المحادثات. للإنتاج استخدم SqliteSaver أو PostgresSaver.`

const CONTENT_EN = `Every call to graph.invoke starts from an empty state, so the agent has no memory of anything said before one message ago. This lesson adds a memory layer that saves state after every step and restores it on the next call.

## 1. What is a Checkpointer?

A Checkpointer captures a snapshot of the graph's state after every node and stores it under a key called thread_id. Calling the graph again with the same key resumes from that last snapshot instead of starting over.

\`\`\`
invoke(msg, thread_id) → load state → agent node → save checkpoint
\`\`\`

## 2. Two lines are enough

Pass the checkpointer at compile time, then pass thread_id inside config on every call:

\`\`\`python
graph = builder.compile(checkpointer=MemorySaver())
graph.invoke(state, {"configurable": {"thread_id": "user-42"}})
\`\`\`

> **Note**
>
> MemorySaver only keeps state in memory; restarting the server loses every conversation. Use SqliteSaver or PostgresSaver in production.`

export const DEMO_EXERCISE: Exercise = {
  id: 9007,
  title: 'Add a Checkpointer so the agent keeps conversation context',
  title_ar: 'أضِف Checkpointer ليحتفظ الوكيل بسياق المحادثة',
  description: 'Wire a MemorySaver checkpointer into the compiled graph and pass a stable thread_id on every invoke call so the agent remembers earlier turns of the same conversation.',
  description_ar: 'اربط MemorySaver كـ checkpointer بالـ graph المُجمَّع، ومرّر thread_id ثابتًا في كل استدعاء invoke حتى يتذكّر الوكيل الأدوار السابقة من نفس المحادثة.',
  starter_code: 'from langgraph.checkpoint.memory import MemorySaver\n\ngraph = builder.compile()\n\ndef run(message: str, thread_id: str):\n    return graph.invoke({"messages": [message]})\n',
  exercise_type: 'code',
  language: 'python',
  grading_available: true,
  difficulty: 'intermediate',
  skill_tested: ['LangGraph', 'State management'],
  lesson_id: DEMO_LESSON_ID,
  course_slug: DEMO_COURSE_SLUG,
}
/** "٣ من ٤": the exercise's position within its module, for the counter
 *  `ExerciseCard` already renders unchanged. */
export const DEMO_EXERCISE_INDEX = 2
export const DEMO_EXERCISE_TOTAL = 4

export const DEMO_LESSON: Lesson = {
  id: DEMO_LESSON_ID,
  title: 'Continuous memory in LangGraph',
  title_ar: 'الذاكرة المستمرة في LangGraph',
  content: CONTENT_EN,
  content_ar: CONTENT_AR,
  order: DEMO_LESSON_NUMBER,
  estimated_minutes: 15,
  has_code_examples: true,
  course_slug: DEMO_COURSE_SLUG,
}

/** 'upcoming': unlocked but not yet reached or completed — same empty mark as
 *  'locked' in the aside, but still a clickable link. The mock module never
 *  produces this state (every row is explicitly done/current/locked); a real
 *  course's later, unlocked lessons do. */
export type ModuleLessonStatus = 'done' | 'current' | 'upcoming' | 'locked'

export interface ModuleLessonRow {
  id: number
  order: number
  title: string
  title_ar: string
  status: ModuleLessonStatus
}

export const DEMO_MODULE_LESSONS: ModuleLessonRow[] = [
  { id: 1005, order: 5, title: 'State and MessagesState', title_ar: 'الحالة و MessagesState', status: 'done' },
  { id: 1006, order: 6, title: 'Tools and conditional nodes', title_ar: 'الأدوات والعُقد الشرطية', status: 'done' },
  { id: DEMO_LESSON_ID, order: 7, title: 'Continuous memory', title_ar: 'الذاكرة المستمرة', status: 'current' },
  { id: 1008, order: 8, title: 'Persisting to disk with SqliteSaver', title_ar: 'الحفظ على القرص بـ SqliteSaver', status: 'locked' },
  { id: 1009, order: 9, title: 'Human in the loop', title_ar: 'الإنسان في الحلقة', status: 'locked' },
]

/** The lesson right after this one in the module — what "Next lesson" links to. */
export const DEMO_NEXT_LESSON_ID = 1008
