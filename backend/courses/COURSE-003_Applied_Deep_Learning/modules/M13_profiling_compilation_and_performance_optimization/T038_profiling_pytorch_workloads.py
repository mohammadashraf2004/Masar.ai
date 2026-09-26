# -*- coding: utf-8 -*-
"""T038 — Applied Deep Learning, module M13.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[668, 953]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M13-L01',
 'source_note': 'Book uses flame graphs/py-spy; Masar keeps the measurement principle and makes '
                'torch.profiler primary.'}

MODERNIZATION = {'labels': ['torch.profiler is current PyTorch profiler; legacy autograd profiler is not the target.'],
 'official_docs_checked_2026_09': True}

TOPIC = {'title': 'Profiling PyTorch Workloads',
 'slug': 'applied-deep-learning-t038-profiling-pytorch-workloads',
 'description': 'تطبيق عملي: Profiling PyTorch Workloads مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'profiler',
                'cpu-device-activities',
                'record-shapes',
                'profile-memory'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Profiling PyTorch Workloads',
            'content': '# Profiling PyTorch Workloads\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M13:** التنميط والترجمة وتحسين الأداء · '
                       '**الدرس T038 / C003-M13-L01** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'torch.profiler, CPU/device activities, record_shapes, profile_memory, trace, warmup\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch.profiler import profile, ProfilerActivity\n'
                       'activities=[ProfilerActivity.CPU]\n'
                       'if torch.cuda.is_available(): activities.append(ProfilerActivity.CUDA)\n'
                       'with profile(activities=activities, record_shapes=True, profile_memory=True) as prof:\n'
                       '    _ = model(inputs)\n'
                       'print(prof.key_averages().table(row_limit=10))\n'
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
                       'Book uses flame graphs/py-spy; Masar keeps the measurement principle and makes '
                       'torch.profiler primary.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch.profiler import profile, ProfilerActivity\n'
                           'activities=[ProfilerActivity.CPU]\n'
                           'if torch.cuda.is_available(): activities.append(ProfilerActivity.CUDA)\n'
                           'with profile(activities=activities, record_shapes=True, profile_memory=True) as '
                           'prof:\n'
                           '    _ = model(inputs)\n'
                           'print(prof.key_averages().table(row_limit=10))',
            'curriculum_id': 'C003-M13-L01'},
 'exercises': [{'title': 'Profile one training step',
                'description': 'Profile forward+loss+backward and report top operators by CPU time and, when CUDA '
                               'exists, device time.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['profiles full step',
                                        'records shapes',
                                        'profile_memory enabled',
                                        'produces operator table'],
                'validation_code': '',
                'hints': []},
               {'title': 'Label pipeline regions',
                'description': 'Use `record_function` to label `load_batch`, `forward`, and `backward` regions, '
                               'then identify the dominant region from trace/table evidence.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['custom labeled regions',
                                        'evidence-based bottleneck statement',
                                        'no optimization before measurement'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Profiling PyTorch Workloads — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Profiling PyTorch Workloads»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Profiling PyTorch "
                                     "Workloads'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
