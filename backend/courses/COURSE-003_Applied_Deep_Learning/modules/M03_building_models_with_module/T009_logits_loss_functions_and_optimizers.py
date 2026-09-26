# -*- coding: utf-8 -*-
"""T009 — Applied Deep Learning, module M03.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[571, 620]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M03-L02',
 'source_note': 'Source correctly removes softmax before CrossEntropyLoss; Masar reinforces logits-based '
                'loss contracts.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Logits, Loss Functions, and Optimizers',
 'slug': 'applied-deep-learning-t009-logits-loss-functions-and-optimizers',
 'description': 'تطبيق عملي: Logits, Loss Functions, and Optimizers مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'logits',
                'crossentropyloss',
                'bcewithlogitsloss',
                'optimizer'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Logits, Loss Functions, and Optimizers',
            'content': '# Logits, Loss Functions, and Optimizers\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M03:** بناء النماذج باستخدام nn.Module · '
                       '**الدرس T009 / C003-M03-L02** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'logits, CrossEntropyLoss, BCEWithLogitsLoss, optimizer, learning rate, parameter update\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       'model = nn.Linear(10, 4)\n'
                       'x = torch.randn(16, 10)\n'
                       'y = torch.randint(0, 4, (16,))\n'
                       'loss_fn = nn.CrossEntropyLoss()\n'
                       'opt = torch.optim.Adam(model.parameters(), lr=1e-3)\n'
                       'opt.zero_grad(set_to_none=True)\n'
                       'loss = loss_fn(model(x), y)\n'
                       'loss.backward(); opt.step()\n'
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
                       'Source correctly removes softmax before CrossEntropyLoss; Masar reinforces logits-based '
                       'loss contracts.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           'model = nn.Linear(10, 4)\n'
                           'x = torch.randn(16, 10)\n'
                           'y = torch.randint(0, 4, (16,))\n'
                           'loss_fn = nn.CrossEntropyLoss()\n'
                           'opt = torch.optim.Adam(model.parameters(), lr=1e-3)\n'
                           'opt.zero_grad(set_to_none=True)\n'
                           'loss = loss_fn(model(x), y)\n'
                           'loss.backward(); opt.step()',
            'curriculum_id': 'C003-M03-L02'},
 'exercises': [{'title': 'Prove parameters update',
                'description': 'Run one optimization step and assert at least one parameter changed while output '
                               'remains finite.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'from torch import nn\n'
                                '# TODO: build model, clone params, step once, compare',
                'acceptance_criteria': ['uses raw logits with CrossEntropyLoss',
                                        'zeroes gradients',
                                        'at least one parameter changes',
                                        'loss finite'],
                'validation_code': '',
                'hints': []},
               {'title': 'Choose the correct loss',
                'description': 'Implement two tiny heads: multiclass 4-way and binary. Pair them with '
                               'CrossEntropyLoss and BCEWithLogitsLoss with correct target shapes/dtypes.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['multiclass output [B,4] + long targets',
                                        'binary output [B] or [B,1] + float targets',
                                        'no softmax/sigmoid before logits-based loss'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Logits, Loss Functions, and Optimizers — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Logits, Loss Functions, and '
                                     'Optimizers»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Logits, Loss Functions, "
                                     "and Optimizers'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'From nn.Module to One Optimizer Step',
             'description': 'Implement a classifier, loss and optimizer and prove that a training step updates '
                            'the intended parameters.',
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
