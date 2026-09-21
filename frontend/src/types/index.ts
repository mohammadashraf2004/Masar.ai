// ─── Auth ────────────────────────────────────────────────────────────────────

export interface User {
  id: number
  email: string
  full_name: string
  role: 'student' | 'mentor' | 'admin'
  experience_level: 'beginner' | 'intermediate' | 'advanced'
  is_verified: boolean
  bio?: string
  github_url?: string
  linkedin_url?: string
  avatar_url?: string
  overall_readiness_score: number
  created_at: string
  /** What the account accepted, and whether that is still current. The client
   *  branches on `requires_legal_acceptance` and never compares versions. */
  terms_version?: string | null
  privacy_version?: string | null
  requires_legal_acceptance?: boolean
  /** Announcements the account has yet to see, in the order to show them. Empty
   *  once they are all acknowledged; absent on a session that predates this field. */
  pending_updates?: string[]
}

// ─── Legal documents ─────────────────────────────────────────────────────
// Served by the API together with their version, so the site never holds a
// copy of the wording (or of the version number).
export interface LegalSection {
  heading: string
  body: string[]
}

export interface LegalDocument {
  kind: 'terms' | 'privacy'
  version: string
  language: 'en' | 'ar'
  title: string
  intro: string
  sections: LegalSection[]
}

export interface TokenResponse {
  access_token: string
  token_type: string
  /** Seconds until the access token expires (server-authoritative). */
  expires_in: number
  user: User
}

// ─── Learning ────────────────────────────────────────────────────────────────

export type Difficulty = 'beginner' | 'intermediate' | 'advanced'

// ── Bilingual content ───────────────────────────────────────────────────
// Every learner-facing text field has an optional `_ar` twin. Optional, not
// required: courses authored before the Arabic-first policy have none, and
// the UI falls back to the English original (see lib/content-language.ts).
// Nothing in `code`-shaped fields has a twin — code is identical in every
// language.

export interface Lesson {
  id: number
  title: string
  content: string
  title_ar?: string | null
  content_ar?: string | null
  order: number
  estimated_minutes: number
  has_code_examples: boolean
}

export interface Exercise {
  id: number
  title: string
  description: string
  title_ar?: string | null
  description_ar?: string | null
  starter_code?: string
  difficulty: Difficulty
  skill_tested: string[]
}

export interface Project {
  id: number
  title: string
  description: string
  title_ar?: string | null
  description_ar?: string | null
  difficulty: Difficulty
  tech_stack: string[]
  objectives: string[]
  rubric: Record<string, number>
  starter_repo_url?: string
  estimated_hours: number
}

export interface QuizQuestion {
  type?: 'mcq' | 'open'  // absent/'mcq' = multiple choice (default, backward compatible)
  question: string
  options?: string[]     // present for mcq
  correct?: number       // present for mcq
  explanation: string
}

export interface Quiz {
  id: number
  title: string
  questions: QuizQuestion[]
  title_ar?: string | null
  /** Same questions, authored in Arabic. Indices line up 1:1 with
   *  `questions`, so grading is language-independent. */
  questions_ar?: QuizQuestion[] | null
  passing_score: number
}

export interface Topic {
  id: number
  title: string
  slug: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  order: number
  difficulty: Difficulty
  estimated_hours: number
  prerequisite_ids: number[]
  skill_tags: string[]
  /** Terminology dictionary ids this topic teaches. */
  technical_terms: string[]
  lessons: Lesson[]
  exercises: Exercise[]
  projects: Project[]
  quizzes: Quiz[]
}

export interface TrackLevel {
  id: number
  title: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  order: number
  topics: Topic[]
}

export interface CareerTrack {
  id: number
  slug: string
  title: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  icon?: string
  estimated_weeks: number
  levels: TrackLevel[]
}

export interface CareerTrackSummary {
  id: number
  slug: string
  title: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  icon?: string
  estimated_weeks: number
}

export interface Enrollment {
  id: number
  track_id: number
  track: CareerTrackSummary
  completion_percentage: number
  enrolled_at: string
  target_job_title?: string
}

