import { describe, expect, it } from 'vitest'
import { STRINGS, countForm, fmt, translate } from '@/lib/i18n'
import type { StringKey } from '@/lib/i18n'
import {
  advisoryText, fieldLabel, labelText, learningLabel, levelLabel, roleLabel, skillLabel, titleLabel,
} from '@/lib/learning'
import { iconFor } from '@/lib/learning-icons'
import { ADVANCED, AI_ENGINEER, FIELDS, NLP, RAG_SKILL, ref } from '@/test/fixtures'

const en = { language: 'en', mode: 'arabic_first' } as const
const arFirst = { language: 'ar', mode: 'arabic_first' } as const
const arIndustry = { language: 'ar', mode: 'industry' } as const
const arTechnical = { language: 'ar', mode: 'english_technical' } as const

describe('learningLabel — how a name reads in each language and terminology mode', () => {
  it('shows English alone in an English interface', () => {
    expect(learningLabel('NLP & LLMs', 'معالجة اللغة الطبيعية', en)).toEqual({ primary: 'NLP & LLMs', primaryDir: 'ltr' })
  })

  it('keeps a technical term in English with an Arabic gloss in Arabic First — NLP (معالجة اللغة الطبيعية)', () => {
    const parts = learningLabel('NLP', 'معالجة اللغة الطبيعية', arFirst)
    expect(parts).toEqual({ primary: 'NLP', primaryDir: 'ltr', gloss: 'معالجة اللغة الطبيعية' })
    expect(labelText(parts)).toBe('NLP (معالجة اللغة الطبيعية)')
  })

  it('drops the gloss in English Technical mode', () => {
    expect(learningLabel('NLP', 'معالجة', arTechnical)).toEqual({ primary: 'NLP', primaryDir: 'ltr' })
  })

  it('Industry Mode keeps the gloss on a heading and drops it in a dense list', () => {
    expect(learningLabel('NLP', 'معالجة', arIndustry).gloss).toBe('معالجة')
    expect(learningLabel('NLP', 'معالجة', arIndustry, { dense: true }).gloss).toBeUndefined()
  })

  it('Arabic First keeps the gloss even in a dense list — the reader opted into it', () => {
    expect(learningLabel('NLP', 'معالجة', arFirst, { dense: true }).gloss).toBe('معالجة')
  })

  it('reads an interface word in Arabic, and only English Technical asks for English', () => {
    expect(learningLabel('Beginner', 'مبتدئ', arFirst, { kind: 'label' })).toEqual({ primary: 'مبتدئ', primaryDir: 'rtl' })
    expect(learningLabel('Beginner', 'مبتدئ', arIndustry, { kind: 'label' }).primary).toBe('مبتدئ')
    expect(learningLabel('Beginner', 'مبتدئ', arTechnical, { kind: 'label' }).primary).toBe('Beginner')
  })

  it('falls back to English when there is no Arabic twin — never blank', () => {
    expect(learningLabel('LangChain', null, arFirst, { kind: 'label' })).toEqual({ primary: 'LangChain', primaryDir: 'ltr' })
    expect(learningLabel('LangChain', '   ', arFirst)).toEqual({ primary: 'LangChain', primaryDir: 'ltr' })
  })

  it('English runs are always left-to-right and Arabic runs right-to-left', () => {
    expect(learningLabel('Computer Vision', 'الرؤية الحاسوبية', arFirst).primaryDir).toBe('ltr')
    expect(learningLabel('Computer Vision', 'الرؤية الحاسوبية', arFirst, { kind: 'label' }).primaryDir).toBe('rtl')
  })

  it('has entity wrappers that pick the right kind', () => {
    expect(levelLabel(ADVANCED, arFirst).primary).toBe('متقدم')
    expect(fieldLabel(NLP, arFirst).primary).toBe('NLP & LLMs')
    expect(roleLabel(AI_ENGINEER, arFirst).gloss).toBe('مهندس ذكاء اصطناعي')
    expect(titleLabel({ title: 'AI Foundations', title_ar: 'أسس الذكاء الاصطناعي' }, arFirst).primary).toBe('أسس الذكاء الاصطناعي')
  })
})

describe('skillLabel — skills go through the existing terminology dictionary', () => {
  it('shows the dictionary form of a skill and its Arabic gloss in Arabic First', () => {
    const parts = skillLabel(RAG_SKILL, arFirst)
    expect(parts.primary).toBe('RAG')
    expect(parts.gloss).toBeTruthy()
  })

  it('shows no gloss in English, Industry or English Technical', () => {
    expect(skillLabel(RAG_SKILL, en).gloss).toBeUndefined()
    expect(skillLabel(RAG_SKILL, arIndustry).gloss).toBeUndefined()
    expect(skillLabel(RAG_SKILL, arTechnical).gloss).toBeUndefined()
  })

  it('falls back to the skill\'s own name when the dictionary does not know it', () => {
    expect(skillLabel({ slug: 'qdrant-ops', name: 'Qdrant Ops', name_ar: null }, arFirst)).toEqual({
      primary: 'Qdrant Ops', primaryDir: 'ltr',
    })
  })
})

