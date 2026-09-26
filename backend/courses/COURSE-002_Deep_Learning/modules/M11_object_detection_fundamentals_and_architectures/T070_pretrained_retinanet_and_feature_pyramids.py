# -*- coding: utf-8 -*-
"""T070 — Deep Learning Foundations, module M11.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 12, 'chapter_title': 'Object detection', 'source_file': 'تم لصق markdown(20260923-015421).md', 'source_line_ranges': [[589, 665]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Pretrained RetinaNet and Feature Pyramids',
    "slug": 'deep-learning-foundations-t070-pretrained-retinanet-and-feature-pyramids',
    "description": 'تجمع شبكة هرم السمات معلومات دلالية عميقة مع خرائط أكثر دقة مكانياً للكشف عن أحجام متعددة.',
    "order": 7,
    "difficulty": 'intermediate',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'object'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Pretrained RetinaNet and Feature Pyramids',
        "content": """# Pretrained RetinaNet and Feature Pyramids

**المساق:** أساسيات التعلم العميق · **الوحدة 11:** أساسيات اكتشاف الأجسام ومعمارياته · **الدرس T070** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

ارسم هرم سمات مع وصلات جانبية وتنبؤات متعددة المستويات. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تجمع شبكة هرم السمات معلومات دلالية عميقة مع خرائط أكثر دقة مكانياً للكشف عن أحجام متعددة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> DETECTOR -> BOXES + CLASSES -> EVALUATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم هرم سمات مع وصلات جانبية وتنبؤات متعددة المستويات.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

لا تفترض أن كل نموذج مسبق يناسب مجال التطبيق. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم هرم سمات مع وصلات جانبية وتنبؤات متعددة المستويات. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تجمع شبكة هرم السمات معلومات دلالية عميقة مع خرائط أكثر دقة مكانياً للكشف عن أحجام متعددة. وتذكر القيد التالي: لا تفترض أن كل نموذج مسبق يناسب مجال التطبيق.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 12 — Object detection.
- ملف المصدر: `تم لصق markdown(20260923-015421).md`.
- مواضع الاستناد في المقتطف: L589–L665.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Pretrained RetinaNet and Feature Pyramids', 'description': 'ارسم هرم سمات مع وصلات جانبية وتنبؤات متعددة المستويات.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: لا تفترض أن كل نموذج مسبق يناسب مجال التطبيق.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'object']}],
    "quiz": {'title': 'Pretrained RetinaNet and Feature Pyramids — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Pretrained RetinaNet and Feature Pyramids»؟', 'options': ['اعتبار مصنف الصورة كاشفاً للأجسام تلقائياً.', 'الاعتماد على عرض بصري دون تقييم شامل.', 'تجمع شبكة هرم السمات معلومات دلالية عميقة مع خرائط أكثر دقة مكانياً للكشف عن أحجام متعددة.', 'نسيان تعديل الصناديق عند تحجيم الصورة.'], 'correct': 2, 'explanation': 'تجمع شبكة هرم السمات معلومات دلالية عميقة مع خرائط أكثر دقة مكانياً للكشف عن أحجام متعددة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Pretrained RetinaNet and Feature Pyramids»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'لا تفترض أن كل نموذج مسبق يناسب مجال التطبيق.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'لا تفترض أن كل نموذج مسبق يناسب مجال التطبيق.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم هرم سمات مع وصلات جانبية وتنبؤات متعددة المستويات.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M11 — Design a warehouse package detector on paper.', 'description': 'مشروع Masar أصلي نظري للوحدة: أساسيات اكتشاف الأجسام ومعمارياته. المطلوب: Design a warehouse package detector on paper. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
