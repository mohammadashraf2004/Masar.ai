# -*- coding: utf-8 -*-
"""T033 — Deep Learning Foundations, module M05.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 5, 'chapter_title': 'Fundamentals of machine learning', 'source_file': 'تم لصق markdown(20260923-014728).md', 'source_line_ranges': [[631, 845]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Regularization: L1, L2, and Dropout',
    "slug": 'deep-learning-foundations-t033-regularization-l1-l2-and-dropout',
    "description": 'تضيف L1 وL2 عقوبات على المعاملات بينما يعطل dropout تنشيطات أثناء التدريب؛ تؤثر هذه الخيارات بطرق مختلفة.',
    "order": 7,
    "difficulty": 'intermediate',
    "estimated_hours": 1.0,
    "skill_tags": ['deep-learning', 'foundations', 'generalization'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Regularization: L1, L2, and Dropout',
        "content": """# Regularization: L1, L2, and Dropout

**المساق:** أساسيات التعلم العميق · **الوحدة 05:** التعميم وتحسين النماذج · **الدرس T033** · **المدة الموجهة:** 60 دقيقة

## موقف تعليمي

قارن صيغ العقوبات وموقع تطبيق dropout في الرسم الحسابي. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تضيف L1 وL2 عقوبات على المعاملات بينما يعطل dropout تنشيطات أثناء التدريب؛ تؤثر هذه الخيارات بطرق مختلفة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
TRAIN -> MONITOR -> DIAGNOSE -> CONTROLLED CHANGE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن صيغ العقوبات وموقع تطبيق dropout في الرسم الحسابي.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

dropout في الاستدلال لا يُستخدم بنفس سلوك التدريب المعتاد. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن صيغ العقوبات وموقع تطبيق dropout في الرسم الحسابي. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تضيف L1 وL2 عقوبات على المعاملات بينما يعطل dropout تنشيطات أثناء التدريب؛ تؤثر هذه الخيارات بطرق مختلفة. وتذكر القيد التالي: dropout في الاستدلال لا يُستخدم بنفس سلوك التدريب المعتاد.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 5 — Fundamentals of machine learning.
- ملف المصدر: `تم لصق markdown(20260923-014728).md`.
- مواضع الاستناد في المقتطف: L631–L845.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 60,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Regularization: L1, L2, and Dropout', 'description': 'قارن صيغ العقوبات وموقع تطبيق dropout في الرسم الحسابي.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: dropout في الاستدلال لا يُستخدم بنفس سلوك التدريب المعتاد.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'generalization']}],
    "quiz": {'title': 'Regularization: L1, L2, and Dropout — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Regularization: L1, L2, and Dropout»؟', 'options': ['اعتبار فرضية تفسيرية ضماناً على كل عينة.', 'تضيف L1 وL2 عقوبات على المعاملات بينما يعطل dropout تنشيطات أثناء التدريب؛ تؤثر هذه الخيارات بطرق مختلفة.', 'استعمال الاختبار في كل جولة ضبط.', 'إضافة طبقات دون تحليل منحنيات التعلم.'], 'correct': 1, 'explanation': 'تضيف L1 وL2 عقوبات على المعاملات بينما يعطل dropout تنشيطات أثناء التدريب؛ تؤثر هذه الخيارات بطرق مختلفة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Regularization: L1, L2, and Dropout»؟', 'options': ['لا يلزم اختبار أي افتراض في المثال.', 'dropout في الاستدلال لا يُستخدم بنفس سلوك التدريب المعتاد.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.'], 'correct': 1, 'explanation': 'dropout في الاستدلال لا يُستخدم بنفس سلوك التدريب المعتاد.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن صيغ العقوبات وموقع تطبيق dropout في الرسم الحسابي.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M05 — Analyze learning curves and propose controlled remedies.', 'description': 'مشروع Masar أصلي نظري للوحدة: التعميم وتحسين النماذج. المطلوب: Analyze learning curves and propose controlled remedies. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
