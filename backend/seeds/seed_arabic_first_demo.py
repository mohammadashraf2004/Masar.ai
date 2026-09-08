"""
backend/seeds/seed_arabic_first_demo.py

Publishes the Arabic-first version of the first LangChain topic, and tags
the course with the terminology it teaches.

This is the reference implementation of docs/content/ARABIC_FIRST_GUIDELINES.md
— a worked example an author can read next to the guidelines to see exactly
what "Arabic explanation, English terminology, untouched code" looks like in
practice, and to verify the reader-side behaviour end to end (language
switch, first-mention chips, vocabulary panel, bilingual search).

It only ever *adds* Arabic alongside the existing English. No English field
is modified, so the course renders exactly as before for a reader who
chooses English.

Idempotent — safe to re-run. Requires seeds/seed_tool_courses.py and
seeds/seed_tool_langchain.py to have run first.

Run from backend/:
    docker compose exec api python seeds/seed_arabic_first_demo.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal
import app.models.user, app.models.learning, app.models.progress      # noqa: F401
import app.models.community, app.models.wallet, app.models.auth_token  # noqa: F401
import app.models.challenge, app.models.exam, app.models.vocabulary    # noqa: F401
from app.models.learning import Lesson
from app.models.tool_course import ToolCourse, ToolTopic

TOOL_SLUG = "langchain"
TOPIC_SLUG = "what-is-langchain"

# ── Course-level metadata ────────────────────────────────────────────────
# `technical_terms` are ids from app/content/ai_terms.json; `industry_skills`
# are the words a recruiter puts in a job posting.
COURSE = {
    "title_ar": "LangChain",
    "description_ar": (
        "ابنِ تطبيقات LLM باستخدام chains و prompts و models و output parsers — "
        "الـ framework الأكثر طلباً في مقابلات الـ AI Developer."
    ),
    "technical_terms": [
        "large_language_model",
        "prompt",
        "prompt_engineering",
        "structured_output",
        "data_pipeline",
        "framework",
        "retrieval_augmented_generation",
        "embeddings",
        "vector_database",
        "agent",
        "tool_calling",
    ],
    "industry_skills": ["LLM", "LangChain", "Prompt Engineering", "RAG"],
}

TOPIC = {
    "title_ar": "ما هو LangChain؟",
    "description_ar": (
        "المشكلة التي يحلّها LangChain، والطريقة الصحيحة للتفكير فيه، "
        "والمفاهيم الخمسة الأساسية التي تبدأ بها."
    ),
    "technical_terms": [
        "large_language_model",
        "framework",
        "data_pipeline",
        "prompt",
        "structured_output",
    ],
}

# ── The lesson ───────────────────────────────────────────────────────────
# Written Arabic-first, not translated:
#   * every technical term is introduced once as `English (عربي)` and then
#     used in English;
#   * the code block is byte-identical to what an English lesson would show;
#   * the ASCII diagram stays in English, because that is what the student
#     will see in the library's own documentation.
LESSON_TITLE_AR = "ما هو LangChain؟"

LESSON_CONTENT_AR = """# ما هو LangChain؟

قبل ما تكتب أي كود، لازم تفهم المشكلة التي يحلّها LangChain.

## الحالة البسيطة

لو عندك Large Language Model (نموذج لغوي كبير)، فالصورة تبدو كالتالي:

```
User -> Question -> LLM -> Answer
```

بسيطة، وتقدر تنفّذها باستدعاء API واحد.

## الحالة الحقيقية

التطبيق الحقيقي نادراً ما يكون بهذه البساطة. غالباً يبدو كالتالي:

```
User question
  -> retrieve relevant documents
  -> build a prompt from them
  -> call the LLM
  -> parse the answer into JSON
  -> validate it
  -> store it
```

كل خطوة من دول تُغذّي التي بعدها، وهذا ما نسميه Pipeline (مسار المعالجة).

