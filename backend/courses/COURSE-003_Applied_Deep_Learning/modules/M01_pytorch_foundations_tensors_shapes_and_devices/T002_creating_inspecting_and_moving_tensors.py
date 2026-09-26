# -*- coding: utf-8 -*-
"""T002 — Applied Deep Learning, module M01.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 1,
 'chapter_title': 'Getting Started with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114052).md',
 'source_line_ranges': [[631, 720]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M01-L02',
 'source_note': 'Source-backed tensor fundamentals; Masar adds validation habits and portable-device checks.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Creating, Inspecting, and Moving Tensors',
 'slug': 'applied-deep-learning-t002-creating-inspecting-and-moving-tensors',
 'description': 'تطبيق عملي: Creating, Inspecting, and Moving Tensors مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'tensor-construction', 'dtype', 'indexing', 'item'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Creating, Inspecting, and Moving Tensors',
            'content': '# Creating, Inspecting, and Moving Tensors\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M01:** أساسيات PyTorch: الموترات والأشكال '
                       'والأجهزة · **الدرس T002 / C003-M01-L02** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'tensor construction, dtype, indexing, item, device movement\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)\n'
                       'print(x.shape, x.dtype)\n'
                       'print(x[0, 1].item())\n'
                       'y = torch.ones_like(x)\n'
                       'z = x + y\n'
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
                       'Source-backed tensor fundamentals; Masar adds validation habits and portable-device '
                       'checks.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)\n'
                           'print(x.shape, x.dtype)\n'
                           'print(x[0, 1].item())\n'
                           'y = torch.ones_like(x)\n'
                           'z = x + y',
            'curriculum_id': 'C003-M01-L02'},
 'exercises': [{'title': 'Prepare a numeric batch',
                'description': 'Implement `prepare_batch(values, device)` that converts nested Python data to '
                               'float32, validates it is rank-2, and moves it to the selected device.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef prepare_batch(values, device):\n    # TODO\n    pass',
                'acceptance_criteria': ['dtype is float32',
                                        'rank must be 2 or raise ValueError',
                                        'result lives on requested device'],
                'validation_code': 'x=prepare_batch([[1,2],[3,4]], torch.device("cpu")); assert '
                                   'x.dtype==torch.float32 and x.ndim==2',
                'hints': []},
               {'title': 'Debug dtype/device mismatch',
                'description': 'Fix the function so matrix multiplication works regardless of CPU/GPU selection '
                               'and without implicit float64 input.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                '\n'
                                'def broken(a, device):\n'
                                '    x = torch.tensor(a)          # may be integer\n'
                                '    w = torch.randn(2, 2, device=device)\n'
                                '    return x @ w',
                'acceptance_criteria': ['inputs and weights share device',
                                        'input dtype compatible with weight dtype',
                                        'no hardcoded device'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Creating, Inspecting, and Moving Tensors — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Creating, Inspecting, and Moving '
                                     'Tensors»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Creating, Inspecting, and "
                                     "Moving Tensors'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
