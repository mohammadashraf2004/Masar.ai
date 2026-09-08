# Arabic-First Content Guidelines

How every course, lesson, exercise, quiz and AI response on this platform is written.

**The goal:** a student learns the concept in Arabic, recognises the term in English, and works in English.

> تعلّم الـ AI بالعربية → افهم مصطلحات السوق → اشتغل واكتب كود بالإنجليزية.

This is not "English courses translated into Arabic". Arabic is where the explanation lives; English is where the terminology lives. Both are first-class, and they do different jobs:

* **Arabic improves understanding.** A student thinking in their own language learns faster.
* **English terminology improves employability.** Documentation, GitHub, Stack Overflow, papers, interviews and job descriptions are in English. A student who only knows «قاعدة بيانات المتجهات» cannot search for it, cannot read the docs, and will not recognise it in a job posting.

---

## 1. The core rule

Write the explanation in clear Modern Standard Arabic — the register a university student reads comfortably, not formal literary Arabic. Keep every AI/ML technical term in English.

❌ **Wrong** — the term has been translated away:

> التضمينات هي طريقة لتحويل النصوص إلى متجهات.

✅ **Right** — the term is introduced, then used:

> Embeddings (التضمينات) هي تمثيلات رقمية للنصوص أو البيانات في صورة vectors، بحيث يمكن للنظام قياس مدى التشابه بينها.

And afterwards, keep using the English term:

> نستخدم Embeddings لتحويل النص إلى vectors، ثم نخزّن هذه vectors داخل Vector Database.

## 2. The first-mention rule

The first time a concept appears **in a lesson**, write it as:

```
English Term (الشرح بالعربية)
```

> Retrieval-Augmented Generation (RAG) هو أسلوب يسمح للنموذج باسترجاع معلومات من مصادر خارجية قبل توليد الإجابة.

Every mention after that uses the English term alone — `RAG`, not the Arabic gloss, and not both again.

The UI enforces the visual half of this for you: `MarkdownLesson` detects dictionary terms in prose and renders the first occurrence as `Embeddings (التضمينات)`, later ones as a clickable `Embeddings`. You still write the first mention explicitly — the renderer reinforces it, it does not replace authoring.

## 3. Never translate code

Nothing inside a code block, and nothing that is an identifier, is ever translated or transliterated:

* Python keywords, syntax
* library, package, framework and module names
* class, function, method and variable names
* CLI and `git` commands, file names, paths, URLs
* error messages
* **code comments** — they are part of the code, write them in English

```python
from langchain_core.documents import Document

documents = vector_store.similarity_search(
    query,
    k=5,
)
```

The prose around that block is Arabic. The block itself is identical in every language and every mode. This is enforced structurally, not by discipline: the schema has no `_ar` twin for `starter_code`, `solution_code` or `tech_stack`, and the lesson renderer never passes code through term annotation (`components/ui/MarkdownLesson.tsx`).

## 4. Never translate technology names

Product and framework names are proper nouns:

Python · PyTorch · TensorFlow · Hugging Face · Transformers · LangChain · LangGraph · LlamaIndex · FastAPI · Docker · Kubernetes · PostgreSQL · FAISS · Chroma · Qdrant · OpenAI · Gemini · Claude

The full list lives in `frontend/src/content/terminology/tech-names.ts`.

## 5. Do not force an Arabic word where the industry uses English

Some terms are used in English by every Arabic-speaking engineer. Introduce the Arabic *meaning* once, then use the English term. Never make the Arabic the working vocabulary for:

Pipeline · Agent · Prompt · Embedding · Token · Framework · Backend · Frontend · API · Deployment · Inference · Fine-tuning · Reranking · Chunking · Streaming · Latency · Observability · Orchestration

✅ `Latency تعني الزمن الذي يستغرقه النظام للرد على الطلب.`
❌ «زمن الكمون» used throughout the UI and the lesson.

## 6. The terminology dictionary

One source of truth: **`frontend/src/content/terminology/ai-terms.ts`**.

```ts
embeddings: {
  id: 'embeddings',
  en: 'Embeddings',
  ar: 'التضمينات',
  preferred: 'Embeddings',   // the form used in prose after the first mention
  category: 'RAG',
  level: 'beginner',
  aliases: ['embedding', 'embed', 'تمثيل النصوص'],
  definitionAr: '...',
  definitionEn: '...',
  exampleAr: '...',
}
```

