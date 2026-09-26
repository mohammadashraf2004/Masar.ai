# -*- coding: utf-8 -*-
"""T005 — Applied Deep Learning, module M02.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[151, 188]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M02-L01',
 'source_note': 'Source introduces Dataset/DataLoader; terminology standardized to sample/target.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Datasets and DataLoaders',
 'slug': 'applied-deep-learning-t005-datasets-and-dataloaders',
 'description': 'تطبيق عملي: Datasets and DataLoaders مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'dataset', 'len', 'getitem', 'dataloader'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Datasets and DataLoaders',
            'content': '# Datasets and DataLoaders\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M02:** بناء خطوط بيانات PyTorch · **الدرس '
                       'T005 / C003-M02-L01** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'Dataset, __len__, __getitem__, DataLoader, batching, workers\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch.utils.data import Dataset, DataLoader\n'
                       '\n'
                       'class PairDataset(Dataset):\n'
                       '    def __init__(self, n=100):\n'
                       '        self.x = torch.randn(n, 10)\n'
                       '        self.y = (self.x.sum(dim=1) > 0).long()\n'
                       '    def __len__(self): return len(self.x)\n'
                       '    def __getitem__(self, idx): return self.x[idx], self.y[idx]\n'
                       '\n'
                       'loader = DataLoader(PairDataset(), batch_size=16, shuffle=True)\n'
                       'xb, yb = next(iter(loader))\n'
                       'assert xb.shape == (16, 10)\n'
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
                       'Source introduces Dataset/DataLoader; terminology standardized to sample/target.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch.utils.data import Dataset, DataLoader\n'
                           '\n'
                           'class PairDataset(Dataset):\n'
                           '    def __init__(self, n=100):\n'
                           '        self.x = torch.randn(n, 10)\n'
                           '        self.y = (self.x.sum(dim=1) > 0).long()\n'
                           '    def __len__(self): return len(self.x)\n'
                           '    def __getitem__(self, idx): return self.x[idx], self.y[idx]\n'
                           '\n'
                           'loader = DataLoader(PairDataset(), batch_size=16, shuffle=True)\n'
                           'xb, yb = next(iter(loader))\n'
                           'assert xb.shape == (16, 10)',
            'curriculum_id': 'C003-M02-L01'},
 'exercises': [{'title': 'Build a custom Dataset',
                'description': 'Create a dataset that validates feature/label lengths and returns `(sample, '
                               'target)` tensors.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch.utils.data import Dataset\n'
                                '\n'
                                'class ClassificationDataset(Dataset):\n'
                                '    def __init__(self, features, labels):\n'
                                '        # TODO\n'
                                '        pass\n'
                                '    def __len__(self):\n'
                                '        pass\n'
                                '    def __getitem__(self, idx):\n'
                                '        pass',
                'acceptance_criteria': ['length mismatch raises ValueError',
                                        'returns sample,target',
                                        'integer labels are torch.long'],
                'validation_code': '',
                'hints': []},
               {'title': 'Batch inspection utility',
                'description': 'Write `inspect_loader(loader)` returning first-batch shapes, dtypes and label '
                               'range without consuming the whole dataset.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def inspect_loader(loader):\n    # TODO\n    pass',
                'acceptance_criteria': ['inspects one batch only',
                                        'returns JSON-serializable metadata where possible',
                                        'does not mutate dataset'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Datasets and DataLoaders — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Datasets and DataLoaders»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Datasets and DataLoaders'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
