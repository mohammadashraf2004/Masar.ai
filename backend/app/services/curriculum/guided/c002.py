"""COURSE-002 Deep Learning: guided implementation exercises."""
from . import Guided

EXERCISES = {
    "COURSE-002.M03.L01.EX02": Guided(
        goal=(
            "Complete a Keras workflow for a binary (0/1) classifier: build, compile, train with validation data, and predict.",
            "أكمل سير عمل Keras لمصنّف ثنائي (0/1): البناء، ثم الترجمة (compile)، ثم التدريب مع بيانات تحقق، ثم التنبؤ.",
        ),
        steps=(
            ("Finish the model with one output unit and a sigmoid activation.",
             "أكمل النموذج بوحدة إخراج واحدة ودالة تنشيط sigmoid."),
            ("Choose the binary cross-entropy loss in `compile`.", "اختر دالة الخسارة binary cross-entropy في `compile`."),
            ("Pass the validation pair to `fit` so Keras evaluates it after every epoch.",
             "مرّر زوج التحقق إلى `fit` ليقيّمه Keras بعد كل حقبة (epoch)."),
            ("Generate predictions for the new inputs.", "أنشئ التنبؤات للمدخلات الجديدة."),
        ),
        starter='''import numpy as np
from tensorflow import keras

rng = np.random.default_rng(0)
X_train = rng.random((200, 4))
y_train = (X_train.sum(axis=1) > 2).astype(int)
X_val = rng.random((50, 4))
y_val = (X_val.sum(axis=1) > 2).astype(int)

# Step 1: one hidden layer, then ONE output unit with a sigmoid for a 0/1 target
model = keras.Sequential([
    keras.layers.Input(shape=(4,)),
    keras.layers.Dense(16, activation="relu"),
    ___,
])

# Step 2: binary cross-entropy loss, Adam optimizer, accuracy metric
model.compile(optimizer="adam", loss=___, metrics=["accuracy"])

# Step 3: train; the validation data is evaluated after each epoch, never trained on
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=___)

# Step 4: probabilities for new inputs
X_new = rng.random((3, 4))
probabilities = ___
''',
        answers=(
            'keras.layers.Dense(1, activation="sigmoid")',
            '"binary_crossentropy"',
            "(X_val, y_val)",
            "model.predict(X_new)",
        ),
        alternatives={
            1: ('keras.layers.Dense(units=1, activation="sigmoid")',),
            2: ("keras.losses.BinaryCrossentropy()",),
            3: ("[X_val, y_val]",),
            4: ("model.predict(X_new, verbose=0)", "model(X_new)"),
        },
        blanks=(
            ("add `keras.layers.Dense(1, activation=\"sigmoid\")` - one unit that outputs a probability.",
             "أضف `keras.layers.Dense(1, activation=\"sigmoid\")` - وحدة واحدة تُخرج احتمالًا."),
            ("for a 0/1 target with a sigmoid output use `\"binary_crossentropy\"`.",
             "لهدف 0/1 مع إخراج sigmoid استخدم `\"binary_crossentropy\"`."),
            ("pass the validation inputs and labels as one tuple: `(X_val, y_val)`.",
             "مرّر مدخلات التحقق وتسمياته في صفّ (tuple) واحد: `(X_val, y_val)`."),
            ("call `model.predict(X_new)`.", "استدعِ `model.predict(X_new)`."),
        ),
        hints=(
            ("A binary classifier ends with a single unit; sigmoid squeezes its output into a probability between 0 and 1.",
             "ينتهي المصنّف الثنائي بوحدة واحدة؛ وتحصر sigmoid مخرجها في احتمال بين 0 و1."),
            ("The loss that matches a sigmoid output and 0/1 labels is binary cross-entropy.",
             "دالة الخسارة المناسبة لإخراج sigmoid وتسميات 0/1 هي binary cross-entropy."),
            ("`validation_data` takes a tuple `(inputs, labels)`; predictions come from `model.predict(...)`.",
             "يأخذ `validation_data` صفًّا `(inputs, labels)`؛ وتأتي التنبؤات من `model.predict(...)`."),
        ),
        success=(
            "Correct! You built, compiled, trained and used a Keras classifier, with validation data used only for evaluation.",
            "صحيح! بنيت مصنّف Keras وترجمته ودرّبته واستخدمته، مع استعمال بيانات التحقق للتقييم فقط.",
        ),
        expected=(
            "A complete Keras sketch: model construction, compile, fit with validation data, and predict. TensorFlow is not installed in the practice sandbox, so your code is checked by reading its structure.",
            "مخطط Keras كامل: بناء النموذج، وcompile، وfit مع بيانات التحقق، وpredict. مكتبة TensorFlow غير مثبّتة في بيئة التدريب، لذلك يُفحص الكود بقراءة بنيته.",
        ),
        reflect=(
            "Why must the validation set never be used to update the model's weights?",
            "لماذا يجب ألا تُستخدم مجموعة التحقق أبدًا في تحديث أوزان النموذج؟",
        ),
    ),
}
