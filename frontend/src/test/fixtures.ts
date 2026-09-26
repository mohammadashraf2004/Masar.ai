import type {
  CareerGoal, CatalogCourse, FieldRef, LearningField, LearningLevel, LearningPath,
  LearningProfile, LevelRef, MySkills, PathCourse, PathStage, PathSummary, RoadmapStep, RoleRef, Skill,
  SkillOption, CourseWhy, SkillGapItem, SkillGaps, CatalogCourseDetail, ReadinessReport, Recommendation, Recommendations,
} from '@/types'
import type { LearningCatalog } from '@/hooks/useLearningCatalog'

// The same vocabulary the backend seeds (slugs and Arabic names included), so a
// test that passes here is passing on data shaped like the real thing.

export const BEGINNER: LevelRef = { slug: 'beginner', name: 'Beginner', name_ar: 'مبتدئ', rank: 1 }
export const INTERMEDIATE: LevelRef = { slug: 'intermediate', name: 'Intermediate', name_ar: 'متوسط', rank: 2 }
export const ADVANCED: LevelRef = { slug: 'advanced', name: 'Advanced', name_ar: 'متقدم', rank: 3 }

export const LEVELS: LearningLevel[] = [
  { ...BEGINNER, description: 'New to programming or AI, and you want to start from the basics.', description_ar: 'جديد على البرمجة أو الـ AI، وتريد أن تبدأ من الأساسيات.' },
  { ...INTERMEDIATE, description: 'You write Python and know the basics of machine learning or AI.', description_ar: 'تكتب Python وتعرف أساسيات الـ Machine Learning أو الـ AI.' },
  { ...ADVANCED, description: 'You have built real ML or AI projects and want depth and specialization.', description_ar: 'بنيت مشاريع ML أو AI حقيقية وتريد التعمق والتخصص.' },
]

function field(slug: string, name: string, name_ar: string, icon: string, position: number, extra: Partial<LearningField> = {}): LearningField {
  return {
    slug, name, name_ar, icon, position,
    description: `${name} description`, description_ar: `وصف ${name_ar}`,
    min_level: null, is_advanced: false, prerequisites: [],
    prerequisite_min_required: 1, prerequisite_recommended: 1,
    course_count: 4, available_course_count: 4,
    ...extra,
  }
}

export const NLP = field('nlp', 'NLP & LLMs', 'معالجة اللغة الطبيعية والـ LLMs', 'message-square', 3)
export const VISION = field('computer-vision', 'Computer Vision', 'الرؤية الحاسوبية', 'eye', 4, { available_course_count: 0 })
export const SPEECH = field('speech', 'Speech & Voice AI', 'الصوت والكلام', 'mic', 5, { available_course_count: 0 })
export const MULTIMODAL = field('multimodal', 'Multimodal AI', 'الذكاء الاصطناعي متعدد الوسائط', 'layers', 6, {
  min_level: ADVANCED, is_advanced: true,
  prerequisites: [NLP, VISION, SPEECH].map(({ slug, name, name_ar, icon }) => ({ slug, name, name_ar, icon })),
  prerequisite_recommended: 2, available_course_count: 1,
})

export const FIELDS: LearningField[] = [
  field('data', 'Data & Analytics', 'تحليل البيانات', 'bar-chart', 1),
  field('machine-learning', 'Machine Learning', 'تعلّم الآلة', 'brain', 2),
  NLP, VISION, SPEECH, MULTIMODAL,
]

function goal(slug: string, title: string, title_ar: string, icon: string, position: number): CareerGoal {
  return {
    slug, title, title_ar, icon, position,
    description: `${title} description`, description_ar: `وصف ${title_ar}`,
    recommended_level: INTERMEDIATE, required_fields: [], recommended_fields: [], required_skills: [],
    course_count: 5, available_course_count: 3,
  }
}

export const GOALS: CareerGoal[] = [
  goal('data-analyst', 'Data Analyst', 'محلل بيانات', 'bar-chart', 1),
  goal('ml-engineer', 'ML Engineer', 'مهندس تعلّم آلة', 'brain', 2),
  goal('ai-developer', 'AI Developer', 'مطوّر تطبيقات ذكاء اصطناعي', 'code', 3),
  goal('mlops-engineer', 'MLOps Engineer', 'مهندس MLOps', 'server', 4),
  goal('ai-engineer', 'AI Engineer', 'مهندس ذكاء اصطناعي', 'layers', 5),
]

export const CATALOG: LearningCatalog = { levels: LEVELS, fields: FIELDS, goals: GOALS }

