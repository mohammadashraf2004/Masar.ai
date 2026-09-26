# -*- coding: utf-8 -*-
"""T018 — Applied Deep Learning, module M07.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 3,
 'chapter_title': 'Convolutional Neural Networks',
 'source_file': 'تم لصق markdown(20260923-114507).md',
 'source_line_ranges': [[665, 689]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M07-L01',
 'source_note': 'Book pretrained=True API modernized to weights enums and weight-provided preprocessing.'}

MODERNIZATION = {'labels': ['TorchVision modern weights API.'], 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Loading and Using Pretrained Vision Models',
 'slug': 'applied-deep-learning-t018-loading-and-using-pretrained-vision-models',
 'description': 'تطبيق عملي: Loading and Using Pretrained Vision Models مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'weights-enums',
                'weights-transforms',
                'classifier-replacement',
                'pretrained-preprocessing'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Loading and Using Pretrained Vision Models',
            'content': '# Loading and Using Pretrained Vision Models\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M07:** النماذج البصرية المدربة مسبقاً وفحص '
                       'المعماريات · **الدرس T018 / C003-M07-L01** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'weights enums, weights.transforms, classifier replacement, pretrained preprocessing\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torchvision.models import resnet18, ResNet18_Weights\n'
                       'weights = ResNet18_Weights.DEFAULT\n'
                       'model = resnet18(weights=weights)\n'
                       'preprocess = weights.transforms()\n'
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
                       'Book pretrained=True API modernized to weights enums and weight-provided preprocessing.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'from torchvision.models import resnet18, ResNet18_Weights\n'
                           'weights = ResNet18_Weights.DEFAULT\n'
                           'model = resnet18(weights=weights)\n'
                           'preprocess = weights.transforms()',
            'curriculum_id': 'C003-M07-L01'},
 'exercises': [{'title': 'Adapt a pretrained model',
                'description': 'Load ResNet18 weights, replace `fc` for 3 classes, and verify a dummy '
                               '`[2,3,224,224]` batch yields `[2,3]`.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'from torch import nn\n'
                                'from torchvision.models import resnet18, ResNet18_Weights\n'
                                '# TODO',
                'acceptance_criteria': ['uses weights enum',
                                        'keeps in_features',
                                        'head outputs 3',
                                        'dummy forward passes'],
                'validation_code': '',
                'hints': []},
               {'title': 'Preprocessing contract inspection',
                'description': 'Programmatically print the weight transform and compare its expected '
                               'crop/resize/normalization with a custom pipeline. Flag mismatches.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torchvision.models import ResNet18_Weights\n# TODO',
                'acceptance_criteria': ['uses weight metadata/transform',
                                        'detects shape/normalization mismatch',
                                        'does not hardcode ImageNet stats unnecessarily'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Loading and Using Pretrained Vision Models — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Loading and Using Pretrained Vision '
                                     'Models»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Loading and Using "
                                     "Pretrained Vision Models'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
