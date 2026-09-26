# -*- coding: utf-8 -*-
"""T024 — Applied Deep Learning, module M09.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[755, 923], [932, 995]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M09-L02',
 'source_note': 'Source custom transforms/progressive resizing retained as experiment strategies, not '
                'guaranteed improvements.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Custom Transforms and Progressive Training',
 'slug': 'applied-deep-learning-t024-custom-transforms-and-progressive-training',
 'description': 'تطبيق عملي: Custom Transforms and Progressive Training مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'custom-callable-transform',
                'randomness',
                'shape-dtype-safety',
                'progressive-resolution'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Custom Transforms and Progressive Training',
            'content': '# Custom Transforms and Progressive Training\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M09:** زيادة البيانات والتدريب البصري الفعال '
                       '· **الدرس T024 / C003-M09-L02** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'custom callable transform, randomness, shape/dtype safety, progressive resolution, '
                       'benchmarking\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'class AddGaussianNoise:\n'
                       '    def __init__(self, std=0.05): self.std = std\n'
                       '    def __call__(self, x): return x + torch.randn_like(x) * self.std\n'
                       '```\n'
                       '\n'
                       'شغّل المثال، غيّر القيم أو الأشكال، ثم أضف assertion واحداً على الأقل يثبت أن المخرج '
                       'يطابق العقد المتوقع.\n'
                       '\n'
                       '## Debugging habit\n'
                       '\n'
                       'قبل تعديل المعمارية: افحص شكل الموتر، dtype، device، القيم غير المنتهية، وضع train/eval، '
                       'وهل الخسارة تستقبل logits/targets بالشكل الصحيح.\n'
                       '\n'
                       '## تمارين الكود\n'
                       '\n'
                       'يوجد تمرينان برمجيان في `TOPIC["exercises"]`. كل تمرين يحتوي starter code ومعايير قبول؛ '
                       'لا تعتبره منجزاً لمجرد أن الكود يعمل دون خطأ.\n'
                       '\n'
                       '## المصدر والتحديث\n'
                       '\n'
                       'Source custom transforms/progressive resizing retained as experiment strategies, not '
                       'guaranteed improvements.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'class AddGaussianNoise:\n'
                           '    def __init__(self, std=0.05): self.std = std\n'
                           '    def __call__(self, x): return x + torch.randn_like(x) * self.std',
            'curriculum_id': 'C003-M09-L02'},
 'exercises': [{'title': 'Testable custom transform',
                'description': 'Implement Gaussian noise transform without in-place mutation. Test shape, dtype, '
                               'input immutability and deterministic behavior under a fixed seed.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\nclass AddGaussianNoise:\n    # TODO\n    pass',
                'acceptance_criteria': ['no in-place mutation',
                                        'shape/dtype preserved',
                                        'seeded run reproducible'],
                'validation_code': '',
                'hints': []},
               {'title': 'Progressive-resolution experiment',
                'description': 'Build a config-driven loop that trains 1 epoch at 64px then 1 epoch at 128px '
                               'while preserving model/optimizer state. Record throughput for each stage.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: resolution schedule + loader factory',
                'acceptance_criteria': ['same model carried forward',
                                        'resolution changes through pipeline',
                                        'reports examples/sec',
                                        'no claim that accuracy must improve'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Custom Transforms and Progressive Training — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Custom Transforms and Progressive '
                                     'Training»؟',
                         'options': ['الاعتماد على عدم ظهور Exception فقط',
                                     'إضافة assertions/قياسات تربط المدخل بالمخرج المتوقع',
                                     'زيادة عدد الطبقات مباشرة',
                                     'نسخ مخرجات مثال آخر'],
                         'correct': 1,
                         'explanation': 'التحقق العملي يحتاج عقداً قابلاً للاختبار، لا مجرد تشغيل الكود.'},
                        {'question': 'عند فشل تمرين PyTorch، ما أول ما ينبغي فحصه؟',
                         'options': ['شكل الموتر وdtype/device والعقد بين المراحل',
                                     'تغيير optimizer عشوائياً',
                                     'زيادة epochs بلا قياس',
                                     'استخدام test set أثناء التطوير'],
                         'correct': 0,
                         'explanation': 'الأخطاء العملية كثيراً ما تكون في الشكل أو النوع أو الجهاز أو contract '
                                        'بين المراحل.'},
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Custom Transforms and "
                                     "Progressive Training'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
