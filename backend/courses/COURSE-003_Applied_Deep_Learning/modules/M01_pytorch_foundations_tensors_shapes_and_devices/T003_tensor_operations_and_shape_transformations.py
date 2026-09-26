# -*- coding: utf-8 -*-
"""T003 — Applied Deep Learning, module M01.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 1,
 'chapter_title': 'Getting Started with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114052).md',
 'source_line_ranges': [[722, 833], [854, 870]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M01-L03',
 'source_note': 'Book covers reshape/view/permute; modern explanation avoids relying on undocumented storage '
                'sharing from reshape.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Tensor Operations and Shape Transformations',
 'slug': 'applied-deep-learning-t003-tensor-operations-and-shape-transformations',
 'description': 'تطبيق عملي: Tensor Operations and Shape Transformations مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'argmax', 'reshape', 'view', 'contiguity'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Tensor Operations and Shape Transformations',
            'content': '# Tensor Operations and Shape Transformations\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M01:** أساسيات PyTorch: الموترات والأشكال '
                       'والأجهزة · **الدرس T003 / C003-M01-L03** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'argmax, reshape, view, contiguity, permute, image layout\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'img_hwc = torch.randn(32, 48, 3)\n'
                       'img_chw = img_hwc.permute(2, 0, 1).contiguous()\n'
                       'flat = img_chw.reshape(-1)\n'
                       'restored = flat.reshape(3, 32, 48)\n'
                       'assert restored.shape == img_chw.shape\n'
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
                       'Book covers reshape/view/permute; modern explanation avoids relying on undocumented '
                       'storage sharing from reshape.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'img_hwc = torch.randn(32, 48, 3)\n'
                           'img_chw = img_hwc.permute(2, 0, 1).contiguous()\n'
                           'flat = img_chw.reshape(-1)\n'
                           'restored = flat.reshape(3, 32, 48)\n'
                           'assert restored.shape == img_chw.shape',
            'curriculum_id': 'C003-M01-L03'},
 'exercises': [{'title': 'HWC → NCHW converter',
                'description': 'Implement a converter accepting a single HWC image or a batch NHWC and returning '
                               'CHW/NCHW with assertions for channel count.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                '\n'
                                'def channels_first(x):\n'
                                '    # TODO: support rank 3 and 4\n'
                                '    pass',
                'acceptance_criteria': ['supports HWC and NHWC',
                                        'raises for unsupported rank',
                                        'preserves values exactly'],
                'validation_code': 'x=torch.arange(2*3*3).reshape(2,3,3); y=channels_first(x); assert '
                                   'y.shape==(3,2,3)',
                'hints': []},
               {'title': 'Shape-debugging challenge',
                'description': 'A flattened batch has shape `[8, 3072]` and represents RGB 32x32 images. Restore '
                               'NCHW, compute per-image argmax channel at pixel (10,10), and assert the batch '
                               'size is unchanged.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\nx = torch.randn(8, 3072)\n# TODO',
                'acceptance_criteria': ['restored shape is (8,3,32,32)',
                                        'uses reshape/permute correctly',
                                        'asserts element count before reshape'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Tensor Operations and Shape Transformations — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Tensor Operations and Shape '
                                     'Transformations»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Tensor Operations and "
                                     "Shape Transformations'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
