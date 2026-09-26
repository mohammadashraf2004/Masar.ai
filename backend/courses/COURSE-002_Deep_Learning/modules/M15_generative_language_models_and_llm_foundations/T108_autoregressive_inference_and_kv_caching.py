# -*- coding: utf-8 -*-
"""T108 — Deep Learning Foundations, module M15.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 16, 'chapter_title': 'Text generation', 'source_file': 'تم لصق markdown(20260923-020108).md', 'source_line_ranges': [[389, 464]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Autoregressive Inference and KV Caching',
    "slug": 'deep-learning-foundations-t108-autoregressive-inference-and-kv-caching',
    "description": 'يخفض KV cache إعادة حساب مفاتيح وقيم الرموز السابقة أثناء فك الترميز المتتابع.',
    "order": 5,
    "difficulty": 'advanced',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'generative'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Autoregressive Inference and KV Caching',
        "content": """# Autoregressive Inference and KV Caching

**المساق:** أساسيات التعلم العميق · **الوحدة 15:** النماذج اللغوية التوليدية وأساسيات LLM · **الدرس T108** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

ارسم مرحلتي prefill وdecode وقارن مع إعادة حساب كامل السياق. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يخفض KV cache إعادة حساب مفاتيح وقيم الرموز السابقة أثناء فك الترميز المتتابع.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
CORPUS -> PRETRAINED MODEL -> ADAPTATION -> GENERATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم مرحلتي prefill وdecode وقارن مع إعادة حساب كامل السياق.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

التجميع والتخزين المؤقت يعالجان عنقَي زجاجة مختلفين. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم مرحلتي prefill وdecode وقارن مع إعادة حساب كامل السياق. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يخفض KV cache إعادة حساب مفاتيح وقيم الرموز السابقة أثناء فك الترميز المتتابع. وتذكر القيد التالي: التجميع والتخزين المؤقت يعالجان عنقَي زجاجة مختلفين.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 16 — Text generation.
- ملف المصدر: `تم لصق markdown(20260923-020108).md`.
- مواضع الاستناد في المقتطف: L389–L464.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Autoregressive Inference and KV Caching', 'description': 'ارسم مرحلتي prefill وdecode وقارن مع إعادة حساب كامل السياق.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: التجميع والتخزين المؤقت يعالجان عنقَي زجاجة مختلفين.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'generative']}],
    "quiz": {'title': 'Autoregressive Inference and KV Caching — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Autoregressive Inference and KV Caching»؟', 'options': ['يخفض KV cache إعادة حساب مفاتيح وقيم الرموز السابقة أثناء فك الترميز المتتابع.', 'اعتبار النص المتولد دليلاً على صدقه.', 'الخلط بين تعديل أوزان النموذج واسترجاع وثائق.', 'اعتبار توفير معاملات LoRA توفيراً لكل الذاكرة.'], 'correct': 0, 'explanation': 'يخفض KV cache إعادة حساب مفاتيح وقيم الرموز السابقة أثناء فك الترميز المتتابع.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Autoregressive Inference and KV Caching»؟', 'options': ['التجميع والتخزين المؤقت يعالجان عنقَي زجاجة مختلفين.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'التجميع والتخزين المؤقت يعالجان عنقَي زجاجة مختلفين.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم مرحلتي prefill وdecode وقارن مع إعادة حساب كامل السياق.', 'type': 'open'}], 'passing_score': 70},
}
