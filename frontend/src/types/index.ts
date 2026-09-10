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
