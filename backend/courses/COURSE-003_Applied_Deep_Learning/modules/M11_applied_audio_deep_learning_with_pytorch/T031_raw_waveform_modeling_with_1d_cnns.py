# -*- coding: utf-8 -*-
"""T031 — Applied Deep Learning, module M11.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 6,
 'chapter_title': 'A Journey into Sound',
 'source_file': 'تم لصق markdown(20260923-115219).md',
 'source_line_ranges': [[482, 552]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M11-L02',
 'source_note': 'Source 1D CNN idea retained; wrong 10-class head/log_softmax pattern corrected.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Raw-Waveform Modeling with 1D CNNs',
 'slug': 'applied-deep-learning-t031-raw-waveform-modeling-with-1d-cnns',
 'description': 'تطبيق عملي: Raw-Waveform Modeling with 1D CNNs مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'conv1d',
                'batchnorm1d',
                'maxpool1d',
                'temporal-receptive-field'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Raw-Waveform Modeling with 1D CNNs',
            'content': '# Raw-Waveform Modeling with 1D CNNs\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M11:** التعلم العميق التطبيقي للصوت · '
                       '**الدرس T031 / C003-M11-L02** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'Conv1d, BatchNorm1d, MaxPool1d, temporal receptive field, BCT shapes\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       'class WaveCNN(nn.Module):\n'
                       '    def __init__(self, classes=50):\n'
                       '        super().__init__(); '
                       'self.net=nn.Sequential(nn.Conv1d(1,32,9,stride=2,padding=4),nn.ReLU(),nn.MaxPool1d(4),nn.Conv1d(32,64,5,padding=2),nn.ReLU(),nn.AdaptiveAvgPool1d(1)); '
                       'self.fc=nn.Linear(64,classes)\n'
                       '    def forward(self,x): return self.fc(self.net(x).squeeze(-1))\n'
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
                       'Source 1D CNN idea retained; wrong 10-class head/log_softmax pattern corrected.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           'class WaveCNN(nn.Module):\n'
                           '    def __init__(self, classes=50):\n'
                           '        super().__init__(); '
                           'self.net=nn.Sequential(nn.Conv1d(1,32,9,stride=2,padding=4),nn.ReLU(),nn.MaxPool1d(4),nn.Conv1d(32,64,5,padding=2),nn.ReLU(),nn.AdaptiveAvgPool1d(1)); '
                           'self.fc=nn.Linear(64,classes)\n'
                           '    def forward(self,x): return self.fc(self.net(x).squeeze(-1))',
            'curriculum_id': 'C003-M11-L02'},
 'exercises': [{'title': 'Build a waveform classifier',
                'description': 'Implement a 1D CNN accepting `[B,1,T]` and returning 50 raw logits with adaptive '
                               'pooling.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch import nn\nclass AudioNet(nn.Module):\n    # TODO\n    pass',
                'acceptance_criteria': ['output [B,50]', 'raw logits', 'works for two different T lengths'],
                'validation_code': '',
                'hints': []},
               {'title': 'Trace temporal shapes',
                'description': 'Hook Conv1d/Pool layers to collect output shapes for a 5-second waveform and '
                               'report temporal downsampling ratio.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['uses forward hooks or explicit tracing',
                                        'reports each stage',
                                        'removes hooks afterward'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Raw-Waveform Modeling with 1D CNNs — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Raw-Waveform Modeling with 1D CNNs»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Raw-Waveform Modeling with "
                                     "1D CNNs'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
