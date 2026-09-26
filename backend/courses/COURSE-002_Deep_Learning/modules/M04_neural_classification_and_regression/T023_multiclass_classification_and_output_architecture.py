# -*- coding: utf-8 -*-
"""T023 — Deep Learning Foundations, module M04.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 4, 'chapter_title': 'Classification and regression', 'source_file': 'تم لصق markdown(20260923-014601).md', 'source_line_ranges': [[437, 586], [759, 780]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Multiclass Classification and Output Architecture',
    "slug": 'deep-learning-foundations-t023-multiclass-classification-and-output-architecture',
    "description": 'للتصنيف متعدد الفئات أحادي التسمية يستخدم رأس بعدد الفئات وتمثيل أهداف متوافق مع دالة الخسارة.',
    "order": 4,
    "difficulty": 'beginner',
    "estimated_hours": 0.8333,
    "skill_tags": ['deep-learning', 'foundations', 'neural'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Multiclass Classification and Output Architecture',
        "content": """# Multiclass Classification and Output Architecture

**المساق:** أساسيات التعلم العميق · **الوحدة 04:** التصنيف والانحدار بالشبكات العصبية · **الدرس T023** · **المدة الموجهة:** 50 دقيقة

## موقف تعليمي

صمم مخرجات عشر فئات وقارن أهدافاً فهرسية بأهداف one-hot. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

للتصنيف متعدد الفئات أحادي التسمية يستخدم رأس بعدد الفئات وتمثيل أهداف متوافق مع دالة الخسارة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
DATA -> OUTPUT HEAD -> LOSS -> VALIDATION
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صمم مخرجات عشر فئات وقارن أهدافاً فهرسية بأهداف one-hot.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

لا تستخدم sigmoid متعددة مستقلة على أنها softmax أحادية التسمية بلا مبرر. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صمم مخرجات عشر فئات وقارن أهدافاً فهرسية بأهداف one-hot. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

للتصنيف متعدد الفئات أحادي التسمية يستخدم رأس بعدد الفئات وتمثيل أهداف متوافق مع دالة الخسارة. وتذكر القيد التالي: لا تستخدم sigmoid متعددة مستقلة على أنها softmax أحادية التسمية بلا مبرر.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 4 — Classification and regression.
- ملف المصدر: `تم لصق markdown(20260923-014601).md`.
- مواضع الاستناد في المقتطف: L437–L586, L759–L780.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 50,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Multiclass Classification and Output Architecture', 'description': 'صمم مخرجات عشر فئات وقارن أهدافاً فهرسية بأهداف one-hot.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: لا تستخدم sigmoid متعددة مستقلة على أنها softmax أحادية التسمية بلا مبرر.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'neural']}],
    "quiz": {'title': 'Multiclass Classification and Output Architecture — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Multiclass Classification and Output Architecture»؟', 'options': ['تحديد المخرج بمعزل عن ترميز الأهداف.', 'اختيار النموذج من دقة التدريب فقط.', 'اعتبار خسارة الانحدار والتصنيف متطابقتين.', 'للتصنيف متعدد الفئات أحادي التسمية يستخدم رأس بعدد الفئات وتمثيل أهداف متوافق مع دالة الخسارة.'], 'correct': 3, 'explanation': 'للتصنيف متعدد الفئات أحادي التسمية يستخدم رأس بعدد الفئات وتمثيل أهداف متوافق مع دالة الخسارة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Multiclass Classification and Output Architecture»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'لا تستخدم sigmoid متعددة مستقلة على أنها softmax أحادية التسمية بلا مبرر.'], 'correct': 3, 'explanation': 'لا تستخدم sigmoid متعددة مستقلة على أنها softmax أحادية التسمية بلا مبرر.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صمم مخرجات عشر فئات وقارن أهدافاً فهرسية بأهداف one-hot.', 'type': 'open'}], 'passing_score': 70},
}