export const ref = (f: LearningField): FieldRef => ({ slug: f.slug, name: f.name, name_ar: f.name_ar, icon: f.icon })
export const role = (g: CareerGoal): RoleRef => ({ slug: g.slug, title: g.title, title_ar: g.title_ar, icon: g.icon })
export const AI_ENGINEER = role(GOALS[4])

export const RAG_SKILL: Skill = { slug: 'rag', name: 'RAG', name_ar: null, kind: 'skill' }
export const EMBEDDINGS_SKILL: Skill = { slug: 'embeddings', name: 'Embeddings', name_ar: null }
export const EVAL_SKILL: Skill = { slug: 'evaluation', name: 'Evaluation', name_ar: null }
export const FASTAPI_SKILL: Skill = { slug: 'fastapi', name: 'FastAPI', name_ar: null, kind: 'tool' }
export const LLMS_SKILL: Skill = { slug: 'llms', name: 'LLMs', name_ar: null, kind: 'skill' }
export const LANGCHAIN_SKILL: Skill = { slug: 'langchain', name: 'LangChain', name_ar: null, kind: 'tool' }

/** What GET /learning/skills returns for AI Engineer + NLP: capabilities filed
 *  under a field, tools apart. The order is the server's. */
export const SKILL_OPTIONS: SkillOption[] = [
  { ...EVAL_SKILL, kind: 'skill', group: null, is_required: true, course_count: 1 },
  { ...LLMS_SKILL, group: ref(NLP), is_required: false, course_count: 3 },
  { ...RAG_SKILL, group: ref(NLP), is_required: false, course_count: 3 },
  { ...EMBEDDINGS_SKILL, kind: 'skill', group: ref(NLP), is_required: false, course_count: 2 },
  { ...LANGCHAIN_SKILL, group: null, is_required: false, course_count: 1 },
  { ...FASTAPI_SKILL, group: null, is_required: false, course_count: 2 },
]

export const MY_SKILLS: MySkills = {
  known: [
    { skill: LLMS_SKILL, status: 'known', source: 'self_declared' },
    { skill: RAG_SKILL, status: 'known', source: 'course_completion' },
  ],
  learning: [EMBEDDINGS_SKILL],
}
export const SYSTEM_SKILL: Skill = { slug: 'system-design', name: 'System Design', name_ar: null }
export const VECTOR_SKILL: Skill = { slug: 'vector-databases', name: 'Vector Databases', name_ar: null }

export function course(over: Partial<CatalogCourse> = {}): CatalogCourse {
  return {
    id: 1, slug: 'rag-knowledge-systems',
    title: 'RAG & Knowledge Systems', title_ar: 'أنظمة RAG والمعرفة',
    description: 'Build retrieval-augmented applications.', description_ar: 'ابنِ تطبيقات تعتمد على الاسترجاع.',
    kind: 'track_level', href: '/tracks/ai-developer',
    level: INTERMEDIATE, fields: [ref(NLP)], roles: [role(GOALS[2]), AI_ENGINEER],
    skills: [RAG_SKILL, EMBEDDINGS_SKILL, VECTOR_SKILL, EVAL_SKILL, FASTAPI_SKILL],
    estimated_hours: 40.5, is_available: true,
    ...over,
  }
}

// `course` is a partial override of the catalogue course, not a whole one — so
// it is removed from the PathCourse override before the two are intersected.
export function pathCourse(over: Omit<Partial<PathCourse>, 'course'> & { course?: Partial<CatalogCourse> } = {}): PathCourse {
  const { course: courseOver, ...rest } = over
  return { course: course(courseOver), state: 'required', reason: null, completion_pct: 0, known_skills: [], ...rest }
}

/** A course located in its stage: what `current_course` / `next_course` carry. */
export function step(over: Omit<Partial<RoadmapStep>, 'course'> & { course?: Partial<CatalogCourse> } = {}): RoadmapStep {
  const { course: courseOver, ...rest } = over
  return {
    ...pathCourse({ course: courseOver }),
    stage_slug: 'nlp-llm', stage_title: 'NLP & LLM Engineering', stage_title_ar: 'هندسة NLP والـ LLMs',
    ...rest,
  }
}

export function stage(over: Partial<PathStage> = {}): PathStage {
  return {
    slug: 'nlp-llm', position: 1, title: 'NLP & LLM Engineering', title_ar: 'هندسة NLP والـ LLMs',
    description: null, description_ar: null, phase: 'specialization', kind: 'learning',
    status: 'upcoming', progress_pct: null, upcoming_count: 0,
    courses: [pathCourse()],
    ...over,
  }
}

