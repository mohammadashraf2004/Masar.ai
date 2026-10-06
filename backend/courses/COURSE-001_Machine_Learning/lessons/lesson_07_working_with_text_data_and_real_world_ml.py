"""M07.L01 — Working with Text Data and Real-World Machine Learning.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-001, Chapters 7–8, pages not provided in extracted source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M07.L01"

MODULE_ORDER = 7

MODULE_TITLE = "Text Data and Real-World Machine Learning"

MODULE_DESCRIPTION = (
    "Learn how to represent text for machine learning, build and interpret text "
    "classification and topic models, and connect model development to problem "
    "definition, production deployment, live testing, and scalable ML practice."
)

SOURCE_CHAPTER = "7–8"

SOURCE_PAGES = "Not provided in extracted source text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Working with Text Data and Real-World Machine Learning",

    "slug": "ml-foundations-m07-l01",

    "description": (
        "Turn raw text into machine-learning features using bag-of-words, tf-idf, "
        "n-grams, token normalization, and topic modeling, then connect those "
        "techniques to a complete real-world ML workflow from problem framing "
        "through production and online evaluation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "machine-learning",
        "nlp",
        "text-data",
        "bag-of-words",
        "count-vectorizer",
        "tfidf",
        "ngrams",
        "stemming",
        "lemmatization",
        "topic-modeling",
        "lda",
        "model-interpretation",
        "production-ml",
        "ab-testing",
        "custom-estimators",
        "scaling",
        "module-07",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Working with Text Data and Real-World Machine Learning",

        "content": (
            "# Working with Text Data and Real-World Machine Learning\n"
            "\n"
            "> **Course:** Machine Learning Foundations  \n"
            "> **Lesson:** M07.L01  \n"
            "> **Module:** Text Data and Real-World Machine Learning  \n"
            "> **Source alignment:** BOOK-001, Chapters 7–8. The extracted "
            "source text does not provide page numbers. This lesson is an "
            "instructor-authored curriculum adaptation rather than a "
            "reproduction of the source text.\n"
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
            "- Distinguish free-form text from categorical and structured strings.\n"
            "- Explain how bag-of-words converts documents into numeric features.\n"
            "- Use CountVectorizer and TfidfVectorizer to represent text.\n"
            "- Explain the role of `min_df`, stopwords, tf-idf, and sparse matrices.\n"
            "- Explain why n-grams can capture context that single words miss.\n"
            "- Distinguish stemming from lemmatization.\n"
            "- Interpret coefficients of a linear text classifier.\n"
            "- Explain the basic idea of topic modeling with Latent Dirichlet Allocation.\n"
            "- Frame a machine-learning problem before choosing an algorithm.\n"
            "- Explain when humans should remain in the decision loop.\n"
            "- Distinguish offline evaluation from online testing such as A/B testing.\n"
            "- Explain why production ML requires software-engineering concerns beyond accuracy.\n"
            "- Describe when a custom scikit-learn estimator or large-scale learning strategy may be needed.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Text is a different kind of machine-learning input\n"
            "\n"
            "Most machine-learning algorithms expect each sample to be represented "
            "by a fixed collection of numerical features. Text does not naturally "
            "look like that.\n"
            "\n"
            "Consider these examples:\n"
            "\n"
            "```text\n"
            "\"Great movie. I loved the ending.\"\n"
            "\"The product stopped working after two days.\"\n"
            "\"Please reset my password.\"\n"
            "```\n"
            "\n"
            "The strings have different lengths, different words, and different "
            "structures. Before a conventional machine-learning model can use "
            "them, we need to convert them into numbers.\n"
            "\n"
            "### Not every string should be treated as free-form text\n"
            "\n"
            "A string-valued column can represent several different things:\n"
            "\n"
            "1. **Categorical data** — a fixed set such as `red`, `green`, and `blue`.\n"
            "2. **Free strings that should be mapped into categories** — manually "
            "entered values such as `grey`, `gray`, or misspelled category names.\n"
            "3. **Structured strings** — dates, phone numbers, addresses, names, or identifiers.\n"
            "4. **Free-form text** — reviews, emails, chat messages, articles, and documents.\n"
            "\n"
            "How you process the field depends on what the string means, not just "
            "on the fact that Python stores it as a string.\n"
            "\n"
            "### Corpus and document\n"
            "\n"
            "In text analysis:\n"
            "\n"
            "- a **document** is one text sample,\n"
            "- a **corpus** is the complete collection of documents.\n"
            "\n"
            "For movie-review sentiment analysis, every review is a document and "
            "all reviews together form the corpus.\n"
            "\n"
            "### Running example: sentiment analysis\n"
            "\n"
            "Chapter 7 uses IMDb movie reviews as a running example. Reviews are "
            "labeled positive or negative, so the final task is supervised binary "
            "classification.\n"
            "\n"
            "However, the first challenge is representation:\n"
            "\n"
            "```text\n"
            "raw review text\n"
            "      |\n"
            "      v\n"
            "numeric feature vector\n"
            "      |\n"
            "      v\n"
            "classifier\n"
            "      |\n"
            "      v\n"
            "positive / negative\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Bag-of-words: turning text into numbers\n"
            "\n"
            "Bag-of-words is one of the simplest and most useful traditional text "
            "representations.\n"
            "\n"
            "It deliberately ignores much of the original structure of a document "
            "and focuses on which words occur and how often they occur.\n"
            "\n"
            "The process has three main steps.\n"
            "\n"
            "### Step 1 — Tokenization\n"
            "\n"
            "Split a document into units called tokens.\n"
            "\n"
            "```text\n"
            "\"machine learning is useful\"\n"
            "\n"
            "-> [\"machine\", \"learning\", \"is\", \"useful\"]\n"
            "```\n"
            "\n"
            "### Step 2 — Build the vocabulary\n"
            "\n"
            "Collect the unique tokens observed in the training corpus.\n"
            "\n"
            "Suppose our corpus contains:\n"
            "\n"
            "```text\n"
            "\"good movie\"\n"
            "\"bad movie\"\n"
            "\"good acting\"\n"
            "```\n"
            "\n"
            "A possible vocabulary is:\n"
            "\n"
            "```text\n"
            "acting\n"
            "bad\n"
            "good\n"
            "movie\n"
            "```\n"
            "\n"
            "Each vocabulary term becomes one feature.\n"
            "\n"
            "### Step 3 — Encode each document\n"
            "\n"
            "Count how often each vocabulary word occurs.\n"
            "\n"
            "Using the vocabulary above:\n"
            "\n"
            "```text\n"
            "document: \"good movie\"\n"
            "\n"
            "acting = 0\n"
            "bad    = 0\n"
            "good   = 1\n"
            "movie  = 1\n"
            "\n"
            "vector = [0, 0, 1, 1]\n"
            "```\n"
            "\n"
            "### CountVectorizer\n"
            "\n"
            "scikit-learn implements bag-of-words with `CountVectorizer`.\n"
            "\n"
            "```python\n"
            "from sklearn.feature_extraction.text import CountVectorizer\n"
            "\n"
            "documents = [\n"
            "    \"good movie\",\n"
            "    \"bad movie\",\n"
            "    \"good acting\",\n"
            "]\n"
            "\n"
            "vectorizer = CountVectorizer()\n"
            "X = vectorizer.fit_transform(documents)\n"
            "\n"
            "print(vectorizer.get_feature_names_out())\n"
            "print(X.toarray())\n"
            "```\n"
            "\n"
            "`fit` learns the vocabulary from the training documents. `transform` "
            "uses that learned vocabulary to encode documents.\n"
            "\n"
            "### Why sparse matrices matter\n"
            "\n"
            "Real text vocabularies can contain tens of thousands of features, "
            "while each document uses only a small fraction of them.\n"
            "\n"
            "A document vector might conceptually look like:\n"
            "\n"
            "```text\n"
            "[0, 0, 0, 3, 0, 0, 1, 0, 0, 0, ...]\n"
            "```\n"
            "\n"
            "Most values are zero. A sparse matrix stores primarily the nonzero "
            "entries instead of wasting memory on every zero.\n"
            "\n"
            "In the chapter's IMDb example, bag-of-words produces tens of "
            "thousands of vocabulary features, which is exactly the kind of "
            "high-dimensional sparse representation where linear models such as "
            "logistic regression can work well.\n"
            "\n"
            "### Unknown words at prediction time\n"
            "\n"
            "If a new document contains a word that was not present when the "
            "vectorizer learned its vocabulary, that word is not represented by "
            "an existing feature and is ignored by the basic CountVectorizer "
            "workflow.\n"
            "\n"
            "This is another reason to learn the vocabulary from training data "
            "and then reuse that fitted representation on later data.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Improving the text representation\n"
            "\n"
            "A raw bag-of-words vocabulary can contain many rare, noisy, or very "
            "common words. We can modify how features are created and weighted.\n"
            "\n"
            "### Removing extremely rare tokens with `min_df`\n"
            "\n"
            "A token that appears in only one training document may not provide "
            "much reusable information.\n"
            "\n"
            "```python\n"
            "vectorizer = CountVectorizer(min_df=5)\n"
            "```\n"
            "\n"
            "This keeps only tokens that appear in at least five documents.\n"
            "\n"
            "In the chapter's IMDb example, this greatly reduces the vocabulary "
            "size while preserving similar validation performance.\n"
            "\n"
            "### Stopwords\n"
            "\n"
            "Stopwords are extremely common words that may carry little useful "
            "information for a particular task.\n"
            "\n"
            "Examples in English include words such as:\n"
            "\n"
            "```text\n"
            "the\n"
            "and\n"
            "of\n"
            "to\n"
            "```\n"
            "\n"
            "A vectorizer can use a predefined stopword list:\n"
            "\n"
            "```python\n"
            "vectorizer = CountVectorizer(\n"
            "    min_df=5,\n"
            "    stop_words=\"english\",\n"
            ")\n"
            "```\n"
            "\n"
            "However, a fixed stopword list does not automatically improve every "
            "model. The chapter's experiment slightly reduced performance, "
            "illustrating an important lesson: preprocessing choices should be "
            "validated rather than assumed to help.\n"
            "\n"
            "### tf-idf\n"
            "\n"
            "Term frequency–inverse document frequency changes the weight of each "
            "word instead of simply counting it.\n"
            "\n"
            "The intuition is:\n"
            "\n"
            "> A word can be informative if it occurs often in one document but "
            "does not occur in most documents in the corpus.\n"
            "\n"
            "Very common words are downweighted because they do little to "
            "distinguish one document from another.\n"
            "\n"
            "scikit-learn offers `TfidfVectorizer`, which performs tokenization, "
            "vocabulary construction, counting, and tf-idf weighting.\n"
            "\n"
            "```python\n"
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "\n"
            "vectorizer = TfidfVectorizer(min_df=5)\n"
            "X_train = vectorizer.fit_transform(text_train)\n"
            "X_test = vectorizer.transform(text_test)\n"
            "```\n"
            "\n"
            "### Put data-dependent text preprocessing inside the pipeline\n"
            "\n"
            "tf-idf learns statistics from the training corpus, so it must be "
            "inside the cross-validation process when we tune a model.\n"
            "\n"
            "```python\n"
            "from sklearn.pipeline import make_pipeline\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import GridSearchCV\n"
            "\n"
            "pipe = make_pipeline(\n"
            "    TfidfVectorizer(min_df=5),\n"
            "    LogisticRegression(max_iter=1000),\n"
            ")\n"
            "\n"
            "param_grid = {\n"
            "    \"logisticregression__C\": [0.01, 0.1, 1, 10]\n"
            "}\n"
            "\n"
            "grid = GridSearchCV(pipe, param_grid, cv=5)\n"
            "grid.fit(text_train, y_train)\n"
            "```\n"
            "\n"
            "This ensures the vectorizer is fitted only on each cross-validation "
            "training fold rather than leaking information from the corresponding "
            "validation fold.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Model interpretation and n-grams\n"
            "\n"
            "One advantage of traditional text models is that their features are "
            "often human-readable.\n"
            "\n"
            "### Inspecting model coefficients\n"
            "\n"
            "For a linear logistic-regression sentiment model, each text feature "
            "receives a learned coefficient.\n"
            "\n"
            "Large positive coefficients indicate features that push predictions "
            "toward the positive-review class. Large negative coefficients push "
            "toward the negative-review class.\n"
            "\n"
            "This allows us to inspect whether the model learned reasonable "
            "signals, suspicious shortcuts, or dataset-specific artifacts.\n"
            "\n"
            "For example, words such as `excellent` and `wonderful` may receive "
            "positive coefficients, while `worst` and `disappointment` may "
            "receive negative coefficients.\n"
            "\n"
            "### The weakness of single-word bag-of-words\n"
            "\n"
            "Consider:\n"
            "\n"
            "```text\n"
            "\"bad, not good\"\n"
            "\"good, not bad\"\n"
            "```\n"
            "\n"
            "A unigram bag-of-words representation sees nearly the same individual "
            "words in both sentences and discards their order.\n"
            "\n"
            "### n-grams\n"
            "\n"
            "An n-gram is a sequence of neighboring tokens.\n"
            "\n"
            "```text\n"
            "1 token  -> unigram\n"
            "2 tokens -> bigram\n"
            "3 tokens -> trigram\n"
            "```\n"
            "\n"
            "For the sentence:\n"
            "\n"
            "```text\n"
            "\"this movie is not good\"\n"
            "```\n"
            "\n"
            "some bigrams are:\n"
            "\n"
            "```text\n"
            "\"this movie\"\n"
            "\"movie is\"\n"
            "\"is not\"\n"
            "\"not good\"\n"
            "```\n"
            "\n"
            "`not good` preserves contextual information that the isolated word "
            "`good` cannot capture by itself.\n"
            "\n"
            "```python\n"
            "vectorizer = TfidfVectorizer(\n"
            "    min_df=5,\n"
            "    ngram_range=(1, 2),\n"
            ")\n"
            "```\n"
            "\n"
            "This keeps both unigrams and bigrams.\n"
            "\n"
            "Longer n-grams create many more features. They can capture useful "
            "phrases, but they can also create highly specific features and "
            "increase computation or overfitting risk.\n"
            "\n"
            "In the chapter's IMDb experiment, adding bigrams improved validation "
            "performance clearly, while trigrams added only a small additional "
            "benefit.\n"
            "\n"

            "{{exercise:M07.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. Advanced tokenization, stemming, and lemmatization\n"
            "\n"
            "Different surface forms of a word may express closely related ideas:\n"
            "\n"
            "```text\n"
            "draw\n"
            "drawing\n"
            "draws\n"
            "drawn\n"
            "```\n"
            "\n"
            "Treating all of these as unrelated features can make the vocabulary "
            "larger and reduce how much evidence each feature receives.\n"
            "\n"
            "### Stemming\n"
            "\n"
            "Stemming applies rule-based transformations that shorten words to a "
            "common stem.\n"
            "\n"
            "The result does not have to be a valid dictionary word.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "meeting -> meet\n"
            "worse   -> wors\n"
            "```\n"
            "\n"
            "Stemming is relatively simple and fast, but its output can be crude.\n"
            "\n"
            "### Lemmatization\n"
            "\n"
            "Lemmatization tries to map a word to a linguistically meaningful "
            "base form called a lemma.\n"
            "\n"
            "It can use information about a word's role in the sentence.\n"
            "\n"
            "For example, a word such as `meeting` may remain `meeting` when it "
            "is used as a noun but become `meet` when used as a verb.\n"
            "\n"
            "Lemmatization is more involved than stemming but can produce more "
            "linguistically meaningful normalization.\n"
            "\n"
            "### Why normalization can help\n"
            "\n"
            "Combining related word forms reduces the number of independent "
            "features. This can behave somewhat like regularization because the "
            "model receives more shared evidence for related forms.\n"
            "\n"
            "The chapter's experiment reduced the vocabulary substantially with "
            "lemmatization and found a modest improvement in a deliberately "
            "small-data setting. The exact benefit depends on the dataset.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Topic modeling with Latent Dirichlet Allocation\n"
            "\n"
            "Text can also be analyzed without using labels.\n"
            "\n"
            "Topic modeling tries to discover recurring patterns of words across "
            "a corpus. A document can be associated with one or several topics.\n"
            "\n"
            "### LDA intuition\n"
            "\n"
            "Latent Dirichlet Allocation, abbreviated LDA in this context, "
            "assumes that documents can be represented as mixtures of topics and "
            "that topics are characterized by groups of words that tend to occur "
            "together.\n"
            "\n"
            "Imagine a news corpus. One discovered component might strongly "
            "weight words such as:\n"
            "\n"
            "```text\n"
            "team, score, season, player\n"
            "```\n"
            "\n"
            "Another might emphasize:\n"
            "\n"
            "```text\n"
            "vote, government, election, party\n"
            "```\n"
            "\n"
            "We might interpret those components as sports and politics.\n"
            "\n"
            "However, LDA does not know those human labels. It only discovers "
            "statistical patterns in word co-occurrence.\n"
            "\n"
            "A component might instead correspond to an author's writing style, "
            "positive-review language, or another pattern that humans would not "
            "normally call a topic.\n"
            "\n"
            "### Basic workflow\n"
            "\n"
            "```python\n"
            "from sklearn.feature_extraction.text import CountVectorizer\n"
            "from sklearn.decomposition import LatentDirichletAllocation\n"
            "\n"
            "vectorizer = CountVectorizer(\n"
            "    max_features=10000,\n"
            "    max_df=0.15,\n"
            ")\n"
            "\n"
            "X = vectorizer.fit_transform(text_train)\n"
            "\n"
            "lda = LatentDirichletAllocation(\n"
            "    n_components=10,\n"
            "    learning_method=\"batch\",\n"
            "    max_iter=25,\n"
            "    random_state=0,\n"
            ")\n"
            "\n"
            "document_topics = lda.fit_transform(X)\n"
            "```\n"
            "\n"
            "The source text uses the older parameter name `n_topics`; current "
            "scikit-learn versions use `n_components` for the number of topics.\n"
            "\n"
            "### Interpreting topics responsibly\n"
            "\n"
            "A topic is usually inspected by looking at its highest-weighted "
            "words and then reading documents that receive high weight for that "
            "topic.\n"
            "\n"
            "This second step is important. Human-readable names such as "
            "`music`, `horror`, or `negative reviews` are our interpretations, "
            "not labels supplied by the algorithm.\n"
            "\n"
            "Topic models are randomized, and changing settings or the random "
            "seed can produce different components. Conclusions should therefore "
            "be checked against actual documents rather than inferred only from "
            "a short list of top words.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Step back: define the machine-learning problem first\n"
            "\n"
            "Chapter 8 shifts from individual techniques to a broader lesson: "
            "the machine-learning algorithm is only one part of a larger "
            "decision-making process.\n"
            "\n"
            "Before choosing an algorithm, ask:\n"
            "\n"
            "```text\n"
            "What question am I trying to answer?\n"
            "How will success be measured?\n"
            "Do I have the right data?\n"
            "What happens if the system succeeds?\n"
            "What happens when it makes mistakes?\n"
            "```\n"
            "\n"
            "### Start with impact, not with a favorite model\n"
            "\n"
            "Suppose the goal is fraud detection.\n"
            "\n"
            "It is not enough to ask whether a classifier can achieve high "
            "accuracy. We also need to know whether detecting additional fraud "
            "has enough practical value to justify building and maintaining the "
            "system.\n"
            "\n"
            "The best metric is ideally connected to the real business or "
            "research objective, such as reducing losses, increasing revenue, "
            "reducing response time, or preventing harmful outcomes.\n"
            "\n"
            "### Model development is a feedback loop\n"
            "\n"
            "A realistic workflow often looks like:\n"
            "\n"
            "```text\n"
            "define problem\n"
            "    |\n"
            "collect data\n"
            "    |\n"
            "clean / represent data\n"
            "    |\n"
            "train model\n"
            "    |\n"
            "analyze errors\n"
            "    |\n"
            "reformulate task or collect better data\n"
            "    |\n"
            "repeat\n"
            "```\n"
            "\n"
            "Analyzing mistakes can reveal missing information or weaknesses in "
            "the problem formulation. Sometimes better data produces more value "
            "than endless hyperparameter tuning.\n"
            "\n"
            "### Humans in the loop\n"
            "\n"
            "Not every model needs to make every decision automatically.\n"
            "\n"
            "A useful system can automatically handle easy, high-confidence cases "
            "and send uncertain or high-risk cases to a human.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "model confidence high -> automated action\n"
            "model uncertain       -> human review\n"
            "```\n"
            "\n"
            "Whether this is possible depends on the application. A system that "
            "must react instantly has different constraints from one where a "
            "human can review difficult cases before action is taken.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. From prototype to production and live evaluation\n"
            "\n"
            "A notebook that produces accurate predictions is not automatically "
            "a production-ready ML system.\n"
            "\n"
            "Production introduces additional requirements such as:\n"
            "\n"
            "- reliability,\n"
            "- predictable behavior,\n"
            "- runtime,\n"
            "- memory usage,\n"
            "- integration with existing systems,\n"
            "- maintainability,\n"
            "- and operational complexity.\n"
            "\n"
            "A small accuracy improvement may not be worth a major increase in "
            "system complexity.\n"
            "\n"
            "### Offline evaluation\n"
            "\n"
            "Evaluation on a held-out test dataset is **offline evaluation**.\n"
            "\n"
            "It answers questions such as:\n"
            "\n"
            "```text\n"
            "How accurately does the model predict stored examples?\n"
            "```\n"
            "\n"
            "Offline evaluation is essential, but user-facing systems often need "
            "another level of testing.\n"
            "\n"
            "### Online testing\n"
            "\n"
            "Once users interact with a model, the model can change their "
            "behavior in ways that an offline dataset did not capture.\n"
            "\n"
            "For example, changing recommendations might alter what users click, "
            "buy, watch, or ignore.\n"
            "\n"
            "### A/B testing\n"
            "\n"
            "A/B testing compares two versions of a system on real users.\n"
            "\n"
            "```text\n"
            "Group A -> system/model A\n"
            "Group B -> system/model B\n"
            "\n"
            "measure relevant outcome for both groups\n"
            "```\n"
            "\n"
            "The important point is that success is evaluated using a real-world "
            "metric rather than only an offline model score.\n"
            "\n"
            "Online testing can reveal unexpected behavioral effects that are "
            "invisible in a static test set.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 9
            # ----------------------------------------------------------------

            "## 9. Custom estimators and scaling beyond memory\n"
            "\n"
            "Sometimes your preprocessing or prediction logic is not available as "
            "a built-in scikit-learn component.\n"
            "\n"
            "If that processing depends on training data and must participate in "
            "cross-validation or grid search, wrapping it in the scikit-learn "
            "estimator interface can make the workflow safer and easier to reuse.\n"
            "\n"
            "### A simple custom transformer\n"
            "\n"
            "```python\n"
            "from sklearn.base import BaseEstimator, TransformerMixin\n"
            "\n"
            "class AddOneTransformer(BaseEstimator, TransformerMixin):\n"
            "    def __init__(self):\n"
            "        pass\n"
            "\n"
            "    def fit(self, X, y=None):\n"
            "        return self\n"
            "\n"
            "    def transform(self, X):\n"
            "        return X + 1\n"
            "```\n"
            "\n"
            "The important interface pattern is:\n"
            "\n"
            "```text\n"
            "__init__ -> store configuration\n"
            "fit      -> learn from training data and return self\n"
            "transform -> transform X\n"
            "```\n"
            "\n"
            "A custom classifier or regressor uses a similar interface but "
            "implements prediction behavior.\n"
            "\n"
            "This allows custom components to participate in pipelines, "
            "cross-validation, and parameter search rather than being performed "
            "as unsafe preprocessing outside the evaluation workflow.\n"
            "\n"
            "### What if the dataset no longer fits in memory?\n"
            "\n"
            "The book discusses two broad strategies.\n"
            "\n"
            "#### Out-of-core learning\n"
            "\n"
            "Read the data in chunks that fit into memory and update a compatible "
            "model incrementally.\n"
            "\n"
            "```text\n"
            "disk/network\n"
            "    |\n"
            "    v\n"
            "small chunk -> update model -> discard chunk\n"
            "    |\n"
            "    v\n"
            "next chunk\n"
            "```\n"
            "\n"
            "This allows one machine to learn from more data than it can hold in "
            "RAM at once, though not every algorithm supports incremental updates.\n"
            "\n"
            "#### Distributed processing\n"
            "\n"
            "Another strategy is to distribute work over multiple machines in a "
            "compute cluster.\n"
            "\n"
            "This can process much larger datasets but requires significantly "
            "more infrastructure and operational complexity.\n"
            "\n"
            "The correct solution depends on whether the extra scale justifies "
            "the complexity.\n"
            "\n"

            "{{exercise:M07.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 10
            # ----------------------------------------------------------------

            "## 10. The complete mental model\n"
            "\n"
            "The two chapters fit together into one useful end-to-end workflow.\n"
            "\n"
            "```text\n"
            "1. Define the real problem and success metric.\n"
            "2. Inspect the data and understand what each feature actually means.\n"
            "3. Build an appropriate representation.\n"
            "4. Train a simple baseline model.\n"
            "5. Evaluate correctly with held-out or cross-validation data.\n"
            "6. Inspect errors and model behavior.\n"
            "7. Improve the representation or collect better data.\n"
            "8. Tune only when the evaluation procedure is trustworthy.\n"
            "9. Package preprocessing and prediction into a reproducible pipeline.\n"
            "10. Evaluate the final system offline.\n"
            "11. Deploy only when reliability and operational requirements are met.\n"
            "12. Measure real-world impact with appropriate online evaluation when applicable.\n"
            "13. Monitor what you learn and feed it back into the next iteration.\n"
            "```\n"
            "\n"
            "For text problems specifically, a strong traditional baseline can "
            "often be surprisingly simple:\n"
            "\n"
            "```text\n"
            "raw text\n"
            "   |\n"
            "TfidfVectorizer\n"
            "   |\n"
            "unigrams + useful bigrams\n"
            "   |\n"
            "linear classifier\n"
            "   |\n"
            "cross-validation\n"
            "   |\n"
            "error / coefficient inspection\n"
            "```\n"
            "\n"
            "The broader lesson is that good machine learning depends as much on "
            "representation, evaluation, problem definition, and system design as "
            "it does on the choice of algorithm.\n"
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
            "> Any column stored as a string should be processed with NLP techniques.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A string may actually represent a category, identifier, date, phone "
            "number, or another structured concept. The representation must follow "
            "the semantic meaning of the field.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Bag-of-words understands sentence meaning.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Basic bag-of-words counts tokens and largely discards order and "
            "syntax. n-grams recover some local context, but the representation "
            "still does not understand language in a human sense.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> tf-idf tells us which words are most predictive of the target label.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "tf-idf is an unsupervised weighting scheme based on word occurrence "
            "patterns across documents. A high tf-idf weight means a term is "
            "distinctive for a document, not necessarily predictive of sentiment "
            "or another target.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> A discovered LDA topic has an objectively correct human meaning.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The model learns statistical components. Topic names are human "
            "interpretations and should be verified by inspecting representative "
            "documents.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Once a model performs well on a test set, the machine-learning "
            "project is finished.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Production systems must also satisfy requirements such as "
            "reliability, runtime, maintainability, and real-world impact. "
            "User-facing models may require online evaluation after offline "
            "testing.\n"
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
            "| Corpus | Collection of documents used for text analysis |\n"
            "| Document | One text sample in a corpus |\n"
            "| Token | Basic text unit used as a feature, often a word |\n"
            "| Vocabulary | Set of tokens learned from the training corpus |\n"
            "| Bag-of-words | Representation based on token occurrence counts |\n"
            "| Sparse matrix | Matrix representation that stores mainly nonzero entries |\n"
            "| Stopword | Very common word that may carry little task-specific information |\n"
            "| tf-idf | Weighting that emphasizes terms frequent in a document but less common across documents |\n"
            "| Unigram | One-token feature |\n"
            "| Bigram | Two neighboring tokens used as one feature |\n"
            "| Trigram | Three neighboring tokens used as one feature |\n"
            "| Stemming | Rule-based reduction of word forms to a stem |\n"
            "| Lemmatization | Linguistic normalization to a base lemma |\n"
            "| Topic modeling | Unsupervised discovery of recurring latent word patterns in documents |\n"
            "| LDA | Latent Dirichlet Allocation, a probabilistic topic-modeling method |\n"
            "| Human in the loop | Workflow where people review or handle cases the model should not decide alone |\n"
            "| Offline evaluation | Evaluation on stored held-out data |\n"
            "| Online testing | Evaluation after the system interacts with real users or environment |\n"
            "| A/B testing | Controlled comparison of two system variants on different user groups |\n"
            "| Estimator | scikit-learn-style object exposing methods such as fit, transform, or predict |\n"
            "| Out-of-core learning | Incremental learning from data chunks that do not all fit in memory |\n"
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
            "1. Why must free-form text be converted into a numerical representation before using most classical ML algorithms?\n"
            "2. What are the three main steps of bag-of-words encoding?\n"
            "3. Why is a sparse matrix useful for text features?\n"
            "4. What does `min_df=5` change in a CountVectorizer vocabulary?\n"
            "5. What is the intuition behind tf-idf?\n"
            "6. Why can the bigram `not good` be more useful than the unigram `good`?\n"
            "7. How does lemmatization differ from stemming?\n"
            "8. Why must LDA topics be inspected rather than blindly given semantic labels?\n"
            "9. What questions should be answered before choosing a machine-learning algorithm?\n"
            "10. What is the difference between offline evaluation and A/B testing?\n"
            "11. Why might a human-in-the-loop system be preferable to full automation?\n"
            "12. Why can a simpler production model be preferable even when a more complex model has slightly better offline accuracy?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Machine learning is not only about fitting an algorithm. For text, "
            "the representation determines what the model can learn; for real "
            "systems, problem framing, evaluation, human oversight, deployment, "
            "and real-world impact determine whether the model is actually useful.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "sections": [
            {
                "id": "text-as-data",
                "title": "Text is a different kind of machine-learning input",
                "order": 1,
            },
            {
                "id": "bag-of-words",
                "title": "Bag-of-words: turning text into numbers",
                "order": 2,
            },
            {
                "id": "improving-text-features",
                "title": "Improving the text representation",
                "order": 3,
            },
            {
                "id": "context-and-interpretation",
                "title": "Model interpretation and n-grams",
                "order": 4,
            },
            {
                "id": "token-normalization",
                "title": "Advanced tokenization, stemming, and lemmatization",
                "order": 5,
            },
            {
                "id": "topic-modeling",
                "title": "Topic modeling with Latent Dirichlet Allocation",
                "order": 6,
            },
            {
                "id": "problem-framing",
                "title": "Step back: define the machine-learning problem first",
                "order": 7,
            },
            {
                "id": "production-and-testing",
                "title": "From prototype to production and live evaluation",
                "order": 8,
            },
            {
                "id": "custom-estimators-and-scale",
                "title": "Custom estimators and scaling beyond memory",
                "order": 9,
            },
            {
                "id": "complete-ml-workflow",
                "title": "The complete mental model",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M07.L01.EX01",

            "title": "Build and Inspect a Traditional Text Classifier",

            "lesson_code": "M07.L01",

            "section_id": "context-and-interpretation",

            "placement": "after_section",

            "description": (
                "Build a leakage-safe text-classification pipeline, compare "
                "unigrams with n-grams, and inspect what the linear model learned."
            ),

            "instructions": (
                "1. Create or load a small labeled text-classification dataset.\n"
                "2. Split the data into training and test sets.\n"
                "3. Build a Pipeline containing TfidfVectorizer and LogisticRegression.\n"
                "4. Use GridSearchCV to compare at least `ngram_range=(1, 1)` and "
                "`ngram_range=(1, 2)`.\n"
                "5. Record the best cross-validation configuration.\n"
                "6. Evaluate the selected pipeline on the untouched test set.\n"
                "7. Inspect several high-magnitude positive and negative model coefficients.\n"
                "8. Explain one useful phrase-level feature and one possible misleading feature."
            ),

            "expected_output": (
                "A notebook or script containing the complete text pipeline, "
                "cross-validation comparison, test result, and a short table of "
                "interpreted model features."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "text-vectorization",
                "tfidf",
                "ngrams",
                "pipelines",
                "cross-validation",
                "model-interpretation",
            ],
        },

        {
            "id": "M07.L01.EX02",

            "title": "Design the Full Lifecycle of a Text ML System",

            "lesson_code": "M07.L01",

            "section_id": "custom-estimators-and-scale",

            "placement": "after_section",

            "description": (
                "Connect text modeling decisions to problem framing, human "
                "review, deployment, live testing, and scaling."
            ),

            "instructions": (
                "Imagine you are building a system that routes customer-support "
                "messages to the correct department.\n"
                "1. Define the prediction target and a real-world success metric.\n"
                "2. Describe how text will be represented for an initial baseline.\n"
                "3. Identify one offline evaluation metric.\n"
                "4. Define which uncertain cases should be sent to a human.\n"
                "5. Describe one A/B test or online metric you could use after deployment.\n"
                "6. Identify two production concerns besides model accuracy.\n"
                "7. Explain when you would create a custom transformer.\n"
                "8. Explain what you would change if the training corpus became too large to fit in RAM."
            ),

            "expected_output": (
                "A concise system-design document or table covering problem "
                "definition, representation, offline evaluation, human review, "
                "production requirements, online testing, custom preprocessing, "
                "and scaling strategy."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "problem-framing",
                "production-ml",
                "human-in-the-loop",
                "online-testing",
                "custom-estimators",
                "scaling",
                "system-thinking",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M07.L01.QZ01",

        "title": "Text Data and Real-World Machine Learning — Knowledge Check",

        "lesson_code": "M07.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M07.L01.Q01",

                "section_id": "bag-of-words",

                "question": (
                    "What does fitting a CountVectorizer primarily learn from "
                    "the training corpus?"
                ),

                "options": [
                    "The final class prediction for every document",
                    "A vocabulary that maps tokens to feature positions",
                    "A neural embedding for every sentence",
                    "The optimal decision threshold for the classifier",
                ],

                "correct": 1,

                "explanation": (
                    "CountVectorizer tokenizes the training documents and builds "
                    "a vocabulary. Transform then encodes documents using those "
                    "learned feature positions."
                ),
            },

            {
                "id": "M07.L01.Q02",

                "section_id": "improving-text-features",

                "question": (
                    "What is the main intuition behind tf-idf?"
                ),

                "options": [
                    "Give every word exactly the same weight",
                    "Remove all words that appear more than once",
                    "Emphasize terms that are frequent in a document but relatively uncommon across the corpus",
                    "Use the class labels to assign positive and negative word weights",
                ],

                "correct": 2,

                "explanation": (
                    "tf-idf increases the relative importance of terms that are "
                    "descriptive of a particular document while downweighting "
                    "terms that appear broadly across many documents. It does not "
                    "use target labels."
                ),
            },

            {
                "id": "M07.L01.Q03",

                "section_id": "context-and-interpretation",

                "question": (
                    "Why can bigrams improve a sentiment classifier compared "
                    "with using only unigrams?"
                ),

                "options": [
                    "They can preserve short local contexts such as `not good`",
                    "They guarantee a smaller vocabulary",
                    "They remove the need for labeled data",
                    "They make every document the same length",
                ],

                "correct": 0,

                "explanation": (
                    "A unigram representation ignores word order. Bigrams preserve "
                    "short neighboring phrases, allowing features such as `not good` "
                    "to differ from the isolated word `good`."
                ),
            },

            {
                "id": "M07.L01.Q04",

                "section_id": "production-and-testing",

                "question": (
                    "What best distinguishes offline evaluation from A/B testing?"
                ),

                "options": [
                    "Offline evaluation can only be used for regression",
                    "A/B testing does not require any success metric",
                    "Offline evaluation uses stored evaluation data, while A/B testing measures system variants through real-world user interaction",
                    "A/B testing is simply another name for k-fold cross-validation",
                ],

                "correct": 2,

                "explanation": (
                    "Offline evaluation measures a model on collected data. "
                    "A/B testing evaluates alternative system behaviors in the "
                    "live environment and records real-world outcome metrics."
                ),
            },

            {
                "id": "M07.L01.Q05",

                "section_id": "complete-ml-workflow",

                "type": "open",

                "question": (
                    "You have built a high-accuracy text classifier for customer "
                    "support messages. Describe the steps you would take before "
                    "calling the project successful, including model inspection, "
                    "human review, production requirements, and real-world evaluation."
                ),
            },
        ],

        "passing_score": 70,
    },
}
