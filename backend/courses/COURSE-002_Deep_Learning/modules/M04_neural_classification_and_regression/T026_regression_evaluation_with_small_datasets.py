# -*- coding: utf-8 -*-
"""T026 — Deep Learning Foundations, module M04.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 4, 'chapter_title': 'Classification and regression', 'source_file': 'تم لصق markdown(20260923-014601).md', 'source_line_ranges': [[949, 1143]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Regression Evaluation with Small Datasets',
    "slug": 'deep-learning-foundations-t026-regression-evaluation-with-small-datasets',
    "description": 'تزيد العينات القليلة تباين تقدير الأداء؛ قد تساعد طرق التحقق المتكرر وتقييس الخصائص اعتماداً على التدريب فقط.',
    "order": 7,
    "difficulty": 'beginner',
    "estimated_hours": 0.9167,
    "skill_tags": ['deep-learning', 'foundations', 'neural'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Regression Evaluation with Small Datasets',
        "content": """# Regression Evaluation with Small Datasets

**المساق:** أساسيات التعلم العميق · **الوحدة 04:** التصنيف والانحدار بالشبكات العصبية · **الدرس T026** · **المدة الموجهة:** 55 دقيقة

## موقف تعليمي

خطط لتحقق K-fold واحسب متوسط أخطاء الطيات مع إبقاء اختبار منفصل. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تزيد العينات القليلة تباين تقدير الأداء؛ قد تساعد طرق التحقق المتكرر وتقييس الخصائص اعتماداً على التدريب فقط.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
DATA -> OUTPUT HEAD -> LOSS -> VALIDATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

خطط لتحقق K-fold واحسب متوسط أخطاء الطيات مع إبقاء اختبار منفصل.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

تقييس كامل البيانات قبل الفصل ينقل معلومات من التحقق للتدريب. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

خطط لتحقق K-fold واحسب متوسط أخطاء الطيات مع إبقاء اختبار منفصل. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تزيد العينات القليلة تباين تقدير الأداء؛ قد تساعد طرق التحقق المتكرر وتقييس الخصائص اعتماداً على التدريب فقط. وتذكر القيد التالي: تقييس كامل البيانات قبل الفصل ينقل معلومات من التحقق للتدريب.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 4 — Classification and regression.
- ملف المصدر: `تم لصق markdown(20260923-014601).md`.
- مواضع الاستناد في المقتطف: L949–L1143.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 55,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Regression Evaluation with Small Datasets', 'description': 'خطط لتحقق K-fold واحسب متوسط أخطاء الطيات مع إبقاء اختبار منفصل.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: تقييس كامل البيانات قبل الفصل ينقل معلومات من التحقق للتدريب.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'neural']}],
    "quiz": {'title': 'Regression Evaluation with Small Datasets — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Regression Evaluation with Small Datasets»؟', 'options': ['اختيار النموذج من دقة التدريب فقط.', 'اعتبار خسارة الانحدار والتصنيف متطابقتين.', 'تزيد العينات القليلة تباين تقدير الأداء؛ قد تساعد طرق التحقق المتكرر وتقييس الخصائص اعتماداً على التدريب فقط.', 'تحديد المخرج بمعزل عن ترميز الأهداف.'], 'correct': 2, 'explanation': 'تزيد العينات القليلة تباين تقدير الأداء؛ قد تساعد طرق التحقق المتكرر وتقييس الخصائص اعتماداً على التدريب فقط.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Regression Evaluation with Small Datasets»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'تقييس كامل البيانات قبل الفصل ينقل معلومات من التحقق للتدريب.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'تقييس كامل البيانات قبل الفصل ينقل معلومات من التحقق للتدريب.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: خطط لتحقق K-fold واحسب متوسط أخطاء الطيات مع إبقاء اختبار منفصل.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M04 — Design classification and regression experiments with protected evaluation.', 'description': 'مشروع Masar أصلي نظري للوحدة: التصنيف والانحدار بالشبكات العصبية. المطلوب: Design classification and regression experiments with protected evaluation. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
