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
  kind: 'terms' | 'privacy' | 'refund'
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

/** A run of lesson Markdown, exactly as authored (code, tables, callouts and equations are inside it). */
export interface MarkdownBlock {
  type: 'markdown'
  content: string
}

/** An image, placed where the lesson's author put it (`{{image:key}}`). `url` is relative to the API root (or absolute). */
export interface ImageBlock {
  type: 'image'
  asset_key: string
  url: string
  alt: string
  caption?: string | null
  /** Language the alt text / caption are actually written in: the reader's language when the course wrote
   *  one, else the other (so an English fallback inside an Arabic lesson keeps its own direction). */
  alt_lang?: 'en' | 'ar'
  caption_lang?: 'en' | 'ar'
  /** Shown before the caption when the course sets one ("Figure 4.2"). */
  figure_number?: string | null
  width?: number | null
  height?: number | null
}

/** The lesson places an image the course no longer has; shown as a note, never silently dropped. */
export interface MissingImageBlock {
  type: 'image_missing'
  asset_key: string
}

/**
 * An unresolved `[[IMAGE_NEEDED: ...]]` authoring request. The API sends it only outside production (title
 * only, never the raw marker); a learner of a published lesson never receives one.
 */
export interface AuthorMarkerBlock {
  type: 'author_marker'
  kind: 'image_needed'
  title: string
}

/** The lesson points at an exercise it does not have. Sent outside production only, as an author diagnostic. */
export interface MissingExerciseBlock {
  type: 'exercise_missing'
  exercise_id: string
}

/** A lesson body is an ordered list of these; the browser renders them in the order given. */
export type LessonBlock = MarkdownBlock | ImageBlock | MissingImageBlock | AuthorMarkerBlock | MissingExerciseBlock

export interface Lesson {
  id: number
  title: string
  content: string
  title_ar?: string | null
  content_ar?: string | null
  /** The body as ordered blocks; null for a lesson with no authoring syntax in it (render `content`). */
  blocks?: LessonBlock[] | null
  blocks_ar?: LessonBlock[] | null
  order: number
  /** Null when the course does not state a duration. */
  estimated_minutes?: number | null
  has_code_examples: boolean
  is_preview?: boolean
  is_locked?: boolean
  course_slug?: string | null
}

export interface Exercise {
  id: number
  title: string
  description: string
  title_ar?: string | null
  description_ar?: string | null
  starter_code?: string
  exercise_type?: 'legacy' | 'code' | 'code_pending'
  language?: string | null
  hint?: string | null
  hint_ar?: string | null
  grading_available?: boolean
  difficulty: Difficulty
  skill_tested: string[]
  is_locked?: boolean
  course_slug?: string | null
  /** The lesson this exercise is graded against, when the course authors a
   *  direct 1:1 pairing. Null/absent for an exercise that only shares a
   *  topic with its sibling lessons. */
  lesson_id?: number | null
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
  estimated_hours?: number | null
  is_locked?: boolean
  course_slug?: string | null
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
  is_locked?: boolean
  course_slug?: string | null
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
  estimated_hours?: number | null
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
  title_en?: string | null
  stack?: string[]
  level?: string | null
  stage_count?: number
  course_count?: number
  hours?: number
  progress?: number
  status?: TrackCatalogueStatus
  cta_href?: string | null
  stages?: TrackCatalogueStage[]
  projects?: string[]
  roles?: string[]
  exam?: TrackExamState | null
}

export type TrackCatalogueStatus = 'done' | 'current' | 'open'
export type TrackStageStatus = 'completed' | 'current' | 'start' | 'locked'

export interface TrackCatalogueStage {
  number: number
  title: string
  hours: number
  courses: string[]
  status: TrackStageStatus
}

