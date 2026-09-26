# -*- coding: utf-8 -*-
"""T016 — Applied Deep Learning, module M06.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 3,
 'chapter_title': 'Convolutional Neural Networks',
 'source_file': 'تم لصق markdown(20260923-114507).md',
 'source_line_ranges': [[208, 297]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M06-L02',
 'source_note': 'Source stride/padding material is turned into an implementation debugging lesson.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'CNN Shape Arithmetic and Architecture Debugging',
 'slug': 'applied-deep-learning-t016-cnn-shape-arithmetic-and-architecture-debugging',
 'description': 'تطبيق عملي: CNN Shape Arithmetic and Architecture Debugging مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'nchw', 'conv-output-size', 'stride', 'padding'],
 'prerequisite_ids': [],
 'lesson': {'title': 'CNN Shape Arithmetic and Architecture Debugging',
            'content': '# CNN Shape Arithmetic and Architecture Debugging\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M06:** تنفيذ الشبكات الالتفافية في PyTorch · '
                       '**الدرس T016 / C003-M06-L02** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'NCHW, conv output size, stride, padding, pooling, channel mismatch, flatten mismatch\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import math\n'
                       '\n'
                       'def conv_out(n, kernel, stride=1, padding=0, dilation=1):\n'
                       '    return math.floor((n + 2*padding - dilation*(kernel-1) - 1)/stride + 1)\n'
                       'assert conv_out(32, 3, padding=1) == 32\n'
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
                       'Source stride/padding material is turned into an implementation debugging lesson.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import math\n'
                           '\n'
                           'def conv_out(n, kernel, stride=1, padding=0, dilation=1):\n'
                           '    return math.floor((n + 2*padding - dilation*(kernel-1) - 1)/stride + 1)\n'
                           'assert conv_out(32, 3, padding=1) == 32',
            'curriculum_id': 'C003-M06-L02'},
 'exercises': [{'title': 'Shape tracer',
                'description': 'Given a list of conv/pool layer specs, compute H/W after each step and compare '
                               'with an actual dummy forward.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: implement trace_spatial_size(size, specs)',
                'acceptance_criteria': ['formula matches PyTorch outputs',
                                        'reports each intermediate size',
                                        'detects non-positive dimensions'],
                'validation_code': '',
                'hints': []},
               {'title': 'Fix a matmul shape crash',
                'description': 'A CNN ends with `Linear(4096,10)` but actual flattened features are different. '
                               'Fix without manually calculating a fragile spatial constant.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: refactor model to remove fragile flatten constant',
                'acceptance_criteria': ['dummy forward succeeds',
                                        'no magic spatial-size product in Linear',
                                        'explain why fix is more robust'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'CNN Shape Arithmetic and Architecture Debugging — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «CNN Shape Arithmetic and Architecture '
                                     'Debugging»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'CNN Shape Arithmetic and "
                                     "Architecture Debugging'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
