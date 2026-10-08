import { useLanguageStore, type UiLanguage } from '@/lib/language'

/** Latin 0-9 to Arabic-Indic ٠-٩. Used only inside Arabic copy ("٧ من ١٢"); scores,
 *  percentages, credits and ids stay Latin in mono. */
export function arabicDigits(value: string | number): string {
  return String(value).replace(/\d/g, (d) => '٠١٢٣٤٥٦٧٨٩'[Number(d)])
}

/** A number inside running copy, in the digits of the reader's language. */
export function copyNumber(value: number, language: UiLanguage): string {
  return language === 'ar' ? arabicDigits(value) : String(value)
}

const STRINGS = {
  en: {
    'home.subtitle': 'You are {n} points from eligibility for the RAG Engineer exam. Pick up where you left off.',
    'home.continue.eyebrow': 'CONTINUE',
    'home.continue.label': 'Continue learning',
    'home.continue.lesson': 'Lesson {n} — {title}',
    'home.continue.meta': 'Lesson {n} of {total} · {min} min left',
    'home.continue.go': 'Continue lesson',
    'home.continue.plan': 'Course plan',
    'home.readiness.title': 'Readiness score',
    'home.readiness.week': 'this week',
    'home.track.label': 'Your career track',
    'home.track.stages': '{done} of {total} stages',
    'home.track.done': 'Done',
    'home.track.now': 'In progress',
    'home.track.lock': 'Locked',
    'home.exam.label': 'Next certification exam',
    'home.exam.meta': 'Proctored by camera · {min} minutes',
    'home.exam.book': 'Book a slot once eligible',
    'home.stats.streak': 'Day streak',
    'home.stats.graded': 'Graded exercises',
    'home.mentor.title': 'AI Mentor',
    'home.mentor.open': 'Open the chat',
  },
  ar: {
    'home.subtitle': 'أنت على بعد {n} نقاط من أهلية اختبار RAG Engineer. تابع من حيث توقفت.',
    'home.continue.eyebrow': 'CONTINUE',
    'home.continue.label': 'تابع التعلّم',
    'home.continue.lesson': 'الدرس {n} — {title}',
    'home.continue.meta': 'الدرس {n} من {total} · {min} دقيقة متبقية',
    'home.continue.go': 'متابعة الدرس',
    'home.continue.plan': 'خطة الدورة',
    'home.readiness.title': 'مؤشر الجاهزية',
    'home.readiness.week': 'هذا الأسبوع',
    'home.track.label': 'مسارك المهني',
    'home.track.stages': '{done} من {total} مراحل',
    'home.track.done': 'مكتمل',
    'home.track.now': 'جارٍ',
    'home.track.lock': 'مقفل',
    'home.exam.label': 'اختبار الاعتماد القادم',
    'home.exam.meta': 'اختبار مراقَب بالكاميرا · {min} دقيقة',
    'home.exam.book': 'احجز موعداً بعد الأهلية',
    'home.stats.streak': 'سلسلة الأيام',
    'home.stats.graded': 'تمارين مقيّمة',
    'home.mentor.title': 'المرشد الذكي',
    'home.mentor.open': 'افتح المحادثة',
  },
} as const

export type HomeStringKey = keyof (typeof STRINGS)['en']

/** Strings for the Home screen, kept next to it rather than in lib/i18n so the feature
 *  ports without edits to a shared dictionary. */
export function useHomeI18n() {
  const language = useLanguageStore((s) => s.language)
  const tf = (key: HomeStringKey, vars: Record<string, string | number> = {}) =>
    STRINGS[language][key].replace(/\{(\w+)\}/g, (m, name) =>
      Object.prototype.hasOwnProperty.call(vars, name) ? String(vars[name]) : m,
    )
  return {
    language,
    tf,
    /** A number in running copy, in the reader's digits. */
    n: (value: number) => copyNumber(value, language),
  }
}
