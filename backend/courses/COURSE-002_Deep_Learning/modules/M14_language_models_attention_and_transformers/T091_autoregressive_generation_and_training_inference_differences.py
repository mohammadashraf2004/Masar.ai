# -*- coding: utf-8 -*-
"""T091 — Deep Learning Foundations, module M14.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 15, 'chapter_title': 'Language models and the Transformer', 'source_file': 'تم لصق markdown(20260923-015925).md', 'source_line_ranges': [[195, 303]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Autoregressive Generation and Training-Inference Differences',
    "slug": 'deep-learning-foundations-t091-autoregressive-generation-and-training-inference-differences',
    "description": 'تكرر عملية التوليد التنبؤ بالرمز ثم إعادته كجزء من السياق، بخلاف التدريب الذي قد يملك رموزاً مرجعية.',
    "order": 2,
    "difficulty": 'advanced',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'language'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Autoregressive Generation and Training-Inference Differences',
        "content": """# Autoregressive Generation and Training-Inference Differences

**المساق:** أساسيات التعلم العميق · **الوحدة 14:** النماذج اللغوية والانتباه والمحوّلات · **الدرس T091** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

تتبع توليد خمسة رموز وسجل السياق في كل خطوة. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تكرر عملية التوليد التنبؤ بالرمز ثم إعادته كجزء من السياق، بخلاف التدريب الذي قد يملك رموزاً مرجعية.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
TOKENS -> EMBEDDINGS -> ATTENTION -> NEXT TOKEN
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

تتبع توليد خمسة رموز وسجل السياق في كل خطوة.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

رمز خاطئ مبكر قد يؤثر في المخرجات التالية. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

تتبع توليد خمسة رموز وسجل السياق في كل خطوة. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تكرر عملية التوليد التنبؤ بالرمز ثم إعادته كجزء من السياق، بخلاف التدريب الذي قد يملك رموزاً مرجعية. وتذكر القيد التالي: رمز خاطئ مبكر قد يؤثر في المخرجات التالية.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 15 — Language models and the Transformer.
- ملف المصدر: `تم لصق markdown(20260923-015925).md`.
- مواضع الاستناد في المقتطف: L195–L303.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Autoregressive Generation and Training-Inference Differences', 'description': 'تتبع توليد خمسة رموز وسجل السياق في كل خطوة.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: رمز خاطئ مبكر قد يؤثر في المخرجات التالية.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'language']}],
    "quiz": {'title': 'Autoregressive Generation and Training-Inference Differences — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Autoregressive Generation and Training-Inference Differences»؟', 'options': ['السماح للمفكك برؤية رموز الهدف المستقبلية.', 'إهمال توافق أبعاد Q وK وV.', 'اعتبار دقة الرمز معيار جودة ترجمة كافياً.', 'تكرر عملية التوليد التنبؤ بالرمز ثم إعادته كجزء من السياق، بخلاف التدريب الذي قد يملك رموزاً مرجعية.'], 'correct': 3, 'explanation': 'تكرر عملية التوليد التنبؤ بالرمز ثم إعادته كجزء من السياق، بخلاف التدريب الذي قد يملك رموزاً مرجعية.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Autoregressive Generation and Training-Inference Differences»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'رمز خاطئ مبكر قد يؤثر في المخرجات التالية.'], 'correct': 3, 'explanation': 'رمز خاطئ مبكر قد يؤثر في المخرجات التالية.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: تتبع توليد خمسة رموز وسجل السياق في كل خطوة.', 'type': 'open'}], 'passing_score': 70},
}
