# -*- coding: utf-8 -*-
"""T017 — Applied Deep Learning, module M06.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 3,
 'chapter_title': 'Convolutional Neural Networks',
 'source_file': 'تم لصق markdown(20260923-114507).md',
 'source_line_ranges': [[303, 427], [932, 955]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M06-L03',
 'source_note': 'Source Dropout/BatchNorm retained; Masar corrects oversimplified explanations and separates '
                'parameter freezing from running-state behavior.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Pooling, Dropout, and Batch Normalization in Practice',
 'slug': 'applied-deep-learning-t017-pooling-dropout-and-batch-normalization-in-practice',
 'description': 'تطبيق عملي: Pooling, Dropout, and Batch Normalization in Practice مع كود وتمارين تحقق وتصحيح '
                'أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'maxpool2d', 'adaptiveavgpool2d', 'dropout', 'batchnorm2d'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Pooling, Dropout, and Batch Normalization in Practice',
            'content': '# Pooling, Dropout, and Batch Normalization in Practice\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M06:** تنفيذ الشبكات الالتفافية في PyTorch · '
                       '**الدرس T017 / C003-M06-L03** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'MaxPool2d, AdaptiveAvgPool2d, Dropout, BatchNorm2d, train/eval state\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       'm = nn.Sequential(nn.BatchNorm1d(8), nn.ReLU(), nn.Dropout(0.5))\n'
                       'x = torch.randn(16, 8)\n'
                       'm.train(); a = m(x); b = m(x)\n'
                       'm.eval(); c = m(x); d = m(x)\n'
                       'print(torch.equal(a,b), torch.allclose(c,d))\n'
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
                       'Source Dropout/BatchNorm retained; Masar corrects oversimplified explanations and '
                       'separates parameter freezing from running-state behavior.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           'm = nn.Sequential(nn.BatchNorm1d(8), nn.ReLU(), nn.Dropout(0.5))\n'
                           'x = torch.randn(16, 8)\n'
                           'm.train(); a = m(x); b = m(x)\n'
                           'm.eval(); c = m(x); d = m(x)\n'
                           'print(torch.equal(a,b), torch.allclose(c,d))',
            'curriculum_id': 'C003-M06-L03'},
 'exercises': [{'title': 'Mode-sensitive layer experiment',
                'description': 'Measure output variance across repeated passes for Dropout in train vs eval mode, '
                               'and inspect BatchNorm running_mean before/after training passes.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\nfrom torch import nn\n# TODO',
                'acceptance_criteria': ['shows stochastic dropout only in train',
                                        'shows BatchNorm running stats update in train',
                                        'eval does not update running stats'],
                'validation_code': '',
                'hints': []},
               {'title': 'Freeze parameters vs BatchNorm statistics',
                'description': 'Demonstrate that `requires_grad=False` on BatchNorm parameters does not by itself '
                               'stop running_mean updates while the module is in train mode.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['freezes affine gradients',
                                        'observes running stats still change in train',
                                        'explains separate concerns'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Pooling, Dropout, and Batch Normalization in Practice — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Pooling, Dropout, and Batch '
                                     'Normalization in Practice»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Pooling, Dropout, and "
                                     "Batch Normalization in Practice'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'CNN Architecture Lab',
             'description': 'Design a CNN that passes dummy-forward shape tests, then train it on a small image '
                            'dataset or FakeData baseline.',
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
