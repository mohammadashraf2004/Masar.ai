# -*- coding: utf-8 -*-
"""T035 — Applied Deep Learning, module M12.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[16, 34]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M12-L01',
 'source_note': 'Source starts with data sanity; Masar formalizes it into a repeatable debugging gate.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Data Sanity Checks and Failure Isolation',
 'slug': 'applied-deep-learning-t035-data-sanity-checks-and-failure-isolation',
 'description': 'تطبيق عملي: Data Sanity Checks and Failure Isolation مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.67,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'class-balance',
                'label-audit',
                'nan-inf',
                'shape-range-checks'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Data Sanity Checks and Failure Isolation',
            'content': '# Data Sanity Checks and Failure Isolation\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M12:** تصحيح التدريب وسلوك النموذج · **الدرس '
                       'T035 / C003-M12-L01** · **المدة:** 40 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'class balance, label audit, NaN/Inf, shape/range checks, tiny-batch overfit, failure '
                       'hierarchy\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       '\n'
                       'def audit_batch(x, y):\n'
                       '    assert torch.isfinite(x).all(), "non-finite input"\n'
                       '    assert x.size(0) == y.size(0), "batch mismatch"\n'
                       '    return {"shape": tuple(x.shape), "min": float(x.min()), "max": float(x.max()), '
                       '"classes": y.unique().tolist()}\n'
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
                       'Source starts with data sanity; Masar formalizes it into a repeatable debugging gate.\n',
            'estimated_minutes': 40,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           '\n'
                           'def audit_batch(x, y):\n'
                           '    assert torch.isfinite(x).all(), "non-finite input"\n'
                           '    assert x.size(0) == y.size(0), "batch mismatch"\n'
                           '    return {"shape": tuple(x.shape), "min": float(x.min()), "max": float(x.max()), '
                           '"classes": y.unique().tolist()}',
            'curriculum_id': 'C003-M12-L01'},
 'exercises': [{'title': 'Dataset sanity report',
                'description': 'Scan a bounded number of batches and report shapes, dtypes, finite-value '
                               'failures, class counts and duplicate IDs if IDs are supplied.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def audit_loader(loader, max_batches=20):\n    # TODO\n    pass',
                'acceptance_criteria': ['bounded scan',
                                        'class counts',
                                        'shape/dtype consistency',
                                        'NaN/Inf detection'],
                'validation_code': '',
                'hints': []},
               {'title': 'Automated tiny-batch gate',
                'description': 'Implement a pre-training gate that attempts to overfit a tiny batch and raises a '
                               'diagnostic warning if loss does not drop enough.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def tiny_batch_gate(model, batch, loss_fn, optimizer, device, steps=100, '
                                'target_ratio=0.2):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['fixed batch',
                                        'loss ratio threshold configurable',
                                        'returns trace for debugging'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Data Sanity Checks and Failure Isolation — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Data Sanity Checks and Failure '
                                     'Isolation»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Data Sanity Checks and "
                                     "Failure Isolation'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
