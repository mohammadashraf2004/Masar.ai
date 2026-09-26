# -*- coding: utf-8 -*-
"""T011 — Applied Deep Learning, module M04.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[858, 988]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M04-L02',
 'source_note': 'Source switches train/eval but lacks no-gradient validation; Masar fixes both concerns.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Validation and Evaluation Loops',
 'slug': 'applied-deep-learning-t011-validation-and-evaluation-loops',
 'description': 'تطبيق عملي: Validation and Evaluation Loops مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'eval-mode', 'inference-mode', 'loss', 'accuracy'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Validation and Evaluation Loops',
            'content': '# Validation and Evaluation Loops\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M04:** تدريب وتقييم نماذج PyTorch · **الدرس '
                       'T011 / C003-M04-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'eval mode, inference_mode, loss, accuracy, confusion inputs, no parameter update\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def evaluate(model, loader, loss_fn, device):\n'
                       '    model.eval(); correct = 0; total = 0; total_loss = 0.0\n'
                       '    with torch.inference_mode():\n'
                       '        for x, y in loader:\n'
                       '            x, y = x.to(device), y.to(device)\n'
                       '            logits = model(x)\n'
                       '            total_loss += loss_fn(logits, y).item() * x.size(0)\n'
                       '            correct += (logits.argmax(1) == y).sum().item(); total += y.numel()\n'
                       '    return {"loss": total_loss/total, "accuracy": correct/total}\n'
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
                       'Source switches train/eval but lacks no-gradient validation; Masar fixes both concerns.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def evaluate(model, loader, loss_fn, device):\n'
                           '    model.eval(); correct = 0; total = 0; total_loss = 0.0\n'
                           '    with torch.inference_mode():\n'
                           '        for x, y in loader:\n'
                           '            x, y = x.to(device), y.to(device)\n'
                           '            logits = model(x)\n'
                           '            total_loss += loss_fn(logits, y).item() * x.size(0)\n'
                           '            correct += (logits.argmax(1) == y).sum().item(); total += y.numel()\n'
                           '    return {"loss": total_loss/total, "accuracy": correct/total}',
            'curriculum_id': 'C003-M04-L02'},
 'exercises': [{'title': 'Evaluation with invariants',
                'description': 'Implement `evaluate` and prove model parameters are unchanged before/after '
                               'evaluation.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                '\n'
                                'def evaluate(model, loader, loss_fn, device):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['model.eval called',
                                        'torch.inference_mode used',
                                        'no gradients stored',
                                        'returns loss and accuracy',
                                        'parameters unchanged'],
                'validation_code': '',
                'hints': []},
               {'title': 'Diagnose train/eval behavior',
                'description': 'Create a tiny model containing BatchNorm and Dropout. Show that repeated outputs '
                               'differ in train mode and stabilize in eval mode for the same input.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\nfrom torch import nn\n# TODO',
                'acceptance_criteria': ['demonstrates mode-dependent behavior',
                                        'does not confuse eval() with gradient disabling'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Validation and Evaluation Loops — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Validation and Evaluation Loops»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Validation and Evaluation "
                                     "Loops'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
