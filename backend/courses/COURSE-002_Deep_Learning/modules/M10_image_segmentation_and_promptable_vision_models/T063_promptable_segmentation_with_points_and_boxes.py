# -*- coding: utf-8 -*-
"""T063 — Deep Learning Foundations, module M10.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 11, 'chapter_title': 'Image segmentation', 'source_file': 'تم لصق markdown(20260923-015315).md', 'source_line_ranges': [[370, 615]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Promptable Segmentation with Points and Boxes',
    "slug": 'deep-learning-foundations-t063-promptable-segmentation-with-points-and-boxes',
    "description": 'تساعد النقاط الموجبة والسالبة والصناديق على إزالة الالتباس بين الأجسام المتداخلة.',
    "order": 6,
    "difficulty": 'intermediate',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'image'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Promptable Segmentation with Points and Boxes',
        "content": """# Promptable Segmentation with Points and Boxes

**المساق:** أساسيات التعلم العميق · **الوحدة 10:** تقسيم الصور ونماذج الرؤية الموجّهة · **الدرس T063** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

صمم موجهين لجسم متداخل وتوقع لماذا قد يختلف القناع. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تساعد النقاط الموجبة والسالبة والصناديق على إزالة الالتباس بين الأجسام المتداخلة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> ENCODER -> DECODER / PROMPT -> MASK
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صمم موجهين لجسم متداخل وتوقع لماذا قد يختلف القناع.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

اختيار القناع يحتاج تحققاً ولا يضمنه الموجه. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صمم موجهين لجسم متداخل وتوقع لماذا قد يختلف القناع. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تساعد النقاط الموجبة والسالبة والصناديق على إزالة الالتباس بين الأجسام المتداخلة. وتذكر القيد التالي: اختيار القناع يحتاج تحققاً ولا يضمنه الموجه.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 11 — Image segmentation.
- ملف المصدر: `تم لصق markdown(20260923-015315).md`.
- مواضع الاستناد في المقتطف: L370–L615.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Promptable Segmentation with Points and Boxes', 'description': 'صمم موجهين لجسم متداخل وتوقع لماذا قد يختلف القناع.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: اختيار القناع يحتاج تحققاً ولا يضمنه الموجه.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'image']}],
    "quiz": {'title': 'Promptable Segmentation with Points and Boxes — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Promptable Segmentation with Points and Boxes»؟', 'options': ['مزج رموز القناع بتوسيع استيفائي غير مناسب.', 'افتراض أن كل قناع يميز المثيلات تلقائياً.', 'اعتبار نتيجة صورة واحدة اختباراً مستقلاً.', 'تساعد النقاط الموجبة والسالبة والصناديق على إزالة الالتباس بين الأجسام المتداخلة.'], 'correct': 3, 'explanation': 'تساعد النقاط الموجبة والسالبة والصناديق على إزالة الالتباس بين الأجسام المتداخلة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Promptable Segmentation with Points and Boxes»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'اختيار القناع يحتاج تحققاً ولا يضمنه الموجه.'], 'correct': 3, 'explanation': 'اختيار القناع يحتاج تحققاً ولا يضمنه الموجه.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صمم موجهين لجسم متداخل وتوقع لماذا قد يختلف القناع.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M10 — Specify a product-segmentation solution and its evaluation.', 'description': 'مشروع Masar أصلي نظري للوحدة: تقسيم الصور ونماذج الرؤية الموجّهة. المطلوب: Specify a product-segmentation solution and its evaluation. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
