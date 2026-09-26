# -*- coding: utf-8 -*-
"""T079 — Deep Learning Foundations, module M12.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 13, 'chapter_title': 'Timeseries forecasting', 'source_file': 'تم لصق markdown(20260923-015526).md', 'source_line_ranges': [[794, 864]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Bidirectional RNNs and Architecture Selection',
    "slug": 'deep-learning-foundations-t079-bidirectional-rnns-and-architecture-selection',
    "description": 'تعالج الشبكة ثنائية الاتجاه نافذة مرصودة من جهتين، ولا يجوز استعمال قياسات من مستقبل وقت القرار.',
    "order": 9,
    "difficulty": 'intermediate',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'time'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Bidirectional RNNs and Architecture Selection',
        "content": """# Bidirectional RNNs and Architecture Selection

**المساق:** أساسيات التعلم العميق · **الوحدة 12:** التنبؤ بالسلاسل الزمنية والشبكات المتكررة · **الدرس T079** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

قارن تصنيف نص مع توقع يوم قادم من نافذة تاريخية كاملة. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تعالج الشبكة ثنائية الاتجاه نافذة مرصودة من جهتين، ولا يجوز استعمال قياسات من مستقبل وقت القرار.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
PAST WINDOW -> TEMPORAL MODEL -> FUTURE TARGET
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن تصنيف نص مع توقع يوم قادم من نافذة تاريخية كاملة.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

ثنائية الاتجاه على تاريخ متاح ليست تسرباً بحد ذاتها. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن تصنيف نص مع توقع يوم قادم من نافذة تاريخية كاملة. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تعالج الشبكة ثنائية الاتجاه نافذة مرصودة من جهتين، ولا يجوز استعمال قياسات من مستقبل وقت القرار. وتذكر القيد التالي: ثنائية الاتجاه على تاريخ متاح ليست تسرباً بحد ذاتها.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 13 — Timeseries forecasting.
- ملف المصدر: `تم لصق markdown(20260923-015526).md`.
- مواضع الاستناد في المقتطف: L794–L864.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Bidirectional RNNs and Architecture Selection', 'description': 'قارن تصنيف نص مع توقع يوم قادم من نافذة تاريخية كاملة.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: ثنائية الاتجاه على تاريخ متاح ليست تسرباً بحد ذاتها.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'time']}],
    "quiz": {'title': 'Bidirectional RNNs and Architecture Selection — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Bidirectional RNNs and Architecture Selection»؟', 'options': ['إدخال قراءة من مستقبل التنبؤ في المدخلات.', 'تقييس السلسلة باستخدام مجموعة الاختبار.', 'إهمال خط أساس معقول عند تقييم نموذج أعقد.', 'تعالج الشبكة ثنائية الاتجاه نافذة مرصودة من جهتين، ولا يجوز استعمال قياسات من مستقبل وقت القرار.'], 'correct': 3, 'explanation': 'تعالج الشبكة ثنائية الاتجاه نافذة مرصودة من جهتين، ولا يجوز استعمال قياسات من مستقبل وقت القرار.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Bidirectional RNNs and Architecture Selection»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'ثنائية الاتجاه على تاريخ متاح ليست تسرباً بحد ذاتها.'], 'correct': 3, 'explanation': 'ثنائية الاتجاه على تاريخ متاح ليست تسرباً بحد ذاتها.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن تصنيف نص مع توقع يوم قادم من نافذة تاريخية كاملة.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M12 — Design and evaluate a leakage-free temperature forecasting experiment.', 'description': 'مشروع Masar أصلي نظري للوحدة: التنبؤ بالسلاسل الزمنية والشبكات المتكررة. المطلوب: Design and evaluate a leakage-free temperature forecasting experiment. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
