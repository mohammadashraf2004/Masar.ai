# -*- coding: utf-8 -*-
"""T028 — Applied Deep Learning, module M10.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 5,
 'chapter_title': 'Text Classification',
 'source_file': 'تم لصق markdown(20260923-114931).md',
 'source_line_ranges': [[1000, 1048]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M10-L03',
 'source_note': 'Masar addition: packed sequences replace behavior previously hidden by legacy '
                'BucketIterator.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Variable-Length Sequences and Packed Batches',
 'slug': 'applied-deep-learning-t028-variable-length-sequences-and-packed-batches',
 'description': 'تطبيق عملي: Variable-Length Sequences and Packed Batches مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'pack-padded-sequence',
                'pad-packed-sequence',
                'lengths',
                'collate'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Variable-Length Sequences and Packed Batches',
            'content': '# Variable-Length Sequences and Packed Batches\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M10:** نماذج التسلسل باستخدام PyTorch · '
                       '**الدرس T028 / C003-M10-L03** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'pack_padded_sequence, pad_packed_sequence, lengths, collate, padding efficiency\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence\n'
                       'packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, '
                       'enforce_sorted=False)\n'
                       'out_packed, state = lstm(packed)\n'
                       'out, out_lengths = pad_packed_sequence(out_packed, batch_first=True)\n'
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
                       'Masar addition: packed sequences replace behavior previously hidden by legacy '
                       'BucketIterator.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence\n'
                           'packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, '
                           'enforce_sorted=False)\n'
                           'out_packed, state = lstm(packed)\n'
                           'out, out_lengths = pad_packed_sequence(out_packed, batch_first=True)',
            'curriculum_id': 'C003-M10-L03'},
 'exercises': [{'title': 'Packed-sequence forward',
                'description': 'Implement an LSTM forward accepting padded IDs + lengths and using '
                               '`pack_padded_sequence(enforce_sorted=False)`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['lengths preserved',
                                        'handles unsorted batch',
                                        'padding does not advance recurrent state'],
                'validation_code': '',
                'hints': []},
               {'title': 'Compare padded vs packed compute',
                'description': 'Run the same variable-length batch with plain padded LSTM and packed LSTM. '
                               'Compare output shapes and time on a deliberately high-padding batch.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same logical batch',
                                        'reports padding ratio',
                                        'benchmarks rather than assumes speedup'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Variable-Length Sequences and Packed Batches — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Variable-Length Sequences and Packed '
                                     'Batches»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Variable-Length Sequences "
                                     "and Packed Batches'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
