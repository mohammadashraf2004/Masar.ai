# -*- coding: utf-8 -*-
"""T046 — Deep Learning Foundations, module M07.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 8, 'chapter_title': 'Image classification', 'source_file': 'تم لصق markdown(20260923-015008).md', 'source_line_ranges': [[997, 1174]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Fine-Tuning and Transfer Learning Trade-offs',
    "slug": 'deep-learning-foundations-t046-fine-tuning-and-transfer-learning-trade-offs',
    "description": 'يفتح الضبط الدقيق جزءاً من النموذج المدرب سابقاً بمعدل تعلم مناسب مع الحذر من فرط الملاءمة وتغير توزيع البيانات.',
    "order": 7,
    "difficulty": 'intermediate',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'image'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Fine-Tuning and Transfer Learning Trade-offs',
        "content": """# Fine-Tuning and Transfer Learning Trade-offs

**المساق:** أساسيات التعلم العميق · **الوحدة 07:** تصنيف الصور وأساسيات الشبكات الالتفافية · **الدرس T046** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

قارن استخراج المميزات المجمدة بضبط بعض الطبقات وناقش التكلفة والمخاطر. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يفتح الضبط الدقيق جزءاً من النموذج المدرب سابقاً بمعدل تعلم مناسب مع الحذر من فرط الملاءمة وتغير توزيع البيانات.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> CONV FEATURES -> CLASS HEAD -> PREDICTION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن استخراج المميزات المجمدة بضبط بعض الطبقات وناقش التكلفة والمخاطر.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

لا تعد نتائج المصدر أو تحسن الضبط الدقيق ضماناً عاماً. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن استخراج المميزات المجمدة بضبط بعض الطبقات وناقش التكلفة والمخاطر. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يفتح الضبط الدقيق جزءاً من النموذج المدرب سابقاً بمعدل تعلم مناسب مع الحذر من فرط الملاءمة وتغير توزيع البيانات. وتذكر القيد التالي: لا تعد نتائج المصدر أو تحسن الضبط الدقيق ضماناً عاماً.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 8 — Image classification.
- ملف المصدر: `تم لصق markdown(20260923-015008).md`.
- مواضع الاستناد في المقتطف: L997–L1174.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Fine-Tuning and Transfer Learning Trade-offs', 'description': 'قارن استخراج المميزات المجمدة بضبط بعض الطبقات وناقش التكلفة والمخاطر.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: لا تعد نتائج المصدر أو تحسن الضبط الدقيق ضماناً عاماً.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'image']}],
    "quiz": {'title': 'Fine-Tuning and Transfer Learning Trade-offs — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Fine-Tuning and Transfer Learning Trade-offs»؟', 'options': ['افتراض أن أي تعديل للصورة يحفظ الفئة.', 'اعتماد تحسن المصدر ضماناً على بياناتنا.', 'يفتح الضبط الدقيق جزءاً من النموذج المدرب سابقاً بمعدل تعلم مناسب مع الحذر من فرط الملاءمة وتغير توزيع البيانات.', 'اعتبار تجمّع السمات بلا فقد للمعلومات.'], 'correct': 2, 'explanation': 'يفتح الضبط الدقيق جزءاً من النموذج المدرب سابقاً بمعدل تعلم مناسب مع الحذر من فرط الملاءمة وتغير توزيع البيانات.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Fine-Tuning and Transfer Learning Trade-offs»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'لا تعد نتائج المصدر أو تحسن الضبط الدقيق ضماناً عاماً.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'لا تعد نتائج المصدر أو تحسن الضبط الدقيق ضماناً عاماً.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن استخراج المميزات المجمدة بضبط بعض الطبقات وناقش التكلفة والمخاطر.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M07 — Design a small-data image classifier and a generalization plan.', 'description': 'مشروع Masar أصلي نظري للوحدة: تصنيف الصور وأساسيات الشبكات الالتفافية. المطلوب: Design a small-data image classifier and a generalization plan. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
