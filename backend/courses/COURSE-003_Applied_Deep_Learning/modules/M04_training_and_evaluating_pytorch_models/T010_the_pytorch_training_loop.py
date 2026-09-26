# -*- coding: utf-8 -*-
"""T010 — Applied Deep Learning, module M04.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[755, 791]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M04-L01',
 'source_note': 'Source loop retained; wording corrected so backward is called on loss, not model.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'The PyTorch Training Loop',
 'slug': 'applied-deep-learning-t010-the-pytorch-training-loop',
 'description': 'تطبيق عملي: The PyTorch Training Loop مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'train-mode', 'zero-grad', 'forward', 'loss'],
 'prerequisite_ids': [],
 'lesson': {'title': 'The PyTorch Training Loop',
            'content': '# The PyTorch Training Loop\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M04:** تدريب وتقييم نماذج PyTorch · **الدرس '
                       'T010 / C003-M04-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'train mode, zero_grad, forward, loss, backward, optimizer step, metric accumulation\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'def train_one_epoch(model, loader, loss_fn, optimizer, device):\n'
                       '    model.train()\n'
                       '    total_loss = 0.0\n'
                       '    for x, y in loader:\n'
                       '        x, y = x.to(device), y.to(device)\n'
                       '        optimizer.zero_grad(set_to_none=True)\n'
                       '        logits = model(x)\n'
                       '        loss = loss_fn(logits, y)\n'
                       '        loss.backward()\n'
                       '        optimizer.step()\n'
                       '        total_loss += loss.item() * x.size(0)\n'
                       '    return total_loss / len(loader.dataset)\n'
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
                       'Source loop retained; wording corrected so backward is called on loss, not model.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'def train_one_epoch(model, loader, loss_fn, optimizer, device):\n'
                           '    model.train()\n'
                           '    total_loss = 0.0\n'
                           '    for x, y in loader:\n'
                           '        x, y = x.to(device), y.to(device)\n'
                           '        optimizer.zero_grad(set_to_none=True)\n'
                           '        logits = model(x)\n'
                           '        loss = loss_fn(logits, y)\n'
                           '        loss.backward()\n'
                           '        optimizer.step()\n'
                           '        total_loss += loss.item() * x.size(0)\n'
                           '    return total_loss / len(loader.dataset)',
            'curriculum_id': 'C003-M04-L01'},
 'exercises': [{'title': 'Implement train_one_epoch',
                'description': 'Complete a reusable function that returns sample-weighted average loss and '
                               'supports any classification model/loader.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def train_one_epoch(model, loader, loss_fn, optimizer, device):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['model.train called',
                                        'batches moved to device',
                                        'gradients cleared before backward',
                                        'sample-weighted average loss'],
                'validation_code': '',
                'hints': []},
               {'title': 'Tiny-batch overfit test',
                'description': 'Write a helper that repeatedly trains on one fixed batch and returns whether loss '
                               'falls below 10% of its starting value.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def tiny_batch_overfit(model, batch, loss_fn, optimizer, device, steps=200):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['reuses same batch',
                                        'tracks initial/final loss',
                                        'useful failure signal when model cannot memorize'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'The PyTorch Training Loop — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «The PyTorch Training Loop»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'The PyTorch Training "
                                     "Loop'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