* `preferred` is what appears in running text (`RAG`, not `Retrieval-Augmented Generation`).
* `ar` explains the term once. It never replaces `preferred`.
* `aliases` make **search** forgiving — every alias is a way a student might type it, in either language. They are not used for auto-linking in lessons.

**After editing the dictionary, run:**

```bash
cd frontend && npm run terminology:export
```

That regenerates `backend/app/content/ai_terms.json`, which the backend uses for bilingual search, the AI tutor's language policy, and the content linter. Commit both files. `pytest tests/test_terminology.py` fails if they fall out of step.

Adding a term is a one-file change. No lesson, component or migration has to be touched.

## 7. Lesson structure

Each lesson follows this shape:

1. **Concept introduction** — what this is, in one Arabic sentence.
2. **Arabic explanation** — the substance.
3. **Industry terminology** — the English terms introduced, first-mention rule applied.
4. **Visual example** — a diagram or a worked walkthrough.
5. **Code example** — real, runnable, untranslated.
6. **Practical exercise**.
7. **Technical vocabulary** — list the terms taught (see `technical_terms` below).
8. **Real-world usage** — where this shows up in production systems.
9. **Interview question** — asked the way it would actually be asked.

Example opening:

> ## ما هو RAG؟
>
> Retrieval-Augmented Generation (RAG) هو architecture يسمح للـ LLM بالوصول إلى external knowledge قبل توليد الإجابة.
>
> **Industry terms:** RAG · Retrieval · Retriever · Embeddings · Vector Database · Chunking · Reranking · Context

## 8. Course and lesson metadata

Every content row has an optional Arabic twin (migration `006_arabic_first_content`):

| Table | Arabic fields | Terminology fields |
|---|---|---|
| `career_tracks`, `track_levels` | `title_ar`, `description_ar` | — |
| `topics` | `title_ar`, `description_ar` | `technical_terms` |
| `lessons` | `title_ar`, `content_ar` | — |
| `exercises`, `projects` | `title_ar`, `description_ar` | — |
| `quizzes` | `title_ar`, `questions_ar` | — |
| `tool_courses` | `title_ar`, `description_ar` | `technical_terms`, `industry_skills` |
| `tool_topics` | `title_ar`, `description_ar` | `technical_terms` |

* **All nullable.** A course with no Arabic version keeps working: the reader gets the English original and a note saying the Arabic version is not published yet. Never delete or overwrite an English field to add Arabic.
* `content_ar` is **authored**, not translated. Write it as an Arabic-first lesson with English terminology inline; the code blocks are identical to the English version.
* `questions_ar` mirrors `questions` index-for-index, so grading never depends on which language the student read.
* `technical_terms` holds **dictionary ids** (`["rag", "embeddings", "vector_database"]`). It drives the vocabulary panel, the vocabulary progress bar, and the job-role mapping.
* `industry_skills` holds the phrasing a recruiter searches for (`["LLM", "RAG", "Vector Search"]`) — free text, not dictionary ids.

## 9. Search

One course per subject, never one per language. Search normalizes and expands the query through the dictionary, so all of these reach the same material:

```
Embeddings · embedding · التضمينات · تمثيل النصوص
RAG · Retrieval Augmented Generation · التوليد المعزز بالاسترجاع
```

Normalization folds Arabic orthography (hamza forms, `ى`/`ي`, `ة`/`ه`), strips the definite article — including the `الـ` glued onto English terms — and is implemented twice, identically, in `frontend/src/content/terminology/index.ts` and `backend/app/content/terminology.py`. **If you change one, change the other**; `tests/test_terminology.py` guards the cases that matter.

Never create a second course because students searched in a different language.

## 10. Industry Mode

The reader chooses how much English terminology they get (header → language control):

| Mode | Reads like |
|---|---|
| **Arabic First** | `الـ Embeddings هي طريقة لتمثيل النصوص كـ vectors.` |
| **Industry Mode** | `نستخدم Embeddings لتحويل documents إلى vectors، ثم Vector Database لتنفيذ similarity search.` |
| **English Technical** | `The pipeline generates embeddings for each chunk, stores them in a vector index, and retrieves the top-k relevant chunks before passing them to the LLM.` |

Code is identical in all three. The mode is forwarded to the AI mentor with every message, so the tutor's register matches the lessons the student is reading.

## 11. AI tutor and voice

`backend/app/services/language/language_policy.py` builds the language block appended to every AI system prompt, from the same dictionary. Its rules:

