"""M05.L01 — Feature Engineering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-XXX, Chapter 5, pages not provided in source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "Feature Engineering for Machine Learning Systems"

MODULE_DESCRIPTION = (
    "Learn how to turn raw data into useful model inputs while handling missing "
    "values, scaling, categorical variables, feature interactions, positional "
    "information, data leakage, feature importance, and generalization."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Feature Engineering",

    "slug": "ml-systems-design-m05-l01",

    "description": (
        "A production-focused introduction to feature engineering, including "
        "learned versus handcrafted features, missing-value strategies, scaling, "
        "discretization, categorical encoding, feature crossing, positional "
        "embeddings, data leakage, feature importance, and feature generalization."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.25,

    "skill_tags": [
        "feature-engineering",
        "learned-features",
        "missing-values",
        "imputation",
        "scaling",
        "standardization",
        "log-transform",
        "discretization",
        "categorical-encoding",
        "feature-hashing",
        "feature-crossing",
        "embeddings",
        "positional-embeddings",
        "data-leakage",
        "feature-importance",
        "shap",
        "feature-generalization",
    ],

    "prerequisite_ids": ["M04.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Feature Engineering",

        "content": (
            "# Feature Engineering\n"
            "\n"
            "> **Lesson:** M05.L01  \n"
            "> **Module:** Feature Engineering for Machine Learning Systems  \n"
            "> **Source alignment:** Chapter 5. Page numbers were not included "
            "in the supplied source. This lesson is an instructor-authored "
            "curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the difference between learned and engineered features.\n"
            "- Identify common feature sources beyond raw text or images.\n"
            "- Distinguish MNAR, MAR, and MCAR missingness.\n"
            "- Compare deletion and imputation strategies for missing values.\n"
            "- Explain feature scaling, standardization, and log transformation.\n"
            "- Explain discretization and its trade-offs.\n"
            "- Handle changing categorical vocabularies with an UNKNOWN category "
            "or feature hashing.\n"
            "- Explain feature crossing and why it can model interactions.\n"
            "- Explain embeddings and positional embeddings at a conceptual level.\n"
            "- Define data leakage and identify its common causes.\n"
            "- Apply practical leakage-prevention rules during splitting and preprocessing.\n"
            "- Use feature importance and feature generalization as two criteria "
            "for judging whether a feature is useful.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Learned features versus engineered features\n"
            "\n"
            "Feature engineering is the process of deciding **what information a "
            "model should use** and converting that information into a form the "
            "model can learn from.\n"
            "\n"
            "Modern deep learning can automatically learn many useful representations, "
            "which is why deep learning is sometimes described as **feature learning**.\n"
            "\n"
            "For example, older NLP pipelines often required manually designed text "
            "processing steps such as:\n"
            "\n"
            "- lowercasing,\n"
            "- punctuation removal,\n"
            "- lemmatization,\n"
            "- contraction expansion,\n"
            "- n-gram extraction.\n"
            "\n"
            "An **n-gram** is a contiguous sequence of `n` items.\n"
            "\n"
            "For the sentence:\n"
            "\n"
            "```text\n"
            "I like food\n"
            "```\n"
            "\n"
            "Word-level 1-grams are:\n"
            "\n"
            "```text\n"
            "I, like, food\n"
            "```\n"
            "\n"
            "Word-level 2-grams are:\n"
            "\n"
            "```text\n"
            "I like, like food\n"
            "```\n"
            "\n"
            "A classical model could then represent the sentence using counts over "
            "a vocabulary of such n-grams.\n"
            "\n"
            "Deep models reduce the need for many handcrafted text and image "
            "features, but they do **not** eliminate feature engineering completely.\n"
            "\n"
            "A spam-detection model, for example, may benefit from information beyond "
            "the comment text itself:\n"
            "\n"
            "- number of upvotes or downvotes,\n"
            "- age of the user's account,\n"
            "- posting frequency,\n"
            "- historical user reputation,\n"
            "- popularity of the thread,\n"
            "- contextual information about where the comment appears.\n"
            "\n"
            "These are not automatically contained in the raw text. Someone still "
            "has to decide whether they matter and how to represent them.\n"
            "\n"
            "[[IMAGE_NEEDED: Learned versus engineered features | "
            "A two-part diagram showing raw text/image going directly into a deep "
            "model that learns representations, alongside contextual metadata such "
            "as user, thread, and behavioral information being explicitly engineered "
            "into features | Learner should notice that representation learning "
            "reduces but does not eliminate feature engineering]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Missing values are not all the same\n"
            "\n"
            "Missing data is common in production, but the *reason* a value is "
            "missing matters.\n"
            "\n"
            "The chapter describes three types.\n"
            "\n"
            "### Missing Not At Random (MNAR)\n"
            "\n"
            "The value is missing for a reason related to the missing value itself.\n"
            "\n"
            "Example: high-income respondents may be less willing to disclose income. "
            "In that case, missingness itself contains information about income.\n"
            "\n"
            "### Missing At Random (MAR)\n"
            "\n"
            "The value is missing because of another observed variable.\n"
            "\n"
            "Example: age might be missing more often for one demographic group.\n"
            "\n"
            "### Missing Completely At Random (MCAR)\n"
            "\n"
            "There is no apparent pattern in the missingness.\n"
            "\n"
            "Example: people sometimes forget to enter a field for no systematic reason.\n"
            "\n"
            "The chapter stresses that MCAR is relatively rare; missingness often has a cause.\n"
            "\n"
            "[[IMAGE_NEEDED: MNAR versus MAR versus MCAR | "
            "Three small panels showing missing income caused by income itself, "
            "missing age explained by another observed group variable, and random "
            "missing job values with no visible pattern | Learner should notice that "
            "the mechanism causing missingness affects how safely data can be removed or imputed]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Deletion versus imputation\n"
            "\n"
            "There are two broad responses to missing values:\n"
            "\n"
            "1. remove affected rows or columns,\n"
            "2. fill missing values using imputation.\n"
            "\n"
            "### Column deletion\n"
            "\n"
            "If a feature has many missing values, you might remove the entire feature.\n"
            "\n"
            "This is simple but can discard important predictive information. A field "
            "with high missingness may still matter strongly to the target.\n"
            "\n"
            "### Row deletion\n"
            "\n"
            "You can drop examples containing missing values.\n"
            "\n"
            "The chapter suggests this is most defensible when missingness is MCAR "
            "and the affected fraction is very small.\n"
            "\n"
            "If missingness is MAR or MNAR, deleting rows can introduce bias or "
            "remove information encoded in the missingness itself.\n"
            "\n"
            "### Imputation\n"
            "\n"
            "Imputation fills missing values with a chosen replacement.\n"
            "\n"
            "Common choices include:\n"
            "\n"
            "- default values,\n"
            "- mean,\n"
            "- median,\n"
            "- mode,\n"
            "- values conditioned on another variable, such as median July temperature.\n"
            "\n"
            "However, careless imputation can create subtle bugs.\n"
            "\n"
            "If missing age is filled with `0`, but age `0` is also a valid value or "
            "never appeared during training, the model may interpret the replacement incorrectly.\n"
            "\n"
            "A useful principle from the chapter is:\n"
            "\n"
            "> Avoid using a normal valid value as the missing-value marker when that "
            "would make real and missing values indistinguishable.\n"
            "\n"
            "There is no perfect universal solution. Deletion can remove signal and "
            "create bias; imputation can inject assumptions, noise, or leakage.\n"
            "\n"
            "{{exercise:M05.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Scaling, standardization, and skewed features\n"
            "\n"
            "Suppose one feature ranges from 20 to 40 and another from 10,000 to 150,000.\n"
            "\n"
            "Many models work better when numerical features have comparable scales. "
            "The chapter presents feature scaling as a common preprocessing step.\n"
            "\n"
            "### Min-max scaling\n"
            "\n"
            "To scale a value `x` into `[0, 1]`:\n"
            "\n"
            "```text\n"
            "x_scaled = (x - x_min) / (x_max - x_min)\n"
            "```\n"
            "\n"
            "The minimum becomes 0 and the maximum becomes 1.\n"
            "\n"
            "### Scaling to an arbitrary range\n"
            "\n"
            "The same idea can map data to another range such as `[-1, 1]`.\n"
            "\n"
            "### Standardization\n"
            "\n"
            "If a feature is treated as approximately normal, it can be standardized:\n"
            "\n"
            "```text\n"
            "z = (x - mean) / standard_deviation\n"
            "```\n"
            "\n"
            "This gives the transformed feature approximately zero mean and unit variance.\n"
            "\n"
            "### Log transformation\n"
            "\n"
            "Highly skewed features can be difficult for models. Applying a logarithmic "
            "transformation can sometimes reduce skewness.\n"
            "\n"
            "However, the transformed values should still be interpreted carefully: "
            "analysis performed in log space is not identical to analysis on the "
            "original scale.\n"
            "\n"
            "### Production warning\n"
            "\n"
            "Scaling requires statistics such as min, max, mean, or standard deviation. "
            "These statistics must come from the **training split only** and then be "
            "reused during inference.\n"
            "\n"
            "If production data shifts substantially, old scaling statistics may "
            "become less representative.\n"
            "\n"
            "[[IMAGE_NEEDED: Scaling and standardization comparison | "
            "A skewed or differently scaled pair of numerical features shown before "
            "and after min-max scaling and standardization | Learner should notice "
            "that the transformation changes numerical scale while preserving the "
            "underlying examples]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Discretization: turning continuous values into buckets\n"
            "\n"
            "**Discretization**, also called binning or quantization, converts a "
            "continuous feature into discrete categories.\n"
            "\n"
            "Example income buckets:\n"
            "\n"
            "```text\n"
            "Lower:  < 35,000\n"
            "Middle: 35,000 to 100,000\n"
            "Upper:  > 100,000\n"
            "```\n"
            "\n"
            "This can make a problem easier when data is limited because the model "
            "learns a smaller number of categories instead of many individual values.\n"
            "\n"
            "But discretization introduces sharp boundaries. For example, 34,999 "
            "and 35,000 become different categories even though they are almost identical, "
            "while 35,000 and 100,000 may share one category.\n"
            "\n"
            "Choosing boundaries therefore requires judgment. The chapter suggests "
            "common sense, quantiles, histograms, and domain expertise as useful guides.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Encoding changing categorical features\n"
            "\n"
            "Categorical variables seem simple until their vocabulary changes in production.\n"
            "\n"
            "Suppose a recommender uses **brand** as a feature. During training, you "
            "encode every known brand as an integer. In production, a new brand appears.\n"
            "\n"
            "If the encoder has no representation for it, the pipeline may fail.\n"
            "\n"
            "### UNKNOWN category\n"
            "\n"
            "A common solution is to map unseen categories into an `UNKNOWN` bucket.\n"
            "\n"
            "But this creates another problem: if `UNKNOWN` never appeared during "
            "training, the model has not learned how to treat it.\n"
            "\n"
            "A practical approach described in the chapter is to map a small tail of "
            "rare training categories into `UNKNOWN` as well, so the model learns "
            "some behavior for that bucket.\n"
            "\n"
            "Even then, all unseen categories collapse into the same representation, "
            "even though they may be very different.\n"
            "\n"
            "### Feature hashing\n"
            "\n"
            "The **hashing trick** maps categories into a fixed-size hash space.\n"
            "\n"
            "For an 18-bit hash space:\n"
            "\n"
            "```text\n"
            "2^18 = 262,144 possible indices\n"
            "```\n"
            "\n"
            "Every category—including unseen categories—can be mapped into that space.\n"
            "\n"
            "The trade-off is **collision**: two categories can map to the same index.\n"
            "\n"
            "A larger hash space reduces collisions. The chapter also notes that "
            "random collisions may be less systematically harmful than forcing all "
            "new categories into a single UNKNOWN bucket.\n"
            "\n"
            "[[IMAGE_NEEDED: UNKNOWN bucket versus feature hashing | "
            "A categorical stream with old and new brands, showing one approach "
            "mapping all unseen brands to UNKNOWN and another hashing every brand "
            "into a fixed index space with occasional collisions | Learner should "
            "notice why hashing handles open-ended vocabularies more gracefully]]\n"
            "\n"
            "{{exercise:M05.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Feature crossing and interactions\n"
            "\n"
            "**Feature crossing** combines two or more features to create a new feature.\n"
            "\n"
            "Suppose house-buying behavior depends not only on marital status or "
            "number of children individually, but on their combination.\n"
            "\n"
            "You can create:\n"
            "\n"
            "```text\n"
            "marital_status = Married\n"
            "children = 2\n"
            "\n"
            "crossed_feature = Married_2\n"
            "```\n"
            "\n"
            "Feature crosses explicitly expose interactions that simpler models may "
            "otherwise fail to learn well.\n"
            "\n"
            "The chapter notes that explicit crossing is especially useful for models "
            "that are weak at learning nonlinear interactions, though it can still "
            "help neural networks in some settings.\n"
            "\n"
            "### The combinatorial cost\n"
            "\n"
            "If feature A has 100 possible values and feature B has 100 possible values:\n"
            "\n"
            "```text\n"
            "100 × 100 = 10,000 possible crossed values\n"
            "```\n"
            "\n"
            "That expands the feature space, increases the amount of data required, "
            "and can increase overfitting risk.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Embeddings and positional information\n"
            "\n"
            "An **embedding** is a vector representation of a piece of data.\n"
            "\n"
            "Words are a familiar example, but embeddings can also represent:\n"
            "\n"
            "- products,\n"
            "- users,\n"
            "- images,\n"
            "- graph entities,\n"
            "- queries.\n"
            "\n"
            "All vectors in one embedding space have the same dimensionality.\n"
            "\n"
            "### Why position matters\n"
            "\n"
            "A sequence model must know order.\n"
            "\n"
            "The sentences:\n"
            "\n"
            "```text\n"
            "a dog bites a child\n"
            "a child bites a dog\n"
            "```\n"
            "\n"
            "contain similar words but mean very different things because the positions differ.\n"
            "\n"
            "Recurrent models process tokens sequentially, so order is naturally "
            "present in the computation. Transformer-style processing is parallel, "
            "so positional information must be injected explicitly.\n"
            "\n"
            "### Learned positional embeddings\n"
            "\n"
            "One approach assigns each position its own learnable vector. The token "
            "embedding and position embedding can be combined so the model receives "
            "both identity and location information.\n"
            "\n"
            "### Fixed positional embeddings\n"
            "\n"
            "Another approach uses predefined sine and cosine functions to generate "
            "a position representation.\n"
            "\n"
            "The chapter connects these ideas to **Fourier features**, which can "
            "also represent continuous coordinates such as positions on a 3D surface.\n"
            "\n"
            "[[IMAGE_NEEDED: Token embeddings plus positional embeddings | "
            "A short token sequence with one vector per token and one vector per "
            "position, followed by element-wise combination before the model | "
            "Learner should notice that token identity and token order are supplied "
            "as separate signals]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Data leakage: when the model learns information it should not have\n"
            "\n"
            "**Data leakage** occurs when information related to the target leaks "
            "into the features or training process in a way that will not be "
            "available during real inference.\n"
            "\n"
            "Leakage is especially dangerous because evaluation can look excellent "
            "while production performance fails.\n"
            "\n"
            "### Hospital-scan example\n"
            "\n"
            "Suppose a hospital sends patients suspected of cancer to a special scan "
            "machine. A model trained on those scans may learn the machine's visual "
            "signature instead of the disease itself.\n"
            "\n"
            "It performs well on data from the same hospital because machine choice "
            "is correlated with diagnosis. At another hospital where machine choice "
            "does not encode that decision, performance collapses.\n"
            "\n"
            "The model learned a shortcut unavailable or invalid at deployment.\n"
            "\n"
            "Other examples described in the chapter include patient position or "
            "hospital-specific text fonts accidentally revealing clinical severity.\n"
            "\n"
            "[[IMAGE_NEEDED: Data leakage shortcut example | "
            "Training images where hospital or scanner artifacts correlate with the "
            "target, followed by deployment images where that artifact-target link "
            "disappears | Learner should notice that the model learned a shortcut "
            "rather than the intended medical signal]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Common causes of data leakage\n"
            "\n"
            "### 1. Randomly splitting time-correlated data\n"
            "\n"
            "If data is time-correlated, random splitting can leak future conditions "
            "into training.\n"
            "\n"
            "For a forecasting problem, train on earlier periods and evaluate on later periods.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Week 1 ─┐\n"
            "Week 2  │\n"
            "Week 3  ├── Training\n"
            "Week 4 ─┘\n"
            "Week 5 ─── Validation / Test\n"
            "```\n"
            "\n"
            "This better reflects the real deployment condition: predict the future "
            "using information from the past.\n"
            "\n"
            "### 2. Scaling before splitting\n"
            "\n"
            "If mean, variance, minimum, or maximum are calculated using the full "
            "data before splitting, information from validation/test examples leaks "
            "into preprocessing.\n"
            "\n"
            "Correct order:\n"
            "\n"
            "```text\n"
            "Split first\n"
            "   ↓\n"
            "Fit scaler on train only\n"
            "   ↓\n"
            "Apply train statistics to train/validation/test\n"
            "```\n"
            "\n"
            "### 3. Imputing using test statistics\n"
            "\n"
            "The same principle applies to missing-value imputation. Compute means, "
            "medians, or other imputation statistics from the training split only.\n"
            "\n"
            "### 4. Duplicates across splits\n"
            "\n"
            "If duplicates or near-duplicates appear in both train and test data, "
            "evaluation can reward memorization.\n"
            "\n"
            "Check for duplicates before splitting and again afterward. If you "
            "oversample, do it **after** splitting.\n"
            "\n"
            "### 5. Group leakage\n"
            "\n"
            "Highly related examples should not be scattered across splits.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- two scans from the same patient,\n"
            "- nearly identical video frames,\n"
            "- repeated observations from one entity.\n"
            "\n"
            "If one correlated example is in training and another is in testing, "
            "the test result may be overly optimistic.\n"
            "\n"
            "### 6. Leakage from the data-generation process\n"
            "\n"
            "The scanner example is a data-generation leak. Detecting this kind of "
            "problem requires understanding how the data was collected and processed.\n"
            "\n"
            "This is why subject-matter experts and data lineage are important.\n"
            "\n"
            "[[IMAGE_NEEDED: Leakage-safe preprocessing pipeline | "
            "A diagram showing deduplication/group handling and time-aware splitting "
            "before fitting imputation/scaling on train only, then applying those "
            "transformations to validation and test | Learner should notice that "
            "test information must never influence fitted preprocessing steps]]\n"
            "\n"
            "{{exercise:M05.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Detecting suspicious features and leakage\n"
            "\n"
            "There is no universal detector for leakage, so teams need several checks.\n"
            "\n"
            "### Inspect unusually predictive features\n"
            "\n"
            "If a feature has unexpectedly strong correlation with the target, ask:\n"
            "\n"
            "- How was it generated?\n"
            "- Was it available at prediction time?\n"
            "- Could it indirectly contain target information?\n"
            "\n"
            "Sometimes leakage emerges only from a **combination** of features.\n"
            "\n"
            "### Run ablation studies\n"
            "\n"
            "Remove a feature or feature group and measure the performance change.\n"
            "\n"
            "If removing one feature causes an unexpectedly large collapse, investigate "
            "why that feature is so powerful.\n"
            "\n"
            "### Watch new features carefully\n"
            "\n"
            "A dramatic performance jump after adding one feature can mean either:\n"
            "\n"
            "1. the feature is genuinely excellent, or\n"
            "2. the feature leaks information about the target.\n"
            "\n"
            "### Protect the test split\n"
            "\n"
            "Do not repeatedly use the test set to invent new features or tune "
            "hyperparameters. Every such use transfers information from the supposed "
            "future evaluation set into the development process.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. More features are not always better\n"
            "\n"
            "Production feature sets often grow over time, but every feature has a cost.\n"
            "\n"
            "Too many features can:\n"
            "\n"
            "- create more opportunities for leakage,\n"
            "- increase overfitting,\n"
            "- increase serving memory,\n"
            "- increase online inference latency,\n"
            "- increase pipeline maintenance burden.\n"
            "\n"
            "A useless feature becomes technical debt. If the upstream data changes, "
            "all downstream logic depending on that feature must also change.\n"
            "\n"
            "The chapter recommends evaluating features using two broad dimensions:\n"
            "\n"
            "1. **feature importance**, and\n"
            "2. **feature generalization**.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Feature importance\n"
            "\n"
            "Feature importance asks:\n"
            "\n"
            "> How much does the model depend on this feature?\n"
            "\n"
            "Some model families provide built-in feature-importance measures. The "
            "chapter also mentions model-agnostic approaches such as SHAP.\n"
            "\n"
            "A useful intuition is ablation-based:\n"
            "\n"
            "> If removing a feature causes performance to deteriorate substantially, "
            "the feature is probably important to that model.\n"
            "\n"
            "SHAP can also help explain how individual features contribute to a "
            "specific prediction, not only to global model behavior.\n"
            "\n"
            "Feature-importance analysis can reveal that a small number of features "
            "carry much of the useful predictive signal while many others contribute little.\n"
            "\n"
            "This makes importance useful for both **feature selection** and "
            "**interpretability**.\n"
            "\n"
            "[[IMAGE_NEEDED: Global versus local feature importance | "
            "A simple bar chart of global feature importance next to one individual "
            "prediction showing positive and negative feature contributions | "
            "Learner should notice that a feature can be important to the model "
            "overall and also contribute differently to individual predictions]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Feature generalization\n"
            "\n"
            "A feature can be highly predictive on training data yet fail on unseen data.\n"
            "\n"
            "The chapter suggests considering two aspects:\n"
            "\n"
            "### Coverage\n"
            "\n"
            "Coverage is the percentage of examples for which the feature is present.\n"
            "\n"
            "A feature available for only 1% of examples may have limited usefulness. "
            "But missingness can itself be informative, especially under MNAR, so "
            "coverage should not be judged blindly.\n"
            "\n"
            "Coverage can also reveal distribution mismatch. If a feature appears "
            "in 90% of training examples but only 20% of test examples, investigate "
            "the split and collection process.\n"
            "\n"
            "### Distribution of values\n"
            "\n"
            "Even 100% coverage does not guarantee generalization.\n"
            "\n"
            "Suppose you train a taxi ETA model using six days of data and test it "
            "on the seventh day.\n"
            "\n"
            "The feature `DAY_OF_WEEK` has 100% coverage, but the training values "
            "might contain Monday through Saturday while testing contains only Sunday.\n"
            "\n"
            "There is no overlap for that categorical value.\n"
            "\n"
            "By contrast, `HOUR_OF_DAY` may have good overlap across all splits and "
            "therefore generalize more naturally.\n"
            "\n"
            "### Generalization versus specificity\n"
            "\n"
            "A broader feature such as `IS_RUSH_HOUR` can generalize better than a "
            "specific exact-hour feature, but it also loses detail.\n"
            "\n"
            "Feature engineering often involves balancing these two properties.\n"
            "\n"
            "{{exercise:M05.L01.EX04}}\n"
            "\n"
            "---\n"
            "\n"

            "## Practical feature-engineering checklist\n"
            "\n"
            "The chapter closes with several production-oriented best practices:\n"
            "\n"
            "1. Prefer time-aware train/validation/test splits when time correlation matters.\n"
            "2. If oversampling, do it after splitting.\n"
            "3. Fit scaling and normalization after splitting.\n"
            "4. Use only training-split statistics for scaling and missing-value imputation.\n"
            "5. Understand how data is generated, collected, and processed.\n"
            "6. Involve domain experts when possible.\n"
            "7. Keep data lineage.\n"
            "8. Understand feature importance.\n"
            "9. Prefer features that generalize well.\n"
            "10. Remove features that no longer provide useful value.\n"
            "\n"
            "And most importantly: feature engineering is not a one-time phase. "
            "It continues as long as the production model and its data continue to evolve.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Deep learning eliminates feature engineering\n"
            "\n"
            "Deep learning automates many representation-learning tasks, but production "
            "systems still rely on contextual, behavioral, user, system, and domain features.\n"
            "\n"
            "### Misconception 2: Missing values should simply be deleted\n"
            "\n"
            "Deletion may remove useful signal or introduce bias, especially when "
            "missingness is MAR or MNAR.\n"
            "\n"
            "### Misconception 3: UNKNOWN completely solves unseen categories\n"
            "\n"
            "An UNKNOWN bucket prevents encoding failure, but the model still needs "
            "training examples for that bucket and may treat very different new "
            "categories identically.\n"
            "\n"
            "### Misconception 4: Excellent validation performance means there is no leakage\n"
            "\n"
            "Leakage can make validation look *better* precisely because the model "
            "has accidentally learned information it would not have in production.\n"
            "\n"
            "### Misconception 5: A feature with high importance is automatically a good feature\n"
            "\n"
            "A feature can be important but fail to generalize, or be important "
            "because it contains leaked information.\n"
            "\n"
            "### Misconception 6: More features always improve the model\n"
            "\n"
            "Extra features can create overfitting, leakage, memory cost, latency, "
            "and maintenance debt.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Feature engineering | Choosing and transforming information into inputs useful for ML models. |\n"
            "| Learned feature | Representation automatically learned by a model. |\n"
            "| Engineered feature | Feature deliberately constructed from raw or contextual data. |\n"
            "| n-gram | Contiguous sequence of n items such as words or characters. |\n"
            "| MNAR | Missingness caused by the missing value itself. |\n"
            "| MAR | Missingness explained by another observed variable. |\n"
            "| MCAR | Missingness with no systematic observed pattern. |\n"
            "| Imputation | Filling missing values with chosen replacements. |\n"
            "| Feature scaling | Transforming numerical features into comparable ranges. |\n"
            "| Standardization | Transforming values to approximately zero mean and unit variance. |\n"
            "| Log transformation | Applying a logarithm to reduce skewness in some distributions. |\n"
            "| Discretization | Converting continuous values into buckets or categories. |\n"
            "| Feature hashing | Hashing categories into a fixed-size index space. |\n"
            "| Hash collision | Two categories mapping to the same hashed index. |\n"
            "| Feature crossing | Combining features to expose interactions. |\n"
            "| Embedding | Fixed-length vector representation of an item. |\n"
            "| Positional embedding | Vector signal representing position in a sequence or coordinate space. |\n"
            "| Data leakage | Target-related information entering features or development in a way unavailable at inference. |\n"
            "| Group leakage | Highly correlated members of the same group appearing across train and test splits. |\n"
            "| Ablation study | Removing a feature or component to measure its contribution. |\n"
            "| Feature importance | How strongly a model depends on a feature for prediction. |\n"
            "| Feature coverage | Fraction of examples with a value for a feature. |\n"
            "| Feature generalization | Ability of a feature to remain useful on unseen data. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why does deep learning reduce but not eliminate feature engineering?\n"
            "2. What is the difference between MNAR, MAR, and MCAR?\n"
            "3. When can row deletion create bias?\n"
            "4. Why can imputing missing age with 0 be dangerous?\n"
            "5. What is the difference between min-max scaling and standardization?\n"
            "6. Why should scaling statistics come only from the training split?\n"
            "7. What information does discretization lose?\n"
            "8. Why is an UNKNOWN bucket insufficient for some open-ended categories?\n"
            "9. What trade-off does feature hashing introduce?\n"
            "10. Why can feature crossing cause overfitting?\n"
            "11. Why do transformer-style models need positional information?\n"
            "12. What is data leakage?\n"
            "13. Why can random splitting be wrong for time-correlated data?\n"
            "14. Why should duplicates be handled before splitting?\n"
            "15. How can ablation studies help detect leakage or measure importance?\n"
            "16. What is feature coverage?\n"
            "17. Why can a feature have 100% coverage and still fail to generalize?\n"
            "18. Why are unused features a form of technical debt?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A good feature is not merely predictive on yesterday's training data. "
            "It must be available at the right time, derived without leakage, useful "
            "to the model, maintainable in production, and able to generalize to "
            "the unseen data the system will actually face.**\n"
        ),

        "estimated_minutes": 195,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "learned-vs-engineered", "title": "Learned features versus engineered features", "order": 1},
            {"id": "missing-values", "title": "Missing values are not all the same", "order": 2},
            {"id": "deletion-imputation", "title": "Deletion versus imputation", "order": 3},
            {"id": "scaling", "title": "Scaling, standardization, and skewed features", "order": 4},
            {"id": "discretization", "title": "Discretization: turning continuous values into buckets", "order": 5},
            {"id": "categorical-encoding", "title": "Encoding changing categorical features", "order": 6},
            {"id": "feature-crossing", "title": "Feature crossing and interactions", "order": 7},
            {"id": "embeddings", "title": "Embeddings and positional information", "order": 8},
            {"id": "data-leakage", "title": "Data leakage: when the model learns information it should not have", "order": 9},
            {"id": "leakage-causes", "title": "Common causes of data leakage", "order": 10},
            {"id": "detecting-leakage", "title": "Detecting suspicious features and leakage", "order": 11},
            {"id": "good-features", "title": "More features are not always better", "order": 12},
            {"id": "feature-importance", "title": "Feature importance", "order": 13},
            {"id": "feature-generalization", "title": "Feature generalization", "order": 14},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",
            "title": "Reason about missing-value mechanisms",
            "lesson_code": "M05.L01",
            "section_id": "deletion-imputation",
            "placement": "after_section",
            "description": (
                "Practice distinguishing missingness mechanisms and choosing a "
                "reasonable first handling strategy."
            ),
            "instructions": (
                "For each scenario, identify whether it most closely resembles "
                "MNAR, MAR, or MCAR, and explain why:\n\n"
                "1. High-income respondents are less likely to report income.\n"
                "2. One demographic group skips the age question more often.\n"
                "3. A sensor occasionally fails at apparently random times.\n\n"
                "Then choose deletion or imputation as the safer first direction "
                "for each case and state one risk of your choice."
            ),
            "expected_output": (
                "Three classifications with explanations and a short handling "
                "recommendation plus risk for each."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "missing-data-reasoning",
                "imputation",
                "bias-awareness",
            ],
        },

        {
            "id": "M05.L01.EX02",
            "title": "Design encoding for an open-ended category",
            "lesson_code": "M05.L01",
            "section_id": "categorical-encoding",
            "placement": "after_section",
            "description": (
                "Compare UNKNOWN-category encoding with feature hashing for "
                "production categories that continually change."
            ),
            "instructions": (
                "You are building a marketplace recommender using seller ID as a "
                "categorical feature. Thousands of new sellers can appear after training.\n\n"
                "1. Explain what would go wrong with a fixed integer vocabulary only.\n"
                "2. Describe how an UNKNOWN bucket could prevent a crash.\n"
                "3. Explain one weakness of putting every unseen seller into UNKNOWN.\n"
                "4. Describe how feature hashing would work instead.\n"
                "5. State the main trade-off introduced by hashing."
            ),
            "expected_output": (
                "A concise comparison of fixed vocabulary, UNKNOWN handling, and "
                "feature hashing, including collision risk."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "categorical-encoding",
                "feature-hashing",
                "production-generalization",
            ],
        },

        {
            "id": "M05.L01.EX03",
            "title": "Find the leakage",
            "lesson_code": "M05.L01",
            "section_id": "leakage-causes",
            "placement": "after_section",
            "description": (
                "Practice spotting leakage in splitting and preprocessing workflows."
            ),
            "instructions": (
                "For each workflow, identify whether leakage exists and explain how "
                "to fix it:\n\n"
                "1. Compute mean and standard deviation on all data, then split.\n"
                "2. Randomly split daily stock-market examples when predicting the future.\n"
                "3. Oversample the minority class first, then randomly split.\n"
                "4. Put two scans from the same patient into train and test.\n"
                "5. Use the final test set repeatedly to decide which features to add."
            ),
            "expected_output": (
                "Five leakage diagnoses, each with the corrected order or split strategy."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "data-leakage",
                "train-test-splitting",
                "preprocessing-order",
            ],
        },

        {
            "id": "M05.L01.EX04",
            "title": "Judge feature importance and generalization",
            "lesson_code": "M05.L01",
            "section_id": "feature-generalization",
            "placement": "after_section",
            "description": (
                "Evaluate whether candidate features are useful beyond the training set."
            ),
            "instructions": (
                "You are building a taxi ETA model. Consider these features:\n"
                "- ride ID,\n"
                "- hour of day,\n"
                "- exact day of week when training uses Monday-Saturday and test uses Sunday,\n"
                "- rush-hour flag,\n"
                "- a feature present in only 1% of examples but strongly associated "
                "with the positive target when present.\n\n"
                "For each feature:\n"
                "1. Comment on likely generalization.\n"
                "2. Comment on coverage or value overlap where relevant.\n"
                "3. Say whether you would investigate, remove, transform, or keep it.\n"
                "4. Explain the trade-off between hour-of-day and a simpler rush-hour flag."
            ),
            "expected_output": (
                "A five-row feature review plus a short explanation of specificity "
                "versus generalization."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "feature-generalization",
                "coverage",
                "distribution-shift",
                "feature-selection",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Feature Engineering — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",
                "section_id": "learned-vs-engineered",
                "question": (
                    "Why is feature engineering still relevant when using deep learning?"
                ),
                "options": [
                    "Deep learning cannot learn any features automatically.",
                    "Production tasks often need contextual and domain information beyond raw text or images.",
                    "Feature engineering is only needed for visualization.",
                    "Deep models cannot process embeddings.",
                ],
                "correct": 1,
                "explanation": (
                    "Representation learning automates many low-level features, but "
                    "contextual and domain-specific signals still need to be selected "
                    "and represented."
                ),
            },

            {
                "id": "M05.L01.Q02",
                "section_id": "missing-values",
                "question": (
                    "Income is missing mainly because high-income respondents prefer "
                    "not to disclose it. Which missingness type best matches?"
                ),
                "options": [
                    "MCAR",
                    "MAR",
                    "MNAR",
                    "Feature hashing",
                ],
                "correct": 2,
                "explanation": (
                    "The missingness depends on the underlying income value itself, "
                    "which is MNAR."
                ),
            },

            {
                "id": "M05.L01.Q03",
                "section_id": "deletion-imputation",
                "question": (
                    "Why can filling a missing number-of-children value with 0 be dangerous?"
                ),
                "options": [
                    "Zero cannot be represented numerically.",
                    "Zero may be a valid value, making missing and genuine zero indistinguishable.",
                    "Imputation always causes leakage.",
                    "Models cannot train on integer values.",
                ],
                "correct": 1,
                "explanation": (
                    "Using a valid value as a missing marker can erase the distinction "
                    "between missingness and the real category/value."
                ),
            },

            {
                "id": "M05.L01.Q04",
                "section_id": "scaling",
                "question": (
                    "Which preprocessing order best avoids leakage when scaling?"
                ),
                "options": [
                    "Scale all data, then split.",
                    "Split first, fit scaling statistics on train, reuse them on validation/test.",
                    "Fit the scaler on the test set.",
                    "Fit a different scaler independently on every split.",
                ],
                "correct": 1,
                "explanation": (
                    "Only training data should determine fitted preprocessing "
                    "statistics."
                ),
            },

            {
                "id": "M05.L01.Q05",
                "section_id": "discretization",
                "question": (
                    "What is a major drawback of discretizing income into buckets?"
                ),
                "options": [
                    "It cannot reduce the number of distinct values.",
                    "It introduces artificial discontinuities at bucket boundaries.",
                    "It always leaks test information.",
                    "It makes every model nonlinear.",
                ],
                "correct": 1,
                "explanation": (
                    "Nearly identical values can fall into different buckets, while "
                    "very different values inside one bucket become indistinguishable."
                ),
            },

            {
                "id": "M05.L01.Q06",
                "section_id": "categorical-encoding",
                "question": (
                    "What is the main trade-off introduced by feature hashing?"
                ),
                "options": [
                    "It cannot encode unseen categories.",
                    "Different categories can collide at the same hashed index.",
                    "It requires an unlimited output space.",
                    "It eliminates categorical information entirely.",
                ],
                "correct": 1,
                "explanation": (
                    "Hashing supports a fixed-size open-ended vocabulary but allows "
                    "collisions between categories."
                ),
            },

            {
                "id": "M05.L01.Q07",
                "section_id": "feature-crossing",
                "question": (
                    "Why can feature crossing become expensive?"
                ),
                "options": [
                    "It always deletes the original features.",
                    "The number of possible combined values can grow multiplicatively.",
                    "It prevents nonlinear relationships.",
                    "It can only be used with text.",
                ],
                "correct": 1,
                "explanation": (
                    "Crossing features with many categories can create a very large "
                    "combined feature space and increase data requirements."
                ),
            },

            {
                "id": "M05.L01.Q08",
                "section_id": "embeddings",
                "question": (
                    "Why do transformer-style sequence models need positional information?"
                ),
                "options": [
                    "Because all words have identical embeddings.",
                    "Because parallel token processing does not by itself encode token order.",
                    "Because positions replace token embeddings.",
                    "Because positional embeddings are labels.",
                ],
                "correct": 1,
                "explanation": (
                    "A transformer processes tokens in parallel, so order must be "
                    "provided explicitly."
                ),
            },

            {
                "id": "M05.L01.Q09",
                "section_id": "data-leakage",
                "question": (
                    "A hospital model learns which scanner was used because sicker "
                    "patients were usually sent to one specific machine. Why is this leakage?"
                ),
                "options": [
                    "The scanner is always the correct clinical target.",
                    "The machine identity indirectly reveals the label-generating process and may not generalize elsewhere.",
                    "The dataset contains too many examples.",
                    "The model is underfitting.",
                ],
                "correct": 1,
                "explanation": (
                    "The model exploits a shortcut tied to the training data-generation "
                    "process rather than the intended disease signal."
                ),
            },

            {
                "id": "M05.L01.Q10",
                "section_id": "leakage-causes",
                "question": (
                    "Which split is most appropriate for a strongly time-correlated "
                    "forecasting task?"
                ),
                "options": [
                    "Randomly mix past and future examples across all splits.",
                    "Train on earlier periods and evaluate on later periods.",
                    "Use the test period to tune feature definitions.",
                    "Duplicate rare future examples into training.",
                ],
                "correct": 1,
                "explanation": (
                    "Time-aware splitting prevents future conditions from leaking "
                    "into the training process."
                ),
            },

            {
                "id": "M05.L01.Q11",
                "section_id": "detecting-leakage",
                "question": (
                    "A newly added feature causes a dramatic validation improvement. "
                    "What should you do next?"
                ),
                "options": [
                    "Assume the project is finished.",
                    "Investigate how the feature is generated and whether it leaks target information.",
                    "Delete the test split.",
                    "Always remove the feature immediately.",
                ],
                "correct": 1,
                "explanation": (
                    "A large jump can indicate either a genuinely useful feature or "
                    "leakage, so provenance and availability must be checked."
                ),
            },

            {
                "id": "M05.L01.Q12",
                "section_id": "good-features",
                "question": (
                    "Why can a useless feature still be harmful even if the model "
                    "learns to assign it little predictive weight?"
                ),
                "options": [
                    "It can add serving cost, pipeline maintenance, latency, and leakage risk.",
                    "Unused features always crash models.",
                    "Every feature must have identical importance.",
                    "Regularization cannot be used in production.",
                ],
                "correct": 0,
                "explanation": (
                    "Production cost includes infrastructure and maintenance, not "
                    "only predictive contribution."
                ),
            },

            {
                "id": "M05.L01.Q13",
                "section_id": "feature-importance",
                "question": (
                    "What does an ablation study do?"
                ),
                "options": [
                    "Adds duplicates to the training set.",
                    "Removes a feature or component and measures the resulting performance change.",
                    "Hashes categories into a fixed space.",
                    "Scales features to zero mean.",
                ],
                "correct": 1,
                "explanation": (
                    "Ablation estimates contribution by measuring what happens when "
                    "a component is removed."
                ),
            },

            {
                "id": "M05.L01.Q14",
                "section_id": "feature-generalization",
                "question": (
                    "A DAY_OF_WEEK feature is present in every example, but training "
                    "contains Monday-Saturday while evaluation contains only Sunday. "
                    "What problem does this illustrate?"
                ),
                "options": [
                    "Low feature coverage",
                    "Perfect value overlap",
                    "Poor value-distribution generalization despite full coverage",
                    "MCAR missingness",
                ],
                "correct": 2,
                "explanation": (
                    "Coverage is 100%, but the unseen split contains a categorical "
                    "value that was absent from training."
                ),
            },

            {
                "id": "M05.L01.Q15",
                "section_id": "leakage-causes",
                "type": "open",
                "question": (
                    "Design a leakage-safe preprocessing order for a time-correlated "
                    "classification problem that has duplicate records, missing "
                    "numerical values, feature scaling, and minority-class oversampling. "
                    "Explain the order of operations and why each step occurs where it does."
                ),
            },
        ],

        "passing_score": 70,
    },
}