describe('advisoryText — sentences for the notes the server attaches to a path', () => {
  const fields = Object.fromEntries(FIELDS.map((f) => [f.slug, ref(f)]))
  const tfFor = (language: 'en' | 'ar') => (key: StringKey, vars?: Record<string, string | number>) =>
    fmt(translate(key, language), vars)
  const ctx = (language: 'en' | 'ar') => ({ ...(language === 'en' ? en : arFirst), tf: tfFor(language), fields })

  it('explains an advanced field without blocking it', () => {
    const text = advisoryText(
      { code: 'field_above_level', severity: 'info', params: { field: 'multimodal', level: 'beginner', min_level: 'advanced' } },
      ctx('en')
    )
    expect(text).toContain('Multimodal AI')
    expect(text).toMatch(/advanced field/i)
    expect(text).toMatch(/can still choose/i)
  })

  it('names the prerequisite route that was added', () => {
    const text = advisoryText(
      { code: 'prerequisite_route_added', severity: 'warning', params: { field: 'multimodal', added: ['nlp'] } },
      ctx('en')
    )
    expect(text).toContain('NLP & LLMs')
    expect(text).toContain('Multimodal AI')
  })

  it('recommends a second modality by name — including one not in the route', () => {
    const text = advisoryText(
      { code: 'prerequisites_recommended', severity: 'info', params: { field: 'multimodal', have: 1, recommended: 2, suggested: ['computer-vision', 'speech'] } },
      ctx('en')
    )
    expect(text).toContain('Computer Vision')
    expect(text).toContain('Speech & Voice AI')
    expect(text).toMatch(/You have 1/)
  })

  it('says content is still being written when a route has nothing published', () => {
    expect(advisoryText({ code: 'no_available_courses', severity: 'info', params: {} }, ctx('en')))
      .toMatch(/still being written/i)
  })

  it('renders the same advisory in Arabic, with English terms kept and glossed', () => {
    const text = advisoryText(
      { code: 'prerequisite_route_added', severity: 'warning', params: { field: 'multimodal', added: ['nlp'] } },
      ctx('ar')
    )
    expect(text).toContain('أضفنا')
    expect(text).toContain('NLP & LLMs (معالجة اللغة الطبيعية والـ LLMs)')
  })

  it('never shows a learner an advisory that is really a catalogue-configuration problem', () => {
    for (const code of ['prerequisite_cycle', 'prerequisite_out_of_order', 'no_template_fallback', 'something_new']) {
      expect(advisoryText({ code, severity: 'warning', params: {} }, ctx('en'))).toBeNull()
    }
  })

  it('falls back to the slug for a field it has not heard of, rather than crashing', () => {
    const text = advisoryText(
      { code: 'field_above_level', severity: 'info', params: { field: 'quantum-robotics' } }, ctx('en')
    )
    expect(text).toContain('quantum-robotics')
  })
})

describe('interface strings', () => {
  it('has an Arabic string for every English key, and the same placeholders in both', () => {
    const placeholders = (s: string) => (s.match(/\{\w+\}/g) ?? []).sort().join(',')
    const keys = Object.keys(STRINGS.en) as StringKey[]
    expect(keys.length).toBeGreaterThan(100)
    for (const key of keys) {
      expect(STRINGS.ar[key], `missing Arabic for ${key}`).toBeTruthy()
      expect(placeholders(STRINGS.ar[key]), `placeholders differ for ${key}`).toBe(placeholders(STRINGS.en[key]))
    }
  })

  it('substitutes placeholders and leaves an unfilled one visible', () => {
    expect(fmt('Step {n} of {total}', { n: 2, total: 4 })).toBe('Step 2 of 4')
    expect(fmt('Hello {name}')).toBe('Hello {name}')
  })

  it('counts courses by each language\'s own plural rule', () => {
    expect([1, 2, 5, 11].map((n) => countForm(n, 'en'))).toEqual(['one', 'many', 'many', 'many'])
    expect([1, 2, 3, 10, 11, 25].map((n) => countForm(n, 'ar'))).toEqual(['one', 'two', 'few', 'few', 'many', 'many'])
    expect(fmt(translate('learn.courses.few', 'ar'), { n: 4 })).toBe('4 دورات')
    expect(fmt(translate('learn.courses.many', 'ar'), { n: 12 })).toBe('12 دورة')
    expect(translate('learn.courses.one', 'en')).toBe('1 course')
  })
})

describe('icons', () => {
  it('resolves a key to a component and falls back for one it does not know', () => {
    expect(iconFor('brain')).toBeTruthy()
    expect(iconFor('not-an-icon')).toBe(iconFor(null))
    expect(iconFor(undefined)).toBe(iconFor(''))
  })
})
