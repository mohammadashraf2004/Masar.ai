# -*- coding: utf-8 -*-
"""T013 — Applied Deep Learning.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[1003, 1063]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M05-L01',
 'source_note': 'Combines Chapter 2 inference with Chapter 8 inference-readiness; softmax confidence is not '
                'treated as certainty.',
 'additional_sources': [{'book_id': 'BOOK-003',
                         'chapter': 8,
                         'chapter_title': 'PyTorch in Production',
                         'source_file': 'تم لصق markdown(20260923-123436).md',
                         'source_line_ranges': [[206, 218]]}]}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Reliable PyTorch Inference',
 'slug': 'applied-deep-learning-t013-reliable-pytorch-inference',
 'description': 'تطبيق عملي: Reliable PyTorch Inference مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'eval',
                'inference-mode',
                'batch-dimension',
                'preprocessing-contract'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Reliable PyTorch Inference',
            'content': '# Reliable PyTorch Inference\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M05:** الاستدلال الموثوق والملفات المحفوظة '
                       'ونقاط الاستئناف · **الدرس T013 / C003-M05-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'eval, inference_mode, batch dimension, preprocessing contract, class mapping, confidence '
                       'caveats\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def predict(model, batch, class_names):\n'
                       '    model.eval()\n'
                       '    with torch.inference_mode():\n'
                       '        logits = model(batch)\n'
                       '        probs = logits.softmax(dim=-1)\n'
                       '        idx = probs.argmax(dim=-1)\n'
                       '    return [(class_names[i], float(probs[n, i])) for n, i in enumerate(idx.tolist())]\n'
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
                       'Combines Chapter 2 inference with Chapter 8 inference-readiness; softmax confidence is '
                       'not treated as certainty.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def predict(model, batch, class_names):\n'
                           '    model.eval()\n'
                           '    with torch.inference_mode():\n'
                           '        logits = model(batch)\n'
                           '        probs = logits.softmax(dim=-1)\n'
                           '        idx = probs.argmax(dim=-1)\n'
                           '    return [(class_names[i], float(probs[n, i])) for n, i in enumerate(idx.tolist())]',
            'curriculum_id': 'C003-M05-L01'},
 'exercises': [{'title': 'Single-item inference function',
                'description': 'Implement `predict_one` that accepts a preprocessed CHW tensor, adds a batch '
                               'dimension, moves it to model device and returns label + probability vector.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef predict_one(model, chw, class_names):\n    # TODO\n    pass',
                'acceptance_criteria': ['model.eval',
                                        'inference_mode',
                                        'unsqueeze on batch axis',
                                        'device-safe',
                                        'returns full probabilities and selected label'],
                'validation_code': '',
                'hints': []},
               {'title': 'Preprocessing parity check',
                'description': 'Create a test that fails if training/evaluation preprocessing produces a '
                               'different shape/dtype/normalization contract than inference preprocessing.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def check_preprocess_contract(train_eval_sample, inference_sample):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['compares shape and dtype',
                                        'documents allowable stochastic differences',
                                        'does not assume max-softmax means in-distribution'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Reliable PyTorch Inference — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Reliable PyTorch Inference»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Reliable PyTorch "
                                     "Inference'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
