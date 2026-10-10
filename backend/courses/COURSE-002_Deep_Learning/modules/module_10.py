"""M13.L01 — Timeseries Forecasting and Recurrent Neural Networks.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 13, page range not provided in supplied source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M13.L01"

MODULE_ORDER = 13

MODULE_TITLE = "Timeseries Forecasting and Recurrent Neural Networks"

MODULE_DESCRIPTION = (
    "Learn how timeseries problems differ from ordinary machine learning "
    "tasks, how to prepare chronological data for forecasting, how to build "
    "meaningful baselines, and how recurrent neural networks such as LSTM "
    "and GRU preserve information across time."
)

SOURCE_CHAPTER = 13

SOURCE_PAGES = "Chapter 13 — page range not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Timeseries Forecasting with RNNs, LSTMs, and GRUs",

    "slug": "deep-learning-foundations-m13-l01",

    "description": (
        "Understand timeseries forecasting from problem framing and "
        "chronological data preparation through baseline models, recurrent "
        "neural networks, LSTMs, recurrent dropout, stacked RNNs, and "
        "bidirectional sequence processing."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.5,

    "skill_tags": [
        "deep-learning",
        "timeseries",
        "forecasting",
        "sequence-modeling",
        "rnn",
        "lstm",
        "gru",
        "recurrent-dropout",
        "bidirectional-rnn",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Timeseries Forecasting with RNNs, LSTMs, and GRUs",

        "content": (
            "# Timeseries Forecasting with RNNs, LSTMs, and GRUs\n"
            "\n"
            "> **Course:** Deep Learning Foundations  \n"
            "> **Lesson:** M13.L01  \n"
            "> **Module:** Timeseries Forecasting and Recurrent Neural Networks  \n"
            "> **Source alignment:** BOOK-002, Chapter 13. "
            "The supplied source did not specify a page range. "
            "This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what makes timeseries data different from ordinary "
            "independent samples.\n"
            "- Distinguish forecasting, anomaly detection, classification, "
            "and event detection on timeseries data.\n"
            "- Explain why temporal order must be preserved when splitting "
            "timeseries data.\n"
            "- Normalize timeseries features without leaking future data.\n"
            "- Convert a continuous timeseries into input windows and future "
            "targets.\n"
            "- Build and interpret a commonsense forecasting baseline.\n"
            "- Explain why simple Dense and Conv1D models may fail when order "
            "and recent history matter strongly.\n"
            "- Explain the internal state concept behind recurrent neural "
            "networks.\n"
            "- Distinguish SimpleRNN, LSTM, and GRU conceptually.\n"
            "- Explain why LSTM was designed to preserve useful information "
            "over longer temporal distances.\n"
            "- Use `return_sequences` correctly when stacking recurrent layers.\n"
            "- Explain recurrent dropout and why the dropout mask should remain "
            "consistent across timesteps.\n"
            "- Explain when stacked recurrent layers may improve performance.\n"
            "- Explain how bidirectional RNNs process sequences in both directions.\n"
            "- Recognize when bidirectional processing is inappropriate for a "
            "forecasting problem.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Understanding Timeseries and Forecasting\n"
            "\n"
            "A **timeseries** is a sequence of measurements recorded over time.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "```text\n"
            "hourly electricity consumption\n"
            "daily stock prices\n"
            "weekly store sales\n"
            "weather measurements\n"
            "website traffic\n"
            "credit card transaction activity\n"
            "```\n"
            "\n"
            "What makes timeseries special is that **order matters**.\n"
            "\n"
            "In ordinary tabular datasets, row 100 may have no meaningful "
            "relationship to row 101.\n"
            "\n"
            "In a timeseries, however:\n"
            "\n"
            "```text\n"
            "past → present → future\n"
            "```\n"
            "\n"
            "The location of a measurement in time is part of its meaning.\n"
            "\n"
            "### Common timeseries tasks\n"
            "\n"
            "Forecasting is only one possible task.\n"
            "\n"
            "#### Forecasting\n"
            "\n"
            "Predict what will happen next.\n"
            "\n"
            "```text\n"
            "past electricity usage\n"
            "→ predict demand a few hours ahead\n"
            "\n"
            "past sales\n"
            "→ predict next month's sales\n"
            "\n"
            "recent weather\n"
            "→ predict tomorrow's temperature\n"
            "```\n"
            "\n"
            "#### Anomaly detection\n"
            "\n"
            "Find unusual behavior in a stream.\n"
            "\n"
            "```text\n"
            "normal network traffic\n"
            "normal network traffic\n"
            "normal network traffic\n"
            "SUDDEN UNUSUAL PATTERN\n"
            "```\n"
            "\n"
            "#### Classification\n"
            "\n"
            "Assign a label to an entire temporal sequence.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "website activity sequence\n"
            "→ human user / bot\n"
            "```\n"
            "\n"
            "#### Event detection\n"
            "\n"
            "Detect a known event inside a continuous stream.\n"
            "\n"
            "For example, an audio model may continuously listen for a "
            "specific wake phrase.\n"
            "\n"
            "### Forecasting temperature\n"
            "\n"
            "The chapter's main problem is:\n"
            "\n"
            "> Given weather observations from the recent past, can we predict "
            "the temperature 24 hours into the future?\n"
            "\n"
            "The dataset contains weather measurements recorded every ten "
            "minutes over several years.\n"
            "\n"
            "There are 14 weather-related numerical variables at each timestep.\n"
            "\n"
            "These include quantities such as:\n"
            "\n"
            "- temperature,\n"
            "- atmospheric pressure,\n"
            "- humidity,\n"
            "- wind speed,\n"
            "- and wind direction.\n"
            "\n"
            "### Periodicity\n"
            "\n"
            "Timeseries often contain repeated cycles.\n"
            "\n"
            "Weather can show:\n"
            "\n"
            "```text\n"
            "daily cycles\n"
            "+\n"
            "seasonal / yearly cycles\n"
            "```\n"
            "\n"
            "Other domains may contain:\n"
            "\n"
            "```text\n"
            "hourly cycles\n"
            "daily cycles\n"
            "weekly cycles\n"
            "yearly cycles\n"
            "```\n"
            "\n"
            "Looking for periodic patterns should therefore be part of initial "
            "timeseries exploration.\n"
            "\n"
            "### Preserve temporal ordering in dataset splits\n"
            "\n"
            "For ordinary classification problems, you might randomly shuffle "
            "examples before splitting them.\n"
            "\n"
            "That can be inappropriate for forecasting.\n"
            "\n"
            "The chapter uses:\n"
            "\n"
            "```text\n"
            "oldest 50% → training\n"
            "next 25%   → validation\n"
            "latest 25% → testing\n"
            "```\n"
            "\n"
            "Why?\n"
            "\n"
            "Because the real forecasting situation is:\n"
            "\n"
            "```text\n"
            "learn from the past\n"
            "       ↓\n"
            "predict the future\n"
            "```\n"
            "\n"
            "Using future data to help train a model intended to predict that "
            "future would create an unrealistic evaluation.\n"
            "\n"
            "### Normalize using training statistics only\n"
            "\n"
            "The 14 weather features use different numerical scales.\n"
            "\n"
            "For example, pressure values may be around 1,000 while another "
            "feature may have values near 3.\n"
            "\n"
            "So each feature is normalized:\n"
            "\n"
            "```python\n"
            "mean = raw_data[:num_train_samples].mean(axis=0)\n"
            "raw_data -= mean\n"
            "\n"
            "std = raw_data[:num_train_samples].std(axis=0)\n"
            "raw_data /= std\n"
            "```\n"
            "\n"
            "Notice that `mean` and `std` are computed using **training data "
            "only**.\n"
            "\n"
            "Validation and test data must not influence preprocessing "
            "statistics.\n"
            "\n"
            "### Turning the series into training examples\n"
            "\n"
            "The forecasting setup is:\n"
            "\n"
            "```text\n"
            "Input:\n"
            "previous 5 days\n"
            "sampled once per hour\n"
            "\n"
            "Target:\n"
            "temperature 24 hours after the input sequence ends\n"
            "```\n"
            "\n"
            "Five days contain:\n"
            "\n"
            "```text\n"
            "5 × 24 = 120 hours\n"
            "```\n"
            "\n"
            "So one input has shape:\n"
            "\n"
            "```text\n"
            "(120, 14)\n"
            "```\n"
            "\n"
            "meaning:\n"
            "\n"
            "```text\n"
            "120 timesteps\n"
            "14 features at each timestep\n"
            "```\n"
            "\n"
            "A training batch has shape:\n"
            "\n"
            "```text\n"
            "(256, 120, 14)\n"
            "```\n"
            "\n"
            "which means:\n"
            "\n"
            "```text\n"
            "256 sequences\n"
            "120 timesteps per sequence\n"
            "14 features per timestep\n"
            "```\n"
            "\n"
            "### Sliding windows\n"
            "\n"
            "Suppose we have:\n"
            "\n"
            "```text\n"
            "[0, 1, 2, 3, 4, 5, 6]\n"
            "```\n"
            "\n"
            "with sequence length 3.\n"
            "\n"
            "Sliding windows produce:\n"
            "\n"
            "```text\n"
            "[0, 1, 2]\n"
            "[1, 2, 3]\n"
            "[2, 3, 4]\n"
            "[3, 4, 5]\n"
            "[4, 5, 6]\n"
            "```\n"
            "\n"
            "If we want to predict the next value:\n"
            "\n"
            "```text\n"
            "[0, 1, 2] → 3\n"
            "[1, 2, 3] → 4\n"
            "[2, 3, 4] → 5\n"
            "```\n"
            "\n"
            "This is the fundamental structure of supervised forecasting data.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Baselines Before Recurrent Neural Networks\n"
            "\n"
            "Before building a complicated model, establish a simple baseline.\n"
            "\n"
            "A baseline answers:\n"
            "\n"
            "> Is the machine learning model actually learning something useful?\n"
            "\n"
            "### Commonsense baseline\n"
            "\n"
            "Temperature changes continuously and has a strong daily cycle.\n"
            "\n"
            "A reasonable naive forecast is:\n"
            "\n"
            "```text\n"
            "temperature tomorrow\n"
            "≈\n"
            "temperature right now\n"
            "```\n"
            "\n"
            "The chapter evaluates this using mean absolute error:\n"
            "\n"
            "```python\n"
            "MAE = np.mean(np.abs(predictions - targets))\n"
            "```\n"
            "\n"
            "The naive method achieves approximately:\n"
            "\n"
            "```text\n"
            "validation MAE ≈ 2.44°C\n"
            "test MAE       ≈ 2.62°C\n"
            "```\n"
            "\n"
            "So any sophisticated model should meaningfully improve on this.\n"
            "\n"
            "### Why baselines matter\n"
            "\n"
            "Imagine a binary classification dataset where:\n"
            "\n"
            "```text\n"
            "90% class A\n"
            "10% class B\n"
            "```\n"
            "\n"
            "A model that always predicts class A already achieves:\n"
            "\n"
            "```text\n"
            "90% accuracy\n"
            "```\n"
            "\n"
            "A neural network achieving 88% would therefore not be impressive.\n"
            "\n"
            "The baseline tells you what performance must be beaten.\n"
            "\n"
            "### Try simple machine learning first\n"
            "\n"
            "Before an RNN, the chapter tries a small Dense model.\n"
            "\n"
            "```python\n"
            "inputs = keras.Input(shape=(120, 14))\n"
            "x = layers.Flatten()(inputs)\n"
            "x = layers.Dense(16, activation=\"relu\")(x)\n"
            "outputs = layers.Dense(1)(x)\n"
            "model = keras.Model(inputs, outputs)\n"
            "```\n"
            "\n"
            "Because this is scalar regression:\n"
            "\n"
            "```text\n"
            "final output units = 1\n"
            "final activation   = none\n"
            "loss               = MSE\n"
            "metric             = MAE\n"
            "```\n"
            "\n"
            "### Why flattening is a problem\n"
            "\n"
            "`Flatten()` converts:\n"
            "\n"
            "```text\n"
            "(120, 14)\n"
            "```\n"
            "\n"
            "into one long vector.\n"
            "\n"
            "The model can still receive all values, but it loses an explicit "
            "architectural understanding of temporal sequence structure.\n"
            "\n"
            "The chapter finds that this simple model does not reliably beat "
            "the commonsense baseline.\n"
            "\n"
            "### A good solution existing is not enough\n"
            "\n"
            "The simple heuristic:\n"
            "\n"
            "```text\n"
            "tomorrow ≈ now\n"
            "```\n"
            "\n"
            "is easy for a human to express.\n"
            "\n"
            "But gradient descent searches within the hypothesis space defined "
            "by the chosen network architecture.\n"
            "\n"
            "A useful solution may technically exist somewhere in that space "
            "without being easy for optimization to discover.\n"
            "\n"
            "This is one reason good architecture priors matter.\n"
            "\n"
            "### Trying a temporal ConvNet\n"
            "\n"
            "The next experiment uses `Conv1D`.\n"
            "\n"
            "A 1D convolution slides along time rather than across image width "
            "and height.\n"
            "\n"
            "```python\n"
            "inputs = keras.Input(shape=(120, 14))\n"
            "\n"
            "x = layers.Conv1D(8, 24, activation=\"relu\")(inputs)\n"
            "x = layers.MaxPooling1D(2)(x)\n"
            "\n"
            "x = layers.Conv1D(8, 12, activation=\"relu\")(x)\n"
            "x = layers.MaxPooling1D(2)(x)\n"
            "\n"
            "x = layers.Conv1D(8, 6, activation=\"relu\")(x)\n"
            "x = layers.GlobalAveragePooling1D()(x)\n"
            "\n"
            "outputs = layers.Dense(1)(x)\n"
            "```\n"
            "\n"
            "This seems reasonable because weather contains repeated daily "
            "cycles.\n"
            "\n"
            "But it performs worse than the naive baseline.\n"
            "\n"
            "### Why the 1D ConvNet struggles\n"
            "\n"
            "The source gives two major reasons.\n"
            "\n"
            "#### 1. Weak translation invariance\n"
            "\n"
            "Image patterns such as an edge are useful almost regardless of "
            "their location.\n"
            "\n"
            "Weather is different.\n"
            "\n"
            "A pattern occurring in the morning may not have the same meaning "
            "as a similar pattern occurring at night.\n"
            "\n"
            "#### 2. Temporal order matters strongly\n"
            "\n"
            "For this forecasting problem:\n"
            "\n"
            "```text\n"
            "recent weather\n"
            "→ highly relevant\n"
            "\n"
            "weather five days ago\n"
            "→ generally less relevant\n"
            "```\n"
            "\n"
            "Pooling operations can destroy some of this temporal-order "
            "information.\n"
            "\n"
            "This motivates a model family designed specifically around "
            "sequential state.\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M13.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Recurrent Neural Networks and LSTM\n"
            "\n"
            "Most networks you have encountered so far are **feedforward "
            "networks**.\n"
            "\n"
            "They process each input and produce an output without maintaining "
            "an internal memory of previous timesteps.\n"
            "\n"
            "RNNs introduce a different idea:\n"
            "\n"
            "> Process a sequence one timestep at a time while carrying an "
            "internal state containing information about what has already "
            "been observed.\n"
            "\n"
            "### The recurrent loop\n"
            "\n"
            "The simplest conceptual RNN looks like:\n"
            "\n"
            "```text\n"
            "input at t\n"
            "    ↓\n"
            "[RNN cell] ← previous state\n"
            "    ↓\n"
            "output at t\n"
            "    ↓\n"
            "new state\n"
            "    ↓\n"
            "used at timestep t + 1\n"
            "```\n"
            "\n"
            "In pseudocode:\n"
            "\n"
            "```python\n"
            "state_t = 0\n"
            "\n"
            "for input_t in input_sequence:\n"
            "    output_t = f(input_t, state_t)\n"
            "    state_t = output_t\n"
            "```\n"
            "\n"
            "The network therefore carries information forward through time.\n"
            "\n"
            "### A simple RNN equation\n"
            "\n"
            "One possible recurrent step is:\n"
            "\n"
            "```python\n"
            "output_t = activation(\n"
            "    W @ input_t\n"
            "    + U @ state_t\n"
            "    + b\n"
            ")\n"
            "```\n"
            "\n"
            "There are two important sources of information:\n"
            "\n"
            "```text\n"
            "current input\n"
            "+\n"
            "previous state\n"
            "```\n"
            "\n"
            "That is what gives the network a form of memory.\n"
            "\n"
            "### Sequence input shapes\n"
            "\n"
            "Keras recurrent layers operate on batched sequence tensors:\n"
            "\n"
            "```text\n"
            "(batch_size, timesteps, input_features)\n"
            "```\n"
            "\n"
            "For the weather problem:\n"
            "\n"
            "```text\n"
            "(256, 120, 14)\n"
            "```\n"
            "\n"
            "means:\n"
            "\n"
            "```text\n"
            "256 samples\n"
            "120 timesteps per sample\n"
            "14 features per timestep\n"
            "```\n"
            "\n"
            "### Return only the last output\n"
            "\n"
            "By default:\n"
            "\n"
            "```python\n"
            "layers.SimpleRNN(16)\n"
            "```\n"
            "\n"
            "returns one vector for each input sequence:\n"
            "\n"
            "```text\n"
            "(batch_size, 16)\n"
            "```\n"
            "\n"
            "The final recurrent output already contains information derived "
            "from previous timesteps.\n"
            "\n"
            "### Return the entire sequence\n"
            "\n"
            "If we use:\n"
            "\n"
            "```python\n"
            "layers.SimpleRNN(16, return_sequences=True)\n"
            "```\n"
            "\n"
            "the layer returns:\n"
            "\n"
            "```text\n"
            "(batch_size, timesteps, 16)\n"
            "```\n"
            "\n"
            "There is one output vector for every timestep.\n"
            "\n"
            "This becomes essential when stacking recurrent layers because "
            "the next recurrent layer expects a sequence as input.\n"
            "\n"
            "### Why SimpleRNN is limited\n"
            "\n"
            "In theory, a simple RNN could carry information across many "
            "timesteps.\n"
            "\n"
            "In practice, learning long-term dependencies is difficult because "
            "of the **vanishing-gradient problem**.\n"
            "\n"
            "As training signals move backward through many recurrent steps, "
            "the useful gradient information can become too weak.\n"
            "\n"
            "### LSTM\n"
            "\n"
            "**Long Short-Term Memory**, or LSTM, was designed to address this "
            "problem.\n"
            "\n"
            "The key idea is an additional information pathway that can carry "
            "useful information across many timesteps.\n"
            "\n"
            "A useful mental model is a conveyor belt:\n"
            "\n"
            "```text\n"
            "t1 ───────────────────────────────→ tN\n"
            "     information can stay on this path\n"
            "     and be reused much later\n"
            "```\n"
            "\n"
            "This allows older information to survive instead of being "
            "repeatedly transformed until it disappears.\n"
            "\n"
            "### LSTM carry state\n"
            "\n"
            "The LSTM maintains a special carry state often written as `c_t`.\n"
            "\n"
            "The source presents the update conceptually as:\n"
            "\n"
            "```text\n"
            "c_(t+1) = i_t * k_t + c_t * f_t\n"
            "```\n"
            "\n"
            "You do not need to memorize the gate equations to use LSTM well.\n"
            "\n"
            "The important mental model is:\n"
            "\n"
            "> LSTM creates a pathway through which useful information can be "
            "preserved and reinjected at later timesteps.\n"
            "\n"
            "### LSTM weather model\n"
            "\n"
            "A very simple forecasting model is:\n"
            "\n"
            "```python\n"
            "inputs = keras.Input(shape=(120, 14))\n"
            "x = layers.LSTM(16)(inputs)\n"
            "outputs = layers.Dense(1)(x)\n"
            "\n"
            "model = keras.Model(inputs, outputs)\n"
            "```\n"
            "\n"
            "Compared with flattening or the tested Conv1D setup, this model "
            "is explicitly designed around sequence order.\n"
            "\n"
            "The chapter reports approximately:\n"
            "\n"
            "```text\n"
            "validation MAE ≈ 2.39°C\n"
            "test MAE       ≈ 2.55°C\n"
            "```\n"
            "\n"
            "This finally beats the commonsense baseline, though only slightly.\n"
            "\n"
            "That small improvement is still important because it demonstrates "
            "that learned sequence modeling adds value for this task.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Getting More from Recurrent Networks\n"
            "\n"
            "The first LSTM model works, but it quickly begins to overfit.\n"
            "\n"
            "The chapter therefore explores several techniques:\n"
            "\n"
            "```text\n"
            "recurrent dropout\n"
            "stacked recurrent layers\n"
            "GRU\n"
            "bidirectional RNNs\n"
            "```\n"
            "\n"
            "### Recurrent dropout\n"
            "\n"
            "Ordinary dropout randomly removes some activations during training "
            "to reduce reliance on accidental correlations.\n"
            "\n"
            "But recurrent networks require special care because information "
            "flows through time.\n"
            "\n"
            "Using a completely different random dropout mask at every "
            "timestep can disrupt the temporal learning signal.\n"
            "\n"
            "Instead, recurrent dropout uses a temporally consistent mask "
            "across the sequence.\n"
            "\n"
            "Keras recurrent layers provide:\n"
            "\n"
            "```text\n"
            "dropout\n"
            "→ dropout applied to layer inputs\n"
            "\n"
            "recurrent_dropout\n"
            "→ dropout applied to recurrent state transformations\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "inputs = keras.Input(shape=(120, 14))\n"
            "\n"
            "x = layers.LSTM(\n"
            "    32,\n"
            "    recurrent_dropout=0.25,\n"
            ")(inputs)\n"
            "\n"
            "x = layers.Dropout(0.5)(x)\n"
            "outputs = layers.Dense(1)(x)\n"
            "```\n"
            "\n"
            "The chapter reports that this reduces early overfitting and "
            "improves performance relative to the initial LSTM.\n"
            "\n"
            "### More capacity after regularization\n"
            "\n"
            "Once overfitting is controlled, increasing capacity may help.\n"
            "\n"
            "Two common approaches are:\n"
            "\n"
            "```text\n"
            "increase units\n"
            "or\n"
            "add recurrent layers\n"
            "```\n"
            "\n"
            "### Stacking recurrent layers\n"
            "\n"
            "Suppose you want:\n"
            "\n"
            "```text\n"
            "GRU layer\n"
            "    ↓\n"
            "GRU layer\n"
            "    ↓\n"
            "regression output\n"
            "```\n"
            "\n"
            "The first recurrent layer must return the entire sequence:\n"
            "\n"
            "```python\n"
            "inputs = keras.Input(shape=(120, 14))\n"
            "\n"
            "x = layers.GRU(\n"
            "    32,\n"
            "    recurrent_dropout=0.5,\n"
            "    return_sequences=True,\n"
            ")(inputs)\n"
            "\n"
            "x = layers.GRU(\n"
            "    32,\n"
            "    recurrent_dropout=0.5,\n"
            ")(x)\n"
            "\n"
            "x = layers.Dropout(0.5)(x)\n"
            "outputs = layers.Dense(1)(x)\n"
            "```\n"
            "\n"
            "Why `return_sequences=True` in the first layer?\n"
            "\n"
            "Because the second GRU expects:\n"
            "\n"
            "```text\n"
            "(batch, timesteps, features)\n"
            "```\n"
            "\n"
            "not just one final vector.\n"
            "\n"
            "### GRU\n"
            "\n"
            "A **Gated Recurrent Unit**, or GRU, is related to LSTM but uses a "
            "somewhat simpler recurrent architecture.\n"
            "\n"
            "Both LSTM and GRU are designed to handle sequence dependencies "
            "better than a naive SimpleRNN.\n"
            "\n"
            "The chapter's stacked GRU model achieves approximately:\n"
            "\n"
            "```text\n"
            "test MAE ≈ 2.39°C\n"
            "```\n"
            "\n"
            "This is an improvement over the original baseline, although the "
            "gain from adding extra recurrent capacity is not dramatic.\n"
            "\n"
            "That illustrates an important lesson:\n"
            "\n"
            "> More complex models do not automatically produce proportionally "
            "better results.\n"
            "\n"
            "### Runtime considerations\n"
            "\n"
            "Small RNNs may run efficiently on CPUs because their matrix "
            "operations are relatively small and recurrent loops limit "
            "parallelism.\n"
            "\n"
            "Larger recurrent models can benefit more from GPUs.\n"
            "\n"
            "The source also notes that certain optimized GPU kernels support "
            "only particular RNN configurations.\n"
            "\n"
            "For example, recurrent dropout may force execution away from a "
            "highly optimized recurrent GPU kernel.\n"
            "\n"
            "So architecture decisions can affect both model quality and runtime.\n"
            "\n"
            "### Bidirectional RNNs\n"
            "\n"
            "A standard RNN reads a sequence in one direction:\n"
            "\n"
            "```text\n"
            "oldest → newest\n"
            "```\n"
            "\n"
            "A bidirectional RNN uses two recurrent networks:\n"
            "\n"
            "```text\n"
            "forward RNN:\n"
            "oldest → newest\n"
            "\n"
            "backward RNN:\n"
            "newest → oldest\n"
            "```\n"
            "\n"
            "Their representations are then combined.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "          sequence\n"
            "          ↙      ↘\n"
            " forward RNN    backward RNN\n"
            "          ↘      ↙\n"
            "       merged representation\n"
            "```\n"
            "\n"
            "In Keras:\n"
            "\n"
            "```python\n"
            "x = layers.Bidirectional(\n"
            "    layers.LSTM(16)\n"
            ")(inputs)\n"
            "```\n"
            "\n"
            "### Why bidirectional is not better here\n"
            "\n"
            "For temperature forecasting, chronological direction contains "
            "important information.\n"
            "\n"
            "The most recent observations are more predictive of tomorrow than "
            "measurements from several days earlier.\n"
            "\n"
            "Reading the sequence backward puts the least recent information "
            "closest to the end of the recurrent computation.\n"
            "\n"
            "The chapter therefore finds that bidirectional processing does "
            "not improve this forecasting problem.\n"
            "\n"
            "It also doubles recurrent capacity, which can make overfitting "
            "happen sooner.\n"
            "\n"
            "### When bidirectional RNNs can help\n"
            "\n"
            "They are more useful when:\n"
            "\n"
            "```text\n"
            "order matters\n"
            "but\n"
            "one particular direction is not inherently privileged\n"
            "```\n"
            "\n"
            "The chapter gives natural language as an example where "
            "bidirectional sequence representations can be valuable.\n"
            "\n"
            "### Architecture should match the data\n"
            "\n"
            "The progression of experiments demonstrates a broader lesson:\n"
            "\n"
            "```text\n"
            "Dense model\n"
            "→ loses explicit temporal structure\n"
            "\n"
            "Conv1D\n"
            "→ assumes reusable local temporal patterns\n"
            "→ pooling can discard order\n"
            "\n"
            "RNN / LSTM / GRU\n"
            "→ explicitly maintains temporal state\n"
            "→ better suited when sequence order matters strongly\n"
            "```\n"
            "\n"
            "The model family should reflect the structure of the problem.\n"
            "\n"
            "### There is always a limit to predictability\n"
            "\n"
            "The source points out that this temperature dataset contains "
            "measurements from only one geographic location.\n"
            "\n"
            "Weather at that location also depends on conditions in surrounding "
            "areas that the model does not observe.\n"
            "\n"
            "No architecture can recover information that is absent from the "
            "input data.\n"
            "\n"

            # Exercise EX02 is rendered here by the frontend.
            "{{exercise:M13.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> Timeseries data can always be randomly shuffled before splitting "
            "into training and test sets.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Forecasting is meant to learn from the past and predict the future. "
            "Validation and test periods should therefore represent later time "
            "periods than the training set.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> A sophisticated neural network is automatically better than a "
            "simple heuristic.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter's naive temperature baseline is difficult for simple "
            "machine learning models to beat. Complex models should justify "
            "their additional complexity by outperforming meaningful baselines.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Flattening a timeseries preserves temporal structure because all "
            "the numerical values are still present.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The values remain present, but the architecture no longer models "
            "the sequence explicitly as ordered recurrent information.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> An RNN stores every previous input exactly.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "An RNN maintains a learned internal state. That state is a "
            "compressed representation derived from previous inputs, not a "
            "perfect copy of the complete history.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> `return_sequences=True` always improves an RNN.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "It controls the output format. It is required for an intermediate "
            "recurrent layer when another recurrent layer follows, but a final "
            "forecasting layer may only need the last recurrent output.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Bidirectional RNNs are always stronger than unidirectional RNNs.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "For causal forecasting, chronological direction may contain more "
            "useful information than reverse processing. The chapter's "
            "temperature experiment performs worse with bidirectional processing.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> If an RNN cannot predict something accurately, a larger RNN "
            "will always solve the problem.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Prediction is limited by the information contained in the input "
            "data. Missing external variables cannot be created by model capacity.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Timeseries | Measurements ordered through time |\n"
            "| Forecasting | Predicting future values from previous observations |\n"
            "| Timestep | One position in a temporal sequence |\n"
            "| Periodicity | Pattern that repeats over regular time intervals |\n"
            "| Sequence window | Consecutive timesteps used as one model input |\n"
            "| Delay | Temporal distance between the input sequence and prediction target |\n"
            "| Baseline | Simple reference method that a learned model should beat |\n"
            "| MAE | Mean absolute error, average absolute distance between prediction and target |\n"
            "| MSE | Mean squared error, average squared prediction error |\n"
            "| Feedforward network | Network without persistent recurrent state across sequence steps |\n"
            "| RNN | Neural network that processes sequences while maintaining an internal state |\n"
            "| Recurrent state | Learned representation carrying information from earlier timesteps |\n"
            "| SimpleRNN | Basic recurrent neural-network layer |\n"
            "| LSTM | Recurrent architecture designed to preserve useful information across longer temporal distances |\n"
            "| GRU | Gated recurrent architecture related to LSTM with a simpler structure |\n"
            "| Carry state | LSTM information pathway used to transport information through time |\n"
            "| Vanishing gradient | Weakening of gradient information across long computational chains |\n"
            "| return_sequences | Setting controlling whether a recurrent layer returns every timestep output or only the final output |\n"
            "| Recurrent dropout | Dropout applied to recurrent computations with a mask consistent through time |\n"
            "| Stacked RNN | Model containing multiple recurrent layers |\n"
            "| Bidirectional RNN | Model processing a sequence in both forward and reverse directions |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What makes timeseries fundamentally different from ordinary independent samples?\n"
            "2. Why should forecasting train/validation/test splits preserve chronological order?\n"
            "3. Why must feature normalization statistics come only from the training period?\n"
            "4. What does an input shape of `(256, 120, 14)` mean?\n"
            "5. Why should a commonsense baseline be built before a complex model?\n"
            "6. Why can flattening a timeseries be a poor architecture choice?\n"
            "7. Why did the tested Conv1D model struggle with the weather data?\n"
            "8. What is the internal state of an RNN?\n"
            "9. How is an RNN different from a feedforward network?\n"
            "10. What problem limits SimpleRNN on long dependencies?\n"
            "11. What is the main purpose of the LSTM carry pathway?\n"
            "12. What is the difference between `return_sequences=False` and `True`?\n"
            "13. Why must an intermediate recurrent layer return sequences when stacking RNNs?\n"
            "14. What is recurrent dropout designed to help with?\n"
            "15. How is GRU related to LSTM?\n"
            "16. Why did bidirectional LSTM not improve this temperature forecasting task?\n"
            "17. Why can adding more recurrent layers eventually produce diminishing returns?\n"
            "18. Why can no model compensate completely for missing predictive information?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Timeseries modeling is about preserving and exploiting temporal "
            "structure. Start with a meaningful baseline, prepare windows without "
            "leaking future information, and use an architecture whose inductive "
            "bias matches the importance of order. RNNs maintain state across "
            "timesteps, while LSTM and GRU improve the ability to preserve useful "
            "information over longer sequences.**\n"
            "\n"
            "Keep this progression in mind:\n"
            "\n"
            "```text\n"
            "TIMESERIES\n"
            "   ↓\n"
            "preserve chronological order\n"
            "   ↓\n"
            "normalize from training period only\n"
            "   ↓\n"
            "build sliding windows\n"
            "   ↓\n"
            "establish commonsense baseline\n"
            "   ↓\n"
            "try simple model\n"
            "   ↓\n"
            "use recurrent model when order matters\n"
            "   ↓\n"
            "LSTM / GRU\n"
            "   ↓\n"
            "regularize with recurrent dropout\n"
            "   ↓\n"
            "stack only when more capacity is justified\n"
            "```\n"
        ),

        "estimated_minutes": 150,

        "has_code_examples": True,

        "sections": [
            {
                "id": "timeseries-foundations",
                "title": "Understanding Timeseries and Forecasting",
                "order": 1,
            },
            {
                "id": "forecasting-baselines",
                "title": "Baselines Before Recurrent Neural Networks",
                "order": 2,
            },
            {
                "id": "rnn-lstm",
                "title": "Recurrent Neural Networks and LSTM",
                "order": 3,
            },
            {
                "id": "advanced-rnn",
                "title": "Getting More from Recurrent Networks",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M13.L01.EX01",

            "title": "Design a Forecasting Dataset and Baseline",

            "lesson_code": "M13.L01",

            "section_id": "forecasting-baselines",

            "placement": "after_section",

            "description": (
                "Practice preparing chronological data, creating sequence "
                "windows, choosing a baseline, and deciding whether a simple "
                "model preserves the information needed for forecasting."
            ),

            "instructions": (
                "Imagine you have hourly electricity-demand measurements plus "
                "weather features covering three years.\n\n"
                "1. Explain how you would split the data into training, "
                "validation, and test periods.\n"
                "2. Explain why randomly mixing future and past samples across "
                "these splits could be misleading.\n"
                "3. Suppose you use the previous 7 days to predict demand "
                "24 hours ahead. How many hourly timesteps are in each input?\n"
                "4. If each timestep contains 10 features, state the shape of "
                "one sample.\n"
                "5. Propose one commonsense forecasting baseline.\n"
                "6. Explain why the learned model must beat that baseline.\n"
                "7. Explain one disadvantage of flattening the 7-day sequence "
                "before giving it to a Dense model.\n"
                "8. Explain whether a Conv1D model would automatically be a "
                "good choice and what assumption you would need to verify."
            ),

            "expected_output": (
                "A short forecasting design that includes chronological data "
                "splits, window dimensions, a baseline, and reasoning about "
                "Dense versus temporal convolution models."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "timeseries-splitting",
                "sequence-windowing",
                "forecasting-baselines",
                "temporal-order",
                "architecture-selection",
            ],
        },

        {
            "id": "M13.L01.EX02",

            "title": "Build the Right Recurrent Architecture",

            "lesson_code": "M13.L01",

            "section_id": "advanced-rnn",

            "placement": "after_section",

            "description": (
                "Practice choosing and configuring recurrent layers for a "
                "sequence forecasting task."
            ),

            "instructions": (
                "You need to forecast a continuous value from a sequence of "
                "96 timesteps with 8 features per timestep.\n\n"
                "1. State the model input shape excluding the batch dimension.\n"
                "2. Explain why an LSTM or GRU may be preferable to flattening "
                "the sequence.\n"
                "3. Write a conceptual single-layer LSTM model with a scalar "
                "regression output.\n"
                "4. Explain why the output Dense layer should not use sigmoid "
                "for an unrestricted continuous target.\n"
                "5. Add recurrent dropout conceptually and explain its purpose.\n"
                "6. Now stack two GRU layers. State which layer needs "
                "`return_sequences=True` and explain why.\n"
                "7. Explain when adding the second recurrent layer would be "
                "justified.\n"
                "8. Decide whether a bidirectional RNN makes sense when the "
                "most recent timesteps are much more predictive than old ones.\n"
                "9. Explain why increasing model size cannot recover external "
                "predictive variables that are absent from the dataset."
            ),

            "expected_output": (
                "A recurrent model design plus explanations of LSTM/GRU state, "
                "return_sequences, recurrent dropout, model capacity, "
                "bidirectionality, and limits imposed by the available data."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "rnn-design",
                "lstm",
                "gru",
                "return-sequences",
                "recurrent-dropout",
                "bidirectional-rnn",
                "model-capacity",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M13.L01.QZ01",

        "title": "Timeseries Forecasting and Recurrent Neural Networks — Knowledge Check",

        "lesson_code": "M13.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M13.L01.Q01",

                "section_id": "timeseries-foundations",

                "question": (
                    "Why should validation and test periods generally come "
                    "after the training period in a forecasting problem?"
                ),

                "options": [
                    "Because recurrent networks cannot read old data",
                    "Because forecasting should simulate learning from the past and predicting later unseen data",
                    "Because normalization only works when data is sorted",
                    "Because test datasets must always contain more samples than training datasets",
                ],

                "correct": 1,

                "explanation": (
                    "Forecasting is inherently temporal. The evaluation setup "
                    "should imitate the real task: learn from earlier data and "
                    "predict later data without using information from the future."
                ),
            },

            {
                "id": "M13.L01.Q02",

                "section_id": "forecasting-baselines",

                "question": (
                    "What is the main purpose of evaluating a simple "
                    "commonsense baseline before training a complex model?"
                ),

                "options": [
                    "To replace the validation set",
                    "To guarantee that an RNN will converge",
                    "To establish a minimum useful performance level the learned model should beat",
                    "To increase the amount of training data",
                ],

                "correct": 2,

                "explanation": (
                    "A baseline gives context to the model's score. A complex "
                    "model that cannot beat a sensible simple heuristic has not "
                    "demonstrated that its extra complexity is useful."
                ),
            },

            {
                "id": "M13.L01.Q03",

                "section_id": "rnn-lstm",

                "question": (
                    "What distinguishes an RNN from a standard feedforward "
                    "network when processing a sequence?"
                ),

                "options": [
                    "An RNN maintains an internal state that is updated as it processes timesteps",
                    "An RNN never uses learned weights",
                    "An RNN can only accept one numerical feature",
                    "An RNN always processes all timesteps simultaneously",
                ],

                "correct": 0,

                "explanation": (
                    "The defining idea of recurrence is that information from "
                    "earlier timesteps is carried forward through an internal "
                    "state and influences later computations."
                ),
            },

            {
                "id": "M13.L01.Q04",

                "section_id": "advanced-rnn",

                "question": (
                    "Why should the first layer in a two-layer recurrent stack "
                    "usually use `return_sequences=True`?"
                ),

                "options": [
                    "To convert the sequence into an image",
                    "To increase the learning rate automatically",
                    "To provide the next recurrent layer with an output sequence rather than only one final vector",
                    "To prevent the model from learning temporal patterns",
                ],

                "correct": 2,

                "explanation": (
                    "A recurrent layer expects a sequence-shaped input. "
                    "`return_sequences=True` makes the intermediate layer return "
                    "one output per timestep so another recurrent layer can "
                    "process the sequence."
                ),
            },

            {
                "id": "M13.L01.Q05",

                "section_id": "advanced-rnn",

                "type": "open",

                "question": (
                    "You receive a new timeseries forecasting problem. Describe "
                    "a complete modeling strategy based on this lesson: how you "
                    "would split and normalize the data, form training windows, "
                    "create a baseline, test a simple model, decide whether an "
                    "RNN is justified, choose between LSTM or GRU, control "
                    "overfitting, and determine whether stacking or "
                    "bidirectional processing is appropriate."
                ),
            },
        ],

        "passing_score": 70,
    },
}
