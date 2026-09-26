# -*- coding: utf-8 -*-
"""T047 — Applied Deep Learning, module M16.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 9,
 'chapter_title': 'PyTorch in the Wild',
 'source_file': 'تم لصق markdown(20260923-220506).md',
 'source_line_ranges': [[847, 1116]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M16-L03',
 'source_note': 'Source abandoned maskrcnn-benchmark workflow replaced with current TorchVision detection '
                'interface.'}

MODERNIZATION = {'labels': ['Use maintained TorchVision detection/segmentation tutorial rather than maskrcnn-benchmark.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Object Detection and Instance Segmentation',
 'slug': 'applied-deep-learning-t047-object-detection-and-instance-segmentation',
 'description': 'تطبيق عملي: Object Detection and Instance Segmentation مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'target-dict', 'boxes', 'labels', 'masks'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Object Detection and Instance Segmentation',
            'content': '# Object Detection and Instance Segmentation\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M16:** تطبيقات الرؤية المتقدمة · **الدرس '
                       'T047 / C003-M16-L03** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'target dict, boxes, labels, masks, Faster R-CNN, Mask R-CNN, TorchVision detection\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '# Typical target structure for one image:\n'
                       'target = {\n'
                       '    "boxes": torch.tensor([[10., 15., 80., 95.]], dtype=torch.float32),\n'
                       '    "labels": torch.tensor([1], dtype=torch.int64),\n'
                       '}\n'
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
                       'Source abandoned maskrcnn-benchmark workflow replaced with current TorchVision detection '
                       'interface.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '# Typical target structure for one image:\n'
                           'target = {\n'
                           '    "boxes": torch.tensor([[10., 15., 80., 95.]], dtype=torch.float32),\n'
                           '    "labels": torch.tensor([1], dtype=torch.int64),\n'
                           '}',
            'curriculum_id': 'C003-M16-L03'},
 'exercises': [{'title': 'Detection dataset contract',
                'description': 'Implement a toy Dataset that returns image tensor and target dict with '
                               'boxes/labels and validates xyxy boxes.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'from torch.utils.data import Dataset\n'
                                'class ToyDetectionDataset(Dataset):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['boxes float32 [N,4]',
                                        'labels int64 [N]',
                                        'x2>x1 and y2>y1',
                                        'image,target returned'],
                'validation_code': '',
                'hints': []},
               {'title': 'Adapt a pretrained detector head',
                'description': 'Using current TorchVision detection APIs, replace the classifier head for a '
                               'custom class count and run one inference on a dummy/real image when weights are '
                               'available.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: use torchvision.models.detection',
                'acceptance_criteria': ['modern TorchVision API',
                                        'custom class count includes background as required',
                                        'eval inference returns boxes/scores/labels'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Object Detection and Instance Segmentation — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Object Detection and Instance '
                                     'Segmentation»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Object Detection and "
                                     "Instance Segmentation'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Advanced Vision Application',
             'description': 'Optional: choose super-resolution, GAN generation, detection, or instance '
                            'segmentation and build a modern PyTorch prototype.',
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