export function path(over: Partial<LearningPath> = {}): LearningPath {
  return {
    id: 1, is_saved: true, status: 'active',
    level: INTERMEDIATE, career_goal: AI_ENGINEER,
    fields: [ref(NLP)], effective_fields: [ref(NLP)],
    template_slug: 'ai-engineer-path',
    stages: [
      stage({ slug: 'foundations', position: 1, title: 'AI Foundations', title_ar: 'أسس الذكاء الاصطناعي', status: 'completed', progress_pct: 100,
        courses: [pathCourse({ course: { id: 10, slug: 'foundations', title: 'AI Foundations', title_ar: 'أسس الذكاء الاصطناعي', level: BEGINNER }, state: 'completed', completion_pct: 100 })] }),
      stage({ slug: 'machine-learning', position: 2, title: 'Machine Learning', title_ar: 'تعلّم الآلة', status: 'coming_soon', courses: [], upcoming_count: 3 }),
      stage({ slug: 'nlp-llm', position: 3, status: 'current', progress_pct: 50,
        courses: [
          pathCourse({ course: { id: 20, slug: 'prompt-engineering', title: 'Prompt Engineering', title_ar: 'هندسة الـ Prompts' }, state: 'completed', completion_pct: 100 }),
          pathCourse({ course: { id: 21, slug: 'langchain', title: 'LangChain', title_ar: null, kind: 'tool_course', href: '/tools/langchain' }, state: 'required', completion_pct: 0 }),
          pathCourse({ course: { id: 22, slug: 'llm-integration', title: 'LLM Integration', level: BEGINNER }, state: 'optional', reason: 'below_level' }),
        ] }),
      stage({ slug: 'rag', position: 4, title: 'RAG Engineering', title_ar: 'هندسة الـ RAG', status: 'upcoming', progress_pct: 0,
        courses: [pathCourse(), pathCourse({ course: { id: 2, slug: 'advanced-rag', title: 'Advanced RAG' } })], upcoming_count: 2 }),
      stage({ slug: 'capstone-ai-engineer', position: 5, title: 'AI Engineer Capstone', title_ar: 'المشروع الختامي: مهندس ذكاء اصطناعي', status: 'coming_soon', courses: [], kind: 'capstone' }),
    ],
    current_stage_slug: 'nlp-llm', advisories: [],
    current_course: step({ course: { id: 21, slug: 'langchain', title: 'LangChain', title_ar: null, kind: 'tool_course', href: '/tools/langchain' } }),
    next_course: step({ course: { id: 1, slug: 'rag-knowledge-systems' }, stage_slug: 'rag', stage_title: 'RAG Engineering', stage_title_ar: 'هندسة الـ RAG' }),
    is_complete: false,
    estimated_hours: 14, estimated_weeks: 3,
    progress: { path_pct: 72, path_total: 10, path_completed: 7, path_known: 2, overall_pct: 64, by_role: { 'ai-engineer': 64 }, by_field: { nlp: 72 }, by_skill: { rag: 40 } },
    generated_at: '2026-09-19T10:00:00Z',
    ...over,
  }
}

export function profile(over: Partial<LearningProfile> = {}): LearningProfile {
  return {
    level: INTERMEDIATE, career_goal: AI_ENGINEER, fields: [ref(NLP)], known_skills: [],
    onboarding_completed: true, needs_onboarding: false, source: 'onboarding', has_active_path: true,
    ...over,
  }
}

export const NEEDS_ONBOARDING: LearningProfile = profile({
  level: null, career_goal: null, fields: [], onboarding_completed: false, needs_onboarding: true,
  source: 'none', has_active_path: false,
})

export function summary(over: Partial<PathSummary> = {}): PathSummary {
  return {
    slug: 'ai-engineer-nlp', career_goal: AI_ENGINEER, field: ref(NLP), recommended_level: INTERMEDIATE,
    stage_count: 9, course_count: 14, available_course_count: 11, estimated_hours: 150,
    ...over,
  }
}

// ─── Skill gaps and "Why this course?" ──────────────────────────────────────
// Shaped exactly like GET /learning/my-skill-gaps and the `why` block on a
// roadmap course. Every fact is written out - the frontend derives none of it.

export function why(over: Partial<CourseWhy> = {}): CourseWhy {
  return {
    career_goal: AI_ENGINEER,
    fields: [ref(NLP)],
    stage: { slug: 'rag', title: 'RAG Engineering', title_ar: 'هندسة الـ RAG' },
    reasons: ['career_requirement', 'field_requirement', 'stage_requirement', 'skill_gap'],
    skills_taught: [RAG_SKILL, EMBEDDINGS_SKILL, VECTOR_SKILL, EVAL_SKILL],
    known_skills: [EMBEDDINGS_SKILL],
    skills_to_gain: [RAG_SKILL, VECTOR_SKILL, EVAL_SKILL],
    goal_skills: [EVAL_SKILL],
    prerequisite_for: [],
    taught_count: 4, known_count: 1, to_gain_count: 3,
    ...over,
  }
}

