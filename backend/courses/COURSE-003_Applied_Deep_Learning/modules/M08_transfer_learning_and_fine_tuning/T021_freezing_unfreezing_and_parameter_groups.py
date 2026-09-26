# -*- coding: utf-8 -*-
"""T021 — Applied Deep Learning, module M08.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[55, 82], [357, 399]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M08-L02',
 'source_note': 'Source parameter-group example omits head in one place; Masar makes optimizer coverage an '
                'explicit test.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Freezing, Unfreezing, and Parameter Groups',
 'slug': 'applied-deep-learning-t021-freezing-unfreezing-and-parameter-groups',
 'description': 'تطبيق عملي: Freezing, Unfreezing, and Parameter Groups مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'requires-grad',
                'partial-unfreeze',
                'optimizer-groups',
                'batchnorm-state'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Freezing, Unfreezing, and Parameter Groups',
            'content': '# Freezing, Unfreezing, and Parameter Groups\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M08:** نقل التعلم والضبط الدقيق · **الدرس '
                       'T021 / C003-M08-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'requires_grad, partial unfreeze, optimizer groups, BatchNorm state, optimizer coverage\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '# Example idea after creating model:\n'
                       'for name, p in model.named_parameters():\n'
                       '    p.requires_grad = name.startswith("layer4") or name.startswith("fc")\n'
                       'optimizer = torch.optim.Adam([\n'
                       '    {"params": model.fc.parameters(), "lr": 1e-3},\n'
                       '    {"params": model.layer4.parameters(), "lr": 1e-4},\n'
                       '])\n'
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
                       'Source parameter-group example omits head in one place; Masar makes optimizer coverage an '
                       'explicit test.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '# Example idea after creating model:\n'
                           'for name, p in model.named_parameters():\n'
                           '    p.requires_grad = name.startswith("layer4") or name.startswith("fc")\n'
                           'optimizer = torch.optim.Adam([\n'
                           '    {"params": model.fc.parameters(), "lr": 1e-3},\n'
                           '    {"params": model.layer4.parameters(), "lr": 1e-4},\n'
                           '])',
            'curriculum_id': 'C003-M08-L02'},
 'exercises': [{'title': 'Optimizer coverage test',
                'description': 'Write a function that verifies every trainable parameter appears in exactly one '
                               'optimizer param group.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def assert_optimizer_covers_trainable(model, optimizer):\n'
                                '    # TODO: compare parameter object ids\n'
                                '    pass',
                'acceptance_criteria': ['detects missing trainable params',
                                        'detects duplicate params across groups',
                                        'ignores frozen params'],
                'validation_code': '',
                'hints': []},
               {'title': 'Two-phase unfreezing',
                'description': 'Implement phase 1 (head only) and phase 2 (layer4 + head) optimizer creation. '
                               'Report trainable counts in each phase.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['head-only phase correct',
                                        'partial fine-tune phase correct',
                                        'different learning rates',
                                        'trainable count increases'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Freezing, Unfreezing, and Parameter Groups — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Freezing, Unfreezing, and Parameter '
                                     'Groups»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Freezing, Unfreezing, and "
                                     "Parameter Groups'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
