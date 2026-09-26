# -*- coding: utf-8 -*-
"""T007 — Deep Learning Foundations, module M02.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 2, 'chapter_title': 'Mathematical building blocks of neural networks', 'source_file': 'تم لصق markdown(20260923-014326).md', 'source_line_ranges': [[616, 839]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Matrix Multiplication and Neural Network Geometry',
    "slug": 'deep-learning-foundations-t007-matrix-multiplication-and-neural-network-geometry',
    "description": 'يحول ضرب المصفوفات متجهات الدخل بأوزان طبقة إلى سمات جديدة؛ ترتيب الأبعاد يحدد صلاحية العملية.',
    "order": 4,
    "difficulty": 'beginner',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'neural'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Matrix Multiplication and Neural Network Geometry',
        "content": """# Matrix Multiplication and Neural Network Geometry

**المساق:** أساسيات التعلم العميق · **الوحدة 02:** الرياضيات الأساسية للشبكات العصبية · **الدرس T007** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

احسب شكل XW عندما X=(32,20) وW=(20,64)، ثم أضف الانحياز. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يحول ضرب المصفوفات متجهات الدخل بأوزان طبقة إلى سمات جديدة؛ ترتيب الأبعاد يحدد صلاحية العملية.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
TENSOR -> FORWARD PASS -> LOSS -> GRADIENT -> UPDATE
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

احسب شكل XW عندما X=(32,20) وW=(20,64)، ثم أضف الانحياز.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

الضرب المصفوفي ليس ضرباً عنصرًا بعنصر. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

احسب شكل XW عندما X=(32,20) وW=(20,64)، ثم أضف الانحياز. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يحول ضرب المصفوفات متجهات الدخل بأوزان طبقة إلى سمات جديدة؛ ترتيب الأبعاد يحدد صلاحية العملية. وتذكر القيد التالي: الضرب المصفوفي ليس ضرباً عنصرًا بعنصر.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 2 — Mathematical building blocks of neural networks.
- ملف المصدر: `تم لصق markdown(20260923-014326).md`.
- مواضع الاستناد في المقتطف: L616–L839.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Matrix Multiplication and Neural Network Geometry', 'description': 'احسب شكل XW عندما X=(32,20) وW=(20,64)، ثم أضف الانحياز.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: الضرب المصفوفي ليس ضرباً عنصرًا بعنصر.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'neural']}],
    "quiz": {'title': 'Matrix Multiplication and Neural Network Geometry — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Matrix Multiplication and Neural Network Geometry»؟', 'options': ['تجاهل أبعاد الموترات عند ضربها.', 'تغيير الأوزان باستعمال مجموعة الاختبار.', 'افتراض أن التدرج يقود إلى أمثلية عالمية مضمونة.', 'يحول ضرب المصفوفات متجهات الدخل بأوزان طبقة إلى سمات جديدة؛ ترتيب الأبعاد يحدد صلاحية العملية.'], 'correct': 3, 'explanation': 'يحول ضرب المصفوفات متجهات الدخل بأوزان طبقة إلى سمات جديدة؛ ترتيب الأبعاد يحدد صلاحية العملية.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Matrix Multiplication and Neural Network Geometry»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'الضرب المصفوفي ليس ضرباً عنصرًا بعنصر.'], 'correct': 3, 'explanation': 'الضرب المصفوفي ليس ضرباً عنصرًا بعنصر.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: احسب شكل XW عندما X=(32,20) وW=(20,64)، ثم أضف الانحياز.', 'type': 'open'}], 'passing_score': 70},
}
