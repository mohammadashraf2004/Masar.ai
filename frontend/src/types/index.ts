// ─── Auth ────────────────────────────────────────────────────────────────────

export interface User {
  id: number
  email: string
  full_name: string
  role: 'student' | 'mentor' | 'admin'
  experience_level: 'beginner' | 'intermediate' | 'advanced'
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
  user: User
}

// ─── Learning ────────────────────────────────────────────────────────────────

export type Difficulty = 'beginner' | 'intermediate' | 'advanced'

export interface Lesson {
  id: number
  title: string
  content: string
  order: number
  estimated_minutes: number
  has_code_examples: boolean
}

export interface Exercise {
  id: number
  title: string
  description: string
  starter_code?: string
  difficulty: Difficulty
  skill_tested: string[]
}

export interface Project {
  id: number
  title: string
  description: string
  difficulty: Difficulty
  tech_stack: string[]
  objectives: string[]
  rubric: Record<string, number>
  starter_repo_url?: string
  estimated_hours: number
}

export interface QuizQuestion {
  question: string
  options: string[]
  correct: number
  explanation: string
}

export interface Quiz {
  id: number
  title: string
  questions: QuizQuestion[]
  passing_score: number
}

export interface Topic {
  id: number
  title: string
  slug: string
  description?: string
  order: number
  difficulty: Difficulty
  estimated_hours: number
  prerequisite_ids: number[]
  skill_tags: string[]
  lessons: Lesson[]
  exercises: Exercise[]
  projects: Project[]
}

export interface TrackLevel {
  id: number
  title: string
  description?: string
  order: number
  topics: Topic[]
}

export interface CareerTrack {
  id: number
  slug: string
  title: string
  description?: string
  icon?: string
  estimated_weeks: number
  levels: TrackLevel[]
}

export interface CareerTrackSummary {
  id: number
  slug: string
  title: string
  description?: string
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
  feedback: Record<string, { correct: boolean; your_answer: number; correct_answer: number; explanation: string }>
  attempted_at: string
}

export interface ProjectSubmission {
  id: number
  project_id: number
  github_url?: string
  description?: string
  ai_review?: CodeReviewResult
  score?: number
  submitted_at: string
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
