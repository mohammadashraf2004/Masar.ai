# -*- coding: utf-8 -*-
"""T032 — Applied Deep Learning, module M11.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 6,
 'chapter_title': 'A Journey into Sound',
 'source_file': 'تم لصق markdown(20260923-115219).md',
 'source_line_ranges': [[621, 731]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M11-L03',
 'source_note': 'Source frequency-domain insight retained; image-rendering detour replaced with '
                'tensor-native features.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Mel Spectrograms and Time-Frequency Modeling',
 'slug': 'applied-deep-learning-t032-mel-spectrograms-and-time-frequency-modeling',
 'description': 'تطبيق عملي: Mel Spectrograms and Time-Frequency Modeling مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'melspectrogram',
                'amplitudetodb',
                'frequency-time-axes',
                '2d-cnn-input'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Mel Spectrograms and Time-Frequency Modeling',
            'content': '# Mel Spectrograms and Time-Frequency Modeling\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M11:** التعلم العميق التطبيقي للصوت · '
                       '**الدرس T032 / C003-M11-L03** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'MelSpectrogram, AmplitudeToDB, frequency/time axes, 2D CNN input\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch, torchaudio\n'
                       'wave = torch.randn(1, 16000)\n'
                       'mel = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=64)(wave)\n'
                       'log_mel = torchaudio.transforms.AmplitudeToDB()(mel)\n'
                       'assert log_mel.ndim == 3  # C,F,T\n'
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
                       'Source frequency-domain insight retained; image-rendering detour replaced with '
                       'tensor-native features.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch, torchaudio\n'
                           'wave = torch.randn(1, 16000)\n'
                           'mel = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=64)(wave)\n'
                           'log_mel = torchaudio.transforms.AmplitudeToDB()(mel)\n'
                           'assert log_mel.ndim == 3  # C,F,T',
            'curriculum_id': 'C003-M11-L03'},
 'exercises': [{'title': 'Tensor-native log-mel pipeline',
                'description': 'Implement waveform→resample→MelSpectrogram→dB without rendering PNGs. Return '
                               '`[C,F,T]`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['tensor-native path',
                                        'fixed sample rate',
                                        'finite output',
                                        'no matplotlib/PIL round trip'],
                'validation_code': '',
                'hints': []},
               {'title': 'Adapt a 2D CNN',
                'description': 'Convert log-mel `[B,1,F,T]` into logits using a small Conv2d model and verify '
                               'variable T works via adaptive pooling.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['input channel 1',
                                        'variable time dimension supported',
                                        'output matches class count'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Mel Spectrograms and Time-Frequency Modeling — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Mel Spectrograms and Time-Frequency '
                                     'Modeling»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Mel Spectrograms and "
                                     "Time-Frequency Modeling'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
