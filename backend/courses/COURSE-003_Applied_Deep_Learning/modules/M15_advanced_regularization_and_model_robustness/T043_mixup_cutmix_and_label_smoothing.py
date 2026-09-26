# -*- coding: utf-8 -*-
"""T043 — Applied Deep Learning, module M15.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 9,
 'chapter_title': 'PyTorch in the Wild',
 'source_file': 'تم لصق markdown(20260923-220506).md',
 'source_line_ranges': [[27, 331]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M15-L01',
 'source_note': 'Source MixUp/label smoothing retained; broken handwritten MixUp code replaced by supported '
                'APIs and CutMix is a Masar addition.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'MixUp, CutMix, and Label Smoothing',
 'slug': 'applied-deep-learning-t043-mixup-cutmix-and-label-smoothing',
 'description': 'تطبيق عملي: MixUp, CutMix, and Label Smoothing مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'mixup', 'cutmix', 'soft-targets', 'label-smoothing'],
 'prerequisite_ids': [],
 'lesson': {'title': 'MixUp, CutMix, and Label Smoothing',
            'content': '# MixUp, CutMix, and Label Smoothing\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M15:** التنظيم المتقدم ومتانة النماذج · '
                       '**الدرس T043 / C003-M15-L01** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'MixUp, CutMix, soft targets, label smoothing, CrossEntropyLoss\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torchvision.transforms import v2\n'
                       'mixup = v2.MixUp(alpha=0.4, num_classes=10)\n'
                       'cutmix = v2.CutMix(alpha=1.0, num_classes=10)\n'
                       'loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)\n'
                       'images2, soft_targets = mixup(images, labels)\n'
                       'loss = torch.nn.CrossEntropyLoss()(model(images2), soft_targets)\n'
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
                       'Source MixUp/label smoothing retained; broken handwritten MixUp code replaced by '
                       'supported APIs and CutMix is a Masar addition.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'from torchvision.transforms import v2\n'
                           'mixup = v2.MixUp(alpha=0.4, num_classes=10)\n'
                           'cutmix = v2.CutMix(alpha=1.0, num_classes=10)\n'
                           'loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)\n'
                           'images2, soft_targets = mixup(images, labels)\n'
                           'loss = torch.nn.CrossEntropyLoss()(model(images2), soft_targets)',
            'curriculum_id': 'C003-M15-L01'},
 'exercises': [{'title': 'Batch regularization switch',
                'description': 'Implement a function applying none/MixUp/CutMix to one batch and returning valid '
                               'targets for CrossEntropyLoss.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torchvision.transforms import v2\n'
                                '\n'
                                'def regularize_batch(images, labels, mode, num_classes):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['supports none/mixup/cutmix',
                                        'soft targets shape [B,C] for mixed modes',
                                        'batch shape valid'],
                'validation_code': '',
                'hints': []},
               {'title': 'Controlled regularization comparison',
                'description': 'Train short identical runs for baseline, label smoothing, MixUp, CutMix. Save '
                               'train/val metrics and compare generalization gap.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO experiment harness',
                'acceptance_criteria': ['same seed/split/model budget',
                                        'records both train and val metrics',
                                        'no guaranteed winner claim'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'MixUp, CutMix, and Label Smoothing — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «MixUp, CutMix, and Label Smoothing»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'MixUp, CutMix, and Label "
                                     "Smoothing'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
