# -*- coding: utf-8 -*-
"""T052 — Deep Learning Foundations, module M08.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 9, 'chapter_title': 'ConvNet architecture patterns', 'source_file': 'تم لصق markdown(20260923-015121).md', 'source_line_ranges': [[380, 390]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Introduction to Vision Transformers',
    "slug": 'deep-learning-foundations-t052-introduction-to-vision-transformers',
    "description": 'تحول محولات الرؤية الصورة إلى رقع ممثلة كتسلسل، بخلاف انحياز الالتفاف المحلي.',
    "order": 6,
    "difficulty": 'intermediate',
    "estimated_hours": 0.5833,
    "skill_tags": ['deep-learning', 'foundations', 'advanced'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Introduction to Vision Transformers',
        "content": """# Introduction to Vision Transformers

**المساق:** أساسيات التعلم العميق · **الوحدة 08:** مبادئ معماريات CNN المتقدمة · **الدرس T052** · **المدة الموجهة:** 35 دقيقة

## موقف تعليمي

قارن طريقة تقسيم الصورة في CNN ومحولات الرؤية. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تحول محولات الرؤية الصورة إلى رقع ممثلة كتسلسل، بخلاف انحياز الالتفاف المحلي.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> REUSABLE BLOCKS -> FEATURE PYRAMID -> HEAD
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن طريقة تقسيم الصورة في CNN ومحولات الرؤية.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

التعمق في المحولات مؤجل للفصل الخامس عشر. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن طريقة تقسيم الصورة في CNN ومحولات الرؤية. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تحول محولات الرؤية الصورة إلى رقع ممثلة كتسلسل، بخلاف انحياز الالتفاف المحلي. وتذكر القيد التالي: التعمق في المحولات مؤجل للفصل الخامس عشر.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 9 — ConvNet architecture patterns.
- ملف المصدر: `تم لصق markdown(20260923-015121).md`.
- مواضع الاستناد في المقتطف: L380–L390.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 35,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Introduction to Vision Transformers', 'description': 'قارن طريقة تقسيم الصورة في CNN ومحولات الرؤية.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: التعمق في المحولات مؤجل للفصل الخامس عشر.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'advanced']}],
    "quiz": {'title': 'Introduction to Vision Transformers — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Introduction to Vision Transformers»؟', 'options': ['تحول محولات الرؤية الصورة إلى رقع ممثلة كتسلسل، بخلاف انحياز الالتفاف المحلي.', 'جمع فروع غير متوافقة أبعادها.', 'استنتاج زمن GPU من عدد المعاملات فقط.', 'اعتبار خيار ترتيب الطبقات قانوناً مطلقاً.'], 'correct': 0, 'explanation': 'تحول محولات الرؤية الصورة إلى رقع ممثلة كتسلسل، بخلاف انحياز الالتفاف المحلي.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Introduction to Vision Transformers»؟', 'options': ['التعمق في المحولات مؤجل للفصل الخامس عشر.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'التعمق في المحولات مؤجل للفصل الخامس عشر.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن طريقة تقسيم الصورة في CNN ومحولات الرؤية.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M08 — Design an efficient CNN architecture and a controlled ablation.', 'description': 'مشروع Masar أصلي نظري للوحدة: مبادئ معماريات CNN المتقدمة. المطلوب: Design an efficient CNN architecture and a controlled ablation. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
