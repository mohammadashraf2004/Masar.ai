'use client'
import { useLanguageStore, directionFor, type UiLanguage } from '@/lib/language'

/**
 * UI chrome strings.
 *
 * Deliberately hand-rolled rather than pulling in an i18n framework: the app
 * has one namespace, two languages, no pluralisation rules and no runtime
 * locale loading. `STRINGS.en` is the source of truth for the key set — a
 * missing Arabic key is a type error, not a silent fallback at runtime.
 *
 * Note what is NOT here: technical terminology. Terms live in
 * `src/content/terminology` and stay in English in both languages, by design.
 */
const EN = {
  // Nav
  'nav.dashboard': 'Dashboard',
  'nav.tracks': 'Learning tracks',
  'nav.tools': 'Tools & frameworks',
  'nav.mentor': 'AI mentor',
  'nav.community': 'Community',
  'nav.challenges': 'Challenges',
  'nav.glossary': 'AI vocabulary',
  'nav.signOut': 'Sign out',
  'nav.menu': 'Menu',
  'nav.openMenu': 'Open navigation menu',
  'nav.readiness': 'Readiness',
  'nav.quickAction': 'Quick action',
  'nav.askMentor': 'Ask your AI mentor',
  'nav.getVerified': 'Get Verified',

  // Language switcher
  'lang.title': 'Language & terminology',
  'lang.uiLanguage': 'Explanations',
  'lang.arabic': 'العربية',
  'lang.english': 'English',
  'lang.mode': 'Terminology level',
  'lang.mode.arabic_first': 'Arabic First',
  'lang.mode.industry': 'Industry Mode',
  'lang.mode.english_technical': 'English Technical',
  'lang.mode.arabic_first.hint': 'Arabic explanations, English terms introduced gently.',
  'lang.mode.industry.hint': 'More English terminology mixed into Arabic explanations.',
  'lang.mode.english_technical.hint': 'Professional English phrasing, as used at work.',
  'lang.annotate': 'Highlight technical terms in lessons',
  'lang.codeNote': 'Code, commands and framework names never change.',

  // Course / lesson chrome
  'course.lessons': 'Lessons',
  'course.exercises': 'Exercises',
  'course.quiz': 'Quiz',
  'course.project': 'Project',
  'course.startLearning': 'Start learning',
  'course.continue': 'Continue',
  'course.review': 'Review',
  'course.enrolled': 'Enrolled',
  'course.comingSoon': 'Coming soon',
  'course.inProgress': 'In progress',
  'course.completed': 'Completed',
  'course.topics': 'topics',
  'course.tools': 'tools',
  'course.estimated': 'estimated',
  'course.markComplete': 'Mark as complete',
  'course.noLessons': 'No lessons for this topic yet.',
  'course.notFound': 'Tool course not found.',
  'course.search': 'Search courses — Arabic or English',
  'course.searchHint': 'Try “RAG”, “Embeddings” or “التضمينات”.',
  'course.noResults': 'No course matches that search.',
  'course.arabicUnavailable': 'Arabic version not published yet — showing the English original.',

  // Exercise / project brief
  'exercise.label': 'Exercise',
  'exercise.of': 'of',
  'exercise.task': 'What to do',
  'exercise.starterCode': 'Starter code',
  'exercise.yourAnswer': 'Your answer',
  'exercise.skills': 'Skills tested',
  'exercise.noneYet': 'No exercises for this topic yet.',
  'project.label': 'Project',
  'project.brief': 'The brief',
  'project.objectives': 'What it must do',
  'project.stack': 'Tech stack',
  'project.noneYet': 'No project for this topic yet.',

  // Terminology UI
  'term.industryTerm': 'Industry term',
  'term.category': 'Category',
  'term.example': 'Example',
  'term.learned': 'Learned',
  'term.markLearned': 'Mark as learned',
  'term.seenIn': "Where you'll see this",
  'term.inThisCourse': 'Technical vocabulary in this course',
  'term.glossaryTitle': 'Your AI vocabulary',
  'term.glossarySubtitle': 'The English terminology behind the Arabic explanations.',
  'term.progress': 'terms learned',
  'term.searchPlaceholder': 'Search a term in Arabic or English',
  'term.allCategories': 'All',
  'term.jdPhrases': 'In real job descriptions',
  'term.relatedRoles': 'Roles that ask for it',
  'term.empty': 'No term matches that search.',

  // Generic
  'common.close': 'Close',
  'common.loading': 'Loading…',
} as const

export type StringKey = keyof typeof EN

