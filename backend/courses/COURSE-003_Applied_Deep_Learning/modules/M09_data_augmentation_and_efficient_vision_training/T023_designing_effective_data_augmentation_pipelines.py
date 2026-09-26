# -*- coding: utf-8 -*-
"""T023 — Applied Deep Learning, module M09.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 4,
 'chapter_title': 'Transfer Learning and Other Tricks',
 'source_file': 'تم لصق markdown(20260923-114716).md',
 'source_line_ranges': [[424, 629]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M09-L01',
 'source_note': 'Source augmentations retained; Masar emphasizes label-preserving domain assumptions and '
                'modern v2 APIs.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Designing Effective Data Augmentation Pipelines',
 'slug': 'applied-deep-learning-t023-designing-effective-data-augmentation-pipelines',
 'description': 'تطبيق عملي: Designing Effective Data Augmentation Pipelines مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'train-only-augmentation',
                'label-preservation',
                'v2-transforms',
                'visual-sanity-checks'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Designing Effective Data Augmentation Pipelines',
            'content': '# Designing Effective Data Augmentation Pipelines\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M09:** زيادة البيانات والتدريب البصري الفعال '
                       '· **الدرس T023 / C003-M09-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'train-only augmentation, label preservation, v2 transforms, visual sanity checks, domain '
                       'constraints\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from torchvision.transforms import v2\n'
                       'train_tf = v2.Compose([v2.RandomResizedCrop((224,224)), v2.RandomHorizontalFlip(), '
                       'v2.ToDtype(torch.float32, scale=True)])\n'
                       'eval_tf = v2.Compose([v2.Resize((224,224)), v2.ToDtype(torch.float32, scale=True)])\n'
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
                       'Source augmentations retained; Masar emphasizes label-preserving domain assumptions and '
                       'modern v2 APIs.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'from torchvision.transforms import v2\n'
                           'train_tf = v2.Compose([v2.RandomResizedCrop((224,224)), v2.RandomHorizontalFlip(), '
                           'v2.ToDtype(torch.float32, scale=True)])\n'
                           'eval_tf = v2.Compose([v2.Resize((224,224)), v2.ToDtype(torch.float32, scale=True)])',
            'curriculum_id': 'C003-M09-L01'},
 'exercises': [{'title': 'Augmentation policy builder',
                'description': 'Create separate train/eval pipelines and a function that applies train transform '
                               '8 times to one image and checks output shape/range consistency.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['train stochastic',
                                        'eval deterministic',
                                        'output range/dtype validated',
                                        'no random transform in eval'],
                'validation_code': '',
                'hints': []},
               {'title': 'Domain-safety review in code',
                'description': 'Represent augmentations as config records with `label_preserving` and `reason`; '
                               'reject policies containing an augmentation explicitly marked unsafe for the task.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def validate_policy(policy):\n    # TODO\n    pass',
                'acceptance_criteria': ['forces explicit domain assumption',
                                        'rejects unsafe augmentation',
                                        'keeps policy machine-readable'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Designing Effective Data Augmentation Pipelines — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Designing Effective Data Augmentation '
                                     'Pipelines»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Designing Effective Data "
                                     "Augmentation Pipelines'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
