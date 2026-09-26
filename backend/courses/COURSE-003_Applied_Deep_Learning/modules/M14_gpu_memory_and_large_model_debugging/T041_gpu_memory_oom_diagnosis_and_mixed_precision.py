# -*- coding: utf-8 -*-
"""T041 — Applied Deep Learning, module M14.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 7,
 'chapter_title': 'Debugging PyTorch Models',
 'source_file': 'تم لصق markdown(20260923-121617).md',
 'source_line_ranges': [[1239, 1368]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M14-L01',
 'source_note': 'Source nvidia-smi/memory debugging retained; Masar adds PyTorch allocator metrics and AMP.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'GPU Memory, OOM Diagnosis, and Mixed Precision',
 'slug': 'applied-deep-learning-t041-gpu-memory-oom-diagnosis-and-mixed-precision',
 'description': 'تطبيق عملي: GPU Memory, OOM Diagnosis, and Mixed Precision مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.83,
 'skill_tags': ['pytorch',
                'applied-deep-learning',
                'allocated-vs-reserved',
                'memory-summary',
                'autocast',
                'gradscaler'],
 'prerequisite_ids': [],
 'lesson': {'title': 'GPU Memory, OOM Diagnosis, and Mixed Precision',
            'content': '# GPU Memory, OOM Diagnosis, and Mixed Precision\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M14:** ذاكرة المسرع وتصحيح النماذج الكبيرة · '
                       '**الدرس T041 / C003-M14-L01** · **المدة:** 50 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'allocated vs reserved, memory summary, autocast, GradScaler, OOM strategy\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'use_amp = torch.cuda.is_available()\n'
                       "scaler = torch.amp.GradScaler('cuda', enabled=use_amp)\n"
                       'for x,y in loader:\n'
                       '    optimizer.zero_grad(set_to_none=True)\n'
                       "    with torch.autocast(device_type='cuda', dtype=torch.float16, enabled=use_amp):\n"
                       '        loss = loss_fn(model(x.to(device)), y.to(device))\n'
                       '    scaler.scale(loss).backward(); scaler.step(optimizer); scaler.update()\n'
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
                       'Source nvidia-smi/memory debugging retained; Masar adds PyTorch allocator metrics and '
                       'AMP.\n',
            'estimated_minutes': 50,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'use_amp = torch.cuda.is_available()\n'
                           "scaler = torch.amp.GradScaler('cuda', enabled=use_amp)\n"
                           'for x,y in loader:\n'
                           '    optimizer.zero_grad(set_to_none=True)\n'
                           "    with torch.autocast(device_type='cuda', dtype=torch.float16, enabled=use_amp):\n"
                           '        loss = loss_fn(model(x.to(device)), y.to(device))\n'
                           '    scaler.scale(loss).backward(); scaler.step(optimizer); scaler.update()',
            'curriculum_id': 'C003-M14-L01'},
 'exercises': [{'title': 'Memory measurement helper',
                'description': 'On CUDA, record allocated/reserved and peak allocated before/after one step; on '
                               'CPU return a clear unsupported marker instead of failing.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n\ndef cuda_memory_report():\n    # TODO\n    pass',
                'acceptance_criteria': ['portable CPU behavior',
                                        'allocated/reserved distinguished',
                                        'peak metric included'],
                'validation_code': '',
                'hints': []},
               {'title': 'AMP A/B benchmark',
                'description': 'Compare FP32 vs AMP for several training steps on CUDA: peak memory, average step '
                               'time and final finite loss. Skip cleanly on non-CUDA.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['same model/data baseline',
                                        'GradScaler used for float16 CUDA training',
                                        'reports memory+time',
                                        'clean skip without CUDA'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'GPU Memory, OOM Diagnosis, and Mixed Precision — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «GPU Memory, OOM Diagnosis, and Mixed '
                                     'Precision»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'GPU Memory, OOM Diagnosis, "
                                     "and Mixed Precision'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
