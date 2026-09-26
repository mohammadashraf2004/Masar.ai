# -*- coding: utf-8 -*-
"""T008 — Applied Deep Learning, module M03.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[491, 563]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M03-L01',
 'source_note': 'Source code has class/super/forward inconsistencies; Masar turns them into a debugging lab.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Defining Models with nn.Module',
 'slug': 'applied-deep-learning-t008-defining-models-with-module',
 'description': 'تطبيق عملي: Defining Models with nn.Module مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'module', 'super', 'registered-layers', 'forward'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Defining Models with nn.Module',
            'content': '# Defining Models with nn.Module\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M03:** بناء النماذج باستخدام nn.Module · '
                       '**الدرس T008 / C003-M03-L01** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'nn.Module, super, registered layers, forward, Flatten, logits\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       '\n'
                       'class MLP(nn.Module):\n'
                       '    def __init__(self, in_features=20, classes=3):\n'
                       '        super().__init__()\n'
                       '        self.net = nn.Sequential(nn.Linear(in_features, 64), nn.ReLU(), nn.Linear(64, '
                       'classes))\n'
                       '    def forward(self, x):\n'
                       '        return self.net(x)\n'
                       '\n'
                       'model = MLP()\n'
                       'assert model(torch.randn(8, 20)).shape == (8, 3)\n'
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
                       'Source code has class/super/forward inconsistencies; Masar turns them into a debugging '
                       'lab.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           '\n'
                           'class MLP(nn.Module):\n'
                           '    def __init__(self, in_features=20, classes=3):\n'
                           '        super().__init__()\n'
                           '        self.net = nn.Sequential(nn.Linear(in_features, 64), nn.ReLU(), nn.Linear(64, '
                           'classes))\n'
                           '    def forward(self, x):\n'
                           '        return self.net(x)\n'
                           '\n'
                           'model = MLP()\n'
                           'assert model(torch.randn(8, 20)).shape == (8, 3)',
            'curriculum_id': 'C003-M03-L01'},
 'exercises': [{'title': 'Implement a classifier module',
                'description': 'Build `Classifier` with two hidden layers, ReLU and Dropout. It must accept `[B, '
                               '20]` and return `[B, 5]` logits.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'from torch import nn\n'
                                '\n'
                                'class Classifier(nn.Module):\n'
                                '    def __init__(self):\n'
                                '        super().__init__()\n'
                                '        # TODO\n'
                                '    def forward(self, x):\n'
                                '        # TODO\n'
                                '        pass',
                'acceptance_criteria': ['all layers registered in __init__',
                                        'forward accepts x',
                                        'returns raw logits shape [B,5]'],
                'validation_code': 'm=Classifier(); assert m(torch.randn(7,20)).shape==(7,5)',
                'hints': []},
               {'title': 'Repair a broken nn.Module',
                'description': 'Fix wrong `super`, missing `x` argument, and a layer stored in a plain local '
                               'variable rather than on `self`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch import nn\n'
                                'class BrokenNet(nn.Module):\n'
                                '    def __init__(self):\n'
                                '        super(Net, self).__init__()\n'
                                '        layer = nn.Linear(10, 2)\n'
                                '    def forward(self):\n'
                                '        return self.layer(x)',
                'acceptance_criteria': ['model parameters are registered',
                                        'forward signature is correct',
                                        'dummy forward succeeds'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Defining Models with nn.Module — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Defining Models with nn.Module»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Defining Models with "
                                     "nn.Module'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