export interface TrackExamState {
  status: 'passed' | 'available' | 'locked'
  score?: number | null
  unlock_after_stage: number
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
  title_en?: string | null
  stack?: string[]
  level?: string | null
  stage_count?: number
  course_count?: number
  hours?: number
  progress?: number
  status?: TrackCatalogueStatus
  cta_href?: string | null
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
  estimated_hours?: number | null
  skill_tags: string[]
  technical_terms: string[]
  prerequisite_ids: number[]
  completion_required?: boolean
  is_optional?: boolean
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
  /** Set on the assistant bubble that reports a failed request, so it is
   *  announced as an alert and styled as one. Never sent to the server. */
  error?: boolean
  /** A Mentor v2 answer's blocks (then `content` is their JSON and is not shown). */
  blocks?: import('@/features/mentor/types').MentorBlock[]
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

// ─── AI Vocabulary (normalized dictionary, migration 022) ──────────────────

export interface VocabularyTermProgressState {
  status: 'new' | 'learning' | 'mastered'
}

export interface VocabularyTermSummary {
  slug: string
  term_en: string
  term_ar: string
  acronym?: string | null
  explanation_simple_ar?: string | null
  definition_en: string
  definition_ar: string
  category?: string | null
  difficulty: string
  course_count: number
  progress?: VocabularyTermProgressState | null
}

export interface VocabularyCourseMapping {
  course_key: string
  course_title?: string | null
  course_href?: string | null
  /** False for a course whose only association is course/module-level (no
   *  lesson body exists, e.g. COURSE-006) — never offer a lesson deep-link
   *  for these, even when `course_href` is set. */
  has_lesson_mapping: boolean
}

export interface VocabularyLessonMapping {
  course_key: string
  module_key?: string | null
  lesson_key: string
  lesson_title?: string | null
  href?: string | null
}

export interface VocabularyRelatedTerm {
  slug: string
  term_en: string
  term_ar: string
}

export interface VocabularyTermDetail {
  slug: string
  term_en: string
  term_ar: string
  acronym?: string | null
  aliases: string[]
  category?: string | null
  difficulty: string
  tags: string[]
  definition_en: string
  definition_ar: string
  explanation_simple_ar?: string | null
  why_it_matters_ar?: string | null
  example_ar?: string | null
  related_terms: VocabularyRelatedTerm[]
  courses: VocabularyCourseMapping[]
  first_introduced?: VocabularyLessonMapping | null
  progress?: VocabularyTermProgressState | null
}

export interface VocabularyListResponse {
  items: VocabularyTermSummary[]
  total: number
  page: number
  page_size: number
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
  /** The role relationship for the single `career_goal` catalogue filter. */
  track_role?: CourseRole | null
  estimated_hours: number
  /** The course's structure. Counts only: a listing never carries lesson text. */
  module_count?: number
  lesson_count?: number
  /** False for a catalogue entry whose lessons are not published yet. */
  is_available: boolean
  is_free?: boolean
  /** Signed-in learners only: where they stand in this course. */
  enrollment?: EnrollmentBrief | null
  readiness?: ReadinessBrief | null
  /** Courses the card suggests studying before this one (advice, never a gate). */
  recommended_before?: Array<Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>>
}

// ─── Independent course enrollment, readiness and recommendations ─────────

export type LearningStatus = 'enrolled' | 'in_progress' | 'completed' | 'paused'

export interface EnrollmentBrief {
  status: LearningStatus
  /** Derived from the learner's activity on every request; never stored. */
  progress_percentage: number
  enrolled_at?: string | null
  started_at?: string | null
  completed_at?: string | null
}

export type ReadinessState = 'ready' | 'mostly_ready' | 'needs_foundation' | 'not_assessed'

export interface ReadinessBrief {
  state: ReadinessState
  score: number
}

export type SkillProficiency = 'not_assessed' | 'beginner' | 'intermediate' | 'advanced'
export type SkillStanding = 'strong' | 'partial' | 'gap' | 'unknown'

export interface SkillStandingItem {
  skill: Skill
  standing: SkillStanding
  level: SkillProficiency
  /** Whether a *required* prerequisite teaches it. */
  required: boolean
}

export interface CourseModule {
  /** The topic id the course viewer opens. */
  id: number
  order: number
  title: string
  title_ar?: string | null
  description?: string | null
  description_ar?: string | null
  estimated_hours?: number | null
  lesson_count: number
  exercise_count: number
  quiz_count: number
  project_count: number
  completion_required?: boolean
  is_optional?: boolean
  completion_pct?: number | null
  status?: 'not_started' | 'in_progress' | 'completed' | null
}

export interface CourseProject {
  id: number
  title: string
  title_ar?: string | null
  estimated_hours?: number | null
  module_order: number
  kind: 'module' | 'lab' | 'capstone' | 'lesson'
}

export interface RoadmapMembership {
  career_goal: RoleRef
  track_role: CourseRole
  position?: number | null
  total: number
}

export interface ReviewModule {
  id: number
  order: number
  title: string
  title_ar?: string | null
}

export interface ReviewItem {
  course: Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>
  skills: Skill[]
  required: boolean
  modules: ReviewModule[]
}

export interface ReadinessReport {
  course_id: number
  course_slug: string
  state: ReadinessState
  score: number
  strengths: SkillStandingItem[]
  gaps: SkillStandingItem[]
  recommended_review: ReviewItem[]
  has_prerequisites: boolean
  /** A short check exists for this course. */
  assessment_available: boolean
  last_assessed_at?: string | null
}

export interface ModuleRef {
  id: number
  order: number
  title: string
  title_ar?: string | null
}

export interface StartPlan {
  mode: 'start' | 'resume'
  recommended_module?: ModuleRef | null
  preparation: ReviewItem[]
}

export interface CourseLearningEnrollment {
  course_id: number
  course_slug: string
  status: LearningStatus
  source: string
  progress_percentage: number
  enrolled_at?: string | null
  started_at?: string | null
  completed_at?: string | null
}

export interface EnrollResult {
  enrollment: CourseLearningEnrollment
  created: boolean
  readiness: ReadinessReport
  start: StartPlan
}

export interface CourseProgress {
  course_id: number
  course_slug: string
  enrolled: boolean
  status: LearningStatus
  progress_percentage: number
  modules_total: number
  modules_completed: number
  lessons_total: number
  modules: CourseModule[]
  next_module?: ModuleRef | null
}

export interface AssessmentQuestion {
  /** "<quiz id>:<index>". No answer key is ever sent. */
  id: string
  skill: Skill
  question: string
  question_ar?: string | null
  options: string[]
  options_ar?: string[] | null
}

export interface ReadinessAssessment {
  course_id: number
  course_slug: string
  question_count: number
  estimated_minutes: number
  questions: AssessmentQuestion[]
}

export interface AssessmentResult {
  assessment_id: number
  score: number
  correct_count: number
  question_count: number
  skill_results: Record<string, number>
  questions: Array<{ id: string; correct: boolean; explanation: string }>
  readiness: ReadinessReport
}

export interface Recommendation {
  course: CatalogCourse
  /** A code the client turns into a sentence in the reader's language. */
  reason_code: string
  params: Record<string, unknown>
  /** An English sentence, for a client that does not localise. */
  reason: string
  readiness?: ReadinessState | null
}

export interface Recommendations {
  continue_learning: Recommendation[]
  recommended_next: Recommendation[]
  build_foundations: Recommendation[]
  completed: Recommendation[]
  career_goal?: RoleRef | null
}

export interface TrackCourse {
  course: CatalogCourse
  track_role: CourseRole
  position: number
  stage?: StageRef | null
}

/** A career roadmap: a recommended, ordered set of canonical courses. */
export interface TrackDetail extends CareerGoal {
  courses: TrackCourse[]
}

export interface SkillLevels {
  levels: Record<string, SkillProficiency>
  skills: Array<{ skill: Skill; level: SkillProficiency }>
  programming_experience?: string | null
  ai_experience?: string | null
}

export type ProgrammingExperience = 'none' | 'basic' | 'comfortable' | 'professional'
export type AiExperience = 'none' | 'basics' | 'projects' | 'applications'

// ─── Course billing and access ─────────────────────────────────────────────

export interface CourseOffer {
  course_id: string
  price_amount: number
  currency: 'EGP'
  original_price_amount?: number | null
}

export type CourseAccessReason = 'admin' | 'pro' | 'free' | 'purchase' | 'admin_grant' | 'legacy_free' | 'purchase_required'

export interface CourseAccess {
  has_access: boolean
  reason: CourseAccessReason
  enrollment_id?: number | null
  free_lesson_count?: number
}

export interface CheckoutResponse {
  order_id: number
  reference_number?: string
  payment_url: string
  amount: number
  currency: 'EGP'
}

export interface BillingOrder {
  id: number
  course: { id: number; slug: string; title: string; title_ar?: string | null }
  amount: number
  currency: 'EGP'
  status: 'pending' | 'paid' | 'failed' | 'cancelled' | 'refunded'
  created_at: string
  paid_at?: string | null
}

export interface CourseEnrollment {
  id: number
  user_id: number
  course_id: string
  source: 'purchase' | 'admin_grant' | 'free' | 'legacy_free'
  status: 'active' | 'revoked' | 'expired'
  enrolled_at: string
  expires_at?: string | null
}

export interface MyCourse {
  course_id: number
  slug: string
  title: string
  title_ar?: string | null
  href?: string | null
  progress: number
  enrolled_at: string
  access_type: 'purchase' | 'admin_grant' | 'free' | 'legacy_free'
  /** Lifecycle, cached on the enrollment; `progress` is always live. */
  status?: LearningStatus
  started_at?: string | null
  completed_at?: string | null
  estimated_hours?: number | null
  module_count?: number
}

/** A course's role is contextual: it can differ between career goals. */
export type CourseRole = 'core' | 'supporting' | 'optional'

export interface CatalogCourseDetail extends CatalogCourse {
  assumes: Skill[]
  /** Required prerequisites: the ones a roadmap is ordered by. Never a gate. */
  prerequisites: Array<Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>>
  /** Advice only. */
  recommended_prerequisites?: Array<Pick<CatalogCourse, 'id' | 'slug' | 'title' | 'title_ar'>>
  learning_objectives: string[]
  learning_objectives_ar: string[]
  modules?: CourseModule[]
  projects?: CourseProject[]
  /** The roadmaps this course appears in: informational only. */
  roadmaps?: RoadmapMembership[]
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

// ─── Career track workflow ─────────────────────────────────────────────────
// The five fixed career tracks, each an ordered workflow over the canonical
// courses. Order, role, required-ness and section all come from the server
// (`course_roles`); nothing here is reconstructed on the client.

export type TrackSection =
  | 'foundations' | 'language-generative-ai' | 'application-production'
  | 'advanced-ai-systems' | 'specializations'

export type WorkflowStatus = 'completed' | 'in_progress' | 'next' | 'locked' | 'available'

export interface CourseRef {
  id: number
  slug: string
  title: string
  title_ar?: string | null
}

export interface TrackWorkflowCourse {
  course_id: number
  slug: string
  title: string
  title_ar?: string | null
  order: number
  role: CourseRole
  required: boolean
  section?: TrackSection | null
  status: WorkflowStatus
  progress_percent: number
  is_available: boolean
  estimated_hours: number
  module_count: number
  lesson_count: number
  prerequisites: CourseRef[]
}

export interface TrackWorkflow {
  career_goal: RoleRef
  courses: TrackWorkflowCourse[]
  required_total: number
  required_completed: number
  /** Completed required courses / total required courses. */
  progress_percent: number
  current?: CourseRef | null
  next?: CourseRef | null
  has_sections: boolean
}

export interface LearningProfile {
  level?: LevelRef | null
  career_goal?: RoleRef | null
  fields: FieldRef[]
  known_skills: Skill[]
  programming_experience?: ProgrammingExperience | null
  ai_experience?: AiExperience | null
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
  programming_experience?: ProgrammingExperience | null
  ai_experience?: AiExperience | null
}

export interface GeneratePathRequest {
  level: string
  career_goal: string
  fields: string[]
}

export interface CourseFilters {
  /** `level` and `difficulty` are one filter (the API accepts both names). */
  level?: string[]
  difficulty?: string[]
  /** A field of the catalogue's own taxonomy (NLP, computer vision ...); `category` is its alias. */
  field?: string[]
  category?: string[]
  career_goal?: string[]
  skill?: string[]
  q?: string
  available_only?: boolean
  /** Only canonical COURSE-001... curriculum; excludes legacy track lessons and frameworks. */
  curriculum_only?: boolean
  /** true: only my courses; false: only those I am not in. */
  enrolled?: boolean
}

/** A certificate as the API returns it, both for the signed-in learner's own list
 *  and for the public verification lookup (the same shape, by design: the public
 *  one shows nothing the certificate itself does not). */
export interface CertificateSummary {
  /** A UUID: the public identifier, and what the verification link carries. */
  certificate_id: string
  /** The career track the exam belonged to. */
  track_title: string
  /** The holder's name as their account has it. */
  user_name: string
  score: number
  issued_at: string
  /** False once revoked. The learner's own list only ever holds valid ones. */
  is_valid: boolean
  /** The exam it was earned in. Only on the learner's own list: the public lookup omits it. */
  exam_id?: number | null
}

// [code-cell]
export interface ExerciseFile {
  /** Storage identifier: saved drafts are keyed by it, so it never changes. */
  name: string
  content: string
  readOnly?: boolean
  /** What the tab shows when it differs from `name` (e.g. `train_model.py`). */
  label?: string
}

export interface TestResult {
  name: string
  passed: boolean
  message?: string
}

export type ExerciseExecutionStatus =
  | 'success' | 'syntax_error' | 'runtime_error' | 'timeout'
  | 'memory_limit' | 'forbidden_operation' | 'execution_error' | 'grading_error' | 'incomplete'

export interface ExerciseRunResult {
  status: ExerciseExecutionStatus
  stdout: string
  stderr: string
  execution_time_ms: number
}

export interface ExerciseFeedback {
  code: string
  message: string
  test_id?: string | null
  messages: { en?: string; ar?: string }
}

export interface GradeResult {
  status: ExerciseExecutionStatus | 'incorrect' | 'correct'
  passed: boolean
  stdout: string
  stderr: string
  execution_time_ms: number
  feedback: ExerciseFeedback
  tests_passed: number
  tests_total: number
  failed_test?: string | null
  attempt?: ExerciseAttemptState | null
}

/** The server's record of one learner on one code exercise; it decides
 *  whether the worked solution may be shown. */
export interface ExerciseAttemptState {
  failed_checks: number
  passed: boolean
  completed_independently: boolean
  solution_viewed: boolean
  solution_available: boolean
  checks_until_solution: number
}
// [/code-cell]
