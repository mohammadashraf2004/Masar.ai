# -*- coding: utf-8 -*-
"""T128 — Deep Learning Foundations, module M16.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 17, 'chapter_title': 'Image generation', 'source_file': 'تم لصق markdown(20260923-020252).md', 'source_line_ranges': [[861, 1004]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Generative Representation Interpolation',
    "slug": 'deep-learning-foundations-t128-generative-representation-interpolation',
    "description": 'يغير استيفاء متجهات النص المشروط الصورة، ويمكن استخدام SLERP كاختيار هندسي مع ضرورة تثبيت العشوائية.',
    "order": 11,
    "difficulty": 'advanced',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'generative'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Generative Representation Interpolation',
        "content": """# Generative Representation Interpolation

**المساق:** أساسيات التعلم العميق · **الوحدة 16:** نماذج توليد الصور والفضاءات الكامنة · **الدرس T128** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

خطط لتدرج وصفين باستخدام ضوضاء بداية ثابتة. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يغير استيفاء متجهات النص المشروط الصورة، ويمكن استخدام SLERP كاختيار هندسي مع ضرورة تثبيت العشوائية.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
LATENT / NOISE + CONDITION -> GENERATOR -> IMAGE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

خطط لتدرج وصفين باستخدام ضوضاء بداية ثابتة.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

كل صورة في كود المصدر تستخدم ضوضاء جديدة؛ لا تعزُ الفرق للاستيفاء وحده. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

خطط لتدرج وصفين باستخدام ضوضاء بداية ثابتة. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يغير استيفاء متجهات النص المشروط الصورة، ويمكن استخدام SLERP كاختيار هندسي مع ضرورة تثبيت العشوائية. وتذكر القيد التالي: كل صورة في كود المصدر تستخدم ضوضاء جديدة؛ لا تعزُ الفرق للاستيفاء وحده.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 17 — Image generation.
- ملف المصدر: `تم لصق markdown(20260923-020252).md`.
- مواضع الاستناد في المقتطف: L861–L1004.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Generative Representation Interpolation', 'description': 'خطط لتدرج وصفين باستخدام ضوضاء بداية ثابتة.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: كل صورة في كود المصدر تستخدم ضوضاء جديدة؛ لا تعزُ الفرق للاستيفاء وحده.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'generative']}],
    "quiz": {'title': 'Generative Representation Interpolation — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Generative Representation Interpolation»؟', 'options': ['يغير استيفاء متجهات النص المشروط الصورة، ويمكن استخدام SLERP كاختيار هندسي مع ضرورة تثبيت العشوائية.', 'اعتبار أي متجه كامن صورة صحيحة مضمونة.', 'الخلط بين توليد الضوضاء وتدريب المصنف.', 'استنتاج أثر النص من صور ببذور عشوائية مختلفة.'], 'correct': 0, 'explanation': 'يغير استيفاء متجهات النص المشروط الصورة، ويمكن استخدام SLERP كاختيار هندسي مع ضرورة تثبيت العشوائية.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Generative Representation Interpolation»؟', 'options': ['كل صورة في كود المصدر تستخدم ضوضاء جديدة؛ لا تعزُ الفرق للاستيفاء وحده.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'كل صورة في كود المصدر تستخدم ضوضاء جديدة؛ لا تعزُ الفرق للاستيفاء وحده.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: خطط لتدرج وصفين باستخدام ضوضاء بداية ثابتة.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M16 — Design and critique a text-to-image pipeline.', 'description': 'مشروع Masar أصلي نظري للوحدة: نماذج توليد الصور والفضاءات الكامنة. المطلوب: Design and critique a text-to-image pipeline. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'advanced', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
