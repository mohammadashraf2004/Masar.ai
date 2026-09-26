# -*- coding: utf-8 -*-
"""T004 — Applied Deep Learning, module M01.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 1,
 'chapter_title': 'Getting Started with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114052).md',
 'source_line_ranges': [[872, 896]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M01-L04',
 'source_note': 'Source broadcasting rules retained and converted into a practical image-normalization task.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Broadcasting and Shape Reasoning',
 'slug': 'applied-deep-learning-t004-broadcasting-and-shape-reasoning',
 'description': 'تطبيق عملي: Broadcasting and Shape Reasoning مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 4,
 'difficulty': 'intermediate',
 'estimated_hours': 0.5,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'broadcasting-rules',
                'singleton-dimensions',
                'normalization',
                'shape-assertions'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Broadcasting and Shape Reasoning',
            'content': '# Broadcasting and Shape Reasoning\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M01:** أساسيات PyTorch: الموترات والأشكال '
                       'والأجهزة · **الدرس T004 / C003-M01-L04** · **المدة:** 30 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'broadcasting rules, singleton dimensions, normalization, shape assertions\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'x = torch.randn(8, 3, 32, 32)\n'
                       'mean = torch.tensor([0.5, 0.4, 0.3]).view(1, 3, 1, 1)\n'
                       'std = torch.tensor([0.2, 0.2, 0.2]).view(1, 3, 1, 1)\n'
                       'y = (x - mean) / std\n'
                       'assert y.shape == x.shape\n'
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
                       'Source broadcasting rules retained and converted into a practical image-normalization '
                       'task.\n',
            'estimated_minutes': 30,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'x = torch.randn(8, 3, 32, 32)\n'
                           'mean = torch.tensor([0.5, 0.4, 0.3]).view(1, 3, 1, 1)\n'
                           'std = torch.tensor([0.2, 0.2, 0.2]).view(1, 3, 1, 1)\n'
                           'y = (x - mean) / std\n'
                           'assert y.shape == x.shape',
            'curriculum_id': 'C003-M01-L04'},
 'exercises': [{'title': 'Broadcast-safe normalization',
                'description': 'Implement channel-wise normalization for NCHW tensors. Reject mean/std lengths '
                               'that do not match C.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef normalize_nchw(x, mean, std):\n    # TODO\n    pass',
                'acceptance_criteria': ['preserves input shape',
                                        'broadcasts over N,H,W',
                                        'validates channels and non-zero std'],
                'validation_code': '',
                'hints': []},
               {'title': 'Find the broadcasting bug',
                'description': 'Fix the following code without loops. Explain why `[3]` does not align with the '
                               'channel axis of `[N,C,H,W]`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'x = torch.randn(4, 3, 16, 16)\n'
                                'mean = torch.tensor([0.5, 0.4, 0.3])\n'
                                '# broken = x - mean',
                'acceptance_criteria': ['uses explicit singleton dimensions',
                                        'no Python loop',
                                        'explanation references trailing-dimension alignment'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Broadcasting and Shape Reasoning — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Broadcasting and Shape Reasoning»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Broadcasting and Shape "
                                     "Reasoning'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Tensor Pipeline Diagnostic Lab',
             'description': 'Repair a malformed tensor pipeline: dtype, device, HWC→CHW, reshape, broadcasting '
                            'and assertions.',
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
