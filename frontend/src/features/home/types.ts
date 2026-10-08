/** Copy that exists in both UI languages (course and track names are content, not chrome). */
export interface Localized {
  en: string
  ar: string
}

export type MilestoneStatus = 'done' | 'now' | 'lock'

export interface HomeMilestone {
  title: Localized
  meta: Localized
  status: MilestoneStatus
  /** Progress inside the stage; only the `now` stage shows it. */
  percent?: number
}

export interface HomeRequirement {
  label: Localized
  done: boolean
  /** e.g. "72/75"; Latin digits in both languages. */
  value?: string
}

/** Everything the signed-in Home shows, in one payload (what the backend will return). */
export interface HomeOverview {
  continueLearning: {
    courseTitle: string
    lessonNumber: number
    lessonTotal: number
    lessonTitle: Localized
    minutesLeft: number
    percent: number
    lessonHref: string
    planHref: string
  }
  readiness: {
    score: number
    weeklyDelta: number
    skills: { name: Localized; value: number }[]
  }
  track: {
    title: Localized
    en: string
    milestones: HomeMilestone[]
  }
  exam: {
    title: string
    minutes: number
    pointsAway: number
    requirements: HomeRequirement[]
  }
  stats: { streakDays: number; gradedExercises: number }
  mentor: { tip: Localized; href: string }
}
