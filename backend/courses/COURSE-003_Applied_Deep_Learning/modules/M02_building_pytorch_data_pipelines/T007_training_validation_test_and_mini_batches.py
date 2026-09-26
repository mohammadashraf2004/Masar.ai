# -*- coding: utf-8 -*-
"""T007 — Applied Deep Learning, module M02.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[304, 417]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M02-L03',
 'source_note': 'Source explains train/validation/test and batching; Masar adds reproducibility and leakage '
                'checks.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Training, Validation, Test, and Mini-Batches',
 'slug': 'applied-deep-learning-t007-training-validation-test-and-mini-batches',
 'description': 'تطبيق عملي: Training, Validation, Test, and Mini-Batches مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'deterministic-split',
                'data-leakage',
                'shuffle-policy',
                'batch-size'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Training, Validation, Test, and Mini-Batches',
            'content': '# Training, Validation, Test, and Mini-Batches\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M02:** بناء خطوط بيانات PyTorch · **الدرس '
                       'T007 / C003-M02-L03** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'deterministic split, data leakage, shuffle policy, batch size, generator seed\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch.utils.data import random_split, DataLoader, TensorDataset\n'
                       '\n'
                       'ds = TensorDataset(torch.randn(1000, 20), torch.randint(0, 3, (1000,)))\n'
                       'g = torch.Generator().manual_seed(42)\n'
                       'train_ds, val_ds, test_ds = random_split(ds, [800, 100, 100], generator=g)\n'
                       'train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)\n'
                       'val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)\n'
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
                       'Source explains train/validation/test and batching; Masar adds reproducibility and '
                       'leakage checks.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch.utils.data import random_split, DataLoader, TensorDataset\n'
                           '\n'
                           'ds = TensorDataset(torch.randn(1000, 20), torch.randint(0, 3, (1000,)))\n'
                           'g = torch.Generator().manual_seed(42)\n'
                           'train_ds, val_ds, test_ds = random_split(ds, [800, 100, 100], generator=g)\n'
                           'train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)\n'
                           'val_loader = DataLoader(val_ds, batch_size=64, shuffle=False)',
            'curriculum_id': 'C003-M02-L03'},
 'exercises': [{'title': 'Reproducible split function',
                'description': 'Implement `make_splits(dataset, seed)` returning 80/10/10 subsets with identical '
                               'indices for identical seeds.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'from torch.utils.data import random_split\n'
                                '\n'
                                'def make_splits(dataset, seed=42):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['exact 80/10/10 for length divisible by 10',
                                        'same seed -> same subset indices',
                                        'test set not reused for tuning'],
                'validation_code': '',
                'hints': []},
               {'title': 'Loader policy audit',
                'description': 'Given three DataLoaders, assert train shuffles and validation/test do not. Also '
                               'report batch size and drop_last.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def audit_loaders(train_loader, val_loader, test_loader):\n'
                                '    # TODO: inspect samplers/configuration\n'
                                '    pass',
                'acceptance_criteria': ['detects obvious shuffle mistakes',
                                        'returns configuration report',
                                        'does not iterate full datasets'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Training, Validation, Test, and Mini-Batches — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Training, Validation, Test, and '
                                     'Mini-Batches»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Training, Validation, "
                                     "Test, and Mini-Batches'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Production-Style Data Pipeline Lab',
             'description': 'Build a reproducible Dataset/DataLoader pipeline with deterministic splits, '
                            'train-only augmentation and batch sanity checks.',
             'project_kind': 'module_lab',
             'is_portfolio': False,
             'deliverables': ['working Python/notebook implementation',
                              'README or experiment notes',
                              'measured checks/metrics',
                              'saved artifact when relevant'],
             'acceptance_criteria': ['code runs without silent shape/device errors',
                                     'results are measured rather than asserted',
                                     'train/validation/test roles remain correct',
                                     'limitations and failed experiments are documented']}}
