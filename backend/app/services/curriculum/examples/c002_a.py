"""COURSE-002 Deep Learning Foundations: example answers (part a)."""

EXAMPLES = {
    "COURSE-002.M01.L01.EX01": (
        """| System | Type |
| Tax calculator with fixed rules | Rule-based automation |
| Spam classifier trained on labelled messages | Machine learning |
| Chess program with only hand-written move rules | Rule-based AI |

The spam classifier is the one that must learn from examples: nobody gives it the rules, it infers them from labelled messages. Spam is hard to cover with hand-written rules because spammers change wording, spelling and tricks constantly, and legitimate mail uses the same words, so any fixed rule list is either incomplete or blocks real messages.""",
        """| النظام | النوع |
| حاسبة ضرائب بقواعد ثابتة | أتمتة قائمة على القواعد |
| مصنف spam مدرَّب على رسائل مصنفة | machine learning |
| برنامج شطرنج بقواعد حركة مكتوبة يدويًا فقط | AI قائم على القواعد |

مصنف الـ spam هو الذي يجب أن يتعلم من الأمثلة: لا يعطيه أحد القواعد، بل يستنتجها من رسائل مصنفة. من الصعب تغطية الـ spam بقواعد يدوية لأن المرسلين يغيّرون الصياغة والإملاء والحيل باستمرار، كما أن الرسائل السليمة تستخدم الكلمات نفسها، فتكون أي قائمة قواعد ثابتة إما ناقصة أو تحجب رسائل حقيقية.""",
    ),
    "COURSE-002.M01.L01.EX02": (
        """1. Hierarchy: AI (any technique that makes machines act intelligently) contains machine learning (systems that learn from data), which contains deep learning (machine learning with many-layered neural networks).
2. "Every AI system is deep learning" - false. "Every deep-learning model is machine learning" - true. "Machine learning is broader than AI" - false.
3. Corrections: deep learning is only one kind of AI; rule-based and search-based systems are AI without deep learning. Machine learning is a subset of AI, not broader than it.
4. Machine learning differs from hand-written rules because the program's behaviour is learned from examples and feedback instead of being written out explicitly by a programmer.""",
        """1. التسلسل: الـ AI (أي تقنية تجعل الآلات تتصرف بذكاء) يحتوي machine learning (أنظمة تتعلم من البيانات)، والذي يحتوي deep learning (machine learning بشبكات عصبية متعددة الطبقات).
2. "كل نظام AI هو deep learning" - خطأ. "كل نموذج deep learning هو machine learning" - صحيح. "machine learning أوسع من AI" - خطأ.
3. التصحيح: الـ deep learning نوع واحد فقط من الـ AI؛ فالأنظمة القائمة على القواعد أو البحث هي AI بلا deep learning. والـ machine learning جزء من الـ AI وليس أوسع منه.
4. يختلف machine learning عن القواعد اليدوية لأن سلوك البرنامج يُتعلَّم من الأمثلة والتغذية الراجعة بدلًا من أن يكتبه المبرمج صراحةً.""",
    ),
    "COURSE-002.M01.L02.EX01": (
        """| Task | Input | Expected output | Performance measure |
| Speech recognition | An audio recording of speech | The written transcript | Word error rate (share of wrongly recognised words) |
| Image tagging | An image | Tags such as "dog", "beach" | Share of correct tags (accuracy, or precision/recall per tag) |

Feedback is necessary because it is the only way the algorithm knows how far its output is from the expected output; that distance is the signal it uses to adjust itself. Without it, the system has no reason to change and cannot improve.""",
        """| المهمة | المدخل | المخرج المتوقع | مقياس الأداء |
| التعرف على الكلام | تسجيل صوتي لكلام | النص المكتوب | word error rate (نسبة الكلمات المتعرَّف عليها خطأً) |
| وسم الصور | صورة | وسوم مثل "dog" و"beach" | نسبة الوسوم الصحيحة (accuracy، أو precision/recall لكل وسم) |

التغذية الراجعة ضرورية لأنها الطريقة الوحيدة التي تعرف بها الخوارزمية مدى بُعد مخرجها عن المخرج المتوقع؛ وهذا البُعد هو الإشارة التي تستخدمها لتعديل نفسها. بدونها لا يوجد سبب لأن يتغير النظام ولا يمكنه التحسن.""",
    ),
    "COURSE-002.M01.L02.EX02": (
        """1. Two classes of 2D points overlap awkwardly in the original x/y axes, for example one class forms a ring around the other.
2. Patching the boundary with more and more special-case rules makes the classifier complicated and fragile. A better representation - for example using the distance from the centre instead of x and y - can make the classes separable by one simple threshold.
3. While searching transformations, the algorithm evaluates each candidate by feedback: how well the transformed data can be classified, measured as the share of correctly classified training points (or a loss).
4. The hypothesis space limits which transformations and rules the algorithm can consider at all, so a good representation must be inside it to be found.""",
        """1. فئتان من النقاط ثنائية الأبعاد تتداخلان بشكل مربك على محوري x وy الأصليين، مثلًا إحداهما حلقة تحيط بالأخرى.
2. ترقيع الحد الفاصل بقواعد استثنائية متزايدة يجعل المصنف معقدًا وهشًا. أما تمثيل أفضل - مثل استخدام البعد عن المركز بدلًا من x وy - فيجعل الفئتين قابلتين للفصل بعتبة بسيطة واحدة.
3. أثناء البحث في التحويلات تقيّم الخوارزمية كل تحويل مرشح عبر التغذية الراجعة: مدى سهولة تصنيف البيانات بعد التحويل، مقيسًا بنسبة نقاط التدريب المصنفة صحيحًا (أو بالـ loss).
4. الـ hypothesis space يحدد أي التحويلات والقواعد يمكن للخوارزمية أن تنظر فيها أصلًا، فلا بد أن يكون التمثيل الجيد داخله كي يُعثر عليه.""",
    ),
    "COURSE-002.M01.L03.EX01": (
        """1. Path: input image (pixels) -> layer 1 (edges and simple strokes) -> layer 2 (shapes and parts) -> layer 3 (object-level patterns) -> class prediction (for example "cat: 0.9").
2. Each layer is controlled by its weights (its parameters); the numbers inside every layer's transformation are what training adjusts.
3. If the weights changed, every layer would transform its input differently, so the internal representations - and finally the predicted class and its score - would change.
4. The architecture is fixed in advance; what makes a network good at a task is only the values of its parameters, so training is the search for weight values that make the predictions match the targets.""",
        """1. المسار: صورة المدخل (pixels) -> الطبقة 1 (حواف وخطوط بسيطة) -> الطبقة 2 (أشكال وأجزاء) -> الطبقة 3 (أنماط على مستوى الكائن) -> التنبؤ بالفئة (مثل "cat: 0.9").
2. كل طبقة تتحكم فيها weights الخاصة بها (الـ parameters)؛ هذه الأرقام داخل تحويل كل طبقة هي ما يعدّله التدريب.
3. إذا تغيرت الـ weights ستحوّل كل طبقة مدخلها بطريقة مختلفة، فتتغير التمثيلات الداخلية، ثم الفئة المتوقعة ودرجتها في النهاية.
4. البنية محددة مسبقًا؛ وما يجعل الشبكة جيدة في مهمة ما هو قيم الـ parameters فقط، لذلك فالتدريب هو البحث عن قيم weights تجعل التنبؤات تطابق الـ targets.""",
    ),
    "COURSE-002.M01.L03.EX02": (
        """1. The target is "cat", but the network outputs a high probability for "dog".
2. The loss function compares prediction and target and returns a large value: the prediction is confidently wrong, so the loss signals a big error.
3. Backpropagation works backwards from the loss through every layer and computes, for each weight, how much it contributed to the error and in which direction it should move to reduce it (its gradient).
4. The optimizer then changes every weight a small step in the direction that lowers the loss, so on the next prediction "cat" gets a slightly higher score and "dog" a slightly lower one.""",
        """1. الـ target هو "cat"، لكن الشبكة تعطي probability عالية لـ "dog".
2. تقارن الـ loss function بين التنبؤ والـ target وتعيد قيمة كبيرة: التنبؤ خاطئ بثقة، فتشير الـ loss إلى خطأ كبير.
3. يعمل backpropagation عكسيًا من الـ loss عبر كل طبقة ويحسب لكل weight مقدار مساهمته في الخطأ والاتجاه الذي يجب أن يتحرك فيه لتقليله (الـ gradient).
4. ثم يغيّر الـ optimizer كل weight خطوة صغيرة في الاتجاه الذي يخفض الـ loss، فيحصل "cat" في التنبؤ التالي على درجة أعلى قليلًا و"dog" على درجة أقل قليلًا.""",
    ),
    "COURSE-002.M01.L04.EX01": (
        """1. Task: recognizing handwritten digits (0-9).
2. Manual features: the number of closed loops in the digit (0, 6, 8, 9 have loops), and the ratio of ink in the upper versus lower half of the image.
3. In deep learning the network receives the raw pixels and discovers its own intermediate features - strokes, curves, loops - during training; the engineer designs the architecture, not the features.
4. Linked strength - simplicity: instead of a fragile pipeline of hand-crafted feature extractors plus a classifier, one model is trained end to end, and the same approach works for letters or other symbols without new feature engineering.""",
        """1. المهمة: التعرف على الأرقام المكتوبة يدويًا (0-9).
2. features يدوية: عدد الحلقات المغلقة في الرقم (0 و6 و8 و9 فيها حلقات)، ونسبة الحبر في النصف العلوي مقابل السفلي من الصورة.
3. في deep learning تستقبل الشبكة الـ pixels الخام وتكتشف features وسيطة خاصة بها - خطوط ومنحنيات وحلقات - أثناء التدريب؛ فالمهندس يصمم البنية لا الـ features.
4. الميزة المرتبطة - البساطة (simplicity): بدلًا من pipeline هش من مستخرجات features يدوية ثم مصنف، يُدرَّب نموذج واحد end to end، وتصلح الطريقة نفسها للحروف أو رموز أخرى دون feature engineering جديد.""",
    ),
    "COURSE-002.M01.L04.EX02": (
        """1. Demonstrated capability: deep learning models reach human-level accuracy on image classification and power working speech recognition and machine translation.
2. Broad future claim: "AI will replace most professional jobs within five years."
3. Questions: What measured evidence shows current systems doing these jobs end to end, not just isolated tasks? Under what conditions and error rates was it tested, and who measured it? What would it cost, and what would still need human oversight or accountability?
4. Skepticism and optimism coexist because they apply to different things: we can be sure deep learning is already useful and will keep improving, while still demanding evidence before believing specific, dated predictions about its impact.""",
        """1. قدرة مثبتة: نماذج deep learning تصل إلى دقة بمستوى البشر في تصنيف الصور، وتشغّل أنظمة فعالة للتعرف على الكلام والترجمة الآلية.
2. ادعاء مستقبلي واسع: "سيحل AI محل معظم الوظائف المهنية خلال خمس سنوات".
3. الأسئلة: ما الدليل المقيس على أن الأنظمة الحالية تؤدي هذه الوظائف كاملة لا مهام منفصلة فقط؟ في أي ظروف وبأي معدلات خطأ اختُبرت، ومن قاسها؟ وما التكلفة، وما الذي سيظل يحتاج إشرافًا أو مسؤولية بشرية؟
4. يتعايش التشكك مع التفاؤل لأنهما ينطبقان على أشياء مختلفة: يمكن أن نكون متأكدين من أن deep learning مفيد فعلًا وسيتحسن، ومع ذلك نطلب أدلة قبل تصديق تنبؤات محددة بمواعيد عن أثره.""",
    ),
    "COURSE-002.M02.L01.EX01": (
        """1. (5000, 12) - rank 2: 5000 customers (samples) x 12 features.
2. (128, 256, 256, 3) - rank 4: 128 images x height 256 x width 256 x 3 colour channels (RGB).
3. (32, 100, 64) - rank 3: 32 sequences x 100 timesteps x 64 features per timestep.
4. (4, 240, 144, 256, 3) - rank 5: 4 videos x 240 frames x height 144 x width 256 x 3 channels.
5. Rank is the number of axes; shape lists how many entries the tensor has along each axis.
6. Shape (5,) is rank 1: it has one axis that happens to hold five entries (a 5-dimensional vector, but a rank-1 tensor).
7. images[:128] has shape (128, 28, 28): slicing the first axis keeps 128 images and leaves the other axes unchanged.""",
        """1. (5000, 12) - rank 2: 5000 عميل (samples) × 12 feature.
2. (128, 256, 256, 3) - rank 4: 128 صورة × ارتفاع 256 × عرض 256 × 3 قنوات ألوان (RGB).
3. (32, 100, 64) - rank 3: 32 تسلسلًا × 100 timestep × 64 feature لكل timestep.
4. (4, 240, 144, 256, 3) - rank 5: 4 فيديوهات × 240 إطارًا × ارتفاع 144 × عرض 256 × 3 قنوات.
5. الـ rank هو عدد المحاور؛ أما الـ shape فيذكر عدد العناصر على كل محور.
6. الـ shape ‏(5,) هو rank 1: له محور واحد يحمل خمسة عناصر (متجه بخمسة أبعاد، لكنه tensor من rank 1).
7. الـ images[:128] لها shape ‏(128, 28, 28): التقطيع على المحور الأول يحتفظ بـ 128 صورة ويترك المحاور الأخرى كما هي.""",
    ),
    "COURSE-002.M02.L01.EX02": (
        """1. Order: input batch -> prediction -> loss calculation -> gradient calculation -> parameter update.
2. Forward pass: feeding the input batch through the network to get the prediction, and computing the loss.
3. Backward pass: the gradient calculation (backpropagation).
4. The loss is one number saying how far the predictions are from the true labels on this batch.
5. The gradient tells, for every weight, how the loss changes if that weight increases - the direction of steepest increase.
6. The optimizer uses the gradients to update the weights so the loss decreases (plain SGD, or variants like Adam).
7. The minus sign moves each weight against its gradient, that is downhill, because the gradient points in the direction that increases the loss.
8. With an extremely large learning rate each step overshoots the minimum: the loss jumps around or explodes (diverges) instead of decreasing.""",
        """1. الترتيب: دفعة المدخلات -> التنبؤ -> حساب الـ loss -> حساب الـ gradients -> تحديث الـ parameters.
2. الـ forward pass: تمرير دفعة المدخلات عبر الشبكة للحصول على التنبؤ، وحساب الـ loss.
3. الـ backward pass: حساب الـ gradients (backpropagation).
4. الـ loss رقم واحد يوضح مدى بُعد التنبؤات عن الـ labels الصحيحة في هذه الدفعة.
5. الـ gradient يوضح لكل weight كيف تتغير الـ loss إذا زادت قيمته - أي اتجاه أسرع زيادة.
6. يستخدم الـ optimizer الـ gradients لتحديث الـ weights بحيث تنخفض الـ loss (SGD البسيط أو أشكال مثل Adam).
7. علامة الطرح تحرك كل weight عكس الـ gradient، أي نزولًا، لأن الـ gradient يشير إلى الاتجاه الذي يزيد الـ loss.
8. مع learning rate كبير جدًا تتخطى كل خطوة نقطة الحد الأدنى: فتقفز الـ loss أو تنفجر (diverge) بدلًا من أن تنخفض.""",
    ),
    "COURSE-002.M03.L01.EX01": (
        """| Framework | How gradients are computed |
| TensorFlow | tf.GradientTape records the forward pass; tape.gradient(loss, weights) returns the gradients |
| PyTorch | loss.backward() runs backpropagation; each parameter's gradient is stored in its .grad attribute, then optimizer.step() applies it |
| JAX | jax.grad(loss_fn) transforms the loss function into a new function that returns the gradients |

All three run the same sequence: forward pass, loss, gradients by the chain rule, parameter update. They differ only in how the program tells the framework what to differentiate - a recording tape, gradients attached to tensors, or a function transformation - while the derivatives and the update rule are mathematically identical.""",
        """| الإطار | طريقة حساب الـ gradients |
| TensorFlow | يسجل tf.GradientTape الـ forward pass، ثم يعيد tape.gradient(loss, weights) الـ gradients |
| PyTorch | يشغّل loss.backward() الـ backpropagation، ويُخزَّن gradient كل parameter في الخاصية .grad، ثم يطبقه optimizer.step() |
| JAX | يحوّل jax.grad(loss_fn) دالة الـ loss إلى دالة جديدة تعيد الـ gradients |

الأطر الثلاثة تنفذ التسلسل نفسه: forward pass ثم loss ثم gradients بقاعدة السلسلة (chain rule) ثم تحديث الـ parameters. الفرق فقط في طريقة إخبار الإطار بما يجب اشتقاقه - شريط تسجيل، أو gradients ملحقة بالـ tensors، أو تحويل للدالة - بينما المشتقات وقاعدة التحديث متطابقة رياضيًا.""",
    ),
    "COURSE-002.M04.L01.EX01": (
        """1. Two output classes: positive and negative.
2. Final layer: Dense(1, activation="sigmoid"), one unit giving a probability between 0 and 1.
3. Loss: binary_crossentropy.
4. An output of 0.92 means the model estimates a 92% probability that the feedback is positive (with a 0.5 threshold it is classified positive).
5. A network only computes with numbers, so text must become tensors first - for example multi-hot vectors over a vocabulary or sequences of word indices.
6. Training set: fits the weights. Validation set: monitors the model during development to choose epochs and settings. Test set: touched once at the end to estimate performance on new data.
7. That is overfitting: the model keeps memorizing the training data while getting worse on unseen data, so I would stop training around the epoch with the best validation accuracy (or add regularization) and not trust further training gains.""",
        """1. فئتا مخرج: positive وnegative.
2. الطبقة الأخيرة: Dense(1, activation="sigmoid")، وحدة واحدة تعطي probability بين 0 و1.
3. الـ loss: binary_crossentropy.
4. المخرج 0.92 يعني أن النموذج يقدّر احتمال أن يكون الرأي إيجابيًا بنسبة 92% (ومع threshold قدره 0.5 يُصنَّف إيجابيًا).
5. الشبكة تحسب بالأرقام فقط، لذا يجب تحويل النص إلى tensors أولًا - مثل متجهات multi-hot على مفردات محددة أو تسلسلات من أرقام الكلمات.
6. مجموعة التدريب: تُضبط بها الـ weights. مجموعة الـ validation: لمراقبة النموذج أثناء التطوير واختيار عدد الـ epochs والإعدادات. مجموعة الاختبار: تُستخدم مرة واحدة في النهاية لتقدير الأداء على بيانات جديدة.
7. هذا overfitting: النموذج يستمر في حفظ بيانات التدريب بينما يسوء على البيانات غير المرئية، لذا أوقف التدريب قرب الـ epoch التي حققت أفضل validation accuracy (أو أضيف regularization) ولا أثق في مكاسب التدريب الإضافية.""",
    ),
}
