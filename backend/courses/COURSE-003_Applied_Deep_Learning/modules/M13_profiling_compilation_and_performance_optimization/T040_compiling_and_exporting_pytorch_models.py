# -*- coding: utf-8 -*-
"""T040 — Applied Deep Learning.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 8,
 'chapter_title': 'PyTorch in Production',
 'source_file': 'تم لصق markdown(20260923-123436).md',
 'source_line_ranges': [[1023, 1443]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M13-L03',
 'source_note': 'Book TorchScript material is legacy context; Masar uses torch.compile/torch.export as '
                'modern implementation.',
 'additional_sources': []}

MODERNIZATION = {'labels': ['TorchScript is no longer in active development; use modern compiler/export stack.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Compiling and Exporting PyTorch Models',
 'slug': 'applied-deep-learning-t040-compiling-and-exporting-pytorch-models',
 'description': 'تطبيق عملي: Compiling and Exporting PyTorch Models مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 3,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'eager', 'compile', 'graph-breaks', 'export'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Compiling and Exporting PyTorch Models',
            'content': '# Compiling and Exporting PyTorch Models\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M13:** التنميط والترجمة وتحسين الأداء · '
                       '**الدرس T040 / C003-M13-L03** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'eager, torch.compile, graph breaks, torch.export, ExportedProgram, output parity\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'model.eval(); x=torch.randn(2, 20)\n'
                       'compiled = torch.compile(model)\n'
                       'with torch.inference_mode():\n'
                       '    eager = model(x); fast = compiled(x)\n'
                       'assert torch.allclose(eager, fast, atol=1e-5, rtol=1e-4)\n'
                       'exported = torch.export.export(model, (x,))\n'
                       'exported_out = exported.module()(x)\n'
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
                       'Book TorchScript material is legacy context; Masar uses torch.compile/torch.export as '
                       'modern implementation.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'model.eval(); x=torch.randn(2, 20)\n'
                           'compiled = torch.compile(model)\n'
                           'with torch.inference_mode():\n'
                           '    eager = model(x); fast = compiled(x)\n'
                           'assert torch.allclose(eager, fast, atol=1e-5, rtol=1e-4)\n'
                           'exported = torch.export.export(model, (x,))\n'
                           'exported_out = exported.module()(x)',
            'curriculum_id': 'C003-M13-L03'},
 'exercises': [{'title': 'Benchmark eager vs compiled',
                'description': 'Warm up both eager and compiled models, time repeated inference, and report '
                               'compile warmup separately from steady-state latency.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['warmup separated',
                                        'same model/input',
                                        'output parity check',
                                        'reports steady-state timings'],
                'validation_code': '',
                'hints': []},
               {'title': 'Export parity contract',
                'description': 'Export a model with representative input, run exported module and compare '
                               'shape/dtype/numerical values with eager output.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['torch.export.export used',
                                        'output parity tolerance explicit',
                                        'records input constraints/shape assumptions'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Compiling and Exporting PyTorch Models — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Compiling and Exporting PyTorch '
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Compiling and Exporting "
                                     "PyTorch Models'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True},
 'project': {'title': 'Profile, Optimize, Compile, Export',
             'description': 'Profile a model/pipeline, implement one measured optimization, benchmark eager vs '
                            'compiled, and verify exported output parity.',
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
