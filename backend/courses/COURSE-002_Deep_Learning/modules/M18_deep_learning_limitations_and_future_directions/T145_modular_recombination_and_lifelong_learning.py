# -*- coding: utf-8 -*-
"""T145 — Deep Learning Foundations, module M18.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 19, 'chapter_title': 'The future of AI', 'source_file': 'تم لصق markdown(20260923-020653).md', 'source_line_ranges': [[393, 421]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Modular Recombination and Lifelong Learning',
    "slug": 'deep-learning-foundations-t145-modular-recombination-and-lifelong-learning',
    "description": 'يعرض الكاتب رؤية لمكتبات وحدات قابلة للتركيب والتعلم التراكمي عبر المهام.',
    "order": 7,
    "difficulty": 'advanced',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'deep'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Modular Recombination and Lifelong Learning',
        "content": """# Modular Recombination and Lifelong Learning

**المساق:** أساسيات التعلم العميق · **الوحدة 18:** حدود التعلم العميق واتجاهات البحث · **الدرس T145** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

اقترح ثلاث وحدات مشتركة بين مسائل متقاربة وآلية للتحقق قبل إعادة الاستخدام. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يعرض الكاتب رؤية لمكتبات وحدات قابلة للتركيب والتعلم التراكمي عبر المهام.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
CLAIM -> CONTROLLED EXPERIMENT -> EVIDENCE -> LIMITATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

اقترح ثلاث وحدات مشتركة بين مسائل متقاربة وآلية للتحقق قبل إعادة الاستخدام.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

الرؤية مستقبلية وليست وصفاً لنظام متحقق. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

اقترح ثلاث وحدات مشتركة بين مسائل متقاربة وآلية للتحقق قبل إعادة الاستخدام. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يعرض الكاتب رؤية لمكتبات وحدات قابلة للتركيب والتعلم التراكمي عبر المهام. وتذكر القيد التالي: الرؤية مستقبلية وليست وصفاً لنظام متحقق.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 19 — The future of AI.
- ملف المصدر: `تم لصق markdown(20260923-020653).md`.
- مواضع الاستناد في المقتطف: L393–L421.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Modular Recombination and Lifelong Learning', 'description': 'اقترح ثلاث وحدات مشتركة بين مسائل متقاربة وآلية للتحقق قبل إعادة الاستخدام.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: الرؤية مستقبلية وليست وصفاً لنظام متحقق.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'deep']}],
    "quiz": {'title': 'Modular Recombination and Lifelong Learning — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Modular Recombination and Lifelong Learning»؟', 'options': ['اعتبار مشروعاً بحثياً متخيلاً نظاماً منفذاً.', 'يعرض الكاتب رؤية لمكتبات وحدات قابلة للتركيب والتعلم التراكمي عبر المهام.', 'نقل وجهة نظر الباحث على أنها قانون مثبت.', 'الاعتماد على رقم معيار تاريخي بوصفه نتيجة حالية.'], 'correct': 1, 'explanation': 'يعرض الكاتب رؤية لمكتبات وحدات قابلة للتركيب والتعلم التراكمي عبر المهام.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Modular Recombination and Lifelong Learning»؟', 'options': ['لا يلزم اختبار أي افتراض في المثال.', 'الرؤية مستقبلية وليست وصفاً لنظام متحقق.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.'], 'correct': 1, 'explanation': 'الرؤية مستقبلية وليست وصفاً لنظام متحقق.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: اقترح ثلاث وحدات مشتركة بين مسائل متقاربة وآلية للتحقق قبل إعادة الاستخدام.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M18 — Write a critical research proposal separating evidence from speculation.', 'description': 'مشروع Masar أصلي نظري للوحدة: حدود التعلم العميق واتجاهات البحث. المطلوب: Write a critical research proposal separating evidence from speculation. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'advanced', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
