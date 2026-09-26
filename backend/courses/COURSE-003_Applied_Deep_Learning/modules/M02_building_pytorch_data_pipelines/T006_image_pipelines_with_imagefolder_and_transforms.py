# -*- coding: utf-8 -*-
"""T006 — Applied Deep Learning, module M02.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 2,
 'chapter_title': 'Image Classification with PyTorch',
 'source_file': 'تم لصق markdown(20260923-114430).md',
 'source_line_ranges': [[190, 263]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M02-L02',
 'source_note': 'Book uses older transforms; Masar modernizes to transforms.v2 and distinguishes custom vs '
                'pretrained preprocessing.'}

MODERNIZATION = {'labels': ['TorchVision transforms v2 recommended for modern pipelines.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Image Pipelines with ImageFolder and Transforms',
 'slug': 'applied-deep-learning-t006-image-pipelines-with-imagefolder-and-transforms',
 'description': 'تطبيق عملي: Image Pipelines with ImageFolder and Transforms مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.58,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'imagefolder', 'transforms-v2', 'resize', 'dtype-scaling'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Image Pipelines with ImageFolder and Transforms',
            'content': '# Image Pipelines with ImageFolder and Transforms\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M02:** بناء خطوط بيانات PyTorch · **الدرس '
                       'T006 / C003-M02-L02** · **المدة:** 35 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'ImageFolder, transforms v2, resize, dtype scaling, normalize, pretrained preprocessing '
                       'contracts\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torchvision.transforms import v2\n'
                       '\n'
                       'train_tf = v2.Compose([\n'
                       '    v2.ToImage(),\n'
                       '    v2.Resize((128, 128)),\n'
                       '    v2.RandomHorizontalFlip(p=0.5),\n'
                       '    v2.ToDtype(torch.float32, scale=True),\n'
                       '    v2.Normalize(mean=[0.5]*3, std=[0.25]*3),\n'
                       '])\n'
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
                       'Book uses older transforms; Masar modernizes to transforms.v2 and distinguishes custom vs '
                       'pretrained preprocessing.\n',
            'estimated_minutes': 35,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torchvision.transforms import v2\n'
                           '\n'
                           'train_tf = v2.Compose([\n'
                           '    v2.ToImage(),\n'
                           '    v2.Resize((128, 128)),\n'
                           '    v2.RandomHorizontalFlip(p=0.5),\n'
                           '    v2.ToDtype(torch.float32, scale=True),\n'
                           '    v2.Normalize(mean=[0.5]*3, std=[0.25]*3),\n'
                           '])',
            'curriculum_id': 'C003-M02-L02'},
 'exercises': [{'title': 'Create separate train/eval transforms',
                'description': 'Build `train_tf` with one random augmentation and `eval_tf` with deterministic '
                               'preprocessing only. Both must output float32 tensors of the same shape.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\nfrom torchvision.transforms import v2\n# TODO',
                'acceptance_criteria': ['train has stochastic transform',
                                        'eval is deterministic',
                                        'same output shape/dtype',
                                        'normalization occurs after scaling'],
                'validation_code': '',
                'hints': []},
               {'title': 'Pretrained weight contract',
                'description': 'Load a TorchVision weight enum and use `weights.transforms()` instead of manually '
                               'guessing normalization. Adapt the final classifier to 4 classes.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torchvision.models import resnet18, ResNet18_Weights\n# TODO',
                'acceptance_criteria': ['uses weights.transforms()',
                                        'uses weights=... API',
                                        'final layer outputs 4 logits'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Image Pipelines with ImageFolder and Transforms — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Image Pipelines with ImageFolder and '
                                     'Transforms»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Image Pipelines with "
                                     "ImageFolder and Transforms'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
