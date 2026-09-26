# -*- coding: utf-8 -*-
"""T039 — Applied Deep Learning, module M13.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[955, 1225]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M13-L02',
 'source_note': 'Source slow transform case retained; terminology corrected to element-wise tensor addition.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Optimizing Data and Transformation Pipelines',
 'slug': 'applied-deep-learning-t039-optimizing-data-and-transformation-pipelines',
 'description': 'تطبيق عملي: Optimizing Data and Transformation Pipelines مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'vectorization',
                'batch-transforms',
                'dataloader-tuning',
                'pin-memory'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Optimizing Data and Transformation Pipelines',
            'content': '# Optimizing Data and Transformation Pipelines\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M13:** التنميط والترجمة وتحسين الأداء · '
                       '**الدرس T039 / C003-M13-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'vectorization, batch transforms, DataLoader tuning, pin_memory, num_workers, benchmark\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       '# Prefer batch tensor operations over Python/PIL loops when semantics allow:\n'
                       'noise = torch.randn_like(batch) * 0.05\n'
                       'batch_aug = batch + noise\n'
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
                       'Source slow transform case retained; terminology corrected to element-wise tensor '
                       'addition.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': '# Prefer batch tensor operations over Python/PIL loops when semantics allow:\n'
                           'noise = torch.randn_like(batch) * 0.05\n'
                           'batch_aug = batch + noise',
            'curriculum_id': 'C003-M13-L02'},
 'exercises': [{'title': 'Vectorize a slow transform',
                'description': 'Replace a per-sample Python loop that adds noise with one batched tensor '
                               'operation and benchmark both.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: slow_loop(batch) and vectorized(batch)',
                'acceptance_criteria': ['numerically comparable behavior',
                                        'timed after warmup',
                                        'reports speed ratio',
                                        'does not call addition matrix multiplication'],
                'validation_code': '',
                'hints': []},
               {'title': 'DataLoader tuning experiment',
                'description': 'Benchmark at least 3 num_workers settings (and pin_memory when CUDA is available) '
                               'on the same dataset. Report batches/sec and choose based on evidence.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same dataset/batch size',
                                        'warmup',
                                        'portable when multiprocessing constraints exist',
                                        'evidence-based recommendation'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Optimizing Data and Transformation Pipelines — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Optimizing Data and Transformation '
                                     'Pipelines»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Optimizing Data and "
                                     "Transformation Pipelines'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