// ─── Answer Evaluation (conversational exercise/quiz grading) ──────────────

export interface AnswerChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface AnswerSubmission {
  id: number
  exercise_id?: number
  quiz_id?: number
  question_index?: number
  messages: AnswerChatMessage[]
  is_correct: boolean | null
  score: number | null
  updated_at?: string
}

// ─── Tool Courses ──────────────────────────────────────────────────────────

export interface ToolCourseSummary {
  id: number
  slug: string
  title: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  icon?: string
  category?: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimated_hours?: number
  related_track_ids: number[]
  /** Terminology dictionary ids the course teaches. */
  technical_terms: string[]
  /** Skill labels as they appear in job descriptions, e.g. "Vector Search". */
  industry_skills: string[]
  topic_count: number
}

export interface ToolTopic {
  id: number
  title: string
  slug: string
  description?: string
  title_ar?: string | null
  description_ar?: string | null
  order: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimated_hours: number
  skill_tags: string[]
  technical_terms: string[]
  prerequisite_ids: number[]
  lessons: Lesson[]
  exercises: Exercise[]
  quizzes: Quiz[]
  projects: Project[]
}

export interface ToolCourse extends Omit<ToolCourseSummary, 'topic_count'> {
  topics: ToolTopic[]
}

export interface ToolEnrollment {
  id: number
  tool_course_id: number
  tool_course: ToolCourseSummary
  progress_pct: number
  enrolled_at: string
  completed_at?: string
}

export interface UserProgress {
  topic_id: number
  status: 'not_started' | 'in_progress' | 'completed'
  lessons_completed: number[]
  exercises_completed: number[]
  time_spent_minutes: number
}

export interface QuizAttempt {
  id: number
  score: number
  passed: boolean
  feedback: Record<string,
    // No `correct_answer`: the API deliberately withholds the key after a
    // submission, so a blank attempt can't be used to dump it.
    | { correct: boolean; your_answer: number | null; explanation: string }
    | { skipped: true; reason: string }
  >
  attempted_at: string
}

export interface ProjectSubmission {
  id: number
  project_id: number
  /** The submitted solution. Null on rows written before submissions
   *  carried code (they held a repo URL, which nothing ever read). */
  code?: string
  /** Optional notes on the approach — context for the reviewer. */
  description?: string
  ai_review?: CodeReviewResult
  score?: number
  submitted_at: string
}

/** One Socratic hint. Same shape the challenge hint returns. */
export interface ProjectHint {
  hint: string
  concept: string
  next_step: string
}

// ─── Mentor ──────────────────────────────────────────────────────────────────

export interface MentorMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface MentorSession {
  id: number
  title?: string
  messages: MentorMessage[]
  created_at: string
  updated_at?: string
}

export interface MentorResponse {
  session_id: number
  reply: string
  suggested_actions: string[]
}

export interface CodeReviewIssue {
  type: 'bug' | 'style' | 'performance' | 'security' | 'architecture'
  severity: 'low' | 'medium' | 'high'
  line?: number
  message: string
  suggestion: string
}

export interface CodeReviewResult {
  overall_quality: 'poor' | 'fair' | 'good' | 'excellent'
  score: number
  issues: CodeReviewIssue[]
  strengths: string[]
  improvements: string[]
  summary: string
}

export interface SkillGapResult {
  target_role: string
  current_skills: string[]
  missing_skills: Array<{ skill: string; priority: 'critical' | 'high' | 'medium'; reason: string }>
  recommended_roadmap: string[]
  readiness_score: number
  summary: string
}

export interface InterviewQuestion {
  question: string
  question_type: 'theoretical' | 'coding' | 'system_design' | 'behavioral'
  hints: string[]
  follow_up?: string
}

export interface RoadmapWeek {
  week: number
  theme: string
  topics: string[]
  project: string
  goal: string
}

export interface SkillScore {
  skill: string
  score: number
}

// ─── Terminology, vocabulary & search ────────────────────────────────────

/** The language settings forwarded to any AI-generated response. */
export interface LanguagePrefs {
  language: 'ar' | 'en'
  terminology_mode: 'arabic_first' | 'industry' | 'english_technical'
}