المشكلة أنك لو كتبت هذا الـ pipeline يدوياً في كل مرة، ستجد نفسك تعيد كتابة
نفس الأكواد: تجهيز الـ Prompt (الأمر النصي)، وإدارة الأخطاء، وتحويل رد النموذج
من نص حر إلى Structured Output (إخراج منظم) يستطيع الكود التعامل معه.

## أين يقع LangChain

LangChain هو Framework (إطار عمل) يعطيك مكوّنات جاهزة لكل خطوة، وطريقة موحّدة
لتركيبها مع بعض:

| المكوّن | وظيفته |
|---|---|
| Models | الاتصال بالـ LLM |
| Prompt Templates | بناء الـ prompt من متغيرات |
| Output Parsers | تحويل رد النموذج إلى صيغة يقرأها الكود |
| Chains | ربط الخطوات في pipeline واحد |
| Retrievers | جلب المستندات المرتبطة بالسؤال |

> النقطة المهمة: LangChain لا يجعل النموذج أذكى. هو ينظّم الكود حول النموذج.

## مثال عملي

الكود نفسه لا يتغيّر بتغيّر لغة الشرح — أسماء الـ classes والـ functions
والـ parameters تُكتب كما هي في التوثيق الرسمي:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} to a first-year engineering student."
)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | model | StrOutputParser()

answer = chain.invoke({"topic": "vector databases"})
print(answer)
```

الثلاث خطوات دي (`prompt | model | parser`) هي أبسط chain ممكن، وهي نفس النمط
الذي ستبني عليه لاحقاً أنظمة Retrieval-Augmented Generation (التوليد المعزز
بالاسترجاع) وأنظمة الـ AI Agent (وكيل ذكاء اصطناعي).

## متى لا تحتاج LangChain

لو تطبيقك عبارة عن استدعاء واحد للنموذج بدون خطوات قبله أو بعده، فاستدعاء
الـ API مباشرة أبسط وأوضح. LangChain يبدأ يستحق قيمته عندما يصبح عندك
pipeline حقيقي بأكثر من خطوة.

## المصطلحات في هذا الدرس

LLM · Framework · Pipeline · Prompt · Structured Output · Chain · Retriever

## سؤال مقابلة

> What does LangChain actually give you over calling the model API directly?

الإجابة المتوقعة: مكوّنات موحّدة لكل خطوة في الـ pipeline (prompting، parsing،
retrieval، memory)، وطريقة قياسية لتركيبها، بدل إعادة كتابة نفس الكود في كل
مشروع — وليس تحسين جودة النموذج نفسه.
"""


def main() -> None:
    db = SessionLocal()
    try:
        course = db.query(ToolCourse).filter(ToolCourse.slug == TOOL_SLUG).first()
        if not course:
            print(f"✗ tool course '{TOOL_SLUG}' not found — run seeds/seed_tool_courses.py first")
            return

        for field, value in COURSE.items():
            setattr(course, field, value)
        print(f"✓ course '{course.title}': Arabic metadata + {len(COURSE['technical_terms'])} terms")

        topic = (
            db.query(ToolTopic)
            .filter(ToolTopic.tool_course_id == course.id, ToolTopic.slug == TOPIC_SLUG)
            .first()
        )
        if not topic:
            print(f"✗ topic '{TOPIC_SLUG}' not found — run seeds/seed_tool_langchain.py first")
            db.commit()
            return

        for field, value in TOPIC.items():
            setattr(topic, field, value)
        print(f"✓ topic '{topic.title}': Arabic metadata")

        lesson = (
            db.query(Lesson)
            .filter(Lesson.tool_topic_id == topic.id)
            .order_by(Lesson.order)
            .first()
        )
        if lesson:
            lesson.title_ar = LESSON_TITLE_AR
            lesson.content_ar = LESSON_CONTENT_AR
            print(f"✓ lesson '{lesson.title}': Arabic body ({len(LESSON_CONTENT_AR)} chars)")
        else:
            print(f"! topic '{TOPIC_SLUG}' has no lesson to publish an Arabic body for")

        db.commit()
        print("\nDone. Open /tools/langchain and switch the language control to العربية.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
