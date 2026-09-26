# -*- coding: utf-8 -*-
"""T020 — Applied Deep Learning, module M08.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[38, 61], [84, 125]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M08-L01',
 'source_note': 'Source transfer-learning workflow retained and modernized to current pretrained model API.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Adapting Pretrained Models to New Tasks',
 'slug': 'applied-deep-learning-t020-adapting-pretrained-models-to-new-tasks',
 'description': 'تطبيق عملي: Adapting Pretrained Models to New Tasks مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'backbone',
                'head-replacement',
                'fixed-feature-extractor',
                'pretrained-weights'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Adapting Pretrained Models to New Tasks',
            'content': '# Adapting Pretrained Models to New Tasks\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M08:** نقل التعلم والضبط الدقيق · **الدرس '
                       'T020 / C003-M08-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'backbone, head replacement, fixed feature extractor, pretrained weights\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torch import nn\n'
                       'from torchvision.models import resnet18, ResNet18_Weights\n'
                       'model = resnet18(weights=ResNet18_Weights.DEFAULT)\n'
                       'for p in model.parameters(): p.requires_grad = False\n'
                       'model.fc = nn.Linear(model.fc.in_features, 4)\n'
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
                       'Source transfer-learning workflow retained and modernized to current pretrained model '
                       'API.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'from torch import nn\n'
                           'from torchvision.models import resnet18, ResNet18_Weights\n'
                           'model = resnet18(weights=ResNet18_Weights.DEFAULT)\n'
                           'for p in model.parameters(): p.requires_grad = False\n'
                           'model.fc = nn.Linear(model.fc.in_features, 4)',
            'curriculum_id': 'C003-M08-L01'},
 'exercises': [{'title': 'Fixed-feature extractor',
                'description': 'Build a helper that freezes a ResNet backbone and replaces the head for N '
                               'classes. Assert only head parameters require gradients.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def make_feature_extractor(num_classes):\n    # TODO\n    pass',
                'acceptance_criteria': ['backbone frozen', 'new head trainable', 'output matches num_classes'],
                'validation_code': '',
                'hints': []},
               {'title': 'Trainable-parameter audit',
                'description': 'Print all trainable parameter names and fail if any unexpected backbone parameter '
                               'is trainable during phase 1.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def assert_trainable_only(model, allowed_prefixes):\n    # TODO\n    pass',
                'acceptance_criteria': ['uses named_parameters',
                                        'clear failure list',
                                        'works after head replacement'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Adapting Pretrained Models to New Tasks — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Adapting Pretrained Models to New '
                                     'Tasks»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Adapting Pretrained Models "
                                     "to New Tasks'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
