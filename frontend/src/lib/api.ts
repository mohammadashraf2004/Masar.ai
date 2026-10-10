import axios, { AxiosInstance, AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios'
import type {
  TokenResponse, User,
  CareerTrack, CareerTrackSummary, Enrollment,
  UserProgress, QuizAttempt, ProjectSubmission,
  MentorResponse, MentorSession, CodeReviewResult,
  SkillGapResult, InterviewQuestion, RoadmapWeek, SkillScore,
  ToolCourse, ToolCourseSummary, ToolEnrollment,
  AnswerSubmission,
  TerminologyDictionary, VocabularyProgress, TerminologyLintResult,
  VocabularyListResponse, VocabularyTermDetail,
  SearchResults, LanguagePrefs,
  AdminAnalyticsOverview, AdminUserLookup, AdminGrantResult,
  ProjectHint,
  LearningLevel, LearningField, CareerGoal, CatalogCourse, CatalogCourseDetail,
  PathSummary, LearningPath, LearningProfile, LearningProfileUpdate, LearningProgress, TrackWorkflow,
  GeneratePathRequest, CourseFilters, SkillOption, SkillOptionsQuery, MySkills, SkillsSaved, SkillGaps,
  LegalDocument, CertificateSummary,
  BillingOrder, CheckoutResponse, CourseAccess, CourseOffer, MyCourse,
  ToolTopic, EnrollResult, CourseLearningEnrollment, CourseProgress, ReadinessReport, ReadinessAssessment,
  AssessmentResult, Recommendations, TrackDetail, SkillLevels,
} from '@/types'
import { useAuthStore } from '@/lib/store'
import { authHref, currentPath } from '@/lib/authRedirect'
import { useLanguageStore } from '@/lib/language'
import type { BillingCycle, CreditPack, Offer, PlanId, RefundPolicySummary, RefundStatus, SubscriptionOrder } from '@/lib/billing/types'
import { mentorV2EndpointLive, mentorV2Live } from '@/features/mentor/flag'

export interface AiAllowance {
  limit: number
  window_seconds: number
  used: number
  remaining: number
  /** When the next credit leaves the rolling window; null while credits remain. */
  next_credit_available_at: string | null
}

export interface AiAllowanceResponse {
  plan: PlanId
  ai_allowance: AiAllowance | null
  all_courses_access: boolean
  /** Where AI actions are paid from now: the included allowance (paid Pro) or the wallet
   *  (Free, and the trial until its first payment). */
  ai_billing: 'allowance' | 'wallet'
  trial: boolean
}

/** The wallet as the server reports it. `purchased_credits` were bought (they never expire);
 *  `included_credits` is the rest of the balance (signup and promo credits). */
export interface WalletInfo {
  credit_balance: number
  lifetime_purchased?: number
  lifetime_spent?: number
  promo_credits_remaining?: number
  promo_expires_at?: string | null
  purchased_credits?: number
  included_credits?: number
}

export type CreditPurchaseStatus =
  | 'pending' | 'expired' | 'failed' | 'paid' | 'partially_refunded' | 'refunded' | 'chargeback'

export interface CreditPurchase {
  reference: string
  package: string | null
  package_code: string | null
  credits: number
  price: number | null
  currency: string
  status: CreditPurchaseStatus
  credits_reversed: number
  created_at: string | null
  paid_at: string | null
}

export interface BillingCatalogApi {
  currency: string
  vat_rate: number
  prices_include_vat: boolean
  current_plan: PlanId
  trial_eligible?: boolean
  plans: Array<{
    id: PlanId
    monthly: number
    yearly: number
    signup_credits: number
    features: Array<`billing.plan.${string}`>
    popular?: boolean
  }>
  packs: CreditPack[]
  offer: Offer | null
  refund_policy?: RefundPolicySummary
}

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
/** Longer than the API worker's 60 s limit (gunicorn --timeout 60), so the browser never gives up on a send the server is still answering. */
export const MENTOR_MESSAGE_TIMEOUT_MS = 65_000
/** How long a paid AI request keeps asking about the same request id while its first attempt runs. */
export const AI_REQUEST_PATIENCE_MS = 70_000

/** A walkthrough record as the wire has it (docs/backend-requests.md §6); the tours feature
 *  translates this into its own local shape (frontend/src/features/tours/sync.ts). */
export interface TourRecordApi {
  tour_id: string
  status: 'completed' | 'skipped' | 'in_progress'
  version: number
  at: string
}

/**
 * The address the browser loads a lesson figure from. The API hands out a path
 * relative to its own root (or, once figures are served from a CDN, a full URL);
 * this is the only place that turns the former into something an <img> can load,
 * so where figures live is a backend decision, not something a component knows.
 */
export function resolveAssetUrl(url: string): string {
  return /^https?:\/\//i.test(url) ? url : `${BASE_URL.replace(/\/+$/, '')}${url.startsWith('/') ? '' : '/'}${url}`
}

/**
 * Drop a dead session from BOTH places it lives.
 *
 * lib/store.ts holds the token in memory (zustand) and mirrors it to
 * localStorage (persist). Removing only the localStorage key — which is
 * all the two interceptors below used to do — left the store still
 * holding `token` and `user`: every component reading the store went on
 * rendering a logged-in UI, the next request went out unauthenticated,
 * and persist wrote the stale entry back to storage on the store's next
 * set(). `clearAuth` is the store's own action, so there is exactly one
 * source of auth truth and this is not a second one.
 *
 * Deliberately does not navigate: each caller below decides that, because
 * the rules differ (a request-time expiry lets the 401 handler deal with
 * it; the 401 handler skips the redirect when already on /auth/* so it
 * cannot loop).
 *
 * `useAuthStore` and this module import each other — store.ts needs `api`
 * for refreshUser(). That is fine: the reference is resolved when this
 * function runs, long after both modules have finished evaluating, never
 * at import time.
 */
/** A request config that knows whether it went out under a session. */
type SessionConfig = InternalAxiosRequestConfig & { _hadSession?: boolean }

function clearDeadSession() {
  if (typeof window === 'undefined') return
  try {
    useAuthStore.getState().clearAuth()
  } catch {
    // Last-ditch: if the store is somehow unavailable, at least do not
    // leave the credential sitting in storage.
    try {
      localStorage.removeItem('auth-storage')
    } catch {}
  }
}

class ApiClient {
  private http: AxiosInstance

  /**
   * POST a paid AI request that carries a client request id. The server charges and answers each
   * id once (backend app/services/mentor/idempotency.py). While the first attempt of an id is still
   * running - a retry after a timeout or a dropped connection - it answers 409
   * `request_in_progress`; this waits the time it asks for and asks again with the same id, never
   * a second charge, until the stored answer comes back or AI_REQUEST_PATIENCE_MS runs out.
   */
  private async postAiOnce<T>(url: string, body: unknown, config?: AxiosRequestConfig): Promise<T> {
    const started = Date.now()
    for (;;) {
      try {
        return (await this.http.post<T>(url, body, config)).data
      } catch (error) {
        const resp = (error as { response?: { status?: number; data?: { detail?: { error?: unknown; retry_after?: unknown } } } }).response
        const detail = resp?.data?.detail
        if (resp?.status !== 409 || typeof detail !== 'object' || detail === null || detail.error !== 'request_in_progress') throw error
        const wait = Math.min(10, Math.max(1, Number(detail.retry_after) || 3)) * 1000
        if (Date.now() - started + wait > AI_REQUEST_PATIENCE_MS) throw error
        await new Promise((resolve) => setTimeout(resolve, wait))
      }
    }
  }

  constructor() {
    this.http = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
    })

    // Attach the JWT on every request — but never one we already know
    // has expired: sending it just leaks a still-valid-looking credential
    // to the wire for a request that is going to 401 anyway.
    this.http.interceptors.request.use((config) => {
      if (typeof window !== 'undefined') {
        try {
          const raw = localStorage.getItem('auth-storage')
          if (raw) {
            const parsed = JSON.parse(raw)
            const token = parsed?.state?.token
            const expiresAt = parsed?.state?.expiresAt
            // Remembered for the 401 handler: only a request made under a
            // session can mean "your session ended".
            if (token) (config as SessionConfig)._hadSession = true
            if (expiresAt && Date.now() >= expiresAt) {
              // Clears the store as well as storage, so the UI drops to
              // its logged-out state now rather than after the 401 comes
              // back. No redirect from here: this runs mid-flight, and the
              // 401 handler below owns that decision.
              clearDeadSession()
            } else if (token) {
              config.headers.Authorization = `Bearer ${token}`
            }
          }
        } catch {}
      }
      return config
    })

    // Auto-logout on 401. A 401 means the server rejected this token —
    // expired, revoked (token_version bumped by a password reset or
    // "log out everywhere"), or the account was deleted. In every case
    // the right move is to drop it locally rather than keep retrying.
    this.http.interceptors.response.use(
      (r) => r,
      (error: AxiosError) => {
        // A 401 for a visitor who never signed in is just "this needs an
        // account": the public pages they browse skip those calls, and the
        // page that made one handles the refusal (or its guard sends them to
        // sign in). Bouncing them to the login page from a catalogue page would
        // make browsing without an account impossible.
        const hadSession = !!(error.config as SessionConfig | undefined)?._hadSession
        if (error.response?.status === 401 && typeof window !== 'undefined' && hadSession) {
          clearDeadSession()
          // Already on an auth screen: clearing is enough, and navigating
          // to the login page from the login page is how a redirect loop
          // starts.
          if (!window.location.pathname.startsWith('/auth/')) {
            // A full navigation on purpose: this runs outside React (no router
            // to call) and the reload is what drops every piece of in-memory
            // session state along with the dead token. `next` brings them back
            // here after signing in again.
            window.location.href = authHref('login', currentPath())
          }
        }
        return Promise.reject(error)
      }
    )
  }

  // ─── Auth ─────────────────────────────────────────────────────────────

  /** `accept_terms` / `accept_privacy` are the learner's agreement only. Which
   *  version of each document that means is decided by the server. */
  async register(data: {
    email: string
    full_name: string
    password: string
    experience_level?: string
    accept_terms: boolean
    accept_privacy: boolean
  }) {
    const res = await this.http.post<TokenResponse>('/auth/register', data)
    return res.data
  }

  /** Accept the Terms and Privacy Policy as currently published. */
  async acceptLegal() {
    const res = await this.http.post<User>('/auth/accept-legal', { accept_terms: true, accept_privacy: true })
    return res.data
  }

  async getLegalDocument(kind: 'terms' | 'privacy' | 'refund', lang: 'en' | 'ar') {
    const res = await this.http.get<LegalDocument>(`/legal/${kind}`, { params: { lang } })
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

  /** Every walkthrough record the account has (see docs/backend-requests.md §6) — one call,
   *  not one per tour. */
  async getMyTours() {
    const res = await this.http.get<TourRecordApi[]>('/auth/me/tours')
    return res.data
  }

  /** Upsert one tour's record. `at` is when the status became true on the client, not the
   *  request's arrival time — see app.services.tour_service.upsert. */
  async putTour(tourId: string, data: { status: 'completed' | 'skipped'; version: number; at?: string }) {
    const res = await this.http.put<TourRecordApi>(`/auth/me/tours/${encodeURIComponent(tourId)}`, data)
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

  // ─── Answer Evaluation (conversational exercise/quiz grading) ─────────

  /** The grader is a tutor too, so it takes the same language settings as
   *  the mentor and answers under the same policy. */
  async answerExercise(exerciseId: number, content: string, prefs?: LanguagePrefs) {
    const res = await this.http.post<AnswerSubmission>(`/practice/exercises/${exerciseId}/answer`, {
      content,
      language: prefs?.language,
      terminology_mode: prefs?.terminology_mode,
    })
    return res.data
  }

  async getExerciseAnswer(exerciseId: number) {
    const res = await this.http.get<AnswerSubmission>(`/practice/exercises/${exerciseId}/answer`)
    return res.data
  }

  /** One good answer to a written exercise; the server opens it after the
   *  learner's first evaluated answer. */
  async getExerciseExample(exerciseId: number) {
    const res = await this.http.get<{ example_answer: string; example_answer_ar?: string | null }>(
      `/practice/exercises/${exerciseId}/example`,
    )
    return res.data
  }

  async answerQuizQuestion(
    quizId: number,
    questionIndex: number,
    content: string,
    prefs?: LanguagePrefs
  ) {
    const res = await this.http.post<AnswerSubmission>(
      `/practice/quizzes/${quizId}/questions/${questionIndex}/answer`,
      { content, language: prefs?.language, terminology_mode: prefs?.terminology_mode }
    )
    return res.data
  }

  async getQuizQuestionAnswer(quizId: number, questionIndex: number) {
    const res = await this.http.get<AnswerSubmission>(
      `/practice/quizzes/${quizId}/questions/${questionIndex}/answer`
    )
    return res.data
  }

  async submitQuiz(quizId: number, answers: Record<string, number>) {
    const res = await this.http.post<QuizAttempt>(`/tracks/quizzes/${quizId}/submit`, { answers })
    return res.data
  }

  async getQuizAttempts(quizId: number) {
    const res = await this.http.get<QuizAttempt[]>(`/tracks/quizzes/${quizId}/attempts`)
    return res.data
  }

  /** A project is submitted as code written in the reader's code cell.
   *  `description` is optional notes on the approach — context for the
   *  reviewer, not the thing reviewed. There is no repo URL: nothing ever
   *  fetched one. */
  async submitProject(projectId: number, data: { code: string; description?: string }) {
    const res = await this.http.post<ProjectSubmission>(`/tracks/projects/${projectId}/submit`, data)
    return res.data
  }

  /** A Socratic hint for a project. Costs 1 credit, so it throws the same
   *  402 `insufficient_credits` payload the challenge hint does. */
  async getProjectHint(
    projectId: number,
    data: { stuck_on: string; code?: string; previous_hints: string[] } & Partial<LanguagePrefs>
  ) {
    const res = await this.http.post<ProjectHint>(`/tracks/projects/${projectId}/hint`, data)
    return res.data
  }

  // ─── Mentor ───────────────────────────────────────────────────────────

  /** `prefs` carries the reader's language settings so the mentor answers
   *  the way their lessons are written — Arabic explanation, English
   *  terminology, untouched code. Omitted, the API applies the
   *  Arabic-first default. */
  async chat(content: string, topicId?: number, prefs?: LanguagePrefs) {
    const res = await this.http.post<MentorResponse>('/mentor/chat', {
      content,
      topic_id: topicId,
      language: prefs?.language,
      terminology_mode: prefs?.terminology_mode,
    })
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

  /** `requestId` names this review: a retry of it with the same id is answered and charged once. */
  async reviewCode(code: string, language: string, context?: string, uiLanguage?: 'ar' | 'en', exerciseId?: string, requestId?: string) {
    return this.postAiOnce<CodeReviewResult>('/mentor/code-review', {
      code, language, context, ui_language: uiLanguage, exercise_id: exerciseId ? Number(exerciseId) : undefined,
      ...(requestId ? { request_id: requestId } : {}),
    })
  }

  async analyzeSkillGap(data: { target_role: string; current_skills: string[]; cv_text?: string; github_url?: string }) {
    const res = await this.http.post<SkillGapResult>('/mentor/skill-gap', data)
    return res.data
  }

  /**
   * `language` is the interview's language; the server adds what the learner has studied itself.
   * `requestId` names the interview turn: asking again for the same turn returns the same question
   * and is charged once.
   */
  async getMockInterviewQuestion(topic: string, difficulty: string, previousQa: Array<{ question: string; answer: string }> = [], language?: 'ar' | 'en', requestId?: string) {
    return this.postAiOnce<InterviewQuestion>('/mentor/mock-interview', {
      topic, difficulty, previous_qa: previousQa, ...(language ? { language } : {}), ...(requestId ? { request_id: requestId } : {}),
    })
  }

  async getRoadmap(track?: string, language?: 'ar' | 'en') {
    const res = await this.http.get<{ track: string; weeks: RoadmapWeek[] }>('/mentor/roadmap', {
      params: { track, language },
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

  async getMyCertificates(): Promise<CertificateSummary[]> {
    const res = await this.http.get('/exams/my-certificates')
    return res.data
  }

  /** Public: anyone holding the link can check a certificate. No account needed. */
  async verifyCertificate(certificateId: string): Promise<CertificateSummary> {
    const res = await this.http.get(`/exams/certificates/${encodeURIComponent(certificateId)}`)
    return res.data
  }
  async getScorecard(refresh = false) {
  const res = await this.http.get('/profile/scorecard', { params: { refresh } })
  return res.data
  }

  /** Days are bucketed in the browser's own timezone. */
  async getProfileActivity(days = 84) {
    const res = await this.http.get<import('@/types').ProfileActivity>('/profile/activity', {
      params: { days, tz_offset_minutes: new Date().getTimezoneOffset() },
    })
    return res.data
  }

  // ─── Wallet ───────────────────────────────────────────────────────────

  async getWallet() {
    const res = await this.http.get<WalletInfo>('/wallet/')
    return res.data
  }

  /** The learner's credit purchases and where each stands. Server-recorded state only. */
  async getCreditPurchases(limit = 30) {
    const res = await this.http.get<{ orders: CreditPurchase[] }>('/wallet/purchases', { params: { limit } })
    return res.data.orders
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

  /** Starts a Kashier checkout for a wallet top-up. Returns a checkout_url
   * (Kashier's hosted page, which offers card and mobile wallet) to redirect
   * the browser to — credits are released by the server-side webhook once
   * Kashier confirms payment, not by this call. */
  async initWalletTopUp(data: { package_id: number; method: 'card' | 'wallet'; phone_number?: string }) {
    const res = await this.http.post('/payments/wallet/topup/init', data)
    return res.data as { checkout_url: string; merchant_order_id: string; reference: string }
  }

 // ─── Challenges ───────────────────────────────────────────────────────

  async getChallenges() {
    const res = await this.http.get('/challenges/')
    return res.data
  }

  /** The public challenge catalogue: the cards only, for anyone signed in or not. */
  async getPublicChallenges() {
    const res = await this.http.get('/challenges/catalog')
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

  /** Starts a Kashier checkout for an exam fee. See initWalletTopUp
   * for the confirmation model — the webhook is authoritative, not this
   * call's response. */
  async initExamPayment(data: { exam_id: number; method: 'card' | 'wallet'; phone_number?: string }) {
    const res = await this.http.post('/payments/exam/init', data)
    return res.data as { checkout_url: string; merchant_order_id: string }
  }

  /** Polled by the /payments/result page after a checkout redirect
   * — only ever reflects what the server-side webhook has confirmed. */
  async getPaymentStatus(merchantOrderId: string) {
    const res = await this.http.get(`/payments/status/${merchantOrderId}`)
    return res.data as {
      kind: 'wallet_topup' | 'exam_payment'
      status: 'pending' | 'confirmed' | 'failed'
      /** For a credit purchase: its learner-facing state and the credits it added. */
      order?: CreditPurchase | null
    }
  }

  async getChallengeHint(
    slug: string,
    data: { stuck_on: string; previous_hints: string[] } & Partial<LanguagePrefs>
  ) {
    const res = await this.http.post(`/challenges/${slug}/hint`, data)
    return res.data
  }

  // ─── Terminology & vocabulary ─────────────────────────────────────────

  /** The dictionary as the server has it. The client ships its own copy
   *  (src/content/terminology) and renders from that; this endpoint exists
   *  so tooling and non-web clients read the same source. */
  async getTerminology() {
    const res = await this.http.get<TerminologyDictionary>('/terminology/')
    return res.data
  }

  async getVocabularyProgress() {
    const res = await this.http.get<VocabularyProgress>('/terminology/progress')
    return res.data
  }

  /** Record terms as met while reading, or proven. Batched by the caller —
   *  see lib/vocabulary.ts. */
  async recordVocabulary(termIds: string[], status: 'encountered' | 'learned') {
    const res = await this.http.post<VocabularyProgress>('/terminology/progress', {
      term_ids: termIds,
      status,
    })
    return res.data
  }

  /** Advisory content check for course authors: flags Arabic glosses used
   *  without ever introducing the English industry term. */
  async lintContent(text: string) {
    const res = await this.http.post<TerminologyLintResult>('/terminology/lint', { text })
    return res.data
  }

  // ─── AI Vocabulary (normalized dictionary, migration 022) ─────────────

  /** The AI Vocabulary list: one canonical row per concept, with course
   *  counts and progress computed server-side. */
  async listVocabularyTerms(params: {
    search?: string
    course_id?: string
    category?: string
    difficulty?: string
    status?: 'new' | 'learning' | 'mastered'
    page?: number
    page_size?: number
  } = {}) {
    const res = await this.http.get<VocabularyListResponse>('/vocabulary/', { params })
    return res.data
  }

  async getVocabularyTerm(slug: string) {
    const res = await this.http.get<VocabularyTermDetail>(`/vocabulary/${slug}`)
    return res.data
  }

  async getVocabularyCategories() {
    const res = await this.http.get<{ categories: string[]; counts: { category: string; term_count: number }[] }>(
      '/vocabulary/categories'
    )
    return res.data
  }

  async getVocabularyCourseCounts() {
    const res = await this.http.get<{
      courses: {
        course_key: string
        term_count: number
        course_title?: string | null
        course_slug?: string | null
        course_href?: string | null
      }[]
    }>('/vocabulary/courses')
    return res.data.courses
  }

  async recordVocabularyTermProgress(slug: string, status: 'learning' | 'mastered') {
    const res = await this.http.post<VocabularyTermDetail>(`/vocabulary/${slug}/progress`, { status })
    return res.data
  }

  // ─── Search ───────────────────────────────────────────────────────────

  /** Bilingual: "Embeddings", "embedding" and "التضمينات" all return the
   *  same courses — the query is expanded through the terminology
   *  dictionary server-side. */
  async search(query: string) {
    const res = await this.http.get<SearchResults>('/search/', { params: { q: query } })
    return res.data
  }

  // ─── Learning paths ───────────────────────────────────────────────────
  // Level -> field(s) -> career goal -> path. Every rule about what a path
  // contains lives on the server; these methods only carry the answers.

  async getLearningLevels() {
    const res = await this.http.get<LearningLevel[]>('/learning/levels')
    return res.data
  }

  async getLearningFields() {
    const res = await this.http.get<LearningField[]>('/learning/fields')
    return res.data
  }

  async getCareerGoals() {
    const res = await this.http.get<CareerGoal[]>('/learning/career-goals')
    return res.data
  }

  /** Filters combine: any-of within a dimension, all-of across them. Arrays
   *  go out as repeated keys (`field=nlp&field=speech`), which is what the API
   *  reads — axios' default `field[]=` would be ignored. */
  async listCatalogCourses(filters: CourseFilters = {}) {
    const res = await this.http.get<CatalogCourse[]>('/learning/courses', {
      params: {
        level: filters.level,
        difficulty: filters.difficulty,
        field: filters.field,
        category: filters.category,
        career_goal: filters.career_goal,
        skill: filters.skill,
        q: filters.q || undefined,
        available_only: filters.available_only || undefined,
        curriculum_only: filters.curriculum_only || undefined,
        enrolled: filters.enrolled,
      },
      paramsSerializer: { indexes: null },
    })
    return res.data
  }

  async getCatalogCourse(slug: string) {
    const res = await this.http.get<CatalogCourseDetail>(`/learning/courses/${slug}`)
    return res.data
  }

  async listLearningPaths() {
    const res = await this.http.get<PathSummary[]>('/learning/paths')
    return res.data
  }

  async getLearningPath(slug: string, level?: string) {
    const res = await this.http.get<LearningPath>(`/learning/paths/${slug}`, { params: { level } })
    return res.data
  }

  /** One of the five fixed career tracks, as an ordered workflow over the
   *  canonical courses. Public; a signed-in learner also gets real completion
   *  state, so a shared course reads as completed in every track it is in. */
  async getTrackWorkflow(goal: string) {
    const res = await this.http.get<TrackWorkflow>(`/learning/tracks/${goal}/workflow`)
    return res.data
  }

  /** A what-if: generated for the caller (their progress applied) and not saved. */
  async generateLearningPath(data: GeneratePathRequest) {
    const res = await this.http.post<LearningPath>('/learning/paths/generate', data)
    return res.data
  }

  async getMyLearningProfile() {
    const res = await this.http.get<LearningProfile>('/learning/my-profile')
    return res.data
  }

  /** Keys that are present replace that part of the profile; absent keys are
   *  left alone (and `null` clears level / career goal). */
  async saveMyLearningProfile(data: LearningProfileUpdate) {
    const res = await this.http.put<LearningProfile>('/learning/my-profile', data)
    return res.data
  }

  /** Resolves null (not a throw) when the learner has no path yet, so callers
   *  branch on the value instead of catching a 404. */
  async getMyLearningPath() {
    try {
      const res = await this.http.get<LearningPath>('/learning/my-path')
      return res.data
    } catch (err) {
      if ((err as AxiosError).response?.status === 404) return null
      throw err
    }
  }

  /** Rebuild the path from the saved profile ("Build My Masar"), or change its
   *  status. See PathUpdate in backend/app/views/learning_path.py. */
  async saveMyLearningPath(data: {
    regenerate?: boolean
    status?: 'active' | 'paused' | 'archived'
    waived_course_ids?: number[]
  } = {}) {
    const res = await this.http.put<LearningPath>('/learning/my-path', data)
    return res.data
  }

  /** The skills worth asking about for a goal, route and level. Arrays go out
   *  as repeated keys, like the course filters. */
  async getSkillOptions(query: SkillOptionsQuery) {
    const res = await this.http.get<SkillOption[]>('/learning/skills', {
      params: { career_goal: query.career_goal, level: query.level || undefined, field: query.field },
      paramsSerializer: { indexes: null },
    })
    return res.data
  }

  async getMySkills() {
    const res = await this.http.get<MySkills>('/learning/my-skills')
    return res.data
  }

  /** Replace the self-declared skills and rebuild the roadmap around them. */
  async saveMySkills(skills: string[]) {
    const res = await this.http.put<SkillsSaved>('/learning/my-skills', { skills })
    return res.data
  }

  /** What the learner still lacks for their own roadmap, decided by the backend. */
  async getMySkillGaps() {
    const res = await this.http.get<SkillGaps>('/learning/my-skill-gaps')
    return res.data
  }

  async getMyLearningProgress() {
    const res = await this.http.get<LearningProgress>('/learning/my-progress')
    return res.data
  }

  // ─── Course billing and ownership ────────────────────────────────────

  async getCourseOffer(courseId: string) {
    const res = await this.http.get<CourseOffer>(`/billing/courses/${courseId}/offer`)
    return res.data
  }

  // ─── Independent course enrollment, readiness, recommendations ───────

  /** Enroll in a course - no track, goal or path needed. Idempotent. A learner who
   *  is not yet ready is never refused: the answer says what to review first. */
  async enrollInCourse(slug: string) {
    const res = await this.http.post<EnrollResult>(`/learning/courses/${slug}/enroll`)
    return res.data
  }

  async setCoursePaused(slug: string, paused: boolean) {
    const res = await this.http.patch<CourseLearningEnrollment>(`/learning/courses/${slug}/enrollment`, {
      status: paused ? 'paused' : 'active',
    })
    return res.data
  }

  async getCourseProgress(slug: string) {
    const res = await this.http.get<CourseProgress>(`/learning/courses/${slug}/progress`)
    return res.data
  }

  async getCourseReadiness(slug: string) {
    const res = await this.http.get<ReadinessReport>(`/learning/courses/${slug}/readiness`)
    return res.data
  }

  /** The questions of the short check: no answer key is ever sent. */
  async getReadinessAssessment(slug: string) {
    const res = await this.http.get<ReadinessAssessment>(`/learning/courses/${slug}/readiness-assessment`)
    return res.data
  }

  /** Answers only (question id -> chosen option index). The score is computed on the server. */
  async submitReadinessAssessment(slug: string, answers: Record<string, number>) {
    const res = await this.http.post<AssessmentResult>(`/learning/courses/${slug}/readiness-assessment`, { answers })
    return res.data
  }

  async getRecommendations() {
    const res = await this.http.get<Recommendations>('/learning/recommendations')
    return res.data
  }

  /** A career roadmap: the recommended, ordered courses. (`getTrack` is the legacy track,
   *  `getRoadmap` the mentor's study plan.) */
  async getCareerRoadmap(slug: string) {
    const res = await this.http.get<TrackDetail>(`/learning/tracks/${slug}`)
    return res.data
  }

  /** One module's content, on demand: the course viewer loads a course a module at a time. */
  async getToolTopic(topicId: number) {
    const res = await this.http.get<ToolTopic>(`/tool-courses/topics/${topicId}`)
    return res.data
  }

  async getMySkillLevels() {
    const res = await this.http.get<SkillLevels>('/learning/my-skill-levels')
    return res.data
  }

  async getCourseAccess(courseId: string) {
    const res = await this.http.get<CourseAccess>(`/learning/courses/${courseId}/access`)
    return res.data
  }

  async getBillingCatalog() {
    const res = await this.http.get<BillingCatalogApi>('/billing/catalog')
    return res.data
  }

  async checkoutSubscription(plan: 'pro', billingPeriod: BillingCycle, method: 'card' | 'wallet' = 'card') {
    const res = await this.http.post<CheckoutResponse>('/billing/subscriptions/checkout', {
      plan,
      billing_period: billingPeriod,
      method,
    })
    return res.data
  }

  async startSubscriptionTrial(plan: 'pro', billingPeriod: BillingCycle) {
    const res = await this.http.post('/billing/subscriptions/trial', { plan, billing_period: billingPeriod })
    return res.data
  }

  async getSubscriptionOrders() {
    const res = await this.http.get<SubscriptionOrder[]>('/billing/subscription-orders')
    return res.data
  }

  async getSubscriptionOrder(referenceNumber: string) {
    const res = await this.http.get<SubscriptionOrder>(
      `/billing/subscription-orders/by-reference/${encodeURIComponent(referenceNumber)}`,
    )
    return res.data
  }

  async requestSubscriptionRefund(
    referenceNumber: string,
    input: { reason: string; amount?: number; confirmed: boolean; idempotency_key: string },
  ) {
    const res = await this.http.post<SubscriptionOrder>(
      `/billing/subscription-orders/${encodeURIComponent(referenceNumber)}/refund`, input,
    )
    return res.data
  }

  async getMySubscription() {
    const res = await this.http.get<{
      plan: PlanId
      subscription: null | {
        id: number
        plan: PlanId
        status: string
        billing_period: BillingCycle
        current_period_start: string
        current_period_end: string
        cancel_at_period_end: boolean
        has_pro_access: boolean
      }
      latest_order: SubscriptionOrder | null
      refund_policy: RefundPolicySummary
    }>('/billing/subscription')
    return res.data
  }

  /** The plan, Pro's included AI allowance (null on Free) and whether every course is open -
   *  all computed by the server from subscription and usage records. */
  async getAiAllowance() {
    const res = await this.http.get<AiAllowanceResponse>('/billing/ai-allowance')
    return res.data
  }

  async adminSubscriptionOrders(params: {
    reference_number?: string
    provider_transaction_id?: string
    customer?: string
    order_id?: number
    refund_status?: RefundStatus
  } = {}) {
    const res = await this.http.get<Array<SubscriptionOrder & {
      id: number
      customer: { email: string; name: string }
      provider_transaction_id: string | null
    }>>('/admin/subscription-orders', { params })
    return res.data
  }

  async adminSubscriptionOrder(referenceNumber: string) {
    const res = await this.http.get<SubscriptionOrder & {
      id: number
      customer: { email: string; name: string }
      provider_transaction_id: string | null
      refund_admin_note: string | null
    }>(`/admin/subscription-orders/${encodeURIComponent(referenceNumber)}`)
    return res.data
  }

  async adminTransitionRefund(
    referenceNumber: string,
    input: {
      status: Exclude<RefundStatus, 'not_requested' | 'requested'>
      idempotency_key: string
      amount?: number
      provider_reference?: string
      note?: string
    },
  ) {
    const res = await this.http.post<SubscriptionOrder>(
      `/admin/subscription-orders/${encodeURIComponent(referenceNumber)}/refund-transition`, input,
    )
    return res.data
  }

  async checkoutCourse(courseId: string, method: 'card' | 'wallet' = 'card', phoneNumber?: string) {
    const res = await this.http.post<CheckoutResponse>('/billing/checkout', {
      course_id: courseId,
      method,
      phone_number: phoneNumber,
    })
    return res.data
  }

  async getBillingOrders() {
    const res = await this.http.get<BillingOrder[]>('/billing/orders')
    return res.data
  }

  async getBillingOrder(orderId: number) {
    const res = await this.http.get<BillingOrder>(`/billing/orders/${orderId}`)
    return res.data
  }

  async getMyCourses() {
    const res = await this.http.get<MyCourse[]>('/learning/my-courses')
    return res.data
  }

  // ─── Admin analytics ──────────────────────────────────────────────────

  /** Aggregate product metrics for the admin dashboard. Admin-only: a
   *  student's token gets a 403 from the server, which is the check that
   *  matters — the route guard in the page is only there to avoid showing
   *  a broken screen to someone who was never going to be allowed in. */
  async getAnalyticsOverview() {
    const res = await this.http.get<AdminAnalyticsOverview>('/admin/analytics/overview')
    return res.data
  }

  // ─── Admin credit grants ──────────────────────────────────────────────

  /** Resolve an email to the account behind it and its current balance, so
   *  a grant can be confirmed against a name rather than a typed address. */
  async adminLookupUser(email: string) {
    const res = await this.http.get<AdminUserLookup>('/wallet/admin/user-lookup', {
      params: { email },
    })
    return res.data
  }

  /** Grant credits to an account by email. Admin-only and audited on the
   *  server; the amount is bounded there, not here. */
  async adminGrantCredits(email: string, credits: number, description: string) {
    const res = await this.http.post<AdminGrantResult>('/wallet/admin/grant', {
      email, credits, description,
    })
    return res.data
  }

  // [mentor-v2]
  async sendMentorV2Message(
    body: {
      text: string
      intent?: import('@/features/mentor/types').MentorIntent
      context: import('@/features/mentor/types').MentorContextRef
      /** Same id on a retry of the same send: the server answers it once and charges once. */
      requestId?: string
      /** The learner started a new conversation. */
      fresh?: boolean
      hintLevel?: 1 | 2 | 3
    },
    language: 'ar' | 'en',
  ) {
    // One send can take the server up to its 60 s worker limit (intent call, reply, one corrected
    // retry). Giving up at the default 30 s let the learner press "retry" while the first send was
    // still running, so the server's same-request-id replay found nothing and both were charged.
    // A retry that does arrive while the first is running is told so (409) and waits for it.
    return this.postAiOnce<import('@/features/mentor/types').MentorMessageV2 & { sessionId: number }>(
      '/mentor/message', { ...body, language }, { timeout: MENTOR_MESSAGE_TIMEOUT_MS },
    )
  }

  async getMentorV2Context(
    params: { lessonId?: string; exerciseId?: string; courseId?: string },
    language: 'ar' | 'en',
  ) {
    const res = await this.http.get<import('@/features/mentor/types').MentorContextSelection>(
      '/mentor/context', { params: { ...params, language } },
    )
    return res.data
  }

  /** The courses the learner is enrolled in: what the hub's course picker offers. Free. */
  async getMentorCourses(language: 'ar' | 'en') {
    const res = await this.http.get<{ courses: import('@/features/mentor/types').MentorCourseOption[] }>(
      '/mentor/courses', { params: { language } },
    )
    return res.data.courses
  }

  /** The question a quiz block shows, in `language`. The same question: no cost, nothing recorded. */
  async getMentorV2Quiz(quizId: string, language: 'ar' | 'en') {
    const res = await this.http.get<Extract<import('@/features/mentor/types').MentorBlock, { kind: 'quiz' }>>(
      `/mentor/quiz/${encodeURIComponent(quizId)}`, { params: { language } },
    )
    return res.data
  }

  /** The weekly plan from the learner's real enrolments and progress. Free. */
  async getMentorPlan(params: { weekStart: string; variant?: number }, language: 'ar' | 'en') {
    const res = await this.http.get<import('@/features/mentor/types').StudyPlanV2>(
      '/mentor/plan', { params: { ...params, language } },
    )
    return res.data
  }

  /** The conversation the server is continuing for this lesson, chosen course, or general: what it
   *  sends the model as history, so a new device shows the same thread. Free. */
  async getMentorThread(lessonId: string | undefined, courseId?: string) {
    const res = await this.http.get<{ messages: import('@/features/mentor/types').MentorMessageV2[] }>(
      '/mentor/thread', { params: lessonId ? { lessonId } : courseId ? { courseId } : {} },
    )
    return res.data.messages
  }

  /** What the mentor knows about the learner: position and quiz-evidenced skills. Free. */
  async getMentorLearner(language: 'ar' | 'en') {
    const res = await this.http.get<import('@/features/mentor/types').LearnerModel>(
      '/mentor/learner', { params: { language } },
    )
    return res.data
  }

  async answerMentorV2Quiz(body: { quizId: string; optionId: string }, language: 'ar' | 'en') {
    const res = await this.http.post<import('@/features/mentor/types').QuizAnswerResult>(
      '/mentor/quiz/answer', { ...body, language },
    )
    return res.data
  }

  async runCodeExercise(id: string | number, code: string) {
    const res = await this.http.post<import('@/types').ExerciseRunResult>(
      `/practice/exercises/${id}/run`, { code, language: useLanguageStore.getState().language },
    )
    return res.data
  }

  async getCodeExercise(id: string | number) {
    const res = await this.http.get<{
      id: number
      title: string
      title_ar?: string | null
      language?: string | null
      starter_code?: string | null
    }>(`/practice/exercises/${id}`)
    return res.data
  }

  async submitCodeExercise(id: string | number, code: string) {
    const res = await this.http.post<import('@/types').GradeResult>(
      `/practice/exercises/${id}/submit`, { code, language: useLanguageStore.getState().language },
    )
    return res.data
  }

  async revealCodeExerciseSolution(id: string | number) {
    const res = await this.http.post<{ solution_code: string }>(`/practice/exercises/${id}/solution`)
    return res.data.solution_code
  }

  async getCodeExerciseAttemptState(id: string | number) {
    const res = await this.http.get<import('@/types').ExerciseAttemptState>(`/practice/exercises/${id}/progress`)
    return res.data
  }
  // [/mentor-v2]

  // [project-lab] Challenges › Projects. Deterministic and free: no credits are charged.
  async getLabProjects() {
    const res = await this.http.get<import('@/features/project-lab/types').LabProjectCard[]>('/project-lab/projects')
    return res.data
  }

  async getLabProject(slug: string) {
    const res = await this.http.get<import('@/features/project-lab/types').LabProjectDetail>(
      `/project-lab/projects/${encodeURIComponent(slug)}`,
    )
    return res.data
  }

  /** Idempotent: returns the learner's existing attempt when there is one. */
  async startLabProject(slug: string) {
    const res = await this.http.post<{ attempt_id: number; created: boolean }>(
      `/project-lab/projects/${encodeURIComponent(slug)}/start`,
    )
    return res.data
  }

  async getLabAttempt(attemptId: number) {
    const res = await this.http.get<import('@/features/project-lab/types').LabAttempt>(`/project-lab/attempts/${attemptId}`)
    return res.data
  }

  async getLabWorkspace(attemptId: number) {
    const res = await this.http.get<import('@/features/project-lab/types').LabWorkspace>(
      `/project-lab/attempts/${attemptId}/workspace`,
    )
    return res.data
  }

  async getLabFile(attemptId: number, path: string) {
    const res = await this.http.get<import('@/features/project-lab/types').LabFile>(
      `/project-lab/attempts/${attemptId}/files`, { params: { path } },
    )
    return res.data
  }

  async saveLabFile(attemptId: number, path: string, content: string) {
    const res = await this.http.put<import('@/features/project-lab/types').LabFile>(
      `/project-lab/attempts/${attemptId}/files`, { content }, { params: { path } },
    )
    return res.data
  }

  async resetLabFile(attemptId: number, path: string) {
    const res = await this.http.post<import('@/features/project-lab/types').LabFile>(
      `/project-lab/attempts/${attemptId}/files/reset`, { path },
    )
    return res.data
  }

  async runLabFile(attemptId: number, path: string) {
    const res = await this.http.post<import('@/features/project-lab/types').LabRunResult>(
      `/project-lab/attempts/${attemptId}/run`, { path, language: useLanguageStore.getState().language },
    )
    return res.data
  }

  async checkLabTask(attemptId: number, taskSlug: string) {
    const res = await this.http.post<import('@/features/project-lab/types').LabCheckResult>(
      `/project-lab/attempts/${attemptId}/tasks/${encodeURIComponent(taskSlug)}/check`,
      { language: useLanguageStore.getState().language },
    )
    return res.data
  }

  async getLabArtifacts(attemptId: number) {
    const res = await this.http.get<import('@/features/project-lab/types').LabArtifact[]>(
      `/project-lab/attempts/${attemptId}/artifacts`,
    )
    return res.data
  }

  async getLabArtifact(attemptId: number, path: string) {
    const res = await this.http.get<import('@/features/project-lab/types').LabArtifactContent>(
      `/project-lab/attempts/${attemptId}/artifacts/content`, { params: { path } },
    )
    return res.data
  }

  async getLabSubmission(attemptId: number) {
    const res = await this.http.get<import('@/features/project-lab/types').LabSubmission>(
      `/project-lab/attempts/${attemptId}/submission`,
    )
    return res.data
  }

  async getLabCompletion(attemptId: number) {
    const res = await this.http.get<import('@/features/project-lab/types').LabCompletion>(
      `/project-lab/attempts/${attemptId}/completion`,
    )
    return res.data
  }

  async submitLabProject(attemptId: number) {
    const res = await this.http.post<import('@/features/project-lab/types').LabSubmission>(
      `/project-lab/attempts/${attemptId}/submit`,
    )
    return res.data
  }
  // [/project-lab]
}

export const api = new ApiClient()

// [code-cell]
/** Temporary exercise endpoints. Keeping this boundary means the UI will not
 * change when these two calls move from the local mock to the backend. */
export async function runExerciseTests(
  id: string | number,
  files: import('@/types').ExerciseFile[],
): Promise<import('@/types').ExerciseRunResult> {
  const code = files.find(file => !file.readOnly)?.content ?? ''
  return api.runCodeExercise(id, code)
}

export async function submitExercise(
  id: string | number,
  files: import('@/types').ExerciseFile[],
): Promise<import('@/types').GradeResult> {
  const code = files.find(file => !file.readOnly)?.content ?? ''
  return api.submitCodeExercise(id, code)
}

export async function showExerciseSolution(id: string | number): Promise<string> {
  return api.revealCodeExerciseSolution(id)
}

/** Attempts and solution access as the server records them, so a reload or a
 *  new device offers the same options. */
export async function getExerciseAttemptState(id: string | number): Promise<import('@/types').ExerciseAttemptState> {
  return api.getCodeExerciseAttemptState(id)
}
// [/code-cell]

// [screens]
/** The signed-in Home's data. Served from the local mock until the backend can supply
 * readiness, milestones and exam eligibility; the screen only ever calls this. */
export async function getHomeOverview(): Promise<import('@/features/home/types').HomeOverview> {
  const { MOCK_HOME_OVERVIEW } = await import('@/features/home/mock')
  return MOCK_HOME_OVERVIEW
}
// [/screens]

// [mentor-v2]
/** Mentor v2 endpoints. Message and quiz can go live independently with
 * NEXT_PUBLIC_MENTOR_V2_LIVE=message,quiz. Once anything is live (`mentorV2Live`), no fixture is
 * ever served: each surface uses its real endpoint, or - where there is none yet - shows nothing. */
type MentorV2Lang = 'ar' | 'en'
const mentorMock = () => import('@/features/mentor/mock')

const HINT_ASK: Record<1 | 2 | 3, { ar: string; en: string }> = {
  1: { ar: 'أعطني تلميحاً مفاهيمياً لهذا التمرين.', en: 'Give me a conceptual nudge for this exercise.' },
  2: { ar: 'أعطني تلميحاً أوضح: اتجاهاً محدداً.', en: 'Give me a clearer hint: a specific direction.' },
  3: { ar: 'أعطني إرشاداً مفصّلاً من دون الحل الكامل.', en: 'Give me detailed guidance, without the full solution.' },
}

export const mentorV2 = {
  async sendMessage(body: { text: string; intent?: import('@/features/mentor/types').MentorIntent; context: import('@/features/mentor/types').MentorContextRef; requestId?: string; fresh?: boolean }, lang: MentorV2Lang) {
    if (mentorV2EndpointLive('message')) return api.sendMentorV2Message(body, lang)
    return (await mentorMock()).mockSendMessage(body, lang)
  },
  /**
   * One rung of the hint ladder. Live, levels 1-3 are mentor replies about the real exercise and
   * the learner's draft (HINT with `hintLevel`), and level 4 is the exercise's own reference
   * solution from the grading service - which records that it was viewed - never a model answer.
   */
  async hint(
    body: { exerciseId: string; level: import('@/features/mentor/types').HintLevel; confirm?: boolean; lessonId?: string; code?: string | null; requestId?: string },
    lang: MentorV2Lang,
  ): Promise<import('@/features/mentor/types').MentorMessageV2> {
    if (!mentorV2Live()) return (await mentorMock()).mockHint(body, lang)
    if (body.level === 4) {
      if (!body.confirm) throw new Error('confirm_required')
      const code = await api.revealCodeExerciseSolution(body.exerciseId)
      return {
        id: `solution-${body.exerciseId}-${Date.now().toString(36)}`, role: 'mentor', intent: 'HINT', creditCost: 0,
        blocks: [{
          kind: 'hint', grounding: 'lesson', level: 4,
          label: lang === 'ar' ? 'الحل المرجعي' : 'Reference solution',
          text: lang === 'ar' ? 'هذا حل التمرين المرجعي، وقد سُجّل أنك عرضته.' : "This is the exercise's reference solution; viewing it is recorded on the exercise.",
          code,
        }],
      }
    }
    const level = body.level as 1 | 2 | 3
    return api.sendMentorV2Message({
      text: HINT_ASK[level][lang], intent: 'HINT', hintLevel: level, requestId: body.requestId,
      context: {
        exerciseId: body.exerciseId, attachCode: true,
        ...(body.lessonId ? { lessonId: body.lessonId } : {}),
        ...(body.code ? { code: body.code } : {}),
      },
    }, lang)
  },
  /** The same quiz question in another language, for a learner who switched language with it on screen. */
  async quiz(quizId: string, lang: MentorV2Lang) {
    if (mentorV2EndpointLive('quiz')) return api.getMentorV2Quiz(quizId, lang)
    return (await mentorMock()).mockQuiz(quizId, lang)
  },
  async answerQuiz(body: { quizId: string; optionId: string }, lang: MentorV2Lang) {
    if (mentorV2EndpointLive('quiz')) return api.answerMentorV2Quiz(body, lang)
    return (await mentorMock()).mockAnswerQuiz(body, lang)
  },
  async review(body: { exerciseId?: string; code?: string; lang: string; requestId?: string }, lang: MentorV2Lang) {
    const result = await api.reviewCode(body.code ?? '', body.lang, undefined, lang, body.exerciseId, body.requestId)
    return {
      executed: false as const,
      summary: result.summary,
      comments: result.issues.map((issue, index) => ({
        line: issue.line ?? index + 1,
        severity: issue.severity === 'high' ? 'issue' as const : issue.severity === 'medium' ? 'suggestion' as const : 'ok' as const,
        title: issue.type,
        text: `${issue.message}${issue.suggestion ? ` ${issue.suggestion}` : ''}`,
      })),
      debugSteps: result.improvements.map((text) => ({ text, unlocked: true })),
    }
  },
  async learner(lang: MentorV2Lang): Promise<import('@/features/mentor/types').LearnerModel> {
    if (mentorV2Live()) return api.getMentorLearner(lang)
    return (await mentorMock()).mockLearner(lang)
  },
  /** No real suggestion endpoint exists yet: live, there is no card rather than an invented one. */
  async suggestion(lang: MentorV2Lang): Promise<import('@/features/mentor/types').MentorSuggestion | null> {
    if (mentorV2Live()) return null
    return (await mentorMock()).mockSuggestion(lang)
  },
  async resolveSuggestion(id: string) {
    if (mentorV2Live()) return
    return (await mentorMock()).mockResolveSuggestion(id)
  },
  async plan(body: { weekStart: string; variant?: number }, lang: MentorV2Lang): Promise<import('@/features/mentor/types').StudyPlanV2> {
    if (mentorV2Live()) return api.getMentorPlan(body, lang)
    return (await mentorMock()).mockPlan(body, lang)
  },
  async approvePlan(plan: import('@/features/mentor/types').StudyPlanV2) { return (await mentorMock()).mockApprovePlan(plan) },
  async addToPlan(blocks: import('@/features/mentor/types').PlanBlock[]) { return (await mentorMock()).mockAddToPlan(blocks) },
  async approvedPlan() { return (await mentorMock()).mockApprovedPlan() },
  /** A proactive card needs a verified trigger the client does not have here: live, none. */
  async proactive(lang: MentorV2Lang): Promise<import('@/features/mentor/types').MentorMessageV2 | null> {
    if (mentorV2Live()) return null
    return (await mentorMock()).mockProactive(lang)
  },
  async interviewReport(id: string, lang: MentorV2Lang) { return (await mentorMock()).mockInterviewReport(id, lang) },
}
// [/mentor-v2]
