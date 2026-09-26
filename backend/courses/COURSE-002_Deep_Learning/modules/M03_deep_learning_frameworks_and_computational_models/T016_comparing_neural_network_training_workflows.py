# -*- coding: utf-8 -*-
"""T016 — Deep Learning Foundations, module M03.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 3, 'chapter_title': 'Introduction to TensorFlow, PyTorch, JAX, and Keras', 'source_file': 'تم لصق markdown(20260923-014500).md', 'source_line_ranges': [[327, 513], [695, 855], [1149, 1241]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Comparing Neural Network Training Workflows',
    "slug": 'deep-learning-foundations-t016-comparing-neural-network-training-workflows',
    "description": 'تتشابه أطر التدريب في الهدف والتمرير الأمامي وحساب التدرج وتحديث المعاملات رغم اختلاف واجهات البرمجة وإدارة الحالة.',
    "order": 5,
    "difficulty": 'beginner',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'deep'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Comparing Neural Network Training Workflows',
        "content": """# Comparing Neural Network Training Workflows

**المساق:** أساسيات التعلم العميق · **الوحدة 03:** أطر العمل ونماذج الحوسبة · **الدرس T016** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

قارن مخططات TensorFlow وPyTorch وJAX بخمسة عناصر مشتركة. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تتشابه أطر التدريب في الهدف والتمرير الأمامي وحساب التدرج وتحديث المعاملات رغم اختلاف واجهات البرمجة وإدارة الحالة.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
INPUT -> TENSOR OPS -> AUTOGRAD -> OPTIMIZER
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن مخططات TensorFlow وPyTorch وJAX بخمسة عناصر مشتركة.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

تشابه المراحل لا يعني تطابق واجهات البرمجة. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن مخططات TensorFlow وPyTorch وJAX بخمسة عناصر مشتركة. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تتشابه أطر التدريب في الهدف والتمرير الأمامي وحساب التدرج وتحديث المعاملات رغم اختلاف واجهات البرمجة وإدارة الحالة. وتذكر القيد التالي: تشابه المراحل لا يعني تطابق واجهات البرمجة.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 3 — Introduction to TensorFlow, PyTorch, JAX, and Keras.
- ملف المصدر: `تم لصق markdown(20260923-014500).md`.
- مواضع الاستناد في المقتطف: L327–L513, L695–L855, L1149–L1241.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Comparing Neural Network Training Workflows', 'description': 'قارن مخططات TensorFlow وPyTorch وJAX بخمسة عناصر مشتركة.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: تشابه المراحل لا يعني تطابق واجهات البرمجة.', 'difficulty': 'beginner', 'skill_tested': ['deep-learning', 'foundations', 'deep']}],
    "quiz": {'title': 'Comparing Neural Network Training Workflows — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Comparing Neural Network Training Workflows»؟', 'options': ['تتشابه أطر التدريب في الهدف والتمرير الأمامي وحساب التدرج وتحديث المعاملات رغم اختلاف واجهات البرمجة وإدارة الحالة.', 'افتراض أن أسماء واجهات البرمجة هي المفاهيم الرياضية نفسها.', 'اختيار الإطار بدلاً من صياغة المهمة.', 'الاعتماد على مخطط لا يحتوي بيانات أو خسارة.'], 'correct': 0, 'explanation': 'تتشابه أطر التدريب في الهدف والتمرير الأمامي وحساب التدرج وتحديث المعاملات رغم اختلاف واجهات البرمجة وإدارة الحالة.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Comparing Neural Network Training Workflows»؟', 'options': ['تشابه المراحل لا يعني تطابق واجهات البرمجة.', 'كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.'], 'correct': 0, 'explanation': 'تشابه المراحل لا يعني تطابق واجهات البرمجة.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن مخططات TensorFlow وPyTorch وJAX بخمسة عناصر مشتركة.', 'type': 'open'}], 'passing_score': 70},
}