/** One dictionary entry as the API serves it. The client normally reads its
 *  own copy from `src/content/terminology`; this shape exists for tooling
 *  and for verifying the two are in step. */
export interface ApiTermEntry {
  id: string
  en: string
  ar: string
  preferred: string
  abbreviation?: string | null
  category: string
  level: string
  aliases: string[]
  definitionAr: string
  definitionEn: string
  exampleAr?: string | null
}

export interface TerminologyDictionary {
  version: number
  terms: ApiTermEntry[]
  /** Official technology names — never translated, in any mode. */
  tech_names: string[]
}

export interface VocabularyProgress {
  /** Term ids the student has met in a lesson. Superset of `learned`. */
  encountered: string[]
  /** Term ids the student has proven, by exercise or by marking them. */
  learned: string[]
  total_terms: number
}

export interface TerminologyWarning {
  term_id: string
  found: string
  suggestion: string
  message: string
}

export interface TerminologyLintResult {
  warnings: TerminologyWarning[]
  terms_used: string[]
}

export interface SearchHit {
  kind: 'tool_course' | 'tool_topic' | 'track' | 'topic' | 'lesson'
  id: number
  title: string
  title_ar?: string | null
  description?: string | null
  description_ar?: string | null
  href: string
  parent_title?: string | null
  score: number
  matched_terms: string[]
}

export interface SearchResults {
  query: string
  /** The surface forms the query was expanded into, both languages. */
  expanded: string[]
  matched_terms: ApiTermEntry[]
  hits: SearchHit[]
}

// ─── Admin analytics ─────────────────────────────────────────────────────
// Mirrors backend/app/controllers/admin_analytics_controller.py. Aggregates
// only — the overview endpoint is identity-free by design, so nothing here
// names an individual user.

export interface TopicCount {
  topic: string
  count: number
}

export interface AdminAnalyticsOverview {
  generated_at: string
  users: {
    total: number
    /** Calendar day, from 00:00 UTC. The 7/30-day figures are rolling. */
    new_today: number
    new_last_7_days: number
    new_last_30_days: number
    verified: number
    /** False when verification email delivery isn't configured, in which
     *  case `verified` reflects the mail setup rather than user intent. */
    verification_reliable: boolean
    verification_note?: string | null
  }
  activation: {
    signed_up: number
    verified: number
    verification_reliable: boolean
    started_learning: number
    completed_first_lesson: number
  }
  learning: {
    lessons_completed: number
    exercises_completed: number
    most_started_topics: TopicCount[]
    most_completed_topics: TopicCount[]
  }
  ai_usage: {
    total_credits_burned: number
    credits_by_feature: Record<string, number>
  }
  retention: {
    available: boolean
    reason?: string | null
    d1?: number | null
    d7?: number | null
    d30?: number | null
  }
}

// ─── Admin credit grants ────────────────────────────────────────────────

export interface AdminUserLookup {
  user_id: number
  email: string
  full_name: string
  credit_balance: number
}

export interface AdminGrantResult {
  message: string
  user_id: number
  email: string
  full_name: string
  credits_granted: number
  new_balance: number
}

// ─── Learning paths ──────────────────────────────────────────────────────
// Mirrors backend/app/views/learning_path.py. Every display string is an
// English field plus an optional `_ar` twin, exactly like the content types
// above; pick between them with `pick()` in lib/content-language.ts. Nothing
// here is translated by the server.

export interface LevelRef {
  slug: string
  name: string
  name_ar?: string | null
  rank: number
}

export interface LearningLevel extends LevelRef {
  description?: string | null
  description_ar?: string | null
}

export interface FieldRef {
  slug: string
  name: string
  name_ar?: string | null
  /** A key resolved to an icon by lib/learning-icons.ts; never a component. */
  icon?: string | null
}