* Response language: Arabic (unless the reader chose English).
* Technical terminology: English.
* Code, framework names, commands, error messages: English, untouched.
* Register: natural Arabic for university students and aspiring AI engineers — not unnecessarily formal.

Example of the behaviour we want:

> **User:** يعني ايه Reranking؟
>
> **AI:** Reranking هو خطوة بنستخدمها بعد مرحلة الـ Retrieval لتحسين ترتيب النتائج. في البداية، الـ Retriever ممكن يرجّع 20 document. بعد كده نستخدم Reranker لتقييم مدى ارتباط كل document بالـ query وإعادة الترتيب بحيث تكون الـ most relevant documents في البداية.
>
> باختصار: `Retrieval → Reranking → LLM`

The same applies to a voice assistant: speak Arabic, pronounce technical terms in English, and never force an Arabic pronunciation of an English technical term.

## 12. Assignments

Written in Arabic, using real industry terminology, so the task reads like a real ticket:

> قم ببناء RAG pipeline باستخدام Python. يجب أن يحتوي النظام على:
> Document loading · Chunking · Embeddings · Vector Database · Retrieval · LLM generation
>
> ثم قم بقياس Retrieval quality.

## 13. Quality check

Before publishing, run the content through the linter:

```bash
curl -X POST localhost:8000/api/v1/terminology/lint \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "<lesson markdown>"}'
```

It returns:

* `warnings` — every place an Arabic gloss was used without the English term appearing anywhere in the text:

  > ⚠ استخدمت «إعادة الترتيب» دون ذكر المصطلح الإنجليزي.
  > قدّمه مرة واحدة على الأقل بصيغة «Reranking (إعادة الترتيب)» ثم استمر في استخدام «Reranking».

* `terms_used` — the dictionary ids the text actually teaches. Paste these into the course's `technical_terms`.

**This never blocks publishing.** Some sentences genuinely want the Arabic word alone; the warning exists so that is a decision, not an accident.

## 14. Writing quiz options

A multiple-choice question only checks understanding if the options don't
give the answer away. Two tells did exactly that across the seeded
catalogue: the correct option was the longest in 92% of questions, and sat
at position 2 in 80% of them. Picking "the long one" scored better than
studying.

**Length.** Give distractors the same weight as the correct answer. The
usual failure is writing the correct option as a full explanation and the
wrong ones as throwaway phrases:

Bad — the answer is the only one anyone would write out:

```
What is RAG?
  a) A database
  b) An architecture that lets an LLM retrieve external documents before
     generating an answer, so the response is grounded in real sources
     rather than the model's own memory
  c) A GPU
```

Good — every option is plausible and about the same length:

```
What is RAG?
  a) An architecture that retrieves relevant documents before the LLM answers
  b) A vector database that stores documents as embeddings
  c) A fine-tuning method that teaches a model new facts
```

Save the reasoning for the `explanation` field — that is what it is for.

**Position.** Don't park the answer at one index. You don't have to balance
this by hand:

```bash
docker compose exec api python seeds/fix_quiz_answer_bias.py --dry-run
docker compose exec api python seeds/fix_quiz_answer_bias.py
```

It reorders options and remaps the answer key — option *text* is never
edited — spreading answers evenly across positions within each quiz. It is
deterministic and idempotent, so re-running it changes nothing. It also
prints the worst length tells, which it deliberately does not touch: a
distractor only stops being obviously wrong when someone writes a better one.

`app/services/content/quiz_lint.py` is the same check as a library, for an
authoring tool.

## 15. Checklist before publishing a lesson

- [ ] Explanations are in clear Arabic, not translated-English Arabic.
- [ ] Every technical term appears in English, introduced once as `English (عربي)`.
- [ ] After the first mention, the English term is used consistently.
- [ ] No code, identifier, command, file name or framework name has been translated.
- [ ] Code comments are in English.
- [ ] `technical_terms` lists the dictionary ids the lesson teaches.
- [ ] Any new term was added to `ai-terms.ts` **and** `npm run terminology:export` was run.
- [ ] The linter returns no warnings you did not consciously accept.
- [ ] Quiz distractors are as substantial as the correct answer, and the answer is not parked at one position (`seeds/fix_quiz_answer_bias.py`).

## 16. The test

A finished lesson should feel like it was **written for Arabic-speaking AI learners**, not translated for them — while leaving the student able to open the English documentation for the same topic and recognise every word that matters.
