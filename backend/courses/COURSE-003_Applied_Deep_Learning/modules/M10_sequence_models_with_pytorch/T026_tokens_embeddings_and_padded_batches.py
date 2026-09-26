# -*- coding: utf-8 -*-
"""T026 — Applied Deep Learning, module M10.
Portable Masar seed data; importing this file performs no database writes.
"""

SOURCE = {'book_id': 'BOOK-003',
 'chapter': 5,
 'chapter_title': 'Text Classification',
 'source_file': 'تم لصق markdown(20260923-114931).md',
 'source_line_ranges': [[306, 415], [960, 1048]],
 'edition': 'SOURCE INFORMATION MISSING',
 'printed_pages': 'SOURCE INFORMATION MISSING',
 'source_is_user_supplied': True,
 'instructional_content_and_exercises_are_masar_original': True,
 'curriculum_id': 'C003-M10-L01',
 'source_note': 'Torchtext Field/BucketIterator omitted; durable embedding and padding concepts retained.'}

MODERNIZATION = {'labels': [], 'official_docs_checked_2026_09': False}

TOPIC = {'title': 'Tokens, Embeddings, and Padded Batches',
 'slug': 'applied-deep-learning-t026-tokens-embeddings-and-padded-batches',
 'description': 'تطبيق عملي: Tokens, Embeddings, and Padded Batches مع كود وتمارين تحقق وتصحيح أخطاء.',
 'order': 1,
 'difficulty': 'intermediate',
 'estimated_hours': 0.75,
 'skill_tags': ['pytorch', 'applied-deep-learning', 'token-ids', 'vocabulary', 'padding', 'pad-sequence'],
 'prerequisite_ids': [],
 'lesson': {'title': 'Tokens, Embeddings, and Padded Batches',
            'content': '# Tokens, Embeddings, and Padded Batches\n'
                       '\n'
                       '**المساق:** Applied Deep Learning · **الوحدة M10:** نماذج التسلسل باستخدام PyTorch · '
                       '**الدرس T026 / C003-M10-L01** · **المدة:** 45 دقيقة\n'
                       '\n'
                       '## هدف عملي\n'
                       '\n'
                       'هذا الدرس عملي بالدرجة الأولى. المطلوب ليس حفظ API، بل كتابة كود يعمل، التحقق من '
                       'الأشكال/الأجهزة/الأنواع، واستخدام اختبارات قصيرة تكشف الأخطاء مبكراً.\n'
                       '\n'
                       '## المهارات\n'
                       '\n'
                       'token ids, vocabulary, padding, pad_sequence, nn.Embedding, padding_idx\n'
                       '\n'
                       '## Guided Code Lab\n'
                       '\n'
                       '```python\n'
                       'import torch\n'
                       'from torch.nn.utils.rnn import pad_sequence\n'
                       'from torch import nn\n'
                       'seqs = [torch.tensor([2,5,7]), torch.tensor([4,3])]\n'
                       'batch = pad_sequence(seqs, batch_first=True, padding_value=0)\n'
                       'emb = nn.Embedding(10, 8, padding_idx=0)\n'
                       'out = emb(batch)\n'
                       'assert out.shape == (2,3,8)\n'
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
                       'Torchtext Field/BucketIterator omitted; durable embedding and padding concepts '
                       'retained.\n',
            'estimated_minutes': 45,
            'has_code_examples': True,
            'guided_code': 'import torch\n'
                           'from torch.nn.utils.rnn import pad_sequence\n'
                           'from torch import nn\n'
                           'seqs = [torch.tensor([2,5,7]), torch.tensor([4,3])]\n'
                           'batch = pad_sequence(seqs, batch_first=True, padding_value=0)\n'
                           'emb = nn.Embedding(10, 8, padding_idx=0)\n'
                           'out = emb(batch)\n'
                           'assert out.shape == (2,3,8)',
            'curriculum_id': 'C003-M10-L01'},
 'exercises': [{'title': 'Vocabulary and collate function',
                'description': 'Implement a tiny vocabulary with PAD=0, UNK=1 and a collate function returning '
                               'padded IDs, lengths and labels.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': 'import torch\n'
                                'from torch.nn.utils.rnn import pad_sequence\n'
                                '\n'
                                'def collate(batch):\n'
                                '    # TODO\n'
                                '    pass',
                'acceptance_criteria': ['PAD and UNK handled',
                                        'returns batch_first padded tensor',
                                        'returns original lengths',
                                        'labels long dtype'],
                'validation_code': '',
                'hints': []},
               {'title': 'Embedding padding test',
                'description': 'Create an embedding with padding_idx=0, run a backward pass and verify padding '
                               'row gradient is zero/absent while a real token row receives gradient.',
                'difficulty': 'intermediate',
                'skill_tested': ['pytorch', 'applied-deep-learning'],
                'starter_code': '# TODO',
                'acceptance_criteria': ['padding row not updated',
                                        'non-padding token receives gradient',
                                        'uses integer token ids'],
                'validation_code': '',
                'hints': []}],
 'quiz': {'title': 'Tokens, Embeddings, and Padded Batches — Practical Check',
          'questions': [{'question': 'ما أفضل طريقة للتحقق عملياً من درس «Tokens, Embeddings, and Padded '
                                     'Batches»؟',
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
                        {'question': "اشرح اختباراً واحداً سيكشف خطأً صامتاً في تطبيق 'Tokens, Embeddings, and "
                                     "Padded Batches'.",
                         'type': 'open'}],
          'passing_score': 70},
 'practice_profile': {'guided_code': True,
                      'code_exercises': 2,
                      'acceptance_criteria': True,
                      'debugging_focus': True}}
