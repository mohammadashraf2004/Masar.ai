import axios, { AxiosInstance, AxiosError } from 'axios'
import type {
  TokenResponse, User,
  CareerTrack, CareerTrackSummary, Enrollment,
  UserProgress, QuizAttempt, ProjectSubmission,
  MentorResponse, MentorSession, CodeReviewResult,
  SkillGapResult, InterviewQuestion, RoadmapWeek, SkillScore,
  ToolCourse, ToolCourseSummary, ToolEnrollment,
} from '@/types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class ApiClient {
  private http: AxiosInstance

  constructor() {
    this.http = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
    })

    // Attach JWT from localStorage on every request
    this.http.interceptors.request.use((config) => {
      if (typeof window !== 'undefined') {
        try {
          const raw = localStorage.getItem('auth-storage')
          if (raw) {
            const parsed = JSON.parse(raw)
            const token = parsed?.state?.token
            if (token) config.headers.Authorization = `Bearer ${token}`
          }
        } catch {}
      }
      return config
    })

    // Auto-logout on 401
    this.http.interceptors.response.use(
      (r) => r,
      (error: AxiosError) => {
        if (error.response?.status === 401 && typeof window !== 'undefined') {
          localStorage.removeItem('auth-storage')
          window.location.href = '/auth/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // ─── Auth ─────────────────────────────────────────────────────────────

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

  async verifyEmail(token: string) {
    const res = await this.http.post<{ message: string }>('/auth/verify-email', { token })
    return res.data
  }

  async resendVerification() {
    const res = await this.http.post<{ message: string }>('/auth/resend-verification')
    return res.data
  }

  async forgotPassword(email: string) {
    const res = await this.http.post<{ message: string }>('/auth/forgot-password', { email })
    return res.data
  }

  async resetPassword(token: string, new_password: string) {
    const res = await this.http.post<{ message: string }>('/auth/reset-password', { token, new_password })
    return res.data
  }

  async logoutAllDevices() {
    const res = await this.http.post<{ message: string }>('/auth/logout-all')
    return res.data
  }

  async deleteAccount() {
    const res = await this.http.delete<{ message: string }>('/auth/me')
    return res.data
  }

  // ─── Tracks ───────────────────────────────────────────────────────────

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

  // ─── Tool Courses ─────────────────────────────────────────────────────

  async listToolCourses() {
    const res = await this.http.get<ToolCourseSummary[]>('/tool-courses/')
    return res.data
  }

  async getToolCourse(slug: string) {
    const res = await this.http.get<ToolCourse>(`/tool-courses/${slug}`)
    return res.data
  }

  async enrollToolCourse(toolCourseId: number) {
    const res = await this.http.post<ToolEnrollment>('/tool-courses/enroll', {
      tool_course_id: toolCourseId,
    })
    return res.data
  }

  async getMyToolEnrollments() {
    const res = await this.http.get<ToolEnrollment[]>('/tool-courses/my-enrollments')
    return res.data
  }

  async updateToolTopicProgress(topicId: number, data: { lesson_id?: number; exercise_id?: number; time_spent_minutes?: number }) {
    const res = await this.http.post(`/tool-courses/topics/${topicId}/progress`, data)
    return res.data
  }

  async getToolTopicProgress(topicId: number) {
    const res = await this.http.get(`/tool-courses/topics/${topicId}/progress`)
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

  // ─── Mentor ───────────────────────────────────────────────────────────

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

  // ─── Exams ────────────────────────────────────────────────────────────

  async startExam(examId: number) {
    const res = await this.http.post(`/exams/${examId}/start`)
    return res.data
  }

  async reportViolation(attemptId: number, data: { violation_type: string; description: string }) {
    const res = await this.http.post(`/exams/attempts/${attemptId}/violation`, data)
    return res.data
  }

  async submitExam(attemptId: number, answers: { question_id: number; answer: any }[]) {
    const res = await this.http.post(`/exams/attempts/${attemptId}/submit`, { answers })
    return res.data
  }

    // ─── Exams ────────────────────────────────────────────────────────────

  async getExamsForTrack(trackId: number) {
    const res = await this.http.get(`/exams/track/${trackId}`)
    return res.data
  }

  async getMyAttempts() {
    const res = await this.http.get('/exams/my-attempts')
    return res.data
  }

  async getMyCertificates() {
    const res = await this.http.get('/exams/my-certificates')
    return res.data
  }
  async getScorecard(refresh = false) {
  const res = await this.http.get('/profile/scorecard', { params: { refresh } })
  return res.data
  }

  // ─── Wallet ───────────────────────────────────────────────────────────

  async getWallet() {
    const res = await this.http.get('/wallet/')
    return res.data
  }

  async getWalletTransactions(limit = 20) {
    const res = await this.http.get('/wallet/transactions', { params: { limit } })
    return res.data
  }

  async getWalletPackages() {
    const res = await this.http.get('/wallet/packages')
    return res.data
  }

  async getWalletCosts() {
    const res = await this.http.get('/wallet/costs')
    return res.data
  }

  async requestTopUp(data: { package_id: number; payment_method: string; payment_ref: string }) {
    const res = await this.http.post('/wallet/topup', data)
    return res.data
  }

  /** Starts a real Paymob checkout for a wallet top-up. Returns a
   * checkout_url to redirect the browser to (card iframe or wallet OTP
   * redirect) — credits are released by the server-side webhook once
   * Paymob confirms payment, not by this call. */
  async initWalletTopUp(data: { package_id: number; method: 'card' | 'wallet'; phone_number?: string }) {
    const res = await this.http.post('/payments/wallet/topup/init', data)
    return res.data as { checkout_url: string; merchant_order_id: string }
  }

 // ─── Challenges ───────────────────────────────────────────────────────

  async getChallenges() {
    const res = await this.http.get('/challenges/')
    return res.data
  }

  async getChallenge(slug: string) {
    const res = await this.http.get(`/challenges/${slug}`)
    return res.data
  }

  async enrollChallenge(slug: string) {
    const res = await this.http.post(`/challenges/${slug}/enroll`)
    return res.data
  }

  async submitChallengeAttempt(slug: string, data: {
    solution_code: string
    solution_notes?: string
    github_url?: string
  }) {
    const res = await this.http.post(`/challenges/${slug}/submit`, data)
    return res.data
  }

  async getChallengeAttempts(slug: string) {
    const res = await this.http.get(`/challenges/${slug}/attempts`)
    return res.data
  }

  async downloadChallengeDataset(slug: string) {
    const res = await this.http.get(`/challenges/${slug}/dataset/download`)
    return res.data
  }

  // ─── Exam Payments ────────────────────────────────────────────────────

  async getExamPaymentPrice() {
    const res = await this.http.get('/exam-payments/price')
    return res.data
  }

  async getExamPaymentStatus(examId: number) {
    const res = await this.http.get(`/exam-payments/status/${examId}`)
    return res.data
  }

  async submitExamPayment(data: {
    exam_id: number
    payment_method: string
    payment_ref: string
  }) {
    const res = await this.http.post('/exam-payments/submit', data)
    return res.data
  }

  /** Starts a real Paymob checkout for an exam fee. See initWalletTopUp
   * for the confirmation model — the webhook is authoritative, not this
   * call's response. */
  async initExamPayment(data: { exam_id: number; method: 'card' | 'wallet'; phone_number?: string }) {
    const res = await this.http.post('/payments/exam/init', data)
    return res.data as { checkout_url: string; merchant_order_id: string }
  }

  /** Polled by the /payments/result page after a Paymob checkout redirect
   * — only ever reflects what the server-side webhook has confirmed. */
  async getPaymentStatus(merchantOrderId: string) {
    const res = await this.http.get(`/payments/status/${merchantOrderId}`)
    return res.data as { kind: 'wallet_topup' | 'exam_payment'; status: 'pending' | 'confirmed' | 'failed' }
  }

  async getChallengeHint(slug: string, data: { stuck_on: string; previous_hints: string[] }) {
    const res = await this.http.post(`/challenges/${slug}/hint`, data)
    return res.data
  }
}

export const api = new ApiClient()