const AR: Record<StringKey, string> = {
  'nav.dashboard': 'لوحة التحكم',
  'nav.tracks': 'المسارات التعليمية',
  'nav.tools': 'الأدوات و الـ Frameworks',
  'nav.mentor': 'المرشد الذكي',
  'nav.community': 'المجتمع',
  'nav.challenges': 'التحديات',
  'nav.glossary': 'مصطلحاتك التقنية',
  'nav.signOut': 'تسجيل الخروج',
  'nav.menu': 'القائمة',
  'nav.openMenu': 'فتح قائمة التنقل',
  'nav.readiness': 'جاهزيتك',
  'nav.quickAction': 'إجراء سريع',
  'nav.askMentor': 'اسأل مرشدك الذكي',
  'nav.getVerified': 'احصل على الشهادة',

  'lang.title': 'اللغة والمصطلحات',
  'lang.uiLanguage': 'لغة الشرح',
  'lang.arabic': 'العربية',
  'lang.english': 'English',
  'lang.mode': 'مستوى المصطلحات',
  'lang.mode.arabic_first': 'العربية أولاً',
  'lang.mode.industry': 'Industry Mode',
  'lang.mode.english_technical': 'English Technical',
  'lang.mode.arabic_first.hint': 'شرح بالعربية، مع تقديم المصطلح الإنجليزي بالتدريج.',
  'lang.mode.industry.hint': 'شرح بالعربية مع مصطلحات إنجليزية أكثر، كما في بيئة العمل.',
  'lang.mode.english_technical.hint': 'صياغة إنجليزية احترافية كما تظهر في الوثائق والمقابلات.',
  'lang.annotate': 'إبراز المصطلحات التقنية داخل الدروس',
  'lang.codeNote': 'الكود والأوامر وأسماء الـ Frameworks لا تتغير في أي وضع.',

  'course.lessons': 'الدروس',
  'course.exercises': 'التمارين',
  'course.quiz': 'الاختبار',
  'course.project': 'المشروع',
  'course.startLearning': 'ابدأ التعلم',
  'course.continue': 'أكمل',
  'course.review': 'مراجعة',
  'course.enrolled': 'مُسجَّل',
  'course.comingSoon': 'قريباً',
  'course.inProgress': 'قيد التقدم',
  'course.completed': 'مكتمل',
  'course.topics': 'موضوعات',
  'course.tools': 'أدوات',
  'course.estimated': 'تقريباً',
  'course.markComplete': 'علّمه كمكتمل',
  'course.noLessons': 'لا توجد دروس لهذا الموضوع بعد.',
  'course.notFound': 'لم يتم العثور على هذه الدورة.',
  'course.search': 'ابحث في الدورات — بالعربية أو الإنجليزية',
  'course.searchHint': 'جرّب «RAG» أو «Embeddings» أو «التضمينات».',
  'course.noResults': 'لا توجد دورة مطابقة لهذا البحث.',
  'course.arabicUnavailable': 'النسخة العربية لم تُنشر بعد — يُعرض النص الإنجليزي الأصلي.',

  'exercise.label': 'تمرين',
  'exercise.of': 'من',
  'exercise.task': 'المطلوب منك',
  'exercise.starterCode': 'الكود المبدئي',
  'exercise.yourAnswer': 'إجابتك',
  'exercise.skills': 'المهارات المُختبَرة',
  'exercise.noneYet': 'لا توجد تمارين لهذا الموضوع بعد.',
  'project.label': 'مشروع',
  'project.brief': 'وصف المشروع',
  'project.objectives': 'ما يجب أن ينفّذه',
  'project.stack': 'التقنيات المستخدمة',
  'project.noneYet': 'لا يوجد مشروع لهذا الموضوع بعد.',

  'term.industryTerm': 'المصطلح المستخدم في السوق',
  'term.category': 'التصنيف',
  'term.example': 'مثال',
  'term.learned': 'تم إتقانه',
  'term.markLearned': 'علّمه كمُتقَن',
  'term.seenIn': 'أين ستقابل هذا المصطلح',
  'term.inThisCourse': 'المصطلحات التقنية في هذه الدورة',
  'term.glossaryTitle': 'حصيلتك من مصطلحات الـ AI',
  'term.glossarySubtitle': 'المصطلحات الإنجليزية التي تقف خلف الشرح العربي.',
  'term.progress': 'مصطلحاً تم إتقانه',
  'term.searchPlaceholder': 'ابحث عن مصطلح بالعربية أو الإنجليزية',
  'term.allCategories': 'الكل',
  'term.jdPhrases': 'في إعلانات الوظائف الحقيقية',
  'term.relatedRoles': 'الوظائف التي تطلبه',
  'term.empty': 'لا يوجد مصطلح مطابق.',

  'common.close': 'إغلاق',
  'common.loading': 'جارٍ التحميل…',
}

const STRINGS: Record<UiLanguage, Record<StringKey, string>> = { en: EN, ar: AR }

export function translate(key: StringKey, language: UiLanguage): string {
  return STRINGS[language][key] ?? EN[key]
}

/**
 * The one hook UI components use for language. Returns the active language,
 * its direction, a `t()` bound to it, and the terminology mode so a component
 * can adjust how much English it shows.
 */
export function useI18n() {
  const language = useLanguageStore((s) => s.language)
  const mode = useLanguageStore((s) => s.mode)
  const annotateTerms = useLanguageStore((s) => s.annotateTerms)
  const dir = directionFor(language)

  return {
    language,
    mode,
    annotateTerms,
    dir,
    isRtl: dir === 'rtl',
    t: (key: StringKey) => translate(key, language),
  }
}
