# -*- coding: utf-8 -*-
"""T039 — Deep Learning Foundations, module M06.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 6, 'chapter_title': 'The universal workflow of machine learning', 'source_file': 'تم لصق markdown(20260923-014830).md', 'source_line_ranges': [[264, 386]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Deployment Architecture and Model Lifecycle',
    "slug": 'deep-learning-foundations-t039-deployment-architecture-and-model-lifecycle',
    "description": 'تشمل دورة النموذج تجهيز مدخلات الاستدلال ومراقبة الأداء واكتشاف تغير البيانات والتحديث المخطط له.',
    "order": 6,
    "difficulty": 'intermediate',
    "estimated_hours": 0.9167,
    "skill_tags": ['deep-learning', 'foundations', 'the'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Deployment Architecture and Model Lifecycle',
        "content": """# Deployment Architecture and Model Lifecycle

**المساق:** أساسيات التعلم العميق · **الوحدة 06:** سير عمل التعلم الآلي · **الدرس T039** · **المدة الموجهة:** 55 دقيقة

## موقف تعليمي

ارسم مخطط نموذج إنتاجي مع مراقبة المدخلات والمخرجات ومراجعة دورية. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تشمل دورة النموذج تجهيز مدخلات الاستدلال ومراقبة الأداء واكتشاف تغير البيانات والتحديث المخطط له.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
PROBLEM -> DATA -> BASELINE -> EVALUATION -> LIFECYCLE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم مخطط نموذج إنتاجي مع مراقبة المدخلات والمخرجات ومراجعة دورية.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

التصميم مفاهيمي؛ نشر API فعلي خارج نطاق هذا المساق. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم مخطط نموذج إنتاجي مع مراقبة المدخلات والمخرجات ومراجعة دورية. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تشمل دورة النموذج تجهيز مدخلات الاستدلال ومراقبة الأداء واكتشاف تغير البيانات والتحديث المخطط له. وتذكر القيد التالي: التصميم مفاهيمي؛ نشر API فعلي خارج نطاق هذا المساق.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 6 — The universal workflow of machine learning.
- ملف المصدر: `تم لصق markdown(20260923-014830).md`.
- مواضع الاستناد في المقتطف: L264–L386.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 55,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Deployment Architecture and Model Lifecycle', 'description': 'ارسم مخطط نموذج إنتاجي مع مراقبة المدخلات والمخرجات ومراجعة دورية.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: التصميم مفاهيمي؛ نشر API فعلي خارج نطاق هذا المساق.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'the']}],
    "quiz": {'title': 'Deployment Architecture and Model Lifecycle — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Deployment Architecture and Model Lifecycle»؟', 'options': ['نشر نموذج دون تعريف معيار نجاح.', 'افتراض تمثيل البيانات للاستخدام الفعلي دون فحص.', 'تغيير كل عناصر التجربة معاً.', 'تشمل دورة النموذج تجهيز مدخلات الاستدلال ومراقبة الأداء واكتشاف تغير البيانات والتحديث المخطط له.'], 'correct': 3, 'explanation': 'تشمل دورة النموذج تجهيز مدخلات الاستدلال ومراقبة الأداء واكتشاف تغير البيانات والتحديث المخطط له.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Deployment Architecture and Model Lifecycle»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'التصميم مفاهيمي؛ نشر API فعلي خارج نطاق هذا المساق.'], 'correct': 3, 'explanation': 'التصميم مفاهيمي؛ نشر API فعلي خارج نطاق هذا المساق.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم مخطط نموذج إنتاجي مع مراقبة المدخلات والمخرجات ومراجعة دورية.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M06 — Design an end-to-end industrial-defect solution on paper.', 'description': 'مشروع Masar أصلي نظري للوحدة: سير عمل التعلم الآلي. المطلوب: Design an end-to-end industrial-defect solution on paper. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
