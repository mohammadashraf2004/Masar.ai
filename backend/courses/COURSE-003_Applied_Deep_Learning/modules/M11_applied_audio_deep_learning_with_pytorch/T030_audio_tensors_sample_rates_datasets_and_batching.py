# -*- coding: utf-8 -*-
"""T030 — Applied Deep Learning, module M11.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 6,
 'chapter_title': 'A Journey into Sound',
 'source_file': 'تم لصق markdown(20260923-115219).md',
 'source_line_ranges': [[311, 459]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M11-L01',
 'source_note': 'Source custom audio Dataset retained; I/O ecosystem is modernized with TorchCodec '
                'awareness.'}

MODERNIZATION = {'labels': ['TorchAudio 2.9+ is in maintenance; decoding/encoding consolidated into TorchCodec.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Audio Tensors, Sample Rates, Datasets, and Batching',
 'slug': 'applied-deep-learning-t030-audio-tensors-sample-rates-datasets-and-batching',
 'description': 'تطبيق عملي: Audio Tensors, Sample Rates, Datasets, and Batching مع كود وتمارين تحقق وتصحيح '
                'أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'waveform', 'sample-rate', 'resampling', 'channels'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Audio Tensors, Sample Rates, Datasets, and Batching',
            'content': '# Audio Tensors, Sample Rates, Datasets, and Batching\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M11:** التعلم العميق التطبيقي للصوت · '
                       '**الدرس T030 / C003-M11-L01** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'waveform, sample rate, resampling, channels, custom Dataset, metadata splits\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'import torchaudio\n'
                       'wave = torch.randn(1, 48000)   # 1 second at 48kHz\n'
                       'resampler = torchaudio.transforms.Resample(orig_freq=48000, new_freq=16000)\n'
                       'wave16 = resampler(wave)\n'
                       'assert wave16.shape[-1] == 16000\n'
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
                       'Source custom audio Dataset retained; I/O ecosystem is modernized with TorchCodec '
                       'awareness.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'import torchaudio\n'
                           'wave = torch.randn(1, 48000)   # 1 second at 48kHz\n'
                           'resampler = torchaudio.transforms.Resample(orig_freq=48000, new_freq=16000)\n'
                           'wave16 = resampler(wave)\n'
                           'assert wave16.shape[-1] == 16000',
            'curriculum_id': 'C003-M11-L01'},
 'exercises': [{'title': 'Sample-rate normalization',
                'description': 'Implement a helper that converts arbitrary mono waveform + sample_rate to 16kHz '
                               'and returns unchanged data when already 16kHz.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torchaudio\n\ndef to_16k(waveform, sample_rate):\n    # TODO\n    pass',
                'acceptance_criteria': ['correct output length within rounding',
                                        'preserves channel axis',
                                        'no needless resample at 16k'],
                'validation_code': '',
                'hints': []},
               {'title': 'Metadata-driven audio split',
                'description': 'Given records `{path,label,fold}`, create datasets for train folds 1-3, val 4, '
                               'test 5 without moving files.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def split_records(records):\n    # TODO\n    pass',
                'acceptance_criteria': ['no physical file movement', 'disjoint splits', 'fold policy explicit'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Audio Tensors, Sample Rates, Datasets, and Batching — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Audio Tensors, Sample Rates, Datasets, '
                                     'and Batching»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Audio Tensors, Sample "
                                     "Rates, Datasets, and Batching'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
