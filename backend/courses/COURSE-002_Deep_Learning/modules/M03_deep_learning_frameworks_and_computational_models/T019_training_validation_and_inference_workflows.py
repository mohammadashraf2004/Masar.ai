# -*- coding: utf-8 -*-
"""T019 — Deep Learning Foundations, module M03.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 3, 'chapter_title': 'Introduction to TensorFlow, PyTorch, JAX, and Keras', 'source_file': 'تم لصق markdown(20260923-014500).md', 'source_line_ranges': [[1560, 1669]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Training, Validation, and Inference Workflows',
    "slug": 'deep-learning-foundations-t019-training-validation-and-inference-workflows',
    "description": 'التدريب يغير المعاملات؛ التحقق يقيس خيارات التطوير؛ والاستدلال يستخدم النموذج المتعلم على بيانات جديدة.',
    "order": 8,
    "difficulty": 'beginner',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'deep'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Training, Validation, and Inference Workflows',
        "content": """# Training, Validation, and Inference Workflows

**المساق:** أساسيات التعلم العميق · **الوحدة 03:** أطر العمل ونماذج الحوسبة · **الدرس T019** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

صنّف خمس عمليات إلى تدريب أو تحقق أو استدلال وحدد مكان تحديث الأوزان. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

التدريب يغير المعاملات؛ التحقق يقيس خيارات التطوير؛ والاستدلال يستخدم النموذج المتعلم على بيانات جديدة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
INPUT -> TENSOR OPS -> AUTOGRAD -> OPTIMIZER
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صنّف خمس عمليات إلى تدريب أو تحقق أو استدلال وحدد مكان تحديث الأوزان.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

لا تستخدم الاختبار النهائي لضبط النموذج مرات متتابعة. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صنّف خمس عمليات إلى تدريب أو تحقق أو استدلال وحدد مكان تحديث الأوزان. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

التدريب يغير المعاملات؛ التحقق يقيس خيارات التطوير؛ والاستدلال يستخدم النموذج المتعلم على بيانات جديدة. وتذكر القيد التالي: لا تستخدم الاختبار النهائي لضبط النموذج مرات متتابعة.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 3 — Introduction to TensorFlow, PyTorch, JAX, and Keras.
- ملف المصدر: `تم لصق markdown(20260923-014500).md`.
- مواضع الاستناد في المقتطف: L1560–L1669.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Training, Validation, and Inference Workflows', 'description': 'صنّف خمس عمليات إلى تدريب أو تحقق أو استدلال وحدد مكان تحديث الأوزان.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: لا تستخدم الاختبار النهائي لضبط النموذج مرات متتابعة.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'deep']}],
    "quiz": {'title': 'Training, Validation, and Inference Workflows — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Training, Validation, and Inference Workflows»؟', 'options': ['افتراض أن أسماء واجهات البرمجة هي المفاهيم الرياضية نفسها.', 'اختيار الإطار بدلاً من صياغة المهمة.', 'الاعتماد على مخطط لا يحتوي بيانات أو خسارة.', 'التدريب يغير المعاملات؛ التحقق يقيس خيارات التطوير؛ والاستدلال يستخدم النموذج المتعلم على بيانات جديدة.'], 'correct': 3, 'explanation': 'التدريب يغير المعاملات؛ التحقق يقيس خيارات التطوير؛ والاستدلال يستخدم النموذج المتعلم على بيانات جديدة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Training, Validation, and Inference Workflows»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'لا تستخدم الاختبار النهائي لضبط النموذج مرات متتابعة.'], 'correct': 3, 'explanation': 'لا تستخدم الاختبار النهائي لضبط النموذج مرات متتابعة.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صنّف خمس عمليات إلى تدريب أو تحقق أو استدلال وحدد مكان تحديث الأوزان.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M03 — Compare two framework-neutral training workflow diagrams.', 'description': 'مشروع Masar أصلي نظري للوحدة: أطر العمل ونماذج الحوسبة. المطلوب: Compare two framework-neutral training workflow diagrams. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
