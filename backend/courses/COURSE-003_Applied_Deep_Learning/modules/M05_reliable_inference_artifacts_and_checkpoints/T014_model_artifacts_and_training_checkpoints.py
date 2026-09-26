# -*- coding: utf-8 -*-
"""T014 — Applied Deep Learning.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[1075, 1138]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M05-L02',
 'source_note': 'Source prefers state_dict; Masar adds explicit artifact metadata and resume semantics.',
 'additional_sources': [{'book_id': 'BOOK-003',
                         'chapter': 8,
                         'chapter_title': 'PyTorch in Production',
                         'source_file': 'تم لصق markdown(20260923-123436).md',
                         'source_line_ranges': [[241, 259]]}]}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Model Artifacts and Training Checkpoints',
 'slug': 'applied-deep-learning-t014-model-artifacts-and-training-checkpoints',
 'description': 'تطبيق عملي: Model Artifacts and Training Checkpoints مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'state-dict', 'optimizer-state', 'epoch', 'metadata'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Model Artifacts and Training Checkpoints',
            'content': '# Model Artifacts and Training Checkpoints\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M05:** الاستدلال الموثوق والملفات المحفوظة '
                       'ونقاط الاستئناف · **الدرس T014 / C003-M05-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'state_dict, optimizer state, epoch, metadata, class mapping, preprocess metadata, resume\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'checkpoint = {\n'
                       '    "model": model.state_dict(),\n'
                       '    "optimizer": optimizer.state_dict(),\n'
                       '    "epoch": epoch,\n'
                       '    "class_names": class_names,\n'
                       '    "preprocess": {"size": [224,224], "normalization": "weights.transforms()"},\n'
                       '}\n'
                       'torch.save(checkpoint, "checkpoint.pt")\n'
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
                       'Source prefers state_dict; Masar adds explicit artifact metadata and resume semantics.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'checkpoint = {\n'
                           '    "model": model.state_dict(),\n'
                           '    "optimizer": optimizer.state_dict(),\n'
                           '    "epoch": epoch,\n'
                           '    "class_names": class_names,\n'
                           '    "preprocess": {"size": [224,224], "normalization": "weights.transforms()"},\n'
                           '}\n'
                           'torch.save(checkpoint, "checkpoint.pt")',
            'curriculum_id': 'C003-M05-L02'},
 'exercises': [{'title': 'Save and restore training',
                'description': 'Write save/load helpers that restore model weights, optimizer state and next '
                               'epoch. Verify a fixed input gives matching logits after reload.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                '\n'
                                'def save_checkpoint(path, model, optimizer, epoch, metadata):\n'
                                '    # TODO\n'
                                '    pass\n'
                                '\n'
                                'def load_checkpoint(path, model, optimizer=None):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['restores model state',
                                        'optionally optimizer state',
                                        'returns epoch/metadata',
                                        'prediction parity on fixed input'],
                'validation_code': '',
                'hints': []},
               {'title': 'Build an inference artifact contract',
                'description': 'Create a metadata dict containing model name/version, class names, input shape, '
                               'dtype and preprocessing identifier. Validate required keys before serving '
                               'inference.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'REQUIRED = {"model_version","class_names","input_shape","dtype","preprocess"}\n'
                                '\n'
                                'def validate_metadata(meta):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['missing key -> clear error',
                                        'JSON-serializable metadata',
                                        'class mapping preserved'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Model Artifacts and Training Checkpoints — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Model Artifacts and Training '
                                     'Checkpoints»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Model Artifacts and "
                                     "Training Checkpoints'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Reproducible Inference Artifact',
             'description': 'Package model weights plus preprocessing/class metadata and reload them into an '
                            'inference function that reproduces predictions.',
             'project_kind': 'portfolio',
             'is_portfolio': True,
             'deliverables': ['working Python/notebook implementation',
                              'README or experiment notes',
                              'measured checks/metrics',
                              'saved artifact when relevant'],
             'acceptance_criteria': ['code runs without silent shape/device errors',
                                     'results are measured rather than asserted',
                                     'train/validation/test roles remain correct',
                                     'limitations and failed experiments are documented']}}
