# -*- coding: utf-8 -*-
"""T034 — Applied Deep Learning, module M11.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 6,
 'chapter_title': 'A Journey into Sound',
 'source_file': 'تم لصق markdown(20260923-115219).md',
 'source_line_ranges': [[1159, 1171], [1284, 1626]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M11-L05',
 'source_note': 'Source custom masks modernized to built-in transforms where available.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Audio Augmentation and SpecAugment',
 'slug': 'applied-deep-learning-t034-audio-augmentation-and-specaugment',
 'description': 'تطبيق عملي: Audio Augmentation and SpecAugment مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 5,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'frequencymasking',
                'timemasking',
                'train-only-augmentation',
                'label-preservation'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Audio Augmentation and SpecAugment',
            'content': '# Audio Augmentation and SpecAugment\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M11:** التعلم العميق التطبيقي للصوت · '
                       '**الدرس T034 / C003-M11-L05** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'FrequencyMasking, TimeMasking, train-only augmentation, label preservation\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torchaudio\n'
                       'freq_mask = torchaudio.transforms.FrequencyMasking(freq_mask_param=8)\n'
                       'time_mask = torchaudio.transforms.TimeMasking(time_mask_param=20)\n'
                       'augmented = time_mask(freq_mask(log_mel))\n'
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
                       'Source custom masks modernized to built-in transforms where available.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torchaudio\n'
                           'freq_mask = torchaudio.transforms.FrequencyMasking(freq_mask_param=8)\n'
                           'time_mask = torchaudio.transforms.TimeMasking(time_mask_param=20)\n'
                           'augmented = time_mask(freq_mask(log_mel))',
            'curriculum_id': 'C003-M11-L05'},
 'exercises': [{'title': 'SpecAugment pipeline',
                'description': 'Apply frequency/time masking only in training. Verify eval path is deterministic '
                               'and shape is preserved.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['train-only stochastic masks', 'shape preserved', 'eval deterministic'],
                'validation_code': '',
                'hints': []},
               {'title': 'Augmentation ablation',
                'description': 'Train or simulate one controlled comparison with no mask, frequency mask, time '
                               'mask, both; report metric and training cost.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO experiment harness',
                'acceptance_criteria': ['same split/model/epochs',
                                        'single variable changed per run',
                                        'results table produced'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Audio Augmentation and SpecAugment — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Audio Augmentation and SpecAugment»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Audio Augmentation and "
                                     "SpecAugment'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Environmental Sound Classifier',
             'description': 'Optional: compare raw-waveform and log-mel models and benchmark '
                            'preprocessing/SpecAugment trade-offs.',
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
