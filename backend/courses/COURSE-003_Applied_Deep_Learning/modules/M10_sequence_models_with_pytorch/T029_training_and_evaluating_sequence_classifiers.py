# -*- coding: utf-8 -*-
"""T029 — Applied Deep Learning, module M10.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 5,
 'chapter_title': 'Text Classification',
 'source_file': 'تم لصق markdown(20260923-114931).md',
 'source_line_ranges': [[1162, 1277]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M10-L04',
 'source_note': 'Source training/inference ideas retained; torchtext-specific batch interface removed.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Training and Evaluating Sequence Classifiers',
 'slug': 'applied-deep-learning-t029-training-and-evaluating-sequence-classifiers',
 'description': 'تطبيق عملي: Training and Evaluating Sequence Classifiers مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 4,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'sequence-trainer',
                'crossentropyloss',
                'bcewithlogitsloss',
                'eval'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Training and Evaluating Sequence Classifiers',
            'content': '# Training and Evaluating Sequence Classifiers\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M10:** نماذج التسلسل باستخدام PyTorch · '
                       '**الدرس T029 / C003-M10-L04** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'sequence trainer, CrossEntropyLoss, BCEWithLogitsLoss, eval, single sequence inference\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       '# Reuse the generic train/evaluate loops from M04 because the model still returns '
                       'logits.\n'
                       '# The new part is collating variable-length inputs and passing lengths into the model.\n'
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
                       'Source training/inference ideas retained; torchtext-specific batch interface removed.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': '# Reuse the generic train/evaluate loops from M04 because the model still returns '
                           'logits.\n'
                           '# The new part is collating variable-length inputs and passing lengths into the '
                           'model.',
            'curriculum_id': 'C003-M10-L04'},
 'exercises': [{'title': 'Sequence train/eval integration',
                'description': 'Adapt the reusable trainer so batches `(ids,lengths,labels)` are supported '
                               'without duplicating all loop logic.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: create a batch adapter or model wrapper',
                'acceptance_criteria': ['reuses generic loop logic where possible',
                                        'lengths delivered to model',
                                        'evaluation gradient-free'],
                'validation_code': '',
                'hints': []},
               {'title': 'Single-sequence inference',
                'description': 'Tokenize one sequence, map OOV→UNK, batch it, run eval/inference_mode and return '
                               'class probabilities.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def predict_sequence(model, tokens, vocab, class_names, device):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['same vocab/preprocess as training',
                                        'handles unknown tokens',
                                        'correct device',
                                        'returns full probability vector'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Training and Evaluating Sequence Classifiers — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Training and Evaluating Sequence '
                                     'Classifiers»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Training and Evaluating "
                                     "Sequence Classifiers'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Recurrent Sequence Classifier',
             'description': 'Build a variable-length text/sequence classifier using embedding + LSTM/GRU, packed '
                            'batches, evaluation and checkpointing.',
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
