# -*- coding: utf-8 -*-
"""T037 — Applied Deep Learning, module M12.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[321, 458], [462, 663]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M12-L03',
 'source_note': 'Source hook concepts retained; deprecated register_backward_hook replaced with modern full '
                'backward hook when module hooks are needed.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Hooks, Activations, Gradients, and Model Inspection',
 'slug': 'applied-deep-learning-t037-hooks-activations-gradients-and-model-inspection',
 'description': 'تطبيق عملي: Hooks, Activations, Gradients, and Model Inspection مع كود وتمارين تحقق وتصحيح '
                'أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'forward-hooks',
                'full-backward-hooks',
                'removablehandle',
                'activation-stats'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Hooks, Activations, Gradients, and Model Inspection',
            'content': '# Hooks, Activations, Gradients, and Model Inspection\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M12:** تصحيح التدريب وسلوك النموذج · **الدرس '
                       'T037 / C003-M12-L03** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'forward hooks, full backward hooks, RemovableHandle, activation stats, gradient stats, '
                       'CAM lab\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'handles=[]; stats={}\n'
                       'def hook(name):\n'
                       '    def fn(module, args, output):\n'
                       '        t = output.detach(); stats[name] = (float(t.mean()), float(t.std()))\n'
                       '    return fn\n'
                       'for name, module in model.named_modules():\n'
                       '    if isinstance(module, torch.nn.ReLU): '
                       'handles.append(module.register_forward_hook(hook(name)))\n'
                       '# ... run one forward ...\n'
                       'for h in handles: h.remove()\n'
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
                       'Source hook concepts retained; deprecated register_backward_hook replaced with modern '
                       'full backward hook when module hooks are needed.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'handles=[]; stats={}\n'
                           'def hook(name):\n'
                           '    def fn(module, args, output):\n'
                           '        t = output.detach(); stats[name] = (float(t.mean()), float(t.std()))\n'
                           '    return fn\n'
                           'for name, module in model.named_modules():\n'
                           '    if isinstance(module, torch.nn.ReLU): '
                           'handles.append(module.register_forward_hook(hook(name)))\n'
                           '# ... run one forward ...\n'
                           'for h in handles: h.remove()',
            'curriculum_id': 'C003-M12-L03'},
 'exercises': [{'title': 'Activation shape/stat collector',
                'description': 'Register temporary forward hooks on Conv/Linear layers, run one batch, collect '
                               'shape/mean/std, and remove all handles.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef collect_stats(model, x):\n    # TODO\n    pass',
                'acceptance_criteria': ['hooks removed even on failure (try/finally)',
                                        'uses detach not .data',
                                        'records per-layer shape/mean/std'],
                'validation_code': '',
                'hints': []},
               {'title': 'Gradient-health report',
                'description': 'After backward, report parameters with missing gradients, non-finite gradients, '
                               'and top-5 gradient norms.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def gradient_report(model):\n    # TODO\n    pass',
                'acceptance_criteria': ['handles grad=None',
                                        'detects non-finite',
                                        'sorted norms',
                                        'names included'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Hooks, Activations, Gradients, and Model Inspection — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Hooks, Activations, Gradients, and '
                                     'Model Inspection»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Hooks, Activations, "
                                     "Gradients, and Model Inspection'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Diagnose a Broken Training Pipeline',
             'description': 'Use tiny-batch overfit tests, TensorBoard and hooks to find and fix multiple planted '
                            'data/model/training bugs.',
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