export interface LearningField extends FieldRef {
  description?: string | null
  description_ar?: string | null
  position: number
  /** Lowest level offered without a prerequisite route; null = every level. */
  min_level?: LevelRef | null
  /** True when the field starts at the top level — what the UI badges "Advanced". */
  is_advanced: boolean
  prerequisites: FieldRef[]
  prerequisite_min_required: number
  prerequisite_recommended: number
  course_count: number
  /** Courses whose lessons are actually published. 0 = "coming soon". */
  available_course_count: number
}

export interface Skill {
  slug: string
  name: string
  name_ar?: string | null
  /** A capability ("skill") or a named product used to apply one ("tool"). */
  kind?: 'skill' | 'tool'
}

export interface RoleRef {
  slug: string
  title: string
  title_ar?: string | null
  icon?: string | null
}

export interface CareerGoal extends RoleRef {
  description?: string | null
  description_ar?: string | null
  position: number
  recommended_level?: LevelRef | null
  required_fields: FieldRef[]
  recommended_fields: FieldRef[]
  required_skills: Skill[]
  course_count: number
  available_course_count: number
}

export interface CatalogCourse {
  id: number
  slug: string
  title: string
  title_ar?: string | null
  description?: string | null
  description_ar?: string | null
  kind: 'tool_course' | 'track_level'
  /** Where the underlying lessons live, e.g. /tools/langchain. */
  href?: string | null
  level: LevelRef
  fields: FieldRef[]
  roles: RoleRef[]
  skills: Skill[]
  estimated_hours: number
  /** False for a catalogue entry whose lessons are not published yet. */
  is_available: boolean
}

export interface CatalogCourseDetail extends CatalogCourse {
  assumes: Skill[]
  prerequisites: Array<Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>>
  learning_objectives: string[]
  learning_objectives_ar: string[]
}

export type PathCourseState = 'required' | 'completed' | 'optional' | 'waived'
export type PathStageStatus = 'completed' | 'current' | 'upcoming' | 'coming_soon' | 'skippable'

/** Why a course is on a roadmap. Codes, not sentences: the wording is interface copy. */
export type CourseReason =
  | 'career_requirement' | 'field_requirement' | 'stage_requirement' | 'skill_gap' | 'prerequisite'

export interface StageRef {
  slug: string
  title: string
  title_ar?: string | null
}

/**
 * The facts behind "Why this course?", all decided by the backend from the
 * catalogue. `known_skills` and `skills_to_gain` partition `skills_taught`.
 */
export interface CourseWhy {
  career_goal: RoleRef
  /** The fields on the learner's route this course belongs to. */
  fields: FieldRef[]
  stage: StageRef
  reasons: CourseReason[]
  skills_taught: Skill[]
  known_skills: Skill[]
  skills_to_gain: Skill[]
  /** Taught skills the career goal requires. */
  goal_skills: Skill[]
  /** Courses still to do that need this one first. */
  prerequisite_for: Array<Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>>
  taught_count: number
  known_count: number
  to_gain_count: number
}

export interface PathCourse {
  course: CatalogCourse
  state: PathCourseState
  /** prerequisite | below_level | known_skills */
  reason?: string | null
  completion_pct?: number | null
  /** The skills this course teaches that the learner declared they know. */
  known_skills: Skill[]
  why?: CourseWhy | null
}

/** A course located in its stage: what "current" and "next" point at. */
export interface RoadmapStep extends PathCourse {
  stage_slug: string
  stage_title: string
  stage_title_ar?: string | null
}

export interface PathStage {
  slug: string
  position: number
  title: string
  title_ar?: string | null
  description?: string | null
  description_ar?: string | null
  phase: string
  kind: string
  status: PathStageStatus
  progress_pct?: number | null
  upcoming_count: number
  courses: PathCourse[]
}

/** A code plus parameters; the wording lives in lib/i18n.ts, in both languages. */
export interface PathAdvisory {
  code: string
  severity: 'info' | 'warning'
  params: Record<string, unknown>
}

export interface LearningProgress {
  path_pct?: number | null
  /** Required and completed courses (what `path_pct` is measured over)... */
  path_total?: number | null
  /** ...how many of those are done... */
  path_completed?: number | null
  /** ...and how many the learner already knows (shown, never counted). */
  path_known?: number | null
  overall_pct: number
  by_role: Record<string, number>
  by_field: Record<string, number>
  by_skill: Record<string, number>
}

