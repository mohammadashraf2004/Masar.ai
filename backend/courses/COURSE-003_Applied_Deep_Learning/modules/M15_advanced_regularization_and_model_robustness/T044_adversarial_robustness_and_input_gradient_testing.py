# -*- coding: utf-8 -*-
"""T044 — Applied Deep Learning, module M15.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 9,
 'chapter_title': 'PyTorch in the Wild',
 'source_file': 'تم لصق markdown(20260923-220506).md',
 'source_line_ranges': [[1119, 1351]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M15-L02',
 'source_note': 'Source FGSM idea retained; multiple code errors corrected and one-example demo upgraded to '
                'robustness evaluation.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Adversarial Robustness and Input-Gradient Testing',
 'slug': 'applied-deep-learning-t044-adversarial-robustness-and-input-gradient-testing',
 'description': 'تطبيق عملي: Adversarial Robustness and Input-Gradient Testing مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'fgsm', 'input-gradients', 'epsilon', 'clean-accuracy'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Adversarial Robustness and Input-Gradient Testing',
            'content': '# Adversarial Robustness and Input-Gradient Testing\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M15:** التنظيم المتقدم ومتانة النماذج · '
                       '**الدرس T044 / C003-M15-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'FGSM, input gradients, epsilon, clean accuracy, adversarial accuracy, threat model\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def fgsm(model, x, y, loss_fn, eps):\n'
                       '    x = x.detach().clone().requires_grad_(True)\n'
                       '    loss = loss_fn(model(x), y)\n'
                       '    model.zero_grad(set_to_none=True); loss.backward()\n'
                       '    adv = x + eps * x.grad.sign()\n'
                       '    return adv.detach().clamp(0, 1)\n'
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
                       'Source FGSM idea retained; multiple code errors corrected and one-example demo upgraded '
                       'to robustness evaluation.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def fgsm(model, x, y, loss_fn, eps):\n'
                           '    x = x.detach().clone().requires_grad_(True)\n'
                           '    loss = loss_fn(model(x), y)\n'
                           '    model.zero_grad(set_to_none=True); loss.backward()\n'
                           '    adv = x + eps * x.grad.sign()\n'
                           '    return adv.detach().clamp(0, 1)',
            'curriculum_id': 'C003-M15-L02'},
 'exercises': [{'title': 'Implement FGSM correctly',
                'description': 'Implement FGSM with explicit input gradients, gradient reset and valid-range '
                               'clipping. Test eps=0 returns original input.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef fgsm(model, x, y, loss_fn, eps):\n    # TODO\n    pass',
                'acceptance_criteria': ['requires_grad on input',
                                        'uses input.grad',
                                        'eps=0 parity',
                                        'clamps valid range'],
                'validation_code': '',
                'hints': []},
               {'title': 'Robustness curve',
                'description': 'Evaluate clean and FGSM accuracy for epsilon=[0,.005,.01,.02,.05] and return a '
                               'table.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def robustness_curve(model, loader, loss_fn, epsilons, device):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['same evaluation set',
                                        'clean baseline included',
                                        'accuracy per epsilon',
                                        'model parameters not updated'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Adversarial Robustness and Input-Gradient Testing — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Adversarial Robustness and '
                                     'Input-Gradient Testing»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Adversarial Robustness and "
                                     "Input-Gradient Testing'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Regularization and Robustness Report',
             'description': 'Train with MixUp/CutMix/label smoothing, then evaluate clean and FGSM robustness '
                            'across epsilon values.',
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
