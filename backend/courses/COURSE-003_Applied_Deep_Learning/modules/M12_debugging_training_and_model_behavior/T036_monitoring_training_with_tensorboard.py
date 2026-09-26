# -*- coding: utf-8 -*-
"""T036 — Applied Deep Learning, module M12.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[125, 137], [194, 318]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M12-L02',
 'source_note': 'Source TensorBoard integration retained; Masar expands logging to debugging-relevant '
                'metrics.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Monitoring Training with TensorBoard',
 'slug': 'applied-deep-learning-t036-monitoring-training-with-tensorboard',
 'description': 'تطبيق عملي: Monitoring Training with TensorBoard مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'summarywriter', 'global-step', 'loss', 'metrics'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Monitoring Training with TensorBoard',
            'content': '# Monitoring Training with TensorBoard\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M12:** تصحيح التدريب وسلوك النموذج · **الدرس '
                       'T036 / C003-M12-L02** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'SummaryWriter, global_step, loss, metrics, learning rate, histograms, run comparison\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torch.utils.tensorboard import SummaryWriter\n'
                       "writer = SummaryWriter('runs/exp01')\n"
                       "writer.add_scalar('train/loss', 0.42, 10)\n"
                       "writer.add_scalar('optim/lr', 1e-3, 10)\n"
                       'writer.close()\n'
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
                       'Source TensorBoard integration retained; Masar expands logging to debugging-relevant '
                       'metrics.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'from torch.utils.tensorboard import SummaryWriter\n'
                           "writer = SummaryWriter('runs/exp01')\n"
                           "writer.add_scalar('train/loss', 0.42, 10)\n"
                           "writer.add_scalar('optim/lr', 1e-3, 10)\n"
                           'writer.close()',
            'curriculum_id': 'C003-M12-L02'},
 'exercises': [{'title': 'Instrument a training loop',
                'description': 'Log train/val loss, accuracy, LR and epoch time with consistent global steps; '
                               'close the writer reliably.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['hierarchical tags',
                                        'correct step semantics',
                                        'writer closed',
                                        'validation logged separately'],
                'validation_code': '',
                'hints': []},
               {'title': 'Log gradient norms',
                'description': 'After backward and before optimizer step, compute global gradient norm and log '
                               'it. Detect/flag NaN/Inf gradients.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef grad_norm(model):\n    # TODO\n    pass',
                'acceptance_criteria': ['ignores None gradients', 'finite check', 'logs scalar per step'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Monitoring Training with TensorBoard — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Monitoring Training with TensorBoard»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Monitoring Training with "
                                     "TensorBoard'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
