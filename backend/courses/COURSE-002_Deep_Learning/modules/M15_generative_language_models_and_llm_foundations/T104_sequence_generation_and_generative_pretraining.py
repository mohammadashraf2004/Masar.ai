# -*- coding: utf-8 -*-
"""T104 — Deep Learning Foundations, module M15.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 16, 'chapter_title': 'Text generation', 'source_file': 'تم لصق markdown(20260923-020108).md', 'source_line_ranges': [[1, 79]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Sequence Generation and Generative Pretraining',
    "slug": 'deep-learning-foundations-t104-sequence-generation-and-generative-pretraining',
    "description": 'يميز تاريخ توليد اللغة بين نماذج تتابعية والتدريب المسبق واسع البيانات واستخدام الأوامر وقت الاستدلال.',
    "order": 1,
    "difficulty": 'advanced',
    "estimated_hours": 0.5833,
    "skill_tags": ['deep-learning', 'foundations', 'generative'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Sequence Generation and Generative Pretraining',
        "content": """# Sequence Generation and Generative Pretraining

**المساق:** أساسيات التعلم العميق · **الوحدة 15:** النماذج اللغوية التوليدية وأساسيات LLM · **الدرس T104** · **المدة الموجهة:** 35 دقيقة

## موقف تعليمي

ارسم خطاً زمنياً وفصل بين pretraining وfine-tuning وprompting. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يميز تاريخ توليد اللغة بين نماذج تتابعية والتدريب المسبق واسع البيانات واستخدام الأوامر وقت الاستدلال.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
CORPUS -> PRETRAINED MODEL -> ADAPTATION -> GENERATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم خطاً زمنياً وفصل بين pretraining وfine-tuning وprompting.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

الأرقام والتواريخ الواردة تاريخية وليست أحدث حالة. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم خطاً زمنياً وفصل بين pretraining وfine-tuning وprompting. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يميز تاريخ توليد اللغة بين نماذج تتابعية والتدريب المسبق واسع البيانات واستخدام الأوامر وقت الاستدلال. وتذكر القيد التالي: الأرقام والتواريخ الواردة تاريخية وليست أحدث حالة.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 16 — Text generation.
- ملف المصدر: `تم لصق markdown(20260923-020108).md`.
- مواضع الاستناد في المقتطف: L1–L79.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 35,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Sequence Generation and Generative Pretraining', 'description': 'ارسم خطاً زمنياً وفصل بين pretraining وfine-tuning وprompting.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: الأرقام والتواريخ الواردة تاريخية وليست أحدث حالة.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'generative']}],
    "quiz": {'title': 'Sequence Generation and Generative Pretraining — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Sequence Generation and Generative Pretraining»؟', 'options': ['يميز تاريخ توليد اللغة بين نماذج تتابعية والتدريب المسبق واسع البيانات واستخدام الأوامر وقت الاستدلال.', 'اعتبار النص المتولد دليلاً على صدقه.', 'الخلط بين تعديل أوزان النموذج واسترجاع وثائق.', 'اعتبار توفير معاملات LoRA توفيراً لكل الذاكرة.'], 'correct': 0, 'explanation': 'يميز تاريخ توليد اللغة بين نماذج تتابعية والتدريب المسبق واسع البيانات واستخدام الأوامر وقت الاستدلال.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Sequence Generation and Generative Pretraining»؟', 'options': ['الأرقام والتواريخ الواردة تاريخية وليست أحدث حالة.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'الأرقام والتواريخ الواردة تاريخية وليست أحدث حالة.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم خطاً زمنياً وفصل بين pretraining وfine-tuning وprompting.', 'type': 'open'}], 'passing_score': 70},
}
