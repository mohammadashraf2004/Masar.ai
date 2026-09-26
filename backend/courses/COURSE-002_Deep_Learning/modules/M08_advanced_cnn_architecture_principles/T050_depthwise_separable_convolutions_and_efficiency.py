# -*- coding: utf-8 -*-
"""T050 — Deep Learning Foundations, module M08.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 9, 'chapter_title': 'ConvNet architecture patterns', 'source_file': 'تم لصق markdown(20260923-015121).md', 'source_line_ranges': [[285, 309]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Depthwise Separable Convolutions and Efficiency',
    "slug": 'deep-learning-foundations-t050-depthwise-separable-convolutions-and-efficiency',
    "description": 'يفصل الالتفاف القابل للفصل بين المرشحات المكانية لكل قناة والخلط الخطي للقنوات لتغيير تكاليف الحساب.',
    "order": 4,
    "difficulty": 'intermediate',
    "estimated_hours": 0.8333,
    "skill_tags": ['deep-learning', 'foundations', 'advanced'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Depthwise Separable Convolutions and Efficiency',
        "content": """# Depthwise Separable Convolutions and Efficiency

**المساق:** أساسيات التعلم العميق · **الوحدة 08:** مبادئ معماريات CNN المتقدمة · **الدرس T050** · **المدة الموجهة:** 50 دقيقة

## موقف تعليمي

قارن عدد معاملات التفاف قياسي وdepthwise مع pointwise. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

يفصل الالتفاف القابل للفصل بين المرشحات المكانية لكل قناة والخلط الخطي للقنوات لتغيير تكاليف الحساب.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
IMAGE -> REUSABLE BLOCKS -> FEATURE PYRAMID -> HEAD
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن عدد معاملات التفاف قياسي وdepthwise مع pointwise.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

انخفاض عدد المعاملات لا يضمن انخفاض زمن التنفيذ. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن عدد معاملات التفاف قياسي وdepthwise مع pointwise. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

يفصل الالتفاف القابل للفصل بين المرشحات المكانية لكل قناة والخلط الخطي للقنوات لتغيير تكاليف الحساب. وتذكر القيد التالي: انخفاض عدد المعاملات لا يضمن انخفاض زمن التنفيذ.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 9 — ConvNet architecture patterns.
- ملف المصدر: `تم لصق markdown(20260923-015121).md`.
- مواضع الاستناد في المقتطف: L285–L309.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 50,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Depthwise Separable Convolutions and Efficiency', 'description': 'قارن عدد معاملات التفاف قياسي وdepthwise مع pointwise.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: انخفاض عدد المعاملات لا يضمن انخفاض زمن التنفيذ.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'advanced']}],
    "quiz": {'title': 'Depthwise Separable Convolutions and Efficiency — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Depthwise Separable Convolutions and Efficiency»؟', 'options': ['استنتاج زمن GPU من عدد المعاملات فقط.', 'اعتبار خيار ترتيب الطبقات قانوناً مطلقاً.', 'يفصل الالتفاف القابل للفصل بين المرشحات المكانية لكل قناة والخلط الخطي للقنوات لتغيير تكاليف الحساب.', 'جمع فروع غير متوافقة أبعادها.'], 'correct': 2, 'explanation': 'يفصل الالتفاف القابل للفصل بين المرشحات المكانية لكل قناة والخلط الخطي للقنوات لتغيير تكاليف الحساب.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Depthwise Separable Convolutions and Efficiency»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'انخفاض عدد المعاملات لا يضمن انخفاض زمن التنفيذ.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'انخفاض عدد المعاملات لا يضمن انخفاض زمن التنفيذ.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن عدد معاملات التفاف قياسي وdepthwise مع pointwise.', 'type': 'open'}], 'passing_score': 70},
}
