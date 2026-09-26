# -*- coding: utf-8 -*-
"""T117 — Deep Learning Foundations, module M15.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 16, 'chapter_title': 'Text generation', 'source_file': 'تم لصق markdown(20260923-020108).md', 'source_line_ranges': [[1285, 1323]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'LLM Scaling, Resources, and Limitations',
    "slug": 'deep-learning-foundations-t117-llm-scaling-resources-and-limitations',
    "description": 'يتوقف تصميم نموذج توليدي على البيانات والعتاد والذاكرة وكلفة الاستدلال وتقييم المخرجات.',
    "order": 14,
    "difficulty": 'advanced',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'generative'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'LLM Scaling, Resources, and Limitations',
        "content": """# LLM Scaling, Resources, and Limitations

**المساق:** أساسيات التعلم العميق · **الوحدة 15:** النماذج اللغوية التوليدية وأساسيات LLM · **الدرس T117** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

قارن مشروعين أحدهما أكبر حجماً والآخر أقل تكلفة واكتب ما يلزم قياسه. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يتوقف تصميم نموذج توليدي على البيانات والعتاد والذاكرة وكلفة الاستدلال وتقييم المخرجات.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
CORPUS -> PRETRAINED MODEL -> ADAPTATION -> GENERATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن مشروعين أحدهما أكبر حجماً والآخر أقل تكلفة واكتب ما يلزم قياسه.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

توقعات السوق والمستقبل الواردة في الكتاب آراء تاريخية. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن مشروعين أحدهما أكبر حجماً والآخر أقل تكلفة واكتب ما يلزم قياسه. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يتوقف تصميم نموذج توليدي على البيانات والعتاد والذاكرة وكلفة الاستدلال وتقييم المخرجات. وتذكر القيد التالي: توقعات السوق والمستقبل الواردة في الكتاب آراء تاريخية.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 16 — Text generation.
- ملف المصدر: `تم لصق markdown(20260923-020108).md`.
- مواضع الاستناد في المقتطف: L1285–L1323.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — LLM Scaling, Resources, and Limitations', 'description': 'قارن مشروعين أحدهما أكبر حجماً والآخر أقل تكلفة واكتب ما يلزم قياسه.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: توقعات السوق والمستقبل الواردة في الكتاب آراء تاريخية.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'generative']}],
    "quiz": {'title': 'LLM Scaling, Resources, and Limitations — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «LLM Scaling, Resources, and Limitations»؟', 'options': ['اعتبار توفير معاملات LoRA توفيراً لكل الذاكرة.', 'يتوقف تصميم نموذج توليدي على البيانات والعتاد والذاكرة وكلفة الاستدلال وتقييم المخرجات.', 'اعتبار النص المتولد دليلاً على صدقه.', 'الخلط بين تعديل أوزان النموذج واسترجاع وثائق.'], 'correct': 1, 'explanation': 'يتوقف تصميم نموذج توليدي على البيانات والعتاد والذاكرة وكلفة الاستدلال وتقييم المخرجات.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «LLM Scaling, Resources, and Limitations»؟', 'options': ['لا يلزم اختبار أي افتراض في المثال.', 'توقعات السوق والمستقبل الواردة في الكتاب آراء تاريخية.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.'], 'correct': 1, 'explanation': 'توقعات السوق والمستقبل الواردة في الكتاب آراء تاريخية.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن مشروعين أحدهما أكبر حجماً والآخر أقل تكلفة واكتب ما يلزم قياسه.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M15 — Design a grounded AI assistant without deploying it.', 'description': 'مشروع Masar أصلي نظري للوحدة: النماذج اللغوية التوليدية وأساسيات LLM. المطلوب: Design a grounded AI assistant without deploying it. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'advanced', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
