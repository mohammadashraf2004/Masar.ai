# -*- coding: utf-8 -*-
"""T012 — Applied Deep Learning, module M04.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[816, 853]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M04-L03',
 'source_note': 'Source CUDA pattern generalized to portable device-aware training.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Device-Aware Training',
 'slug': 'applied-deep-learning-t012-device-aware-training',
 'description': 'تطبيق عملي: Device-Aware Training مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'model-to',
                'batch-to',
                'device-mismatch',
                'non-blocking-transfer-awareness'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Device-Aware Training',
            'content': '# Device-Aware Training\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M04:** تدريب وتقييم نماذج PyTorch · **الدرس '
                       'T012 / C003-M04-L03** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'model.to, batch.to, device mismatch, non-blocking transfer awareness, portable CPU/GPU\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def move_batch(batch, device):\n'
                       '    return tuple(t.to(device) if torch.is_tensor(t) else t for t in batch)\n'
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
                       'Source CUDA pattern generalized to portable device-aware training.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def move_batch(batch, device):\n'
                           '    return tuple(t.to(device) if torch.is_tensor(t) else t for t in batch)',
            'curriculum_id': 'C003-M04-L03'},
 'exercises': [{'title': 'Portable device trainer',
                'description': 'Refactor a CPU-only training function so the model and every tensor use a '
                               'selected device without hardcoded `.cuda()`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: implement select_device(), move model, move batch',
                'acceptance_criteria': ['runs on CPU-only machine',
                                        'no .cuda() calls',
                                        'all model params and batch tensors share device'],
                'validation_code': '',
                'hints': []},
               {'title': 'Device mismatch debugger',
                'description': 'Write `assert_same_device(model, *tensors)` that raises a clear error if any '
                               'tensor is on a different device than the model.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def assert_same_device(model, *tensors):\n    # TODO\n    pass',
                'acceptance_criteria': ['reports model device',
                                        'reports offending tensor device',
                                        'works for parameterized models'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Device-Aware Training — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Device-Aware Training»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Device-Aware Training'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Reusable PyTorch Trainer',
             'description': 'Build train/eval functions that work on CPU or accelerator, track metrics, and keep '
                            'evaluation gradient-free.',
             'project_kind': 'portfolio',
             'is_portfolio': True,
             'deliverables': ['working Python/notebook implementation',
                              'README or experiment notes',
                              'measured checks/metrics',
                              'saved artifact when relevant'],
             'acceptance_criteria': ['code runs without silent shape/device errors',
                                     'results are measured rather than asserted',
                                     'train/validation/test roles remain correct',
                                     'limitations and failed experiments are documented']}}
