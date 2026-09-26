# -*- coding: utf-8 -*-
"""T078 — Deep Learning Foundations, module M12.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 13, 'chapter_title': 'Timeseries forecasting', 'source_file': 'تم لصق markdown(20260923-015526).md', 'source_line_ranges': [[675, 792]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Recurrent Dropout, Capacity, and Training',
    "slug": 'deep-learning-foundations-t078-recurrent-dropout-capacity-and-training',
    "description": 'تؤثر regularization وسعة الطبقات وتكلفة التكرار في الأداء؛ يعرض النص مقارنة LSTM وGRU المكدسة.',
    "order": 8,
    "difficulty": 'intermediate',
    "estimated_hours": 0.75,
    "skill_tags": ['deep-learning', 'foundations', 'time'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Recurrent Dropout, Capacity, and Training',
        "content": """# Recurrent Dropout, Capacity, and Training

**المساق:** أساسيات التعلم العميق · **الوحدة 12:** التنبؤ بالسلاسل الزمنية والشبكات المتكررة · **الدرس T078** · **المدة الموجهة:** 45 دقيقة

## موقف تعليمي

صمم تجربة واحدة العامل تقارن النموذج الأساسي والم regularized. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تؤثر regularization وسعة الطبقات وتكلفة التكرار في الأداء؛ يعرض النص مقارنة LSTM وGRU المكدسة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
PAST WINDOW -> TEMPORAL MODEL -> FUTURE TARGET
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

صمم تجربة واحدة العامل تقارن النموذج الأساسي والم regularized.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

نتيجة مجموعة طقس واحدة لا تعمم على كل السلاسل. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

صمم تجربة واحدة العامل تقارن النموذج الأساسي والم regularized. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تؤثر regularization وسعة الطبقات وتكلفة التكرار في الأداء؛ يعرض النص مقارنة LSTM وGRU المكدسة. وتذكر القيد التالي: نتيجة مجموعة طقس واحدة لا تعمم على كل السلاسل.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 13 — Timeseries forecasting.
- ملف المصدر: `تم لصق markdown(20260923-015526).md`.
- مواضع الاستناد في المقتطف: L675–L792.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 45,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Recurrent Dropout, Capacity, and Training', 'description': 'صمم تجربة واحدة العامل تقارن النموذج الأساسي والم regularized.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: نتيجة مجموعة طقس واحدة لا تعمم على كل السلاسل.', 'difficulty': 'intermediate', 'skill_tested': ['deep-learning', 'foundations', 'time']}],
    "quiz": {'title': 'Recurrent Dropout, Capacity, and Training — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Recurrent Dropout, Capacity, and Training»؟', 'options': ['تقييس السلسلة باستخدام مجموعة الاختبار.', 'إهمال خط أساس معقول عند تقييم نموذج أعقد.', 'تؤثر regularization وسعة الطبقات وتكلفة التكرار في الأداء؛ يعرض النص مقارنة LSTM وGRU المكدسة.', 'إدخال قراءة من مستقبل التنبؤ في المدخلات.'], 'correct': 2, 'explanation': 'تؤثر regularization وسعة الطبقات وتكلفة التكرار في الأداء؛ يعرض النص مقارنة LSTM وGRU المكدسة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Recurrent Dropout, Capacity, and Training»؟', 'options': ['يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'نتيجة مجموعة طقس واحدة لا تعمم على كل السلاسل.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.'], 'correct': 2, 'explanation': 'نتيجة مجموعة طقس واحدة لا تعمم على كل السلاسل.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: صمم تجربة واحدة العامل تقارن النموذج الأساسي والم regularized.', 'type': 'open'}], 'passing_score': 70},
}
