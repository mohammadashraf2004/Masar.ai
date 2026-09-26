# -*- coding: utf-8 -*-
"""T001 — Applied Deep Learning, module M01.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 1,
 'chapter_title': 'Getting Started with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114052).md',
 'source_line_ranges': [[422, 434], [569, 624]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M01-L01',
 'source_note': 'Source sections cover Jupyter/setup, import verification and CUDA checks; installation '
                'commands are modernized rather than copied.'}

MODERNIZATION = {'labels': ['Use current official PyTorch install selector; avoid historical Ubuntu/CUDA/Conda commands.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'PyTorch Workspace and Accelerator Verification',
 'slug': 'applied-deep-learning-t001-pytorch-workspace-and-accelerator-verification',
 'description': 'تطبيق عملي: PyTorch Workspace and Accelerator Verification مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.42,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'version-inspection',
                'device-detection',
                'portable-execution',
                'reproducibility-seed'],
 'prerequisite_ids': [],
 'lesson': {'title': 'PyTorch Workspace and Accelerator Verification',
            'content': '# PyTorch Workspace and Accelerator Verification\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M01:** أساسيات PyTorch: الموترات والأشكال '
                       'والأجهزة · **الدرس T001 / C003-M01-L01** · **المدة:** 25 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'version inspection, device detection, portable execution, reproducibility seed\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def select_device():\n'
                       '    if torch.cuda.is_available():\n'
                       '        return torch.device("cuda")\n'
                       '    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():\n'
                       '        return torch.device("mps")\n'
                       '    return torch.device("cpu")\n'
                       '\n'
                       'torch.manual_seed(7)\n'
                       'device = select_device()\n'
                       'x = torch.randn(4, 3, device=device)\n'
                       'print({"torch": torch.__version__, "device": str(device), "shape": tuple(x.shape)})\n'
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
                       'Source sections cover Jupyter/setup, import verification and CUDA checks; installation '
                       'commands are modernized rather than copied.\n',
            'estimated_minutes': 25,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def select_device():\n'
                           '    if torch.cuda.is_available():\n'
                           '        return torch.device("cuda")\n'
                           '    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():\n'
                           '        return torch.device("mps")\n'
                           '    return torch.device("cpu")\n'
                           '\n'
                           'torch.manual_seed(7)\n'
                           'device = select_device()\n'
                           'x = torch.randn(4, 3, device=device)\n'
                           'print({"torch": torch.__version__, "device": str(device), "shape": tuple(x.shape)})',
            'curriculum_id': 'C003-M01-L01'},
 'exercises': [{'title': 'Build an environment report',
                'description': 'Write `environment_report()` that returns PyTorch version, selected device, CUDA '
                               'availability and a successful tensor operation on that device.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                '\n'
                                'def environment_report():\n'
                                '    # TODO: select a usable device without hardcoding CUDA\n'
                                '    # TODO: create a 2x2 tensor on it and compute its mean\n'
                                '    return {}',
                'acceptance_criteria': ['returns a dict with version/device',
                                        'works on CPU-only machines',
                                        'tensor is created on the selected device'],
                'validation_code': 'r=environment_report(); assert "device" in r and "torch_version" in r',
                'hints': ['Do not assume a GPU exists.']},
               {'title': 'Make a reproducible smoke test',
                'description': 'Create two runs with the same seed and prove the generated tensor is identical; '
                               'then change the seed and prove it differs.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef sample(seed):\n    # TODO\n    pass',
                'acceptance_criteria': ['same seed -> equal tensors', 'different seed -> different tensor'],
                'validation_code': 'a=sample(11); b=sample(11); c=sample(12); assert torch.equal(a,b); assert not '
                                   'torch.equal(a,c)',
                'hints': []}],
 'quiz': {'title': 'PyTorch Workspace and Accelerator Verification — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «PyTorch Workspace and Accelerator '
                                     'Verification»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'PyTorch Workspace and "
                                     "Accelerator Verification'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
