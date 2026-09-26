# -*- coding: utf-8 -*-
"""T089 — Deep Learning Foundations, module M13.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 14, 'chapter_title': 'Text classification', 'source_file': 'تم لصق markdown(20260923-015643).md', 'source_line_ranges': [[797, 823], [1217, 1234], [1423, 1452]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Evaluating Text Representations and Complexity',
    "slug": 'deep-learning-foundations-t089-evaluating-text-representations-and-complexity',
    "description": 'تُقارن نماذج النص عبر بيانات وإعدادات متكافئة، وتُوزن المكاسب بالتكلفة والتعميم.',
    "order": 10,
    "difficulty": 'intermediate',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'text'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Evaluating Text Representations and Complexity',
        "content": """# Evaluating Text Representations and Complexity

**المساق:** أساسيات التعلم العميق · **الوحدة 13:** تصنيف النصوص وتمثيل اللغة · **الدرس T089** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

صمم مقارنة بين BoW وembeddings مع تثبيت التقسيم. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تُقارن نماذج النص عبر بيانات وإعدادات متكافئة، وتُوزن المكاسب بالتكلفة والتعميم.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
RAW TEXT -> TOKENS -> REPRESENTATIONS -> CLASS
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صمم مقارنة بين BoW وembeddings مع تثبيت التقسيم.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

الأرقام المنشورة على IMDb لا تحدد ترتيباً عاماً للنماذج. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صمم مقارنة بين BoW وembeddings مع تثبيت التقسيم. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تُقارن نماذج النص عبر بيانات وإعدادات متكافئة، وتُوزن المكاسب بالتكلفة والتعميم. وتذكر القيد التالي: الأرقام المنشورة على IMDb لا تحدد ترتيباً عاماً للنماذج.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 14 — Text classification.
- ملف المصدر: `تم لصق markdown(20260923-015643).md`.
- مواضع الاستناد في المقتطف: L797–L823, L1217–L1234, L1423–L1452.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Evaluating Text Representations and Complexity', 'description': 'صمم مقارنة بين BoW وembeddings مع تثبيت التقسيم.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: الأرقام المنشورة على IMDb لا تحدد ترتيباً عاماً للنماذج.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'text']}],
    "quiz": {'title': 'Evaluating Text Representations and Complexity — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Evaluating Text Representations and Complexity»؟', 'options': ['اعتبار تضمين الكلمات قاموس معانٍ عالمياً.', 'تُقارن نماذج النص عبر بيانات وإعدادات متكافئة، وتُوزن المكاسب بالتكلفة والتعميم.', 'بناء مفردات المهمة من الاختبار النهائي.', 'افتراض أن BoW يحتفظ بترتيب الكلمات كاملاً.'], 'correct': 1, 'explanation': 'تُقارن نماذج النص عبر بيانات وإعدادات متكافئة، وتُوزن المكاسب بالتكلفة والتعميم.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Evaluating Text Representations and Complexity»؟', 'options': ['لا يلزم اختبار أي افتراض في المثال.', 'الأرقام المنشورة على IMDb لا تحدد ترتيباً عاماً للنماذج.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.'], 'correct': 1, 'explanation': 'الأرقام المنشورة على IMDb لا تحدد ترتيباً عاماً للنماذج.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صمم مقارنة بين BoW وembeddings مع تثبيت التقسيم.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M13 — Design a sentiment classifier with a valid evaluation protocol.', 'description': 'مشروع Masar أصلي نظري للوحدة: تصنيف النصوص وتمثيل اللغة. المطلوب: Design a sentiment classifier with a valid evaluation protocol. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'advanced', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
