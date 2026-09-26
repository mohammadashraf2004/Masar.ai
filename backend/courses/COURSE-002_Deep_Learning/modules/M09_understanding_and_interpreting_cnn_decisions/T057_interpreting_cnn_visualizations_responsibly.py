# -*- coding: utf-8 -*-
"""T057 — Deep Learning Foundations, module M09.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 10, 'chapter_title': 'Interpreting what ConvNets learn', 'source_file': 'تم لصق markdown(20260923-015219).md', 'source_line_ranges': [[7, 15], [522, 528], [796, 808]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Interpreting CNN Visualizations Responsibly',
    "slug": 'deep-learning-foundations-t057-interpreting-cnn-visualizations-responsibly',
    "description": 'تخدم خرائط التنشيط وأنماط المرشحات وخرائط الفئات أسئلة مختلفة ولا تكفي وحدها للتحقق من الصلاحية.',
    "order": 5,
    "difficulty": 'intermediate',
    "estimated_hours": 0.5833,
    "skill_tags": ['deep-learning', 'foundations', 'understanding'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Interpreting CNN Visualizations Responsibly',
        "content": """# Interpreting CNN Visualizations Responsibly

**المساق:** أساسيات التعلم العميق · **الوحدة 09:** فهم قرارات الشبكات الالتفافية وتفسيرها · **الدرس T057** · **المدة الموجهة:** 35 دقيقة

## موقف تعليمي

صنف ثلاث صور تفسيرية بحسب ما يظهر فعلاً وما يبقى فرضية. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تخدم خرائط التنشيط وأنماط المرشحات وخرائط الفئات أسئلة مختلفة ولا تكفي وحدها للتحقق من الصلاحية.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> CNN -> INTERNAL SIGNAL -> VISUAL EVIDENCE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صنف ثلاث صور تفسيرية بحسب ما يظهر فعلاً وما يبقى فرضية.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

هذه قواعد نقد إضافية من Masar وليست إطاراً كاملاً من المصدر. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صنف ثلاث صور تفسيرية بحسب ما يظهر فعلاً وما يبقى فرضية. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تخدم خرائط التنشيط وأنماط المرشحات وخرائط الفئات أسئلة مختلفة ولا تكفي وحدها للتحقق من الصلاحية. وتذكر القيد التالي: هذه قواعد نقد إضافية من Masar وليست إطاراً كاملاً من المصدر.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 10 — Interpreting what ConvNets learn.
- ملف المصدر: `تم لصق markdown(20260923-015219).md`.
- مواضع الاستناد في المقتطف: L7–L15, L522–L528, L796–L808.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 35,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Interpreting CNN Visualizations Responsibly', 'description': 'صنف ثلاث صور تفسيرية بحسب ما يظهر فعلاً وما يبقى فرضية.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: هذه قواعد نقد إضافية من Masar وليست إطاراً كاملاً من المصدر.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'understanding']}],
    "quiz": {'title': 'Interpreting CNN Visualizations Responsibly — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Interpreting CNN Visualizations Responsibly»؟', 'options': ['الحكم على موثوقية النموذج من صورة واحدة.', 'تخدم خرائط التنشيط وأنماط المرشحات وخرائط الفئات أسئلة مختلفة ولا تكفي وحدها للتحقق من الصلاحية.', 'اعتبار الخريطة الحرارية برهاناً سببياً.', 'تسمية كل قناة بمعنى مؤكّد.'], 'correct': 1, 'explanation': 'تخدم خرائط التنشيط وأنماط المرشحات وخرائط الفئات أسئلة مختلفة ولا تكفي وحدها للتحقق من الصلاحية.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Interpreting CNN Visualizations Responsibly»؟', 'options': ['لا يلزم اختبار أي افتراض في المثال.', 'هذه قواعد نقد إضافية من Masar وليست إطاراً كاملاً من المصدر.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.'], 'correct': 1, 'explanation': 'هذه قواعد نقد إضافية من Masar وليست إطاراً كاملاً من المصدر.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صنف ثلاث صور تفسيرية بحسب ما يظهر فعلاً وما يبقى فرضية.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M09 — Investigate a hypothetical misclassification using visualization evidence.', 'description': 'مشروع Masar أصلي نظري للوحدة: فهم قرارات الشبكات الالتفافية وتفسيرها. المطلوب: Investigate a hypothetical misclassification using visualization evidence. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