export interface LearningPath {
  id?: number | null
  is_saved: boolean
  status: string
  level: LevelRef
  career_goal: RoleRef
  fields: FieldRef[]
  /** Requested fields plus any prerequisite routes the backend added. */
  effective_fields: FieldRef[]
  template_slug?: string | null
  stages: PathStage[]
  current_stage_slug?: string | null
  /** Decided by the server: the course to work on now and the one after it. */
  current_course?: RoadmapStep | null
  next_course?: RoadmapStep | null
  /** Every required course is done (decided by the server). */
  is_complete?: boolean
  advisories: PathAdvisory[]
  estimated_hours: number
  estimated_weeks: number
  progress?: LearningProgress | null
  generated_at?: string | null
}

export interface PathSummary {
  slug: string
  career_goal: RoleRef
  field?: FieldRef | null
  recommended_level?: LevelRef | null
  stage_count: number
  course_count: number
  available_course_count: number
  estimated_hours: number
}

export interface LearningProfile {
  level?: LevelRef | null
  career_goal?: RoleRef | null
  fields: FieldRef[]
  known_skills: Skill[]
  onboarding_completed: boolean
  /** The one flag the client branches on to send someone to onboarding. */
  needs_onboarding: boolean
  source: string
  has_active_path: boolean
}

/** A skill offered in "Skills & Technologies I know". */
export interface SkillOption extends Skill {
  /** The field most of its courses belong to; null for tools and uncovered skills. */
  group?: FieldRef | null
  is_required: boolean
  course_count: number
}

export type SkillStatus = 'known' | 'partially_covered' | 'missing'

/** One relevant skill and where the learner stands on it (decided by the backend). */
export interface SkillGapItem extends Skill {
  status: SkillStatus
  /** The field most of the roadmap courses teaching it belong to. */
  group?: FieldRef | null
  /** The earliest roadmap stage that teaches it. */
  stage?: StageRef | null
  is_goal_required: boolean
  /** Taught by a required course in the current stage. */
  is_immediate: boolean
  /** 0 on a goal-required skill: no published course teaches it yet. */
  course_count: number
  /** Not declared, but a course teaching it is finished. */
  covered_by_completed: boolean
}

export interface SkillGapGroup {
  key: string
  kind: 'field' | 'general' | 'tools'
  field?: FieldRef | null
  total: number
  known_count: number
  /** What is still to do here: partially covered, then missing. */
  skills: SkillGapItem[]
}

export interface SkillGapCounts {
  required: number
  known: number
  partial: number
  missing: number
  immediate: number
  /** Declared share of the relevant skills; null when nothing is relevant. */
  coverage_pct: number | null
}

export interface SkillGaps {
  /** False when the learner has no roadmap yet. */
  available: boolean
  level?: LevelRef | null
  career_goal?: RoleRef | null
  fields: FieldRef[]
  current_stage?: StageRef | null
  summary: SkillGapCounts
  known: SkillGapItem[]
  partial: SkillGapItem[]
  missing: SkillGapItem[]
  groups: SkillGapGroup[]
}

export interface LearnerSkill {
  skill: Skill
  /** known | mastered */
  status: string
  /** self_declared | assessment | course_completion */
  source: string
}

export interface MySkills {
  known: LearnerSkill[]
  learning: Skill[]
}

export interface SkillsSaved extends MySkills {
  /** The rebuilt roadmap, or null when the learner has no complete profile yet. */
  path?: LearningPath | null
  roadmap_updated: boolean
}

export interface SkillOptionsQuery {
  career_goal: string
  level?: string | null
  field?: string[]
}

export interface LearningProfileUpdate {
  level?: string | null
  career_goal?: string | null
  fields?: string[]
  known_skills?: string[]
}

export interface GeneratePathRequest {
  level: string
  career_goal: string
  fields: string[]
}

export interface CourseFilters {
  level?: string[]
  field?: string[]
  career_goal?: string[]
  q?: string
  available_only?: boolean
}
