# -*- coding: utf-8 -*-
"""T019 — Applied Deep Learning, module M07.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 3,
 'chapter_title': 'Convolutional Neural Networks',
 'source_file': 'تم لصق markdown(20260923-114507).md',
 'source_line_ranges': [[692, 699], [977, 998]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M07-L02',
 'source_note': 'Source model inspection expanded into practical architecture/constraint comparison.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Inspecting and Comparing Model Architectures',
 'slug': 'applied-deep-learning-t019-inspecting-and-comparing-model-architectures',
 'description': 'تطبيق عملي: Inspecting and Comparing Model Architectures مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'named-modules',
                'named-parameters',
                'parameter-counts',
                'trainable-counts'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Inspecting and Comparing Model Architectures',
            'content': '# Inspecting and Comparing Model Architectures\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M07:** النماذج البصرية المدربة مسبقاً وفحص '
                       'المعماريات · **الدرس T019 / C003-M07-L02** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'named_modules, named_parameters, parameter counts, trainable counts, latency/size '
                       'trade-off\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'def parameter_report(model):\n'
                       '    total = sum(p.numel() for p in model.parameters())\n'
                       '    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)\n'
                       '    return {"total": total, "trainable": trainable}\n'
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
                       'Source model inspection expanded into practical architecture/constraint comparison.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'def parameter_report(model):\n'
                           '    total = sum(p.numel() for p in model.parameters())\n'
                           '    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)\n'
                           '    return {"total": total, "trainable": trainable}',
            'curriculum_id': 'C003-M07-L02'},
 'exercises': [{'title': 'Model architecture report',
                'description': 'Return total/trainable params, first/last parameter names, number of modules, and '
                               'output shape for a supplied sample batch.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def architecture_report(model, sample):\n    # TODO\n    pass',
                'acceptance_criteria': ['uses named_parameters/named_modules',
                                        'dummy forward under inference_mode',
                                        'JSON-friendly summary'],
                'validation_code': '',
                'hints': []},
               {'title': 'Compare two backbones',
                'description': 'Compare ResNet18 and MobileNetV3 Small on parameter count and measured CPU '
                               'inference latency for the same dummy batch. Warm up before timing.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO: instantiate both models, warm up, time repeated inference',
                'acceptance_criteria': ['same input shape',
                                        'warmup included',
                                        'reports median/mean latency and params',
                                        'does not claim universal winner'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Inspecting and Comparing Model Architectures — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Inspecting and Comparing Model '
                                     'Architectures»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Inspecting and Comparing "
                                     "Model Architectures'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Pretrained Model Audit',
             'description': 'Load a modern TorchVision weight package, adapt its head, inspect parameters and '
                            'produce an architecture/preprocessing report.',
             'project_kind': 'module_lab',
             'is_portfolio': False,
             'deliverables': ['working Python/notebook implementation',
                              'README or experiment notes',
                              'measured checks/metrics',
                              'saved artifact when relevant'],
             'acceptance_criteria': ['code runs without silent shape/device errors',
                                     'results are measured rather than asserted',
                                     'train/validation/test roles remain correct',
                                     'limitations and failed experiments are documented']}}
