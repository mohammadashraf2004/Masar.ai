# -*- coding: utf-8 -*-
"""T042 — Applied Deep Learning, module M14.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[1370, 1529]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M14-L02',
 'source_note': 'Source checkpointing concept retained; recomputation explanation and modern use_reentrant '
                'guidance corrected.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Activation Checkpointing and Memory–Compute Trade-offs',
 'slug': 'applied-deep-learning-t042-activation-checkpointing-and-memory-compute-trade-offs',
 'description': 'تطبيق عملي: Activation Checkpointing and Memory–Compute Trade-offs مع كود وتمارين تحقق وتصحيح '
                'أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'activation-checkpointing',
                'recompute',
                'use-reentrant-false',
                'rng-state-caution'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Activation Checkpointing and Memory–Compute Trade-offs',
            'content': '# Activation Checkpointing and Memory–Compute Trade-offs\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M14:** ذاكرة المسرع وتصحيح النماذج الكبيرة · '
                       '**الدرس T042 / C003-M14-L02** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'activation checkpointing, recompute, use_reentrant=False, RNG/state caution, '
                       'memory/compute benchmark\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch.utils.checkpoint import checkpoint\n'
                       '\n'
                       'def forward(self, x):\n'
                       '    x = checkpoint(self.block1, x, use_reentrant=False)\n'
                       '    return self.block2(x)\n'
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
                       'Source checkpointing concept retained; recomputation explanation and modern use_reentrant '
                       'guidance corrected.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch.utils.checkpoint import checkpoint\n'
                           '\n'
                           'def forward(self, x):\n'
                           '    x = checkpoint(self.block1, x, use_reentrant=False)\n'
                           '    return self.block2(x)',
            'curriculum_id': 'C003-M14-L02'},
 'exercises': [{'title': 'Checkpoint one block',
                'description': 'Wrap a model block with `checkpoint(..., use_reentrant=False)` and verify '
                               'outputs/grads match an uncheckpointed copy within tolerance.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['explicit use_reentrant=False',
                                        'same weights/inputs',
                                        'output and gradient parity'],
                'validation_code': '',
                'hints': []},
               {'title': 'Measure trade-off',
                'description': 'On CUDA if available, compare peak memory and step time for checkpointed vs '
                               'normal model. Report the trade-off rather than only memory.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same model weights',
                                        'peak memory measured',
                                        'step time measured',
                                        'trade-off documented'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Activation Checkpointing and Memory–Compute Trade-offs — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Activation Checkpointing and '
                                     'Memory–Compute Trade-offs»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Activation Checkpointing "
                                     "and Memory–Compute Trade-offs'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Fit a Larger Model into Memory',
             'description': 'Measure memory, apply AMP and activation checkpointing, and report speed/memory '
                            'trade-offs.',
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
