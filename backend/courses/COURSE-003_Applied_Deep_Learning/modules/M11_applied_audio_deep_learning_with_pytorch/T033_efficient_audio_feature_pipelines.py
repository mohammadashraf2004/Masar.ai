# -*- coding: utf-8 -*-
"""T033 — Applied Deep Learning, module M11.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 6,
 'chapter_title': 'A Journey into Sound',
 'source_file': 'تم لصق markdown(20260923-115219).md',
 'source_line_ranges': [[761, 903]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M11-L04',
 'source_note': 'Source caching/precompute section generalized into an ML engineering performance exercise.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Efficient Audio Feature Pipelines',
 'slug': 'applied-deep-learning-t033-efficient-audio-feature-pipelines',
 'description': 'تطبيق عملي: Efficient Audio Feature Pipelines مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 4,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'online-transform', 'cache', 'precompute', 'benchmark'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Efficient Audio Feature Pipelines',
            'content': '# Efficient Audio Feature Pipelines\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M11:** التعلم العميق التطبيقي للصوت · '
                       '**الدرس T033 / C003-M11-L04** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'online transform, cache, precompute, benchmark, samples/sec\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'from time import perf_counter\n'
                       '\n'
                       'def benchmark_getitem(dataset, n=100):\n'
                       '    t0=perf_counter()\n'
                       '    for i in range(min(n,len(dataset))): _=dataset[i]\n'
                       '    return min(n,len(dataset))/(perf_counter()-t0)\n'
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
                       'Source caching/precompute section generalized into an ML engineering performance '
                       'exercise.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'from time import perf_counter\n'
                           '\n'
                           'def benchmark_getitem(dataset, n=100):\n'
                           '    t0=perf_counter()\n'
                           '    for i in range(min(n,len(dataset))): _=dataset[i]\n'
                           '    return min(n,len(dataset))/(perf_counter()-t0)',
            'curriculum_id': 'C003-M11-L04'},
 'exercises': [{'title': 'Benchmark preprocessing strategies',
                'description': 'Create toy datasets for online expensive transform vs cached/precomputed features '
                               'and report items/sec after warmup.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same logical samples',
                                        'warmup included',
                                        'reports speed and storage/memory trade-off'],
                'validation_code': '',
                'hints': []},
               {'title': 'Choose a strategy from measurements',
                'description': 'Return `online|cache|precompute` from measured transform cost, reuse count and '
                               'memory budget, and document the heuristic.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def choose_strategy(ms_per_item, epochs, fits_memory):\n    # TODO\n    pass',
                'acceptance_criteria': ['decision uses measured values',
                                        'heuristic documented',
                                        'does not claim universal optimum'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Efficient Audio Feature Pipelines — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Efficient Audio Feature Pipelines»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Efficient Audio Feature "
                                     "Pipelines'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
