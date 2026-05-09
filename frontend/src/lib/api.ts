import axios, { AxiosInstance, AxiosError } from 'axios'
import type {
  TokenResponse, User,
  CareerTrack, CareerTrackSummary, Enrollment,
  UserProgress, QuizAttempt, ProjectSubmission,
  MentorResponse, MentorSession, CodeReviewResult,
  SkillGapResult, InterviewQuestion, RoadmapWeek, SkillScore,
} from '@/types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  private http: AxiosInstance

  constructor() {
    this.http = axios.create({ baseURL: BASE_URL })

    // Attach JWT to every request
    this.http.interceptors.request.use((config) => {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token')
        if (token) config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Auto-logout on 401
    this.http.interceptors.response.use(
      (r) => r,
      (error: AxiosError) => {
        if (error.response?.status === 401 && typeof window !== 'undefined') {
          localStorage.removeItem('token')
          window.location.href = '/auth/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // ─── Auth ──────────────────────────────────────────────────────────────────

  async register(data: { email: string; full_name: string; password: string; experience_level: string }) {
    const res = await this.http.post<TokenResponse>('/auth/register', data)
    return res.data
  }

  async login(email: string, password: string) {
    const res = await this.http.post<TokenResponse>('/auth/login', { email, password })
    return res.data
  }

  async getMe() {
    const res = await this.http.get<User>('/auth/me')
    return res.data
  }

  async updateMe(data: Partial<Pick<User, 'full_name' | 'bio' | 'github_url' | 'linkedin_url' | 'experience_level'>>) {
    const res = await this.http.patch<User>('/auth/me', data)
    return res.data
  }

  // ─── Tracks ────────────────────────────────────────────────────────────────

  async listTracks() {
    const res = await this.http.get<CareerTrackSummary[]>('/tracks/')
    return res.data
  }

  async getTrack(slug: string) {
    const res = await this.http.get<CareerTrack>(`/tracks/${slug}`)
    return res.data
  }

  async enroll(trackId: number, targetJobTitle?: string) {
    const res = await this.http.post<Enrollment>('/tracks/enroll', {
      track_id: trackId,
      target_job_title: targetJobTitle,
    })
    return res.data
  }

  async getMyEnrollments() {
    const res = await this.http.get<Enrollment[]>('/tracks/my-enrollments')
    return res.data
  }

  async updateProgress(topicId: number, data: { lesson_id?: number; exercise_id?: number; time_spent_minutes?: number }) {
    const res = await this.http.post<UserProgress>(`/tracks/topics/${topicId}/progress`, data)
    return res.data
  }

  async getTopicProgress(topicId: number) {
    const res = await this.http.get<UserProgress>(`/tracks/topics/${topicId}/progress`)
    return res.data
  }

  async submitQuiz(quizId: number, answers: Record<string, number>) {
    const res = await this.http.post<QuizAttempt>(`/tracks/quizzes/${quizId}/submit`, { answers })
    return res.data
  }

  async submitProject(projectId: number, data: { github_url?: string; description?: string }) {
    const res = await this.http.post<ProjectSubmission>(`/tracks/projects/${projectId}/submit`, data)
    return res.data
  }

  // ─── Mentor ────────────────────────────────────────────────────────────────

  async chat(content: string, topicId?: number) {
    const res = await this.http.post<MentorResponse>('/mentor/chat', { content, topic_id: topicId })
    return res.data
  }

  async newMentorSession() {
    const res = await this.http.post<MentorSession>('/mentor/new-session')
    return res.data
  }

  async getMentorSessions() {
    const res = await this.http.get<MentorSession[]>('/mentor/sessions')
    return res.data
  }

  async getMentorSession(id: number) {
    const res = await this.http.get<MentorSession>(`/mentor/sessions/${id}`)
    return res.data
  }

  async reviewCode(code: string, language: string, context?: string) {
    const res = await this.http.post<CodeReviewResult>('/mentor/code-review', { code, language, context })
    return res.data
  }

  async analyzeSkillGap(data: { target_role: string; current_skills: string[]; cv_text?: string; github_url?: string }) {
    const res = await this.http.post<SkillGapResult>('/mentor/skill-gap', data)
    return res.data
  }

  async getMockInterviewQuestion(topic: string, difficulty: string, previousQa: Array<{ question: string; answer: string }> = []) {
    const res = await this.http.post<InterviewQuestion>('/mentor/mock-interview', {
      topic, difficulty, previous_qa: previousQa,
    })
    return res.data
  }

  async getRoadmap(track?: string) {
    const res = await this.http.get<{ track: string; weeks: RoadmapWeek[] }>('/mentor/roadmap', {
      params: { track },
    })
    return res.data
  }

  async getSkillScores() {
    const res = await this.http.get<{ readiness_score: number; skills: SkillScore[] }>('/mentor/skill-scores')
    return res.data
  }
}

export const api = new ApiClient()
