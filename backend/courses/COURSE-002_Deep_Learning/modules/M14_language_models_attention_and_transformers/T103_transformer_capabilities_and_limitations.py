# -*- coding: utf-8 -*-
"""T103 — Deep Learning Foundations, module M14.
Portable seed data compatible in *shape* with the uploaded TOPIC template.
No database changes are performed by importing this file.
"""

SOURCE = {'book_id': 'BOOK-002', 'chapter': 15, 'chapter_title': 'Language models and the Transformer', 'source_file': 'تم لصق markdown(20260923-015925).md', 'source_line_ranges': [[1427, 1479]], 'edition': 'SOURCE INFORMATION MISSING', 'printed_pages': 'SOURCE INFORMATION MISSING', 'source_is_user_supplied': True, 'instructional_content_and_exercise_are_masar_original': True}

TOPIC = {
    "title": 'Transformer Capabilities and Limitations',
    "slug": 'deep-learning-foundations-t103-transformer-capabilities-and-limitations',
    "description": 'تسمح آليات الانتباه والتمثيلات السياقية بتجارب قوية لكن الأحكام عن الفهم والتعميم تعتمد التقييم.',
    "order": 14,
    "difficulty": 'advanced',
    "estimated_hours": 0.6667,
    "skill_tags": ['deep-learning', 'foundations', 'language'],
    "prerequisite_ids": [],  # Resolve to real database IDs when integrating.
    "lesson": {
        "title": 'Transformer Capabilities and Limitations',
        "content": """# Transformer Capabilities and Limitations

**المساق:** أساسيات التعلم العميق · **الوحدة 14:** النماذج اللغوية والانتباه والمحوّلات · **الدرس T103** · **المدة الموجهة:** 40 دقيقة

## موقف تعليمي

قارن RNN وTransformer تحت قيود طول وتسلسل مختلفة. هذا الموقف هو نقطة انطلاق لتحليل الآلية، لا نتيجة تجربة نُفذت في هذه الحزمة.

## الهدف من الدرس

بنهاية الدرس يستطيع المتعلم شرح الفكرة الأساسية، وتمييز المدخلات والمخرجات والعناصر المؤثرة فيها، وتطبيقها على موقف مماثل، وتحديد ما لا يمكن استنتاجه من المثال وحده.

## الشرح الأساسي

تسمح آليات الانتباه والتمثيلات السياقية بتجارب قوية لكن الأحكام عن الفهم والتعميم تعتمد التقييم.

لفهم هذه الفكرة فهماً عملياً، ابدأ بتحديد **المدخل** و**التمثيل الداخلي أو العملية** و**المخرج** و**الطريقة التي ستتحقق بها من النتيجة**. اسأل عن كل مرحلة: ما المعلومات المتاحة لها؟ ما الذي تغيّره؟ وما الافتراض الذي تعتمد عليه؟ عند وجود معادلة أو شكل موتر، اكتب الأبعاد والوحدات بوضوح قبل الانتقال للمرحلة التالية. لا يكفي تذكر أسماء الطبقات أو المكتبات دون تفسير وظيفتها.

## مخطط مفاهيمي

```
TOKENS -> EMBEDDINGS -> ATTENTION -> NEXT TOKEN
```

اقرأ المخطط بوصفه تبسيطاً لسير المعلومات، ثم بيّن أي مرحلة يقابلها موضوع هذا الدرس؛ ليس مخططاً ملزماً لكل المعماريات.

## مثال محلّل

قارن RNN وTransformer تحت قيود طول وتسلسل مختلفة.

1. **حدد المعطيات:** دوّن المدخلات والهدف والشروط اللازمة.
2. **تتبع العملية:** اربط كل مرحلة من المثال بالمبدأ المشروح؛ احسب الأبعاد أو القيم عند توفرها.
3. **افحص النتيجة:** اقترح تجربة مقارنة أو اختبار تحقق يكشف خطأ في الافتراضات.

## حدود المفهوم وتنبيه تحريري

استعارات قاعدة البيانات والتفكير ليست مبرهنات رياضية. يجب فصل ما يعرضه المصدر فعلياً عن نتائج يمكن أن تختلف مع البيانات والعتاد وإعدادات التجربة. إن احتاج المثال إلى تصحيح قبل تحويله إلى شيفرة تنفيذية فلا تعرضه على أنه برنامج جرى اختباره.

## تدريب تطبيقي نظري

قارن RNN وTransformer تحت قيود طول وتسلسل مختلفة. قدم إجابة مرتبة تتضمن رسمًا أو حسابًا عند الحاجة، وتفسيراً للمبدأ، ومثالاً مضاداً واحداً أو اختباراً يوضح حدوده. **لا يتطلب التدريب تشغيل نموذج أو تثبيت Keras.**

## ما يجب أن تحتفظ به

تسمح آليات الانتباه والتمثيلات السياقية بتجارب قوية لكن الأحكام عن الفهم والتعميم تعتمد التقييم. وتذكر القيد التالي: استعارات قاعدة البيانات والتفكير ليست مبرهنات رياضية.

## التوثيق والحدود المصدرية

- الكتاب: BOOK-002 — Deep Learning Foundations (المادة المقدمة من المستخدم).
- الفصل الأصلي: 15 — Language models and the Transformer.
- ملف المصدر: `تم لصق markdown(20260923-015925).md`.
- مواضع الاستناد في المقتطف: L1427–L1479.
- Edition / printed pages: `SOURCE INFORMATION MISSING`.
- الشرح التدريبي والأمثلة والتمارين والأسئلة هنا من تطوير Masar، وليست منسوبة حرفياً للمؤلف.
""",
        "estimated_minutes": 40,
        "has_code_examples": False,
    },
    "exercises": [{'title': 'تحليل تطبيقي — Transformer Capabilities and Limitations', 'description': 'قارن RNN وTransformer تحت قيود طول وتسلسل مختلفة.\n\nالمطلوب: (1) تحديد المعطيات والمخرج، (2) شرح المبدأ أو إجراء الحساب المناسب، (3) بيان اختبار تحقق أو حدّ من الحدود: استعارات قاعدة البيانات والتفكير ليست مبرهنات رياضية.', 'difficulty': 'advanced', 'skill_tested': ['deep-learning', 'foundations', 'language']}],
    "quiz": {'title': 'Transformer Capabilities and Limitations — Knowledge Check', 'questions': [{'question': 'أي وصف يعبّر عن المفهوم الرئيسي في درس «Transformer Capabilities and Limitations»؟', 'options': ['السماح للمفكك برؤية رموز الهدف المستقبلية.', 'إهمال توافق أبعاد Q وK وV.', 'اعتبار دقة الرمز معيار جودة ترجمة كافياً.', 'تسمح آليات الانتباه والتمثيلات السياقية بتجارب قوية لكن الأحكام عن الفهم والتعميم تعتمد التقييم.'], 'correct': 3, 'explanation': 'تسمح آليات الانتباه والتمثيلات السياقية بتجارب قوية لكن الأحكام عن الفهم والتعميم تعتمد التقييم.'}, {'question': 'أي تنبيه يجب مراعاته عند تطبيق درس «Transformer Capabilities and Limitations»؟', 'options': ['كل نتائج نموذج واحد تنطبق دون اختبار على كل مجموعات البيانات.', 'يكفي عرض مخرجات التدريب لتأكيد التعميم.', 'لا يلزم اختبار أي افتراض في المثال.', 'استعارات قاعدة البيانات والتفكير ليست مبرهنات رياضية.'], 'correct': 3, 'explanation': 'استعارات قاعدة البيانات والتفكير ليست مبرهنات رياضية.'}, {'question': 'اشرح المثال التالي وبيّن كيف تتحقق من صحة استنتاجك: قارن RNN وTransformer تحت قيود طول وتسلسل مختلفة.', 'type': 'open'}], 'passing_score': 70},
    "project": {'title': 'M14 — Explain a Transformer translation system from first principles.', 'description': 'مشروع Masar أصلي نظري للوحدة: النماذج اللغوية والانتباه والمحوّلات. المطلوب: Explain a Transformer translation system from first principles. قدّم تقريراً يحدد المشكلة والمدخلات والمخرجات والمخطط التقني وخطة التحقق وحدود الاقتراح. لا حاجة لكتابة كود أو نشر نموذج.', 'difficulty': 'advanced', 'tech_stack': [], 'objectives': ['Explain the key mechanisms and architectural assumptions.', 'Draw a coherent conceptual pipeline or system diagram.', 'Specify evaluation evidence and discuss failure modes.'], 'rubric': {'conceptual_accuracy': 30, 'design_and_shapes': 25, 'evaluation_and_evidence': 25, 'limitations_and_clarity': 20}, 'starter_repo_url': None, 'estimated_hours': 2.5},
}
