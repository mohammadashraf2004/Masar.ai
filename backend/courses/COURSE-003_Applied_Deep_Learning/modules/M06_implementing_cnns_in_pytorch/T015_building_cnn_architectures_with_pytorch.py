# -*- coding: utf-8 -*-
"""T015 — Applied Deep Learning, module M06.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 3,
 'chapter_title': 'Convolutional Neural Networks',
 'source_file': 'تم لصق markdown(20260923-114507).md',
 'source_line_ranges': [[25, 98]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M06-L01',
 'source_note': 'Source CNN implementation retained; Masar adds resolution-tolerant heads and dummy-forward '
                'tests.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Building CNN Architectures with PyTorch',
 'slug': 'applied-deep-learning-t015-building-cnn-architectures-with-pytorch',
 'description': 'تطبيق عملي: Building CNN Architectures with PyTorch مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'conv2d',
                'sequential',
                'adaptiveavgpool2d',
                'feature-extractor'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Building CNN Architectures with PyTorch',
            'content': '# Building CNN Architectures with PyTorch\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M06:** تنفيذ الشبكات الالتفافية في PyTorch · '
                       '**الدرس T015 / C003-M06-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'Conv2d, Sequential, AdaptiveAvgPool2d, feature extractor, classifier head, dummy forward\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       '\n'
                       'class SmallCNN(nn.Module):\n'
                       '    def __init__(self, classes=5):\n'
                       '        super().__init__()\n'
                       '        self.features = nn.Sequential(\n'
                       '            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),\n'
                       '            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((1,1)))\n'
                       '        self.head = nn.Linear(64, classes)\n'
                       '    def forward(self, x):\n'
                       '        x = self.features(x).flatten(1)\n'
                       '        return self.head(x)\n'
                       '\n'
                       'assert SmallCNN()(torch.randn(4,3,96,96)).shape == (4,5)\n'
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
                       'Source CNN implementation retained; Masar adds resolution-tolerant heads and '
                       'dummy-forward tests.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           '\n'
                           'class SmallCNN(nn.Module):\n'
                           '    def __init__(self, classes=5):\n'
                           '        super().__init__()\n'
                           '        self.features = nn.Sequential(\n'
                           '            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),\n'
                           '            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d((1,1)))\n'
                           '        self.head = nn.Linear(64, classes)\n'
                           '    def forward(self, x):\n'
                           '        x = self.features(x).flatten(1)\n'
                           '        return self.head(x)\n'
                           '\n'
                           'assert SmallCNN()(torch.randn(4,3,96,96)).shape == (4,5)',
            'curriculum_id': 'C003-M06-L01'},
 'exercises': [{'title': 'Design a resolution-tolerant CNN',
                'description': 'Build a CNN that accepts both 64x64 and 96x96 RGB batches and returns 6 logits '
                               'without hardcoding flatten spatial dimensions.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch import nn\nclass FlexibleCNN(nn.Module):\n    # TODO\n    pass',
                'acceptance_criteria': ['uses AdaptiveAvgPool2d or equivalent',
                                        'both resolutions pass',
                                        'output [B,6]'],
                'validation_code': '',
                'hints': []},
               {'title': 'Architecture smoke tests',
                'description': 'Write a function that runs dummy forwards for several batch sizes/resolutions and '
                               'reports failures with shapes.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def smoke_test_model(model, shapes):\n    # TODO\n    pass',
                'acceptance_criteria': ['tests multiple shapes',
                                        'uses no real dataset',
                                        'returns useful failure messages'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Building CNN Architectures with PyTorch — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Building CNN Architectures with '
                                     'PyTorch»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Building CNN Architectures "
                                     "with PyTorch'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
