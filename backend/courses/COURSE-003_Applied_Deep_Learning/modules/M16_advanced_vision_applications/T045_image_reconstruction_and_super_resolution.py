# -*- coding: utf-8 -*-
"""T045 — Applied Deep Learning, module M16.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 9,
 'chapter_title': 'PyTorch in the Wild',
 'source_file': 'تم لصق markdown(20260923-220506).md',
 'source_line_ranges': [[377, 565]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M16-L01',
 'source_note': 'Source super-resolution retained as optional implementation; theoretical GAN context reused '
                'from COURSE-002.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Image Reconstruction and Super-Resolution',
 'slug': 'applied-deep-learning-t045-image-reconstruction-and-super-resolution',
 'description': 'تطبيق عملي: Image Reconstruction and Super-Resolution مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'encoder-decoder',
                'convtranspose2d',
                'reconstruction-loss',
                'upsampling'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Image Reconstruction and Super-Resolution',
            'content': '# Image Reconstruction and Super-Resolution\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M16:** تطبيقات الرؤية المتقدمة · **الدرس '
                       'T045 / C003-M16-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'encoder-decoder, ConvTranspose2d, reconstruction loss, upsampling, artifact awareness\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch import nn\n'
                       'class AutoEncoder(nn.Module):\n'
                       '    def __init__(self):\n'
                       '        super().__init__(); self.enc=nn.Sequential(nn.Conv2d(3,32,4,2,1),nn.ReLU()); '
                       'self.dec=nn.Sequential(nn.ConvTranspose2d(32,3,4,2,1),nn.Sigmoid())\n'
                       '    def forward(self,x): return self.dec(self.enc(x))\n'
                       'assert AutoEncoder()(torch.rand(2,3,64,64)).shape==(2,3,64,64)\n'
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
                       'Source super-resolution retained as optional implementation; theoretical GAN context '
                       'reused from COURSE-002.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch import nn\n'
                           'class AutoEncoder(nn.Module):\n'
                           '    def __init__(self):\n'
                           '        super().__init__(); self.enc=nn.Sequential(nn.Conv2d(3,32,4,2,1),nn.ReLU()); '
                           'self.dec=nn.Sequential(nn.ConvTranspose2d(32,3,4,2,1),nn.Sigmoid())\n'
                           '    def forward(self,x): return self.dec(self.enc(x))\n'
                           'assert AutoEncoder()(torch.rand(2,3,64,64)).shape==(2,3,64,64)',
            'curriculum_id': 'C003-M16-L01'},
 'exercises': [{'title': 'Build a reconstruction model',
                'description': 'Implement an encoder/decoder that preserves input spatial size and train one step '
                               'with L1 loss.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same input/output shape',
                                        'loss on reconstructed image',
                                        'raw task has no class logits'],
                'validation_code': '',
                'hints': []},
               {'title': 'Super-resolution shape task',
                'description': 'Build a model mapping `[B,3,32,32]` to `[B,3,64,64]` and assert shape before '
                               'training.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['2x spatial output',
                                        'dummy-forward test',
                                        'explains ConvTranspose2d is not a mathematical inverse'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Image Reconstruction and Super-Resolution — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Image Reconstruction and '
                                     'Super-Resolution»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Image Reconstruction and "
                                     "Super-Resolution'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