export function gapItem(skill: Skill, over: Partial<SkillGapItem> = {}): SkillGapItem {
  return {
    ...skill, kind: skill.kind ?? 'skill', status: 'missing', group: ref(NLP),
    stage: { slug: 'rag', title: 'RAG Engineering', title_ar: 'هندسة الـ RAG' },
    is_goal_required: false, is_immediate: false, course_count: 2, covered_by_completed: false,
    ...over,
  }
}

const KNOWN_EMBEDDINGS = gapItem(EMBEDDINGS_SKILL, { status: 'known' })
const MISSING_RAG = gapItem(RAG_SKILL, { is_immediate: true })
const PARTIAL_VECTOR = gapItem(VECTOR_SKILL, { status: 'partially_covered' })
const MISSING_EVAL = gapItem(EVAL_SKILL, { group: null, is_goal_required: true })
const MISSING_LANGCHAIN = gapItem(LANGCHAIN_SKILL, { group: null })

export function skillGaps(over: Partial<SkillGaps> = {}): SkillGaps {
  return {
    available: true,
    level: INTERMEDIATE, career_goal: AI_ENGINEER, fields: [ref(NLP)],
    current_stage: { slug: 'rag', title: 'RAG Engineering', title_ar: 'هندسة الـ RAG' },
    summary: { required: 5, known: 1, partial: 1, missing: 3, immediate: 1, coverage_pct: 20 },
    known: [KNOWN_EMBEDDINGS],
    partial: [PARTIAL_VECTOR],
    missing: [MISSING_RAG, MISSING_EVAL, MISSING_LANGCHAIN],
    groups: [
      { key: 'field:nlp', kind: 'field', field: ref(NLP), total: 3, known_count: 1, skills: [PARTIAL_VECTOR, MISSING_RAG] },
      { key: 'general', kind: 'general', field: null, total: 1, known_count: 0, skills: [MISSING_EVAL] },
      { key: 'tools', kind: 'tools', field: null, total: 1, known_count: 0, skills: [MISSING_LANGCHAIN] },
    ],
    ...over,
  }
}

export const NO_GAPS_YET: SkillGaps = {
  available: false, fields: [], known: [], partial: [], missing: [], groups: [],
  summary: { required: 0, known: 0, partial: 0, missing: 0, immediate: 0, coverage_pct: null },
}

// ─── Independent enrollment, readiness and recommendations ───────────────────

export const NO_RECOMMENDATIONS: Recommendations = {
  continue_learning: [], recommended_next: [], build_foundations: [], completed: [], career_goal: null,
}

export function recommendation(over: Partial<Recommendation> = {}): Recommendation {
  return {
    course: course(), reason_code: 'good_place_to_start', params: {},
    reason: 'A good place to start: it assumes no earlier course.', readiness: 'ready',
    ...over,
  }
}

export function readinessReport(over: Partial<ReadinessReport> = {}): ReadinessReport {
  return {
    course_id: 1, course_slug: 'rag-knowledge-systems', state: 'mostly_ready', score: 78,
    strengths: [{ skill: LLMS_SKILL, standing: 'strong', level: 'intermediate', required: true }],
    gaps: [{ skill: EMBEDDINGS_SKILL, standing: 'gap', level: 'beginner', required: true }],
    recommended_review: [{
      course: { id: 4, slug: 'embeddings-search', title: 'Embeddings & Semantic Search', title_ar: null },
      skills: [EMBEDDINGS_SKILL], required: true,
      modules: [{ id: 41, order: 2, title: 'Vector similarity', title_ar: null }],
    }],
    has_prerequisites: true, assessment_available: true, last_assessed_at: null,
    ...over,
  }
}

export function courseDetail(over: Partial<CatalogCourseDetail> = {}): CatalogCourseDetail {
  return {
    ...course(),
    assumes: [], prerequisites: [], learning_objectives: ['Build a retrieval pipeline'], learning_objectives_ar: [],
    modules: [{
      id: 11, order: 1, title: 'Chunking', title_ar: null, lesson_count: 4, exercise_count: 1, quiz_count: 1, project_count: 0,
    }],
    projects: [{ id: 21, title: 'Support bot', title_ar: null, module_order: 1, kind: 'capstone' }],
    roadmaps: [{ career_goal: AI_ENGINEER, track_role: 'core', position: 3, total: 9 }],
    ...over,
  }
}
