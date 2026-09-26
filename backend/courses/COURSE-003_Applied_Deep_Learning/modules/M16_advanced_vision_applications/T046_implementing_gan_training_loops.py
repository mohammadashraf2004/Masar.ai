# -*- coding: utf-8 -*-
"""T046 — Applied Deep Learning, module M16.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 9,
 'chapter_title': 'PyTorch in the Wild',
 'source_file': 'تم لصق markdown(20260923-220506).md',
 'source_line_ranges': [[567, 788]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M16-L02',
 'source_note': 'Source GAN pseudocode has model.backward mistakes; Masar supplies correct loss.backward '
                'workflow.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Implementing GAN Training Loops',
 'slug': 'applied-deep-learning-t046-implementing-gan-training-loops',
 'description': 'تطبيق عملي: Implementing GAN Training Loops مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 2,
 'difficulty': 'intermediate',
 'estimated_hours': 0.92,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'generator', 'discriminator', 'separate-optimizers', 'detach'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Implementing GAN Training Loops',
            'content': '# Implementing GAN Training Loops\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M16:** تطبيقات الرؤية المتقدمة · **الدرس '
                       'T046 / C003-M16-L02** · **المدة:** 55 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'generator, discriminator, separate optimizers, detach, alternating phases, mode collapse\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       '# D step: fake is detached so G is not updated.\n'
                       'opt_d.zero_grad(set_to_none=True)\n'
                       'fake = generator(z).detach()\n'
                       'loss_d = loss_fn(discriminator(real), torch.ones(len(real),1,device=real.device)) + '
                       'loss_fn(discriminator(fake), torch.zeros(len(fake),1,device=fake.device))\n'
                       'loss_d.backward(); opt_d.step()\n'
                       '# G step\n'
                       'opt_g.zero_grad(set_to_none=True)\n'
                       'fake = generator(z)\n'
                       'loss_g = loss_fn(discriminator(fake), torch.ones(len(fake),1,device=fake.device))\n'
                       'loss_g.backward(); opt_g.step()\n'
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
                       'Source GAN pseudocode has model.backward mistakes; Masar supplies correct loss.backward '
                       'workflow.\n',
            'estimated_minutes': 55,
            'has_code_examples': True,
            'guided_code': '# D step: fake is detached so G is not updated.\n'
                           'opt_d.zero_grad(set_to_none=True)\n'
                           'fake = generator(z).detach()\n'
                           'loss_d = loss_fn(discriminator(real), torch.ones(len(real),1,device=real.device)) + '
                           'loss_fn(discriminator(fake), torch.zeros(len(fake),1,device=fake.device))\n'
                           'loss_d.backward(); opt_d.step()\n'
                           '# G step\n'
                           'opt_g.zero_grad(set_to_none=True)\n'
                           'fake = generator(z)\n'
                           'loss_g = loss_fn(discriminator(fake), torch.ones(len(fake),1,device=fake.device))\n'
                           'loss_g.backward(); opt_g.step()',
            'curriculum_id': 'C003-M16-L02'},
 'exercises': [{'title': 'Correct alternating GAN updates',
                'description': 'Implement D and G update functions and verify D parameters do not change during G '
                               'step and G parameters do not change during D step.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['separate optimizers',
                                        'fake detached in D step',
                                        'backward called on losses',
                                        'parameter-isolation test'],
                'validation_code': '',
                'hints': []},
               {'title': 'Mode-collapse monitor',
                'description': 'For generated feature vectors/images, compute a simple diversity statistic across '
                               'a fixed latent batch over epochs and flag severe collapse.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'def diversity_score(samples):\n    # TODO\n    pass',
                'acceptance_criteria': ['metric documented as heuristic',
                                        'fixed latent sample for comparison',
                                        'does not claim to solve mode collapse'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Implementing GAN Training Loops — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Implementing GAN Training Loops»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Implementing GAN Training "
                                     "Loops'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
