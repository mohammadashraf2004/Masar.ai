# -*- coding: utf-8 -*-
"""T027 — Applied Deep Learning, module M10.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 5,
 'chapter_title': 'Text Classification',
 'source_file': 'تم لصق markdown(20260923-114931).md',
 'source_line_ranges': [[1106, 1143], [228, 276]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M10-L02',
 'source_note': 'Source recurrent model retained; Masar adds explicit shape reasoning and modern batch_first '
                'usage.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Building LSTM, GRU, and Bidirectional Models',
 'slug': 'applied-deep-learning-t027-building-lstm-gru-and-bidirectional-models',
 'description': 'تطبيق عملي: Building LSTM, GRU, and Bidirectional Models مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'lstm', 'gru', 'batch-first', 'hidden-state'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Building LSTM, GRU, and Bidirectional Models',
            'content': '# Building LSTM, GRU, and Bidirectional Models\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M10:** نماذج التسلسل باستخدام PyTorch · '
                       '**الدرس T027 / C003-M10-L02** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'LSTM, GRU, batch_first, hidden state, cell state, bidirectional, D*H\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       'class SeqClassifier(nn.Module):\n'
                       '    def __init__(self, vocab=100, emb=32, hidden=64, classes=3, bidirectional=True):\n'
                       '        super().__init__(); self.emb=nn.Embedding(vocab,emb,padding_idx=0)\n'
                       '        self.rnn=nn.LSTM(emb,hidden,batch_first=True,bidirectional=bidirectional)\n'
                       '        self.fc=nn.Linear(hidden*(2 if bidirectional else 1), classes)\n'
                       '    def forward(self, ids):\n'
                       '        _, (h, _) = self.rnn(self.emb(ids))\n'
                       '        rep = torch.cat([h[-2],h[-1]],1) if self.rnn.bidirectional else h[-1]\n'
                       '        return self.fc(rep)\n'
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
                       'Source recurrent model retained; Masar adds explicit shape reasoning and modern '
                       'batch_first usage.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           'class SeqClassifier(nn.Module):\n'
                           '    def __init__(self, vocab=100, emb=32, hidden=64, classes=3, bidirectional=True):\n'
                           '        super().__init__(); self.emb=nn.Embedding(vocab,emb,padding_idx=0)\n'
                           '        self.rnn=nn.LSTM(emb,hidden,batch_first=True,bidirectional=bidirectional)\n'
                           '        self.fc=nn.Linear(hidden*(2 if bidirectional else 1), classes)\n'
                           '    def forward(self, ids):\n'
                           '        _, (h, _) = self.rnn(self.emb(ids))\n'
                           '        rep = torch.cat([h[-2],h[-1]],1) if self.rnn.bidirectional else h[-1]\n'
                           '        return self.fc(rep)',
            'curriculum_id': 'C003-M10-L02'},
 'exercises': [{'title': 'LSTM/GRU swap',
                'description': 'Write a classifier configurable with `rnn_type="lstm"|"gru"` and keep the same '
                               'output contract.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch import nn\n'
                                'class FlexibleRNNClassifier(nn.Module):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['both variants run',
                                        'batch_first=True',
                                        'correct hidden extraction',
                                        'same logits shape'],
                'validation_code': '',
                'hints': []},
               {'title': 'Bidirectional hidden-state test',
                'description': 'For a 2-layer bidirectional LSTM, assert hidden-state shape and correctly '
                               'concatenate the final forward/backward states of the last layer.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['correct h_n shape reasoning',
                                        'does not use output[:,-1] as a substitute',
                                        'returns [B,2H] representation'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Building LSTM, GRU, and Bidirectional Models — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Building LSTM, GRU, and Bidirectional '
                                     'Models»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Building LSTM, GRU, and "
                                     "Bidirectional Models'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
