# -*- coding: utf-8 -*-
"""T136 — Deep Learning Foundations, module M17.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 18, 'chapter_title': 'Best practices for the real world', 'source_file': 'تم لصق markdown(20260923-020454).md', 'source_line_ranges': [[717, 760]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Mixed-Precision Training and Loss Scaling',
    "slug": 'deep-learning-foundations-t136-mixed-precision-training-and-loss-scaling',
    "description": 'تفصل الدقة المختلطة بين عمليات منخفضة الدقة وحالة معاملات أكثر دقة، وتحد loss scaling من فقد التدرجات الصغيرة.',
    "order": 8,
    "difficulty": 'advanced',
    "estimated_hours": 0.9167,
    "skill_tags": ['deep-learning', 'foundations', 'model'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Mixed-Precision Training and Loss Scaling',
        "content": """# Mixed-Precision Training and Loss Scaling

**المساق:** أساسيات التعلم العميق · **الوحدة 17:** تحسين النماذج وكفاءة التعلم العميق · **الدرس T136** · **المدة الموجهة:** 55 دقيقة

## موقف تعليمي

ارسم مروراً أمامياً fp16 مع معاملات fp32 وتحقق من معالجة underflow. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تفصل الدقة المختلطة بين عمليات منخفضة الدقة وحالة معاملات أكثر دقة، وتحد loss scaling من فقد التدرجات الصغيرة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
BASELINE -> EXPERIMENT -> MEASURE -> RESOURCE TRADE-OFF
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ارسم مروراً أمامياً fp16 مع معاملات fp32 وتحقق من معالجة underflow.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

تحويل تدرج أصبح صفراً إلى fp32 لا يستعيد قيمته. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ارسم مروراً أمامياً fp16 مع معاملات fp32 وتحقق من معالجة underflow. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تفصل الدقة المختلطة بين عمليات منخفضة الدقة وحالة معاملات أكثر دقة، وتحد loss scaling من فقد التدرجات الصغيرة. وتذكر القيد التالي: تحويل تدرج أصبح صفراً إلى fp32 لا يستعيد قيمته.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 18 — Best practices for the real world.
- ملف المصدر: `تم لصق markdown(20260923-020454).md`.
- مواضع الاستناد في المقتطف: L717–L760.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 55,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Mixed-Precision Training and Loss Scaling', 'description': 'ارسم مروراً أمامياً fp16 مع معاملات fp32 وتحقق من معالجة underflow.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: تحويل تدرج أصبح صفراً إلى fp32 لا يستعيد قيمته.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'model']}],
    "quiz": {'title': 'Mixed-Precision Training and Loss Scaling — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Mixed-Precision Training and Loss Scaling»؟', 'options': ['تفصل الدقة المختلطة بين عمليات منخفضة الدقة وحالة معاملات أكثر دقة، وتحد loss scaling من فقد التدرجات الصغيرة.', 'الاختيار النهائي اعتماداً على الاختبار بشكل متكرر.', 'افتراض تسريع خطي مضمون مع إضافة GPUs.', 'إهمال تغير الجودة عند خفض الدقة.'], 'correct': 0, 'explanation': 'تفصل الدقة المختلطة بين عمليات منخفضة الدقة وحالة معاملات أكثر دقة، وتحد loss scaling من فقد التدرجات الصغيرة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Mixed-Precision Training and Loss Scaling»؟', 'options': ['تحويل تدرج أصبح صفراً إلى fp32 لا يستعيد قيمته.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'تحويل تدرج أصبح صفراً إلى fp32 لا يستعيد قيمته.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ارسم مروراً أمامياً fp16 مع معاملات fp32 وتحقق من معالجة underflow.', 'type': 'open'}], 'passing_score': 70},
}
