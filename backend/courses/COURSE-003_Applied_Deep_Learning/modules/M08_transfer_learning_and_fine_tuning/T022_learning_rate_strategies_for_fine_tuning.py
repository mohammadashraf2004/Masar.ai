# -*- coding: utf-8 -*-
"""T022 — Applied Deep Learning, module M08.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[133, 216], [304, 330]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M08-L03',
 'source_note': 'Source LR finder retained conceptually; Masar adds current scheduler practice and '
                'restoration checks.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Learning-Rate Strategies for Fine-Tuning',
 'slug': 'applied-deep-learning-t022-learning-rate-strategies-for-fine-tuning',
 'description': 'تطبيق عملي: Learning-Rate Strategies for Fine-Tuning مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'lr-range-idea',
                'scheduler',
                'onecyclelr',
                'cosineannealinglr'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Learning-Rate Strategies for Fine-Tuning',
            'content': '# Learning-Rate Strategies for Fine-Tuning\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M08:** نقل التعلم والضبط الدقيق · **الدرس '
                       'T022 / C003-M08-L03** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'LR range idea, scheduler, OneCycleLR, CosineAnnealingLR, checkpoint restore, per-batch '
                       'scheduler\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)\n'
                       'scheduler = torch.optim.lr_scheduler.OneCycleLR(\n'
                       '    optimizer, max_lr=3e-4, epochs=5, steps_per_epoch=len(train_loader)\n'
                       ')\n'
                       '# inside each training batch: optimizer.step(); scheduler.step()\n'
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
                       'Source LR finder retained conceptually; Masar adds current scheduler practice and '
                       'restoration checks.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)\n'
                           'scheduler = torch.optim.lr_scheduler.OneCycleLR(\n'
                           '    optimizer, max_lr=3e-4, epochs=5, steps_per_epoch=len(train_loader)\n'
                           ')\n'
                           '# inside each training batch: optimizer.step(); scheduler.step()',
            'curriculum_id': 'C003-M08-L03'},
 'exercises': [{'title': 'Integrate OneCycleLR',
                'description': 'Add OneCycleLR to a training loop and record learning rate after every optimizer '
                               'step. Assert number of scheduler steps equals optimizer steps.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['scheduler.step after optimizer.step',
                                        'records lr curve',
                                        'step counts match'],
                'validation_code': '',
                'hints': []},
               {'title': 'Checkpoint an LR experiment',
                'description': 'Save model+optimizer before a short LR sweep, mutate them during the experiment, '
                               'then restore and prove fixed-input logits match the pre-sweep logits.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['full state restored',
                                        'prediction parity after restore',
                                        'experiment state not leaked into real training'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Learning-Rate Strategies for Fine-Tuning — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Learning-Rate Strategies for '
                                     'Fine-Tuning»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Learning-Rate Strategies "
                                     "for Fine-Tuning'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Fine-Tune a Pretrained Vision Model',
             'description': 'Run frozen-head training then partial fine-tuning with verified optimizer groups, '
                            'scheduler, checkpoints and comparison report.',
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
