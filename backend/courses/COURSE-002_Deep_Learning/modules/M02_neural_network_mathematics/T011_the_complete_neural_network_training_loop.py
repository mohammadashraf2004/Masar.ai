# -*- coding: utf-8 -*-
"""T011 — Deep Learning Foundations, module M02.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 2, 'chapter_title': 'Mathematical building blocks of neural networks', 'source_file': 'تم لصق markdown(20260923-014326).md', 'source_line_ranges': [[1115, 1432]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'The Complete Neural Network Training Loop',
    "slug": 'deep-learning-foundations-t011-the-complete-neural-network-training-loop',
    "description": 'تتكرر خطوات تجهيز دفعة والتمرير الأمامي وحساب الخسارة والتدرجات وتحديث الأوزان مع فصل التحقق عن التدريب.',
    "order": 8,
    "difficulty": 'beginner',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'neural'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'The Complete Neural Network Training Loop',
        "content": """# The Complete Neural Network Training Loop

**المساق:** أساسيات التعلم العميق · **الوحدة 02:** الرياضيات الأساسية للشبكات العصبية · **الدرس T011** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

ضع عمليات حلقة التدريب في الترتيب الصحيح وحدد مكان فحص التحقق والحفظ. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تتكرر خطوات تجهيز دفعة والتمرير الأمامي وحساب الخسارة والتدرجات وتحديث الأوزان مع فصل التحقق عن التدريب.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
TENSOR -> FORWARD PASS -> LOSS -> GRADIENT -> UPDATE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

ضع عمليات حلقة التدريب في الترتيب الصحيح وحدد مكان فحص التحقق والحفظ.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

بيانات الاختبار لا تستخدم لاختيار كل تحديث أو ضبط متكرر. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

ضع عمليات حلقة التدريب في الترتيب الصحيح وحدد مكان فحص التحقق والحفظ. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تتكرر خطوات تجهيز دفعة والتمرير الأمامي وحساب الخسارة والتدرجات وتحديث الأوزان مع فصل التحقق عن التدريب. وتذكر القيد التالي: بيانات الاختبار لا تستخدم لاختيار كل تحديث أو ضبط متكرر.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 2 — Mathematical building blocks of neural networks.
- ملف المصدر: `تم لصق markdown(20260923-014326).md`.
- مواضع الاستناد في المقتطف: L1115–L1432.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — The Complete Neural Network Training Loop', 'description': 'ضع عمليات حلقة التدريب في الترتيب الصحيح وحدد مكان فحص التحقق والحفظ.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: بيانات الاختبار لا تستخدم لاختيار كل تحديث أو ضبط متكرر.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'neural']}],
    "quiz": {'title': 'The Complete Neural Network Training Loop — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «The Complete Neural Network Training Loop»؟', 'options': ['تجاهل أبعاد الموترات عند ضربها.', 'تغيير الأوزان باستعمال مجموعة الاختبار.', 'افتراض أن التدرج يقود إلى أمثلية عالمية مضمونة.', 'تتكرر خطوات تجهيز دفعة والتمرير الأمامي وحساب الخسارة والتدرجات وتحديث الأوزان مع فصل التحقق عن التدريب.'], 'correct': 3, 'explanation': 'تتكرر خطوات تجهيز دفعة والتمرير الأمامي وحساب الخسارة والتدرجات وتحديث الأوزان مع فصل التحقق عن التدريب.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «The Complete Neural Network Training Loop»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'بيانات الاختبار لا تستخدم لاختيار كل تحديث أو ضبط متكرر.'], 'correct': 3, 'explanation': 'بيانات الاختبار لا تستخدم لاختيار كل تحديث أو ضبط متكرر.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: ضع عمليات حلقة التدريب في الترتيب الصحيح وحدد مكان فحص التحقق والحفظ.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M02 — Trace a small network end-to-end by hand and explain its gradient updates.', 'description': 'مشروع Masar أصلي نظري للوحدة: الرياضيات الأساسية للشبكات العصبية. المطلوب: Trace a small network end-to-end by hand and explain its gradient updates. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
