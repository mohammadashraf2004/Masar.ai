# -*- coding: utf-8 -*-
"""T040 — Deep Learning Foundations, module M07.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 8, 'chapter_title': 'Image classification', 'source_file': 'تم لصق markdown(20260923-015008).md', 'source_line_ranges': [[16, 117]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Understanding CNNs and Image Classification Shapes',
    "slug": 'deep-learning-foundations-t040-understanding-cnns-and-image-classification-shapes',
    "description": 'تحول طبقات الالتفاف صورة إلى خرائط سمات تتغير أبعادها؛ يعتمد شكل القنوات على تمثيل الإطار.',
    "order": 1,
    "difficulty": 'intermediate',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'image'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Understanding CNNs and Image Classification Shapes',
        "content": """# Understanding CNNs and Image Classification Shapes

**المساق:** أساسيات التعلم العميق · **الوحدة 07:** تصنيف الصور وأساسيات الشبكات الالتفافية · **الدرس T040** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

تتبع صورة MNIST عبر طبقات ملتفة واكتب ارتفاعها وعرضها وقنواتها. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تحول طبقات الالتفاف صورة إلى خرائط سمات تتغير أبعادها؛ يعتمد شكل القنوات على تمثيل الإطار.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> CONV FEATURES -> CLASS HEAD -> PREDICTION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

تتبع صورة MNIST عبر طبقات ملتفة واكتب ارتفاعها وعرضها وقنواتها.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

لا تخلط ترتيب القنوات في PyTorch بترتيبها في أمثلة Keras. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

تتبع صورة MNIST عبر طبقات ملتفة واكتب ارتفاعها وعرضها وقنواتها. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تحول طبقات الالتفاف صورة إلى خرائط سمات تتغير أبعادها؛ يعتمد شكل القنوات على تمثيل الإطار. وتذكر القيد التالي: لا تخلط ترتيب القنوات في PyTorch بترتيبها في أمثلة Keras.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 8 — Image classification.
- ملف المصدر: `تم لصق markdown(20260923-015008).md`.
- مواضع الاستناد في المقتطف: L16–L117.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Understanding CNNs and Image Classification Shapes', 'description': 'تتبع صورة MNIST عبر طبقات ملتفة واكتب ارتفاعها وعرضها وقنواتها.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: لا تخلط ترتيب القنوات في PyTorch بترتيبها في أمثلة Keras.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'image']}],
    "quiz": {'title': 'Understanding CNNs and Image Classification Shapes — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Understanding CNNs and Image Classification Shapes»؟', 'options': ['تحول طبقات الالتفاف صورة إلى خرائط سمات تتغير أبعادها؛ يعتمد شكل القنوات على تمثيل الإطار.', 'اعتبار تجمّع السمات بلا فقد للمعلومات.', 'افتراض أن أي تعديل للصورة يحفظ الفئة.', 'اعتماد تحسن المصدر ضماناً على بياناتنا.'], 'correct': 0, 'explanation': 'تحول طبقات الالتفاف صورة إلى خرائط سمات تتغير أبعادها؛ يعتمد شكل القنوات على تمثيل الإطار.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Understanding CNNs and Image Classification Shapes»؟', 'options': ['لا تخلط ترتيب القنوات في PyTorch بترتيبها في أمثلة Keras.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'لا تخلط ترتيب القنوات في PyTorch بترتيبها في أمثلة Keras.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: تتبع صورة MNIST عبر طبقات ملتفة واكتب ارتفاعها وعرضها وقنواتها.', 'type': 'open'}], 'passing_score': 70},
}
