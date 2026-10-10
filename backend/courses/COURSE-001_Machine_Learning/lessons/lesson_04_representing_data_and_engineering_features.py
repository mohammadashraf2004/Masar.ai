"""M04.L01 — Representing Data and Engineering Features.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapter 4, sections 4.1–4.9.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Representing Data and Engineering Features"

MODULE_DESCRIPTION = (
    "Learn how feature representation changes what a machine learning model can "
    "learn, including categorical encoding, column-wise preprocessing, binning, "
    "interactions, polynomial and nonlinear transformations, automatic feature "
    "selection, and expert-designed features."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Sections 4.1–4.9"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Representing Data and Engineering Features",

    "slug": "ml-foundations-m04-l01",

    "description": (
        "Learn how to turn raw continuous and categorical data into useful model "
        "inputs, engineer richer representations, select useful features, and "
        "use domain knowledge to improve machine-learning systems."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.0,

    "skill_tags": [
        "machine-learning",
        "feature-engineering",
        "categorical-data",
        "one-hot-encoding",
        "column-transformer",
        "binning",
        "polynomial-features",
        "feature-interactions",
        "feature-selection",
        "domain-knowledge",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Representing Data and Engineering Features",

        "content": (
            "# Representing Data and Engineering Features\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M04.L01  \n"
            "> **Module:** Representing Data and Engineering Features  \n"
            "> **Source alignment:** BOOK-001, Chapter 4, sections 4.1–4.9. "
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
            "- Distinguish continuous features from categorical features.\n"
            "- Explain why feature representation can strongly affect model performance.\n"
            "- Convert categorical variables into machine-readable features using one-hot encoding.\n"
            "- Recognize when integer values actually represent categories rather than quantities.\n"
            "- Apply different preprocessing steps to different feature groups.\n"
            "- Explain when binning can make a linear model more expressive.\n"
            "- Create interaction and polynomial features conceptually.\n"
            "- Explain why logarithmic transformations can help with skewed count data.\n"
            "- Compare univariate, model-based, and iterative feature-selection strategies.\n"
            "- Use domain knowledge to create features that expose useful structure to a model.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Feature representation and categorical variables\n"
            "\n"
            "Machine-learning algorithms do not work directly with the meaning "
            "that humans attach to data. They work with the numerical "
            "representation we give them.\n"
            "\n"
            "That means two datasets describing the same real-world objects can "
            "behave very differently if they are represented differently.\n"
            "\n"
            "This is the central idea of **feature engineering**:\n"
            "\n"
            "> Represent the available information in a form that makes useful "
            "patterns easier for the chosen model to learn.\n"
            "\n"
            "### Continuous features\n"
            "\n"
            "A continuous feature represents a quantity where nearby numeric "
            "values have meaningful relationships.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "age = 39\n"
            "temperature = 27.4\n"
            "flower width = 2.1 cm\n"
            "hours worked per week = 40\n"
            "```\n"
            "\n"
            "If one person is 40 years old and another is 41, the numerical "
            "difference has meaning.\n"
            "\n"
            "### Categorical features\n"
            "\n"
            "A categorical feature describes membership in a discrete group.\n"
            "\n"
            "Examples:\n"
            "\n"
            "```text\n"
            "product color -> red / green / blue\n"
            "department    -> books / clothing / hardware\n"
            "workclass     -> private / government / self-employed\n"
            "occupation    -> engineer / teacher / technician / ...\n"
            "```\n"
            "\n"
            "These values are labels, not measurements. There is no natural "
            "numeric distance between `books` and `clothing`, and `hardware` "
            "does not sit mathematically between them.\n"
            "\n"
            "### Why raw strings are a problem\n"
            "\n"
            "Many models expect numerical features. A linear classifier, for "
            "example, works with a weighted numerical expression such as:\n"
            "\n"
            "```text\n"
            "score = w0*x0 + w1*x1 + ... + wp*xp + b\n"
            "```\n"
            "\n"
            "This expression can multiply a coefficient by a number such as "
            "`40`, but it cannot meaningfully multiply a coefficient by the "
            "word `Bachelors` or `Private`.\n"
            "\n"
            "So categorical values need a useful numerical representation.\n"
            "\n"
            "### One-hot encoding\n"
            "\n"
            "The most common representation introduced in this chapter is "
            "**one-hot encoding**, also called dummy variables.\n"
            "\n"
            "Suppose `workclass` has four categories:\n"
            "\n"
            "```text\n"
            "Government\n"
            "Private\n"
            "Self Employed\n"
            "Self Employed Incorporated\n"
            "```\n"
            "\n"
            "Instead of storing one text column, create one binary feature for "
            "each category:\n"
            "\n"
            "| workclass | Government | Private | Self Employed | Self Employed Inc. |\n"
            "|---|---:|---:|---:|---:|\n"
            "| Government | 1 | 0 | 0 | 0 |\n"
            "| Private | 0 | 1 | 0 | 0 |\n"
            "| Self Employed | 0 | 0 | 1 | 0 |\n"
            "| Self Employed Inc. | 0 | 0 | 0 | 1 |\n"
            "\n"
            "Each row has one active indicator for the observed category.\n"
            "\n"
            "### Using pandas\n"
            "\n"
            "A simple way to encode string-valued categorical columns is:\n"
            "\n"
            "```python\n"
            "import pandas as pd\n"
            "\n"
            "encoded = pd.get_dummies(data)\n"
            "```\n"
            "\n"
            "Continuous numeric columns such as age can remain numeric, while "
            "categorical string columns expand into binary indicator columns.\n"
            "\n"
            "### Check categories before encoding\n"
            "\n"
            "Real data often contains inconsistent spelling or capitalization.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Male\n"
            "male\n"
            "man\n"
            "```\n"
            "\n"
            "These might represent the same intended category but would be "
            "treated as separate values unless cleaned first.\n"
            "\n"
            "A useful inspection step is:\n"
            "\n"
            "```python\n"
            "print(data['gender'].value_counts())\n"
            "```\n"
            "\n"
            "Always understand what the unique values actually mean before "
            "encoding them.\n"
            "\n"
            "### Numbers can still be categorical\n"
            "\n"
            "One of the most important ideas in this chapter is that **numeric "
            "storage does not automatically mean numeric meaning**.\n"
            "\n"
            "Suppose employment type is stored as:\n"
            "\n"
            "```text\n"
            "0 -> government\n"
            "1 -> private\n"
            "2 -> self-employed\n"
            "```\n"
            "\n"
            "The numbers are only codes. Treating them as continuous would "
            "incorrectly suggest relationships such as:\n"
            "\n"
            "```text\n"
            "2 is twice 1\n"
            "2 is farther from 0 than 1 is\n"
            "```\n"
            "\n"
            "Those statements have no meaningful connection to employment "
            "status.\n"
            "\n"
            "When the numbers are identifiers for unordered states, treat the "
            "feature as categorical.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Safe preprocessing with mixed feature types\n"
            "\n"
            "Real datasets often contain both continuous and categorical "
            "features.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "age             -> continuous\n"
            "hours-per-week  -> continuous\n"
            "workclass       -> categorical\n"
            "education       -> categorical\n"
            "gender          -> categorical\n"
            "occupation      -> categorical\n"
            "```\n"
            "\n"
            "Different feature types often need different preprocessing.\n"
            "\n"
            "A common strategy is:\n"
            "\n"
            "```text\n"
            "continuous columns  -> scaling\n"
            "categorical columns -> one-hot encoding\n"
            "```\n"
            "\n"
            "### OneHotEncoder\n"
            "\n"
            "scikit-learn provides `OneHotEncoder` for categorical variables.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import OneHotEncoder\n"
            "\n"
            "encoder = OneHotEncoder()\n"
            "X_encoded = encoder.fit_transform(X_categorical)\n"
            "```\n"
            "\n"
            "The important distinction is between `fit` and `transform`:\n"
            "\n"
            "- `fit` learns which categories exist in the training data.\n"
            "- `transform` applies that learned mapping to data.\n"
            "\n"
            "### Why training and test columns must mean the same thing\n"
            "\n"
            "Imagine that we encode the training and test sets independently.\n"
            "\n"
            "Training categories:\n"
            "\n"
            "```text\n"
            "Government\n"
            "Private\n"
            "```\n"
            "\n"
            "Test categories:\n"
            "\n"
            "```text\n"
            "Self Employed\n"
            "Self Employed Incorporated\n"
            "```\n"
            "\n"
            "Both independently encoded matrices could contain two columns, but "
            "column 1 would mean one thing in training and something completely "
            "different in testing.\n"
            "\n"
            "A model assumes feature positions have the same semantics. If the "
            "meaning changes, the model receives corrupted input.\n"
            "\n"
            "The safe mental model is:\n"
            "\n"
            "```text\n"
            "training data\n"
            "    ↓\n"
            "fit preprocessing\n"
            "    ↓\n"
            "transform training data\n"
            "transform test data using SAME fitted preprocessing\n"
            "```\n"
            "\n"
            "### ColumnTransformer\n"
            "\n"
            "`ColumnTransformer` lets us apply different transformations to "
            "different columns.\n"
            "\n"
            "A chapter-style example is:\n"
            "\n"
            "```python\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n"
            "\n"
            "ct = ColumnTransformer([\n"
            "    ('scaling', StandardScaler(), ['age', 'hours-per-week']),\n"
            "    ('onehot', OneHotEncoder(),\n"
            "        ['workclass', 'education', 'gender', 'occupation']),\n"
            "])\n"
            "```\n"
            "\n"
            "Then the training workflow becomes:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import train_test_split\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    data_features,\n"
            "    target,\n"
            "    random_state=0,\n"
            ")\n"
            "\n"
            "ct.fit(X_train)\n"
            "X_train_transformed = ct.transform(X_train)\n"
            "X_test_transformed = ct.transform(X_test)\n"
            "```\n"
            "\n"
            "This keeps the preprocessing rules consistent.\n"
            "\n"
            "### A critical supervised-learning mistake: target leakage\n"
            "\n"
            "Suppose the target is whether income is above 50K. After encoding, "
            "we might accidentally leave an `income_>50K` indicator inside the "
            "input matrix.\n"
            "\n"
            "Then the model receives the answer as one of its features.\n"
            "\n"
            "That is **target leakage**.\n"
            "\n"
            "The model might score extremely well during evaluation while being "
            "useless for real prediction.\n"
            "\n"
            "Always separate:\n"
            "\n"
            "```text\n"
            "X -> input features\n"
            "y -> target to predict\n"
            "```\n"
            "\n"
            "and make sure information derived from `y` does not accidentally "
            "enter `X`.\n"
            "\n"

            "{{exercise:M04.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Binning, interactions, polynomials, and nonlinear transformations\n"
            "\n"
            "Feature engineering is not only about converting categories to "
            "numbers. We can also create new representations of continuous "
            "features to make useful patterns easier for some models to learn.\n"
            "\n"
            "A key lesson from the chapter is:\n"
            "\n"
            "> The usefulness of a representation depends on both the data and "
            "the model family.\n"
            "\n"
            "### Binning continuous features\n"
            "\n"
            "Suppose a feature ranges from -3 to 3. Instead of giving the model "
            "the exact value, divide the range into intervals called **bins**.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "[-3.0, -2.4) -> bin 1\n"
            "[-2.4, -1.8) -> bin 2\n"
            "...\n"
            "[ 2.4,  3.0] -> bin 10\n"
            "```\n"
            "\n"
            "Each value can then be represented by the bin it belongs to.\n"
            "\n"
            "With one-hot encoded bins:\n"
            "\n"
            "```text\n"
            "value = -0.75\n"
            "\n"
            "[0, 0, 0, 1, 0, 0, 0, 0, 0, 0]\n"
            "```\n"
            "\n"
            "scikit-learn provides `KBinsDiscretizer` for this transformation.\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import KBinsDiscretizer\n"
            "\n"
            "kb = KBinsDiscretizer(n_bins=10, strategy='uniform')\n"
            "X_binned = kb.fit_transform(X)\n"
            "```\n"
            "\n"
            "### Why binning can help linear models\n"
            "\n"
            "With one original continuous feature, a linear regression model "
            "can only learn one straight-line relationship.\n"
            "\n"
            "After binning, the model can learn a different value for each "
            "region of the input range. This can make the model much more "
            "flexible.\n"
            "\n"
            "Tree-based models usually benefit less from manual binning because "
            "a decision tree can already learn useful split points by itself.\n"
            "\n"
            "### Interaction features\n"
            "\n"
            "Sometimes the effect of one feature depends on another feature.\n"
            "\n"
            "Imagine:\n"
            "\n"
            "```text\n"
            "feature A = day of week\n"
            "feature B = hour of day\n"
            "```\n"
            "\n"
            "The importance of 8:00 AM may be very different on Monday than on "
            "Sunday.\n"
            "\n"
            "An **interaction feature** gives the model a way to represent the "
            "combination.\n"
            "\n"
            "In simple mathematical form:\n"
            "\n"
            "```text\n"
            "interaction = x1 * x2\n"
            "```\n"
            "\n"
            "This is not just 'another copy' of either feature. It captures "
            "information about them occurring together.\n"
            "\n"
            "### Polynomial features\n"
            "\n"
            "A linear model can become nonlinear with respect to the original "
            "input when we add transformed features such as:\n"
            "\n"
            "```text\n"
            "x\n"
            "x²\n"
            "x³\n"
            "x⁴\n"
            "```\n"
            "\n"
            "The model is still linear in its learned coefficients, but it now "
            "has nonlinear versions of the original input available.\n"
            "\n"
            "scikit-learn provides `PolynomialFeatures`:\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import PolynomialFeatures\n"
            "\n"
            "poly = PolynomialFeatures(degree=2)\n"
            "X_poly = poly.fit_transform(X)\n"
            "```\n"
            "\n"
            "For multiple input features, degree 2 can create:\n"
            "\n"
            "```text\n"
            "x0\n"
            "x1\n"
            "x0²\n"
            "x0*x1\n"
            "x1²\n"
            "```\n"
            "\n"
            "The interaction terms allow a linear model to represent patterns "
            "that depend on combinations of features.\n"
            "\n"
            "### More features are not automatically better\n"
            "\n"
            "Polynomial and interaction features can dramatically increase the "
            "number of columns.\n"
            "\n"
            "In the chapter's housing example, 13 original features expand to "
            "105 features when degree-2 polynomial and interaction features are "
            "created.\n"
            "\n"
            "That extra representation helped a Ridge model, but the same "
            "expansion did not help the random forest in that example.\n"
            "\n"
            "The lesson is not:\n"
            "\n"
            "> Always add polynomial features.\n"
            "\n"
            "The lesson is:\n"
            "\n"
            "> Feature engineering and model choice must be considered together.\n"
            "\n"
            "### Univariate nonlinear transformations\n"
            "\n"
            "Some features have highly skewed distributions. Count data is a "
            "common example: many observations may have small values while a "
            "few observations have very large values.\n"
            "\n"
            "A logarithmic transformation can compress large values:\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "\n"
            "X_log = np.log(X + 1)\n"
            "```\n"
            "\n"
            "The `+ 1` allows zero-valued counts to be transformed because "
            "`log(0)` is undefined.\n"
            "\n"
            "In the chapter's synthetic count example, Ridge performed much "
            "better after applying this transformation.\n"
            "\n"
            "Other transformations such as sine and cosine can be useful when "
            "a variable contains periodic structure.\n"
            "\n"
            "### Model dependence matters\n"
            "\n"
            "Linear models and neural networks are sensitive to scale and the "
            "form in which relationships are presented. Tree-based models care "
            "more about ordering and can often discover useful split structures "
            "without the same explicit transformations.\n"
            "\n"
            "So there is no universally best feature transformation.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Feature selection and expert knowledge\n"
            "\n"
            "Feature engineering can create many new columns. But adding too "
            "many features increases model complexity and can increase the risk "
            "of overfitting.\n"
            "\n"
            "Sometimes we want the opposite operation: keep only the most useful "
            "features.\n"
            "\n"
            "This is **feature selection**.\n"
            "\n"
            "The chapter introduces three major strategies.\n"
            "\n"
            "### 4.1 Univariate feature selection\n"
            "\n"
            "Univariate methods examine each feature individually and estimate "
            "how strongly it is related to the target.\n"
            "\n"
            "Examples in scikit-learn include:\n"
            "\n"
            "```text\n"
            "SelectKBest\n"
            "SelectPercentile\n"
            "```\n"
            "\n"
            "The advantage is speed and simplicity.\n"
            "\n"
            "The limitation is important: because features are considered one "
            "at a time, a feature that is useful only when combined with another "
            "feature may appear unimportant and be removed.\n"
            "\n"
            "Conceptual workflow:\n"
            "\n"
            "```python\n"
            "from sklearn.feature_selection import SelectPercentile\n"
            "\n"
            "select = SelectPercentile(percentile=50)\n"
            "select.fit(X_train, y_train)\n"
            "\n"
            "X_train_selected = select.transform(X_train)\n"
            "X_test_selected = select.transform(X_test)\n"
            "```\n"
            "\n"
            "Notice that feature selection is fitted on the **training set**, "
            "not on the full dataset.\n"
            "\n"
            "### 4.2 Model-based feature selection\n"
            "\n"
            "A supervised model can also estimate which features matter most.\n"
            "\n"
            "Examples of importance signals include:\n"
            "\n"
            "- tree-based `feature_importances_`\n"
            "- absolute coefficient magnitudes from linear models\n"
            "- sparse coefficients from L1-regularized models\n"
            "\n"
            "scikit-learn's `SelectFromModel` can use such a model as a selector.\n"
            "\n"
            "```python\n"
            "from sklearn.feature_selection import SelectFromModel\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "\n"
            "selector = SelectFromModel(\n"
            "    RandomForestClassifier(n_estimators=100, random_state=42),\n"
            "    threshold='median',\n"
            ")\n"
            "\n"
            "selector.fit(X_train, y_train)\n"
            "X_train_selected = selector.transform(X_train)\n"
            "```\n"
            "\n"
            "Unlike a univariate test, a sufficiently capable model can consider "
            "features together.\n"
            "\n"
            "### 4.3 Iterative feature selection\n"
            "\n"
            "Iterative methods repeatedly build models while changing the set of "
            "features.\n"
            "\n"
            "One example is **Recursive Feature Elimination (RFE)**.\n"
            "\n"
            "The basic idea is:\n"
            "\n"
            "```text\n"
            "start with all features\n"
            "        ↓\n"
            "fit model\n"
            "        ↓\n"
            "remove least useful feature(s)\n"
            "        ↓\n"
            "fit again\n"
            "        ↓\n"
            "repeat until desired number remains\n"
            "```\n"
            "\n"
            "RFE can produce strong selections, but it is much more "
            "computationally expensive because many models must be trained.\n"
            "\n"
            "### Why feature selection is useful\n"
            "\n"
            "Feature selection may help with:\n"
            "\n"
            "- reducing overfitting risk\n"
            "- reducing prediction cost\n"
            "- making models easier to interpret\n"
            "- making very high-dimensional problems manageable\n"
            "- removing clearly uninformative variables\n"
            "\n"
            "It does not guarantee a large performance improvement, but it is a "
            "valuable tool.\n"
            "\n"
            "### Expert knowledge: designing better inputs\n"
            "\n"
            "Machine learning does not mean domain knowledge becomes useless.\n"
            "\n"
            "A model can only learn from information that is represented in its "
            "inputs.\n"
            "\n"
            "Suppose we are predicting flight prices and our raw data contains:\n"
            "\n"
            "```text\n"
            "date\n"
            "airline\n"
            "origin\n"
            "destination\n"
            "```\n"
            "\n"
            "A domain expert may know that school holidays and public holidays "
            "strongly affect prices. If those events are not directly "
            "represented by the raw calendar date in a learnable way, we can "
            "create features such as:\n"
            "\n"
            "```text\n"
            "is_public_holiday\n"
            "is_school_holiday\n"
            "days_until_holiday\n"
            "```\n"
            "\n"
            "We are not manually telling the model what prediction to make. We "
            "are exposing useful information so the model can decide whether it "
            "matters.\n"
            "\n"
            "### Worked example: bike rentals\n"
            "\n"
            "The chapter uses bicycle-rental demand to show how representation "
            "can completely change model performance.\n"
            "\n"
            "The raw input is a timestamp, and the target is the number of bikes "
            "rented during a time interval.\n"
            "\n"
            "#### Attempt 1: raw POSIX timestamp\n"
            "\n"
            "A random forest trained on raw time performs poorly on future "
            "timestamps.\n"
            "\n"
            "Why?\n"
            "\n"
            "The future timestamps lie outside the numeric range seen during "
            "training. Tree models cannot naturally extrapolate beyond the "
            "ranges defined by their learned splits.\n"
            "\n"
            "#### Attempt 2: hour of day\n"
            "\n"
            "Instead of raw timestamp, extract:\n"
            "\n"
            "```text\n"
            "hour_of_day\n"
            "```\n"
            "\n"
            "Now the model can learn the daily pattern.\n"
            "\n"
            "#### Attempt 3: hour + day of week\n"
            "\n"
            "Add:\n"
            "\n"
            "```text\n"
            "day_of_week\n"
            "hour_of_day\n"
            "```\n"
            "\n"
            "Now the model can distinguish weekday and weekend behavior.\n"
            "\n"
            "#### Attempt 4: one-hot encoding for a linear model\n"
            "\n"
            "If day and hour are fed to linear regression as plain integers, the "
            "model incorrectly assumes a simple continuous relationship.\n"
            "\n"
            "One-hot encoding lets the model learn a separate effect for each "
            "day and each time slot.\n"
            "\n"
            "#### Attempt 5: interactions\n"
            "\n"
            "An interaction between day and hour lets a linear model learn "
            "different time-of-day patterns for different days.\n"
            "\n"
            "This final representation allows a relatively simple linear model "
            "to perform similarly to the more complex random-forest model in the "
            "chapter example.\n"
            "\n"
            "### The deeper lesson\n"
            "\n"
            "The algorithm did not suddenly become smarter.\n"
            "\n"
            "We changed the **representation** so the important structure became "
            "easier for the algorithm to learn.\n"
            "\n"

            "{{exercise:M04.L01.EX02}}\n"
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
            "> If a column contains integers, it should always be treated as a "
            "continuous numeric feature.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Integers may simply be category codes. The meaning of the feature, "
            "not its storage type, determines whether it is continuous or "
            "categorical.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Adding more engineered features always improves a model.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Extra features increase dimensionality and model complexity. They "
            "can help one model and hurt another. The chapter shows that "
            "polynomial interactions improved Ridge in one example while not "
            "improving the random forest.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Training and test data can be one-hot encoded independently as "
            "long as the output matrices have the same number of columns.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Equal shape does not guarantee equal meaning. A column may "
            "represent `Private` in the training data and `Self Employed` in the "
            "test data. Preprocessing must preserve feature semantics.\n"
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
            "| Feature engineering | Designing or transforming input representations to make useful patterns easier to learn |\n"
            "| Continuous feature | A quantitative feature with meaningful numeric ordering and distances |\n"
            "| Categorical feature | A feature representing membership in discrete categories |\n"
            "| One-hot encoding | Replacing a categorical feature with binary indicator columns |\n"
            "| Dummy variable | A binary indicator used to encode a category |\n"
            "| Target leakage | Accidentally giving the model information derived from the answer it is supposed to predict |\n"
            "| ColumnTransformer | A scikit-learn mechanism for applying different transformations to different columns |\n"
            "| Binning | Converting a continuous range into discrete intervals |\n"
            "| Interaction feature | A feature representing the joint effect of multiple original features |\n"
            "| Polynomial feature | A power or product of original features, such as x² or x1*x2 |\n"
            "| Nonlinear transformation | Applying a function such as log to change a feature's representation |\n"
            "| Feature selection | Keeping useful features and discarding less useful ones |\n"
            "| Univariate selection | Selecting features by evaluating each feature separately against the target |\n"
            "| Model-based selection | Selecting features using importance estimates from a supervised model |\n"
            "| Recursive Feature Elimination | Iteratively fitting a model and removing the least useful features |\n"
            "| Expert knowledge | Domain understanding used to design more informative features |\n"
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
            "1. Why can a categorical variable not always be passed directly into a linear model?\n"
            "2. How does one-hot encoding represent four possible categories?\n"
            "3. Why might an integer-valued column still need categorical encoding?\n"
            "4. Why must preprocessing learned from the training set be reused for the test set?\n"
            "5. What is target leakage?\n"
            "6. Why can binning increase the expressive power of a linear model?\n"
            "7. What information does an interaction feature represent?\n"
            "8. Why might a log transformation help with skewed count data?\n"
            "9. How do univariate, model-based, and iterative feature selection differ?\n"
            "10. What did the bike-rental example teach about domain knowledge and representation?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**A machine-learning model can only learn from the representation "
            "you give it. Choosing and engineering features that expose the "
            "right structure can matter as much as, and sometimes more than, "
            "changing the model itself.**\n"
        ),

        "estimated_minutes": 120,

        "has_code_examples": True,

        "sections": [
            {
                "id": "categorical-representation",
                "title": "Feature representation and categorical variables",
                "order": 1,
            },
            {
                "id": "safe-preprocessing",
                "title": "Safe preprocessing with mixed feature types",
                "order": 2,
            },
            {
                "id": "feature-transformations",
                "title": "Binning, interactions, polynomials, and nonlinear transformations",
                "order": 3,
            },
            {
                "id": "selection-and-domain-knowledge",
                "title": "Feature selection and expert knowledge",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Build a Safe Preprocessing Plan",

            "lesson_code": "M04.L01",

            "section_id": "safe-preprocessing",

            "placement": "after_section",

            "description": (
                "Classify feature types and design a preprocessing plan without "
                "introducing target leakage."
            ),

            "instructions": (
                "You have a customer dataset with these columns:\n"
                "\n"
                "- age\n"
                "- monthly_spend\n"
                "- city\n"
                "- membership_type\n"
                "- device_code, where 0=mobile, 1=desktop, 2=tablet\n"
                "- churned, the target to predict\n"
                "\n"
                "1. Identify which input features are continuous.\n"
                "2. Identify which input features are categorical.\n"
                "3. Explain why device_code should not automatically be treated "
                "as continuous just because it contains integers.\n"
                "4. Propose a ColumnTransformer-style preprocessing plan.\n"
                "5. Explain why churned must not be included among the input features.\n"
                "6. Explain which preprocessing object should be fitted on the "
                "training set and then reused for the test set."
            ),

            "expected_output": (
                "A feature-type table plus a short preprocessing plan that "
                "separates continuous features, categorical features, and the target."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "categorical-vs-continuous",
                "one-hot-encoding",
                "column-transformer",
                "target-leakage",
                "train-test-preprocessing",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Engineer Features for Bike Demand",

            "lesson_code": "M04.L01",

            "section_id": "selection-and-domain-knowledge",

            "placement": "after_section",

            "description": (
                "Use domain knowledge to redesign a weak raw feature "
                "representation for a demand-prediction problem."
            ),

            "instructions": (
                "You want to predict bicycle rentals from a timestamp.\n"
                "\n"
                "The first model receives only the raw timestamp and performs "
                "poorly on future dates.\n"
                "\n"
                "1. Propose at least three useful features that can be derived "
                "from the timestamp.\n"
                "2. Identify which of those features should be considered "
                "categorical for a linear model.\n"
                "3. Explain why one-hot encoding can help the linear model.\n"
                "4. Create one interaction you expect to be useful.\n"
                "5. Explain what additional domain feature, beyond the timestamp "
                "itself, could help predict unusual demand.\n"
                "6. Explain why raw future timestamps are difficult for a tree "
                "model trained only on earlier timestamps."
            ),

            "expected_output": (
                "A short feature-engineering proposal containing derived "
                "features, encoding decisions, one interaction, and reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "domain-feature-engineering",
                "categorical-encoding",
                "feature-interactions",
                "model-representation-match",
                "reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Representing Data and Engineering Features — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",

                "section_id": "categorical-representation",

                "question": (
                    "Which statement best describes one-hot encoding?"
                ),

                "options": [
                    "It sorts categories from smallest to largest",
                    "It replaces each category with its average target value",
                    "It creates binary indicator features for categorical values",
                    "It removes all categorical features from the dataset",
                ],

                "correct": 2,

                "explanation": (
                    "One-hot encoding represents categorical membership using "
                    "binary indicator columns, usually one column per category."
                ),
            },

            {
                "id": "M04.L01.Q02",

                "section_id": "safe-preprocessing",

                "question": (
                    "A feature stores workclass as 0=government, 1=private, "
                    "2=self-employed. What is the most important question before "
                    "treating it as continuous?"
                ),

                "options": [
                    "Whether the column is stored using integers",
                    "Whether the numbers represent meaningful ordered quantities",
                    "Whether the target is binary",
                    "Whether the dataset has more than 1,000 rows",
                ],

                "correct": 1,

                "explanation": (
                    "Storage type does not determine semantics. If the numbers "
                    "are merely unordered category codes, they should be treated "
                    "as categorical rather than as continuous measurements."
                ),
            },

            {
                "id": "M04.L01.Q03",

                "section_id": "feature-transformations",

                "question": (
                    "Why can binning make a linear model more flexible?"
                ),

                "options": [
                    "It allows the model to learn separate effects for different input regions",
                    "It guarantees that all data becomes normally distributed",
                    "It automatically removes the target variable",
                    "It turns every linear model into a decision tree",
                ],

                "correct": 0,

                "explanation": (
                    "Representing input regions with separate bin indicators "
                    "allows a linear model to learn different values for "
                    "different regions instead of relying on one global line."
                ),
            },

            {
                "id": "M04.L01.Q04",

                "section_id": "selection-and-domain-knowledge",

                "question": (
                    "Which statement correctly describes univariate feature selection?"
                ),

                "options": [
                    "It always captures complex interactions between features",
                    "It requires training dozens of models recursively",
                    "It evaluates each feature individually in relation to the target",
                    "It can only be used with random forests",
                ],

                "correct": 2,

                "explanation": (
                    "Univariate selection examines one feature at a time. This "
                    "makes it fast, but it may miss features that are only "
                    "informative in combination with others."
                ),
            },

            {
                "id": "M04.L01.Q05",

                "section_id": "selection-and-domain-knowledge",

                "type": "open",

                "question": (
                    "A model receives a raw calendar timestamp but fails to "
                    "capture weekly demand patterns. Propose a better feature "
                    "representation and explain why your representation makes the "
                    "pattern easier for the model to learn."
                ),
            },
        ],

        "passing_score": 70,
    },
}
