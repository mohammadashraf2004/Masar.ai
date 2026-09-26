# -*- coding: utf-8 -*-
"""T146 — Deep Learning Foundations, module M19.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 20, 'chapter_title': 'Conclusion', 'source_file': 'تم لصق markdown (2).md', 'source_line_ranges': [[10, 61], [74, 260]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Deep Learning Knowledge Map and Architecture Review',
    "slug": 'deep-learning-foundations-t146-deep-learning-knowledge-map-and-architecture-review',
    "description": 'يجمع الملخص بين تمييز AI وML وDL وطبيعة التمثيلات والمشتقات والعائلات المعمارية وارتباطها بالبيانات.',
    "order": 1,
    "difficulty": 'advanced',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'deep'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Deep Learning Knowledge Map and Architecture Review',
        "content": """# Deep Learning Knowledge Map and Architecture Review

**المساق:** أساسيات التعلم العميق · **الوحدة 19:** مراجعة شاملة وإتمام المساق · **الدرس T146** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

ارسم خريطة تربط الصور بـ CNN والتتابعات بـ RNN/Transformer والتوليد بـ diffusion. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يجمع الملخص بين تمييز AI وML وDL وطبيعة التمثيلات والمشتقات والعائلات المعمارية وارتباطها بالبيانات.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
PROBLEM -> REPRESENTATION -> MODEL -> VALIDATION -> NEXT STEP
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم خريطة تربط الصور بـ CNN والتتابعات بـ RNN/Transformer والتوليد بـ diffusion.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

هذا تجميع لما سبق وليس إعادة تقديم كل المعادلات. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم خريطة تربط الصور بـ CNN والتتابعات بـ RNN/Transformer والتوليد بـ diffusion. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يجمع الملخص بين تمييز AI وML وDL وطبيعة التمثيلات والمشتقات والعائلات المعمارية وارتباطها بالبيانات. وتذكر القيد التالي: هذا تجميع لما سبق وليس إعادة تقديم كل المعادلات.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 20 — Conclusion.
- ملف المصدر: `تم لصق markdown (2).md`.
- مواضع الاستناد في المقتطف: L10–L61, L74–L260.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Deep Learning Knowledge Map and Architecture Review', 'description': 'ارسم خريطة تربط الصور بـ CNN والتتابعات بـ RNN/Transformer والتوليد بـ diffusion.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: هذا تجميع لما سبق وليس إعادة تقديم كل المعادلات.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'deep']}],
    "quiz": {'title': 'Deep Learning Knowledge Map and Architecture Review — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Deep Learning Knowledge Map and Architecture Review»؟', 'options': ['اختيار النموذج قبل تحديد الهدف والبيانات.', 'إهمال حدود الدراسة عند قراءة ورقة بحثية.', 'يجمع الملخص بين تمييز AI وML وDL وطبيعة التمثيلات والمشتقات والعائلات المعمارية وارتباطها بالبيانات.', 'تكرار حفظ جميع واجهات Keras بدلاً من فهم المفاهيم.'], 'correct': 2, 'explanation': 'يجمع الملخص بين تمييز AI وML وDL وطبيعة التمثيلات والمشتقات والعائلات المعمارية وارتباطها بالبيانات.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Deep Learning Knowledge Map and Architecture Review»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'هذا تجميع لما سبق وليس إعادة تقديم كل المعادلات.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'هذا تجميع لما سبق وليس إعادة تقديم كل المعادلات.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم خريطة تربط الصور بـ CNN والتتابعات بـ RNN/Transformer والتوليد بـ diffusion.', 'type': 'open'}], 'passing_score': 70},
}
