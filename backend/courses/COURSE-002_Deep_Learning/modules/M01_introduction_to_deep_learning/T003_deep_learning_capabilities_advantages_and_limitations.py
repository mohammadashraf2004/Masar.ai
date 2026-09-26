# -*- coding: utf-8 -*-
"""T003 — Deep Learning Foundations, module M01.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 1, 'chapter_title': 'What is deep learning?', 'source_file': 'تم لصق markdown(20260923-014224).md', 'source_line_ranges': [[154, 228]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Deep Learning Capabilities, Advantages, and Limitations',
    "slug": 'deep-learning-foundations-t003-deep-learning-capabilities-advantages-and-limitations',
    "description": 'تميز الشبكات العميقة في تعلم تمثيلات الصور والنصوص يتوقف على ملاءمة البيانات والمهمة والموارد؛ التعميم على بيانات جديدة يجب قياسه.',
    "order": 3,
    "difficulty": 'beginner',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'introduction'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Deep Learning Capabilities, Advantages, and Limitations',
        "content": """# Deep Learning Capabilities, Advantages, and Limitations

**المساق:** أساسيات التعلم العميق · **الوحدة 01:** مدخل إلى التعلم العميق · **الدرس T003** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

قارن مهمة تصنيف صور بمهمة تعتمد قواعد حسابية دقيقة، وحدد البيانات ومعيار النجاح المناسبين. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تميز الشبكات العميقة في تعلم تمثيلات الصور والنصوص يتوقف على ملاءمة البيانات والمهمة والموارد؛ التعميم على بيانات جديدة يجب قياسه.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
DATA -> REPRESENTATIONS -> PREDICTION -> LOSS
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن مهمة تصنيف صور بمهمة تعتمد قواعد حسابية دقيقة، وحدد البيانات ومعيار النجاح المناسبين.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

الأمثلة الناجحة لا تعني أن أي مهمة تُحل بالشبكات العميقة. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن مهمة تصنيف صور بمهمة تعتمد قواعد حسابية دقيقة، وحدد البيانات ومعيار النجاح المناسبين. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تميز الشبكات العميقة في تعلم تمثيلات الصور والنصوص يتوقف على ملاءمة البيانات والمهمة والموارد؛ التعميم على بيانات جديدة يجب قياسه. وتذكر القيد التالي: الأمثلة الناجحة لا تعني أن أي مهمة تُحل بالشبكات العميقة.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 1 — What is deep learning?.
- ملف المصدر: `تم لصق markdown(20260923-014224).md`.
- مواضع الاستناد في المقتطف: L154–L228.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Deep Learning Capabilities, Advantages, and Limitations', 'description': 'قارن مهمة تصنيف صور بمهمة تعتمد قواعد حسابية دقيقة، وحدد البيانات ومعيار النجاح المناسبين.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: الأمثلة الناجحة لا تعني أن أي مهمة تُحل بالشبكات العميقة.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'introduction']}],
    "quiz": {'title': 'Deep Learning Capabilities, Advantages, and Limitations — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Deep Learning Capabilities, Advantages, and Limitations»؟', 'options': ['تسمية التعلم العميق مرادفاً لأي برنامج ذكاء اصطناعي.', 'الحكم على الأداء باستخدام أمثلة التدريب فقط.', 'افتراض نجاح النموذج دون بيانات ملائمة.', 'تميز الشبكات العميقة في تعلم تمثيلات الصور والنصوص يتوقف على ملاءمة البيانات والمهمة والموارد؛ التعميم على بيانات جديدة يجب قياسه.'], 'correct': 3, 'explanation': 'تميز الشبكات العميقة في تعلم تمثيلات الصور والنصوص يتوقف على ملاءمة البيانات والمهمة والموارد؛ التعميم على بيانات جديدة يجب قياسه.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Deep Learning Capabilities, Advantages, and Limitations»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'الأمثلة الناجحة لا تعني أن أي مهمة تُحل بالشبكات العميقة.'], 'correct': 3, 'explanation': 'الأمثلة الناجحة لا تعني أن أي مهمة تُحل بالشبكات العميقة.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن مهمة تصنيف صور بمهمة تعتمد قواعد حسابية دقيقة، وحدد البيانات ومعيار النجاح المناسبين.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M01 — Design an explanatory map of a deep-learning application.', 'description': 'مشروع Masar أصلي نظري للوحدة: مدخل إلى التعلم العميق. المطلوب: Design an explanatory map of a deep-learning application. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'intermediate', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
