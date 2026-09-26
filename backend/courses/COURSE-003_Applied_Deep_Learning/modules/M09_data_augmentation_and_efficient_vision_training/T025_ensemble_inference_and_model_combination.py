# -*- coding: utf-8 -*-
"""T025 — Applied Deep Learning, module M09.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[997, 1054]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M09-L03',
 'source_note': 'Source ensemble code is unusable as written; Masar replaces it with standard PyTorch '
                'inference.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Ensemble Inference and Model Combination',
 'slug': 'applied-deep-learning-t025-ensemble-inference-and-model-combination',
 'description': 'تطبيق عملي: Ensemble Inference and Model Combination مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'ensemble-probabilities',
                'model-diversity',
                'latency-trade-off',
                'evaluation-protocol'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Ensemble Inference and Model Combination',
            'content': '# Ensemble Inference and Model Combination\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M09:** زيادة البيانات والتدريب البصري الفعال '
                       '· **الدرس T025 / C003-M09-L03** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'ensemble probabilities, model diversity, latency trade-off, evaluation protocol\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def ensemble_probs(models, x):\n'
                       '    probs=[]\n'
                       '    with torch.inference_mode():\n'
                       '        for m in models:\n'
                       '            m.eval(); probs.append(m(x).softmax(-1))\n'
                       '    return torch.stack(probs).mean(0)\n'
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
                       'Source ensemble code is unusable as written; Masar replaces it with standard PyTorch '
                       'inference.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def ensemble_probs(models, x):\n'
                           '    probs=[]\n'
                           '    with torch.inference_mode():\n'
                           '        for m in models:\n'
                           '            m.eval(); probs.append(m(x).softmax(-1))\n'
                           '    return torch.stack(probs).mean(0)',
            'curriculum_id': 'C003-M09-L03'},
 'exercises': [{'title': 'Implement an ensemble predictor',
                'description': 'Average probability distributions from 3 models and return predictions. Verify '
                               'each model is eval-only and output distributions sum to 1.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef ensemble_probs(models, x):\n    # TODO\n    pass',
                'acceptance_criteria': ['uses inference_mode', 'mean over model axis', 'probabilities sum to ~1'],
                'validation_code': '',
                'hints': []},
               {'title': 'Accuracy-latency trade-off',
                'description': 'Benchmark one model vs a 3-model ensemble on the same validation subset; report '
                               'latency multiplier and metric delta.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same samples/protocol',
                                        'warmup before timing',
                                        'reports both metric and cost',
                                        'no universal winner claim'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Ensemble Inference and Model Combination — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Ensemble Inference and Model '
                                     'Combination»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Ensemble Inference and "
                                     "Model Combination'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Augmentation Ablation Study',
             'description': 'Compare baseline, augmentation, progressive resolution and ensemble choices using '
                            'the same validation protocol.',
             'project_kind': 'module_lab',
             'is_portfolio': False,
             'deliverables': ['working Python/notebook implementation',
                              'README or experiment notes',
                              'measured checks/metrics',
                              'saved artifact when relevant'],
             'acceptance_criteria': ['code runs without silent shape/device errors',
                                     'results are measured rather than asserted',
                                     'train/validation/test roles remain correct',
                                     'limitations and failed experiments are documented']}}
