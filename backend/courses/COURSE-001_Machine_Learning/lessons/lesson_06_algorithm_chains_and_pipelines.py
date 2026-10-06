"""M06.L01 — Algorithm Chains and Pipelines.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapter 6, sections 6.1–6.7.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "Algorithm Chains and Pipelines"

MODULE_DESCRIPTION = (
    "Learn how to combine preprocessing, feature extraction, feature selection, "
    "and machine-learning models into safe scikit-learn pipelines, and how to "
    "tune complete workflows without leaking information across validation folds."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Sections 6.1–6.7"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Algorithm Chains and Pipelines",

    "slug": "ml-foundations-m06-l01",

    "description": (
        "Build end-to-end scikit-learn pipelines that keep preprocessing inside "
        "cross-validation, avoid information leakage, support GridSearchCV, and "
        "tune preprocessing and model choices as one workflow."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.75,

    "skill_tags": [
        "machine-learning",
        "scikit-learn",
        "pipeline",
        "preprocessing",
        "cross-validation",
        "grid-search",
        "data-leakage",
        "feature-selection",
        "hyperparameter-tuning",
        "module-06",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Algorithm Chains and Pipelines",

        "content": (
            "# Algorithm Chains and Pipelines\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M06.L01  \n"
            "> **Module:** Algorithm Chains and Pipelines  \n"
            "> **Source alignment:** BOOK-001, Chapter 6, sections 6.1–6.7. "
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
            "- Explain why real machine-learning workflows usually require several processing steps.\n"
            "- Identify how preprocessing outside cross-validation can leak information.\n"
            "- Build and fit a scikit-learn `Pipeline`.\n"
            "- Explain what happens internally during `fit`, `predict`, and `score`.\n"
            "- Tune pipeline parameters with `GridSearchCV` using `step__parameter` names.\n"
            "- Access fitted estimators and learned attributes inside a pipeline.\n"
            "- Tune preprocessing choices and model parameters together.\n"
            "- Search over different model families in one pipeline.\n"
            "- Explain when pipeline caching can reduce redundant computation.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Why machine-learning workflows need pipelines\n"
            "\n"
            "A real machine-learning system usually does more than fit a single "
            "model to raw data.\n"
            "\n"
            "A typical workflow may look like this:\n"
            "\n"
            "```text\n"
            "raw data\n"
            "   ↓\n"
            "scaling\n"
            "   ↓\n"
            "feature extraction\n"
            "   ↓\n"
            "feature selection\n"
            "   ↓\n"
            "classifier or regressor\n"
            "   ↓\n"
            "prediction\n"
            "```\n"
            "\n"
            "The chapter calls these connected processing steps an "
            "**algorithm chain**.\n"
            "\n"
            "The main problem is not only writing less code. The more important "
            "problem is making sure every processing step is learned from the "
            "correct data.\n"
            "\n"
            "### Example: scaling before an SVM\n"
            "\n"
            "Suppose we want to train an SVM on the breast-cancer dataset. "
            "Because the input features are on different scales, we first apply "
            "`MinMaxScaler`.\n"
            "\n"
            "A manual version looks like this:\n"
            "\n"
            "```python\n"
            "from sklearn.datasets import load_breast_cancer\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import MinMaxScaler\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "cancer = load_breast_cancer()\n"
            "\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    cancer.data,\n"
            "    cancer.target,\n"
            "    random_state=0,\n"
            ")\n"
            "\n"
            "scaler = MinMaxScaler().fit(X_train)\n"
            "X_train_scaled = scaler.transform(X_train)\n"
            "\n"
            "svm = SVC()\n"
            "svm.fit(X_train_scaled, y_train)\n"
            "\n"
            "X_test_scaled = scaler.transform(X_test)\n"
            "score = svm.score(X_test_scaled, y_test)\n"
            "```\n"
            "\n"
            "The important pattern is:\n"
            "\n"
            "```text\n"
            "fit scaler on training data\n"
            "transform training data\n"
            "fit model\n"
            "transform test data with SAME scaler\n"
            "evaluate model\n"
            "```\n"
            "\n"
            "This is safe for one train/test split.\n"
            "\n"
            "The difficulty appears when we combine preprocessing with "
            "**cross-validation** or **grid search**.\n"
            "\n"
            "### The dangerous shortcut\n"
            "\n"
            "A tempting workflow is:\n"
            "\n"
            "```text\n"
            "1. Fit scaler on all training data\n"
            "2. Transform all training data\n"
            "3. Run GridSearchCV on the already-scaled data\n"
            "```\n"
            "\n"
            "At first this looks correct because the external test set was not "
            "used.\n"
            "\n"
            "But cross-validation creates its own internal training and "
            "validation folds. If the scaler was fitted before those folds were "
            "created, the scaler has already seen information from every fold.\n"
            "\n"
            "That means each validation fold influenced preprocessing before it "
            "was used for validation.\n"
            "\n"
            "This is **information leakage**.\n"
            "\n"
            "### Correct principle\n"
            "\n"
            "Any step that learns something from the data should be fitted only "
            "on the training portion of each cross-validation split.\n"
            "\n"
            "So the correct order is conceptually:\n"
            "\n"
            "```text\n"
            "Cross-validation split 1\n"
            "    ├─ training fold -> fit scaler -> fit model\n"
            "    └─ validation fold -> transform with fitted scaler -> score\n"
            "\n"
            "Cross-validation split 2\n"
            "    ├─ training fold -> fit NEW scaler -> fit NEW model\n"
            "    └─ validation fold -> transform with fitted scaler -> score\n"
            "\n"
            "... repeat for every fold ...\n"
            "```\n"
            "\n"
            "This is exactly the kind of process that `Pipeline` is designed "
            "to manage safely.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Building and using a scikit-learn Pipeline\n"
            "\n"
            "A `Pipeline` combines multiple processing steps into one "
            "scikit-learn estimator.\n"
            "\n"
            "That combined object can expose familiar methods such as:\n"
            "\n"
            "```text\n"
            "fit\n"
            "predict\n"
            "score\n"
            "transform\n"
            "```\n"
            "\n"
            "depending on the final step.\n"
            "\n"
            "### Basic pipeline\n"
            "\n"
            "To combine `MinMaxScaler` with `SVC`:\n"
            "\n"
            "```python\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import MinMaxScaler\n"
            "from sklearn.svm import SVC\n"
            "\n"
            "pipe = Pipeline([\n"
            "    ('scaler', MinMaxScaler()),\n"
            "    ('svm', SVC()),\n"
            "])\n"
            "```\n"
            "\n"
            "Each pipeline step is a tuple:\n"
            "\n"
            "```text\n"
            "(step_name, estimator)\n"
            "```\n"
            "\n"
            "Now we can fit the whole workflow at once:\n"
            "\n"
            "```python\n"
            "pipe.fit(X_train, y_train)\n"
            "```\n"
            "\n"
            "Internally this does the equivalent of:\n"
            "\n"
            "```text\n"
            "scaler.fit(X_train)\n"
            "X_train_scaled = scaler.transform(X_train)\n"
            "svm.fit(X_train_scaled, y_train)\n"
            "```\n"
            "\n"
            "Then evaluation becomes:\n"
            "\n"
            "```python\n"
            "pipe.score(X_test, y_test)\n"
            "```\n"
            "\n"
            "Internally:\n"
            "\n"
            "```text\n"
            "X_test_scaled = scaler.transform(X_test)\n"
            "svm.score(X_test_scaled, y_test)\n"
            "```\n"
            "\n"
            "The pipeline remembers the correct sequence and applies it "
            "consistently.\n"
            "\n"
            "### The general pipeline interface\n"
            "\n"
            "A pipeline is not limited to two steps.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "feature extraction\n"
            "      ↓\n"
            "feature selection\n"
            "      ↓\n"
            "scaling\n"
            "      ↓\n"
            "classification\n"
            "```\n"
            "\n"
            "The main requirement is:\n"
            "\n"
            "- Every step except the last must be able to transform data.\n"
            "- The last step must at least support fitting.\n"
            "\n"
            "A simplified version of pipeline fitting is:\n"
            "\n"
            "```python\n"
            "X_transformed = X\n"
            "\n"
            "for transformer in intermediate_steps:\n"
            "    X_transformed = transformer.fit_transform(X_transformed, y)\n"
            "\n"
            "final_estimator.fit(X_transformed, y)\n"
            "```\n"
            "\n"
            "During prediction:\n"
            "\n"
            "```python\n"
            "X_transformed = X\n"
            "\n"
            "for transformer in intermediate_steps:\n"
            "    X_transformed = transformer.transform(X_transformed)\n"
            "\n"
            "predictions = final_estimator.predict(X_transformed)\n"
            "```\n"
            "\n"
            "The key difference is that prediction **does not refit** the "
            "transformers. It reuses what they learned during training.\n"
            "\n"
            "### `make_pipeline`\n"
            "\n"
            "If you do not need custom step names, scikit-learn can generate "
            "them automatically:\n"
            "\n"
            "```python\n"
            "from sklearn.pipeline import make_pipeline\n"
            "\n"
            "pipe = make_pipeline(\n"
            "    MinMaxScaler(),\n"
            "    SVC(C=100),\n"
            ")\n"
            "```\n"
            "\n"
            "The automatically generated names are based on lowercased class "
            "names, such as:\n"
            "\n"
            "```text\n"
            "minmaxscaler\n"
            "svc\n"
            "```\n"
            "\n"
            "If the same class appears more than once, scikit-learn adds "
            "numbers so the names remain unique.\n"
            "\n"
            "### Accessing individual steps\n"
            "\n"
            "Fitted steps are accessible through `named_steps`.\n"
            "\n"
            "For example, if a pipeline contains PCA:\n"
            "\n"
            "```python\n"
            "components = pipe.named_steps['pca'].components_\n"
            "```\n"
            "\n"
            "This is useful when you need learned attributes such as:\n"
            "\n"
            "- model coefficients\n"
            "- PCA components\n"
            "- feature importances\n"
            "- learned scaling parameters\n"
            "\n"

            "{{exercise:M06.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Pipelines with GridSearchCV and cross-validation\n"
            "\n"
            "One of the most important reasons to use a pipeline is that the "
            "entire workflow can be passed directly into cross-validation or "
            "`GridSearchCV`.\n"
            "\n"
            "### Parameter names inside a pipeline\n"
            "\n"
            "Suppose our pipeline is:\n"
            "\n"
            "```python\n"
            "pipe = Pipeline([\n"
            "    ('scaler', MinMaxScaler()),\n"
            "    ('svm', SVC()),\n"
            "])\n"
            "```\n"
            "\n"
            "We want to tune the SVM parameters `C` and `gamma`.\n"
            "\n"
            "Pipeline parameters use this naming convention:\n"
            "\n"
            "```text\n"
            "step_name__parameter_name\n"
            "```\n"
            "\n"
            "The double underscore is important.\n"
            "\n"
            "So the parameter grid becomes:\n"
            "\n"
            "```python\n"
            "param_grid = {\n"
            "    'svm__C': [0.001, 0.01, 0.1, 1, 10, 100],\n"
            "    'svm__gamma': [0.001, 0.01, 0.1, 1, 10, 100],\n"
            "}\n"
            "```\n"
            "\n"
            "Then grid search works normally:\n"
            "\n"
            "```python\n"
            "from sklearn.model_selection import GridSearchCV\n"
            "\n"
            "grid = GridSearchCV(\n"
            "    pipe,\n"
            "    param_grid=param_grid,\n"
            "    cv=5,\n"
            ")\n"
            "\n"
            "grid.fit(X_train, y_train)\n"
            "```\n"
            "\n"
            "Now each cross-validation fold behaves correctly:\n"
            "\n"
            "```text\n"
            "training fold\n"
            "   ↓\n"
            "fit MinMaxScaler\n"
            "   ↓\n"
            "transform training fold\n"
            "   ↓\n"
            "fit SVC\n"
            "\n"
            "validation fold\n"
            "   ↓\n"
            "transform with scaler learned ONLY from training fold\n"
            "   ↓\n"
            "score SVC\n"
            "```\n"
            "\n"
            "No validation-fold information is used to fit the scaler.\n"
            "\n"
            "### Why leakage can be catastrophic\n"
            "\n"
            "The chapter demonstrates leakage with a deliberately random "
            "dataset:\n"
            "\n"
            "```text\n"
            "100 samples\n"
            "10,000 random features\n"
            "random target\n"
            "```\n"
            "\n"
            "Because both `X` and `y` are random and independent, no real "
            "predictive relationship exists.\n"
            "\n"
            "But if feature selection is fitted on the full dataset **before** "
            "cross-validation, it can accidentally find random features that "
            "look correlated with the target.\n"
            "\n"
            "Then cross-validation may report an unrealistically strong score.\n"
            "\n"
            "The problem is not that Ridge suddenly learned a real pattern. The "
            "validation folds influenced which features were selected.\n"
            "\n"
            "Putting feature selection inside a pipeline fixes the procedure:\n"
            "\n"
            "```python\n"
            "from sklearn.feature_selection import SelectPercentile, f_regression\n"
            "from sklearn.linear_model import Ridge\n"
            "\n"
            "pipe = Pipeline([\n"
            "    ('select', SelectPercentile(\n"
            "        score_func=f_regression,\n"
            "        percentile=5,\n"
            "    )),\n"
            "    ('ridge', Ridge()),\n"
            "])\n"
            "```\n"
            "\n"
            "Now feature selection is recomputed from only the training fold in "
            "every cross-validation split.\n"
            "\n"
            "This is the correct evaluation.\n"
            "\n"
            "### Rule to remember\n"
            "\n"
            "> If a preprocessing step learns anything from the data, it belongs "
            "inside the cross-validation loop.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- scaling\n"
            "- feature selection\n"
            "- dimensionality reduction\n"
            "- learned feature extraction\n"
            "- imputation based on observed data\n"
            "\n"
            "### Accessing the best fitted pipeline\n"
            "\n"
            "After `GridSearchCV` finishes, the best full workflow is stored in:\n"
            "\n"
            "```python\n"
            "grid.best_estimator_\n"
            "```\n"
            "\n"
            "If that object is a pipeline, individual fitted steps can be "
            "accessed with `named_steps`:\n"
            "\n"
            "```python\n"
            "best_logreg = (\n"
            "    grid.best_estimator_\n"
            "        .named_steps['logisticregression']\n"
            ")\n"
            "\n"
            "coefficients = best_logreg.coef_\n"
            "```\n"
            "\n"
            "So using a pipeline does not hide the final model. You can still "
            "inspect its learned parameters.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Searching complete machine-learning workflows\n"
            "\n"
            "Pipelines allow us to tune more than model parameters. We can tune "
            "preprocessing and model choices together.\n"
            "\n"
            "This is powerful because the best preprocessing often depends on "
            "the model and the task.\n"
            "\n"
            "### Tune preprocessing and model parameters together\n"
            "\n"
            "Suppose a regression workflow contains:\n"
            "\n"
            "```text\n"
            "StandardScaler\n"
            "      ↓\n"
            "PolynomialFeatures\n"
            "      ↓\n"
            "Ridge\n"
            "```\n"
            "\n"
            "The pipeline can be created with:\n"
            "\n"
            "```python\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.preprocessing import StandardScaler, PolynomialFeatures\n"
            "from sklearn.linear_model import Ridge\n"
            "\n"
            "pipe = make_pipeline(\n"
            "    StandardScaler(),\n"
            "    PolynomialFeatures(),\n"
            "    Ridge(),\n"
            ")\n"
            "```\n"
            "\n"
            "Now we can search over both polynomial degree and Ridge alpha:\n"
            "\n"
            "```python\n"
            "param_grid = {\n"
            "    'polynomialfeatures__degree': [1, 2, 3],\n"
            "    'ridge__alpha': [0.001, 0.01, 0.1, 1, 10, 100],\n"
            "}\n"
            "```\n"
            "\n"
            "This lets cross-validation answer a larger question:\n"
            "\n"
            "> Which combination of representation **and** model regularization "
            "works best?\n"
            "\n"
            "That is more useful than tuning the model while treating "
            "preprocessing as fixed.\n"
            "\n"
            "### Search over which model to use\n"
            "\n"
            "A pipeline step itself can also be replaced during grid search.\n"
            "\n"
            "For example, define a generic two-step pipeline:\n"
            "\n"
            "```python\n"
            "pipe = Pipeline([\n"
            "    ('preprocessing', StandardScaler()),\n"
            "    ('classifier', SVC()),\n"
            "])\n"
            "```\n"
            "\n"
            "Then use a list of parameter grids to compare different workflows:\n"
            "\n"
            "```python\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "\n"
            "param_grid = [\n"
            "    {\n"
            "        'classifier': [SVC()],\n"
            "        'preprocessing': [StandardScaler(), None],\n"
            "        'classifier__C': [0.1, 1, 10],\n"
            "        'classifier__gamma': [0.01, 0.1, 1],\n"
            "    },\n"
            "    {\n"
            "        'classifier': [RandomForestClassifier(n_estimators=100)],\n"
            "        'preprocessing': [None],\n"
            "        'classifier__max_features': [1, 2, 3],\n"
            "    },\n"
            "]\n"
            "```\n"
            "\n"
            "`None` means that the preprocessing step is skipped for that "
            "candidate workflow.\n"
            "\n"
            "This makes it possible to compare combinations such as:\n"
            "\n"
            "```text\n"
            "StandardScaler + SVC\n"
            "No scaler + SVC\n"
            "No scaler + RandomForestClassifier\n"
            "```\n"
            "\n"
            "inside one systematic search.\n"
            "\n"
            "### Be careful with search-space size\n"
            "\n"
            "Grid search tries every combination in the specified grid.\n"
            "\n"
            "Suppose we search:\n"
            "\n"
            "```text\n"
            "3 polynomial degrees\n"
            "× 6 alpha values\n"
            "× 5 cross-validation folds\n"
            "```\n"
            "\n"
            "That already requires many model fits.\n"
            "\n"
            "Adding more preprocessing options, model families, and "
            "hyperparameters multiplies the work quickly.\n"
            "\n"
            "So pipeline search should be deliberate, not an attempt to try "
            "every imaginable combination.\n"
            "\n"
            "### Avoiding redundant computation with caching\n"
            "\n"
            "During a large grid search, the same expensive transformation may "
            "be recomputed many times.\n"
            "\n"
            "A pipeline can cache intermediate computations using `memory`:\n"
            "\n"
            "```python\n"
            "pipe = Pipeline(\n"
            "    [\n"
            "        ('preprocessing', StandardScaler()),\n"
            "        ('classifier', SVC()),\n"
            "    ],\n"
            "    memory='cache_folder',\n"
            ")\n"
            "```\n"
            "\n"
            "Caching is most useful when a transformation is expensive, such as "
            "PCA or another costly feature extraction step.\n"
            "\n"
            "For very cheap transformations such as simple scaling, reading and "
            "writing cached results to disk may cost more than recomputing them.\n"
            "\n"
            "### Why pipelines matter in practice\n"
            "\n"
            "A pipeline gives us one object representing the whole machine-"
            "learning workflow:\n"
            "\n"
            "```text\n"
            "preprocessing\n"
            "+ feature engineering\n"
            "+ feature selection\n"
            "+ model\n"
            "=\n"
            "one estimator\n"
            "```\n"
            "\n"
            "That provides several benefits:\n"
            "\n"
            "- fewer preprocessing mistakes\n"
            "- consistent train/test transformations\n"
            "- safer cross-validation\n"
            "- safer feature selection\n"
            "- easier grid search\n"
            "- shorter, clearer code\n"
            "- easier experimentation with whole workflows\n"
            "\n"
            "The most important benefit is not convenience. It is **correct "
            "evaluation**.\n"
            "\n"

            "{{exercise:M06.L01.EX02}}\n"
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
            "> If I never touch the final test set, preprocessing all training "
            "data before cross-validation cannot leak information.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Cross-validation creates validation folds inside the training set. "
            "If preprocessing was fitted on all training data first, each "
            "validation fold influenced that preprocessing. The validation "
            "process is therefore no longer independent.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Pipelines are mainly a shorter way to write preprocessing code.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Shorter code is useful, but the crucial benefit is that fitting and "
            "transforming happen in the correct place during cross-validation "
            "and parameter search.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> GridSearchCV can only tune parameters of the final model.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Pipeline parameters from any step can be tuned using the "
            "`step__parameter` syntax. Whole estimators and preprocessing steps "
            "can also be replaced during the search.\n"
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
            "| Algorithm chain | A sequence of preprocessing, transformation, and modeling steps |\n"
            "| Pipeline | A scikit-learn object that combines multiple processing steps into one estimator |\n"
            "| Transformer | A step that learns from data and produces a transformed representation |\n"
            "| Estimator | An object that can be fitted to data |\n"
            "| Information leakage | Validation or test information influencing training-time decisions |\n"
            "| Cross-validation fold | One train/validation split used during cross-validation |\n"
            "| GridSearchCV | Cross-validated search over combinations of hyperparameters |\n"
            "| `step__parameter` | Syntax used to address a parameter belonging to a pipeline step |\n"
            "| `named_steps` | Mapping used to access fitted estimators inside a pipeline |\n"
            "| `best_estimator_` | Best fitted estimator found by GridSearchCV |\n"
            "| `make_pipeline` | Convenience function that creates a pipeline with automatic step names |\n"
            "| Caching | Reusing intermediate computations to reduce repeated expensive work |\n"
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
            "1. Why can fitting a scaler before cross-validation create leakage?\n"
            "2. What does `pipe.fit(X_train, y_train)` do to intermediate transformers?\n"
            "3. What is the difference between fitting and transforming during prediction?\n"
            "4. How would you refer to the `C` parameter of a pipeline step named `svm`?\n"
            "5. Why should feature selection be inside the pipeline during cross-validation?\n"
            "6. How can you inspect coefficients from the best model found by GridSearchCV?\n"
            "7. How can a grid search compare different preprocessing steps or model families?\n"
            "8. Why can a very large pipeline grid become computationally expensive?\n"
            "9. When is pipeline caching most useful?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**If a processing step learns anything from the data, treat it as "
            "part of the model-building process and keep it inside the pipeline "
            "so cross-validation and grid search evaluate the complete workflow "
            "without leaking information.**\n"
        ),

        "estimated_minutes": 105,

        "has_code_examples": True,

        "sections": [
            {
                "id": "why-pipelines",
                "title": "Why machine-learning workflows need pipelines",
                "order": 1,
            },
            {
                "id": "building-pipelines",
                "title": "Building and using a scikit-learn Pipeline",
                "order": 2,
            },
            {
                "id": "pipelines-grid-search",
                "title": "Pipelines with GridSearchCV and cross-validation",
                "order": 3,
            },
            {
                "id": "searching-complete-workflows",
                "title": "Searching complete machine-learning workflows",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Build a Safe Scaling Pipeline",

            "lesson_code": "M06.L01",

            "section_id": "building-pipelines",

            "placement": "after_section",

            "description": (
                "Convert a manual preprocessing-and-model workflow into a "
                "single scikit-learn Pipeline."
            ),

            "instructions": (
                "You are given a classification dataset in X and y.\n"
                "\n"
                "1. Split the data into training and test sets.\n"
                "2. Create a Pipeline with StandardScaler followed by "
                "LogisticRegression.\n"
                "3. Fit the pipeline on the unscaled training data.\n"
                "4. Evaluate the pipeline directly on the unscaled test data.\n"
                "5. Explain which step learns the scaling parameters.\n"
                "6. Explain why you do not manually transform X_test before "
                "calling pipe.score."
            ),

            "expected_output": (
                "A short executable scikit-learn example plus an explanation of "
                "how the pipeline handles training and test transformations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "pipeline-construction",
                "fit-transform-flow",
                "safe-preprocessing",
                "scikit-learn",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Fix a Leaky Grid Search",

            "lesson_code": "M06.L01",

            "section_id": "searching-complete-workflows",

            "placement": "after_section",

            "description": (
                "Identify information leakage and redesign the workflow so "
                "preprocessing is evaluated correctly inside cross-validation."
            ),

            "instructions": (
                "A teammate writes the following workflow:\n"
                "\n"
                "1. Fit SelectPercentile on all of X_train and y_train.\n"
                "2. Transform all of X_train.\n"
                "3. Run GridSearchCV on Ridge using the transformed training data.\n"
                "\n"
                "Answer the following:\n"
                "\n"
                "1. Explain precisely where leakage occurs.\n"
                "2. Build a Pipeline containing SelectPercentile and Ridge.\n"
                "3. Create a parameter grid that searches both the feature "
                "selection percentile and Ridge alpha.\n"
                "4. Explain what happens to SelectPercentile in each CV fold.\n"
                "5. Explain why this gives a more trustworthy validation score.\n"
                "6. State one reason why the new grid search may require more computation."
            ),

            "expected_output": (
                "A corrected Pipeline + GridSearchCV design and a short written "
                "explanation of why the original workflow was invalid."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "information-leakage",
                "cross-validation",
                "pipeline-grid-search",
                "feature-selection",
                "reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "Algorithm Chains and Pipelines — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",

                "section_id": "why-pipelines",

                "question": (
                    "Why is fitting a scaler on all training data before "
                    "GridSearchCV potentially problematic?"
                ),

                "options": [
                    "The scaler makes the data too small",
                    "The scaler has already used information from validation folds",
                    "GridSearchCV cannot work with scaled data",
                    "SVC cannot be used after MinMaxScaler",
                ],

                "correct": 1,

                "explanation": (
                    "Cross-validation validation folds are part of the original "
                    "training set. If the scaler is fitted before the folds are "
                    "created, information from those validation folds influences "
                    "the learned preprocessing."
                ),
            },

            {
                "id": "M06.L01.Q02",

                "section_id": "building-pipelines",

                "question": (
                    "What happens when `pipe.fit(X_train, y_train)` is called on "
                    "a pipeline containing a scaler followed by a classifier?"
                ),

                "options": [
                    "Only the classifier is fitted",
                    "The classifier is fitted first and then the scaler",
                    "The scaler is fitted and transforms the data before the classifier is fitted",
                    "Both steps receive the test set automatically",
                ],

                "correct": 2,

                "explanation": (
                    "Intermediate transformers are fitted and used to transform "
                    "the data in order. The final estimator is then fitted on "
                    "the transformed representation."
                ),
            },

            {
                "id": "M06.L01.Q03",

                "section_id": "pipelines-grid-search",

                "question": (
                    "A pipeline step is named `svm`. Which key correctly tunes "
                    "its `C` parameter in GridSearchCV?"
                ),

                "options": [
                    "C__svm",
                    "svm_C",
                    "svm.C",
                    "svm__C",
                ],

                "correct": 3,

                "explanation": (
                    "Pipeline parameters use the syntax "
                    "`step_name__parameter_name`, with a double underscore."
                ),
            },

            {
                "id": "M06.L01.Q04",

                "section_id": "searching-complete-workflows",

                "question": (
                    "Which statement about GridSearchCV and pipelines is correct?"
                ),

                "options": [
                    "Only parameters of the final estimator can be tuned",
                    "Preprocessing parameters and model parameters can be tuned together",
                    "A pipeline cannot compare different model families",
                    "A preprocessing step can never be skipped",
                ],

                "correct": 1,

                "explanation": (
                    "GridSearchCV can search parameters from any pipeline step, "
                    "and can even replace whole preprocessing or estimator steps."
                ),
            },

            {
                "id": "M06.L01.Q05",

                "section_id": "searching-complete-workflows",

                "type": "open",

                "question": (
                    "You need to compare StandardScaler + SVC against an "
                    "unscaled RandomForestClassifier. Describe how you would "
                    "structure the pipeline and parameter grid so both workflows "
                    "are evaluated fairly within the same GridSearchCV."
                ),
            },
        ],

        "passing_score": 70,
    },
}
