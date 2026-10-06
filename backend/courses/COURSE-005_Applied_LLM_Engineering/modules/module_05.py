"""M05.L01 — Text Clustering and Topic Modeling.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 5; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "Text Clustering and Topic Modeling"

MODULE_DESCRIPTION = (
    "Learn how to discover structure in unlabeled text using semantic embeddings, "
    "dimensionality reduction, density-based clustering, and BERTopic. Explore "
    "cluster inspection, outliers, c-TF-IDF topic representations, modular "
    "representation refinement with KeyBERTInspired and MMR, and generative "
    "topic labeling."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Text Clustering and Topic Modeling",

    "slug": "llm-foundations-m05-l01",

    "description": (
        "A practical introduction to unsupervised text analysis: turning documents "
        "into semantic embeddings, reducing dimensionality, discovering clusters "
        "without labels, interpreting those clusters as topics, and improving topic "
        "representations with BERTopic, c-TF-IDF, embedding-based reranking, "
        "diversification, and generative labels."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.75,

    "skill_tags": [
        "text-clustering",
        "topic-modeling",
        "unsupervised-learning",
        "embeddings",
        "umap",
        "hdbscan",
        "outliers",
        "bertopic",
        "bag-of-words",
        "ctfidf",
        "keybert",
        "mmr",
        "generative-topic-labeling",
        "visualization",
        "module-05",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
        "M04.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Text Clustering and Topic Modeling",

        "content": (
            r"""
# Text Clustering and Topic Modeling

> **Course:** Large Language Models Foundations  
> **Lesson:** M05.L01  
> **Module:** Text Clustering and Topic Modeling  
> **Source alignment:** Chapter 5, “Text Clustering and Topic Modeling.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between **supervised classification** and **unsupervised clustering**.
- Explain why semantic embeddings are useful for grouping text.
- Reproduce the chapter’s common clustering pipeline:
  **documents → embeddings → dimensionality reduction → clustering**.
- Interpret an embedding matrix such as `(44949, 384)`.
- Explain why dimensionality reduction can help clustering.
- Explain why dimensionality reduction also loses information.
- Describe the roles of **UMAP** and **HDBSCAN** in the chapter’s pipeline.
- Explain why a density-based clustering method can identify outliers.
- Inspect clusters manually instead of trusting cluster IDs blindly.
- Explain why a 2D visualization is only an approximation of the original embedding space.
- Distinguish **text clustering** from **topic modeling**.
- Explain BERTopic as two broad stages:
  semantic clustering and topic representation.
- Explain the intuition behind **bag-of-words**, **class-based term frequency**, and **c-TF-IDF**.
- Explain why BERTopic is considered modular.
- Interpret BERTopic’s topic IDs, topic keywords, and outlier topic `-1`.
- Explain how **KeyBERTInspired** can rerank topic keywords using semantic similarity.
- Explain how **Maximal Marginal Relevance (MMR)** can reduce redundant keywords.
- Explain why generative models can label topics efficiently at the topic level instead of processing every document.
- Compare multiple topic representations rather than treating one representation as perfect.

---

## 1. Why clustering matters when nobody gave us labels

In supervised classification, we begin with labeled examples.

For example:

```text
"This movie was excellent."       → positive
"This movie was disappointing."   → negative
```

The labels tell the model what the categories are.

But many real datasets do not come with labels.

Imagine receiving:

```text
50,000 research abstracts
100,000 support tickets
millions of product reviews
thousands of customer comments
```

without category annotations.

You may not even know which categories exist.

That is where **unsupervised learning** becomes useful.

Text clustering asks:

> Which documents appear similar enough to form groups, even though we were never told what those groups should be?

The basic goal is:

```text
unlabeled documents
       ↓
discover similarity structure
       ↓
groups of related documents
```

{{image:classification-vs-clustering}}

### Why clustering can be useful

The chapter highlights uses beyond simply grouping documents.

Clustering can support:

- exploratory data analysis,
- discovering hidden patterns,
- finding outliers,
- accelerating manual labeling,
- identifying potentially incorrect labels,
- understanding dataset complexity.

The most important difference is:

```text
classification:
the categories are known

clustering:
the groups are discovered
```

---

## 2. From clusters to topics

A cluster ID by itself is not very informative.

Suppose an algorithm tells you:

```text
Cluster 0
Cluster 1
Cluster 2
```

That does not explain what those groups mean.

If you inspect documents in Cluster 0 and discover they repeatedly discuss:

```text
sign language
translation
gesture
recognition
```

you might describe the cluster as:

```text
Sign Language Translation
```

That transition—from a group of related texts to an interpretable theme—is the core intuition behind **topic modeling**.

Topic modeling asks:

> What themes or latent topics appear across a collection of documents?

Traditionally, a topic may be represented using keywords:

```text
translation
nmt
machine
neural
bleu
```

A human can inspect those words and infer:

```text
Neural Machine Translation
```

[[IMAGE_NEEDED: Cluster to topic | Show a cluster containing several semantically related documents, then extract representative keywords, then assign a human-readable topic concept | Learner should understand that clustering groups documents while topic representation helps explain what each group is about]]

### Clustering and topic modeling are related but not identical

A useful distinction is:

```text
CLUSTERING
Which documents belong together?

TOPIC MODELING
What themes exist, and how can we describe them?
```

BERTopic connects both ideas.

---

## 3. The chapter’s dataset: ArXiv Computation and Language

The chapter works with research articles from ArXiv’s:

```text
cs.CL — Computation and Language
```

section.

The supplied source reports:

```text
44,949 abstracts
covering 1991–2024
```

Load the dataset:

```python
from datasets import load_dataset

dataset = load_dataset(
    "maartengr/arxiv_nlp"
)["train"]
```

Extract fields:

```python
abstracts = dataset["Abstracts"]
titles = dataset["Titles"]
```

This is a useful dataset for clustering because many subfields coexist:

```text
machine translation
speech recognition
sentiment analysis
summarization
embeddings
topic modeling
medical NLP
and many more
```

The algorithm is not given those topic names in advance.

It has to discover structure from the text.

---

## 4. The common text-clustering pipeline

The chapter presents a very useful three-stage pipeline:

```text
1. Convert documents into embeddings
2. Reduce embedding dimensionality
3. Cluster the reduced embeddings
```

In compact form:

```text
Documents
    ↓
Embedding model
    ↓
High-dimensional semantic vectors
    ↓
Dimensionality reduction
    ↓
Lower-dimensional vectors
    ↓
Clustering algorithm
    ↓
Groups + possible outliers
```

This pipeline is worth remembering because it appears in many practical unsupervised text systems.

[[IMAGE_NEEDED: Three-step clustering pipeline | Show documents → embedding model → high-dimensional vectors → UMAP dimensionality reduction → low-dimensional vectors → HDBSCAN → clusters/outliers | Learner should memorize the order and role of the three stages]]

Why not cluster raw text directly?

Because clustering algorithms need numerical features.

Embeddings give us those features while attempting to preserve semantic information.

---

## 5. Step 1 — Embed the documents

The first stage converts each abstract into a vector.

The chapter uses:

```text
thenlper/gte-small
```

through sentence-transformers:

```python
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "thenlper/gte-small"
)

embeddings = embedding_model.encode(
    abstracts,
    show_progress_bar=True,
)
```

Then:

```python
embeddings.shape
```

returns:

```text
(44949, 384)
```

Interpretation:

```text
44,949 documents
×
384 numerical values per document
```

Each abstract is represented by one point in a 384-dimensional semantic space.

### Why semantic embeddings help clustering

Suppose three documents discuss:

```text
automatic speech recognition
speech-to-text systems
ASR acoustic modeling
```

They may use different words, but a useful embedding model can place them near one another because their meanings are related.

That is much more useful for semantic clustering than relying only on exact word overlap.

[[IMAGE_NEEDED: Document embedding space | Show several short document snippets becoming dense vectors and then points in a conceptual semantic space where similar topics lie near one another | Learner should notice that clustering works on vectors, not raw strings]]

### Model choice matters

The chapter chooses an embedding model with clustering performance and inference speed in mind.

The broader lesson is:

> Choose an embedding model that matches the similarity behavior your clustering task needs.

A strong embedding model for one task is not automatically optimal for all tasks.

---

## 6. Why dimensionality reduction comes before clustering

Our embeddings contain:

```text
384 dimensions
```

That is useful for representing meaning, but high-dimensional spaces can be difficult for clustering algorithms.

The chapter therefore compresses the embeddings before clustering.

This is called **dimensionality reduction**.

Conceptually:

```text
384-dimensional vector
        ↓
dimensionality-reduction model
        ↓
5-dimensional vector
```

The objective is not simply to delete arbitrary columns.

The reduction method tries to preserve useful structure while expressing the data in fewer dimensions.

[[IMAGE_NEEDED: High-dimensional to low-dimensional representation | Show a cloud of conceptual high-dimensional document vectors being compressed into a lower-dimensional space while trying to keep neighboring groups together | Learner should see dimensionality reduction as structure-preserving compression rather than dropping random features]]

### Important limitation

Dimensionality reduction is lossy.

The chapter explicitly warns that:

```text
high-dimensional structure
≠
perfectly preserved low-dimensional structure
```

Information will be lost.

So there is always a balance:

```text
reduce enough to help clustering
but
retain enough structure to remain meaningful
```

---

## 7. Using UMAP

The chapter selects **UMAP** for dimensionality reduction.

The code is:

```python
from umap import UMAP

umap_model = UMAP(
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
)

reduced_embeddings = umap_model.fit_transform(
    embeddings
)
```

Let's unpack the parameters.

### `n_components=5`

The output representation has:

```text
5 dimensions
```

instead of 384.

The chapter notes that values around 5–10 can work well for this kind of pipeline.

### `min_dist=0.0`

This allows points to be packed tightly in the reduced representation.

The chapter uses this setting to encourage tighter cluster structure.

### `metric="cosine"`

Cosine distance/similarity is commonly useful when working with text embeddings.

### `random_state=42`

This improves reproducibility.

The chapter also notes a tradeoff:

```text
reproducibility
versus
parallelism / speed
```

for this UMAP setup.

### What comes out?

If:

```text
embeddings.shape
→ (44949, 384)
```

then conceptually:

```text
reduced_embeddings.shape
→ (44949, 5)
```

The number of documents stays the same.

Only the feature-space dimensionality changes.

---

## 8. Step 3 — Cluster with HDBSCAN

Now we have a lower-dimensional representation.

The next question is:

> How many clusters should we create?

With k-means, we normally choose the number of clusters in advance.

But in this dataset, we may not know how many natural groups exist.

The chapter therefore uses a density-based method:

```text
HDBSCAN
```

which stands for:

```text
Hierarchical Density-Based Spatial Clustering
of Applications with Noise
```

The most important intuition is:

> Dense regions become clusters, while isolated points can remain unassigned as outliers.

This is especially useful for datasets where some documents are niche or do not fit cleanly into a larger topic.

[[IMAGE_NEEDED: Centroid clustering versus density clustering | Show k-means forcing all points into a fixed number of centroid-centered groups beside HDBSCAN discovering dense irregular groups and leaving isolated points as outliers | Learner should understand why density clustering is attractive when the number of clusters is unknown]]

### Code

```python
from hdbscan import HDBSCAN

hdbscan_model = HDBSCAN(
    min_cluster_size=50,
    metric="euclidean",
    cluster_selection_method="eom",
).fit(reduced_embeddings)

clusters = hdbscan_model.labels_
```

The chapter reports:

```python
len(set(clusters))
```

producing:

```text
156
```

cluster labels in this run.

### `min_cluster_size`

This controls the minimum size a dense group needs to be treated as a cluster.

The chapter explains:

```text
smaller min_cluster_size
→ potentially more clusters

larger min_cluster_size
→ fewer, larger clusters
```

### Outliers are a feature, not necessarily an error

HDBSCAN does not force every point into a cluster.

Some documents may receive:

```text
-1
```

meaning they are treated as noise/outliers.

That can be helpful.

Forcing a niche research paper into the closest unrelated group could create a misleading topic.

---

## 9. Never trust a cluster number without reading the documents

The algorithm may output:

```text
cluster 0
```

but `0` has no semantic meaning by itself.

You need to inspect representative documents.

The chapter does this with:

```python
import numpy as np

cluster = 0

for index in np.where(
    clusters == cluster
)[0][:3]:
    print(
        abstracts[index][:300] + "...\n"
    )
```

The displayed abstracts discuss ideas such as:

```text
sign language
translation
gesture
recognition
synthesis
```

From that inspection, the chapter infers that this cluster appears to concern sign-language translation.

This demonstrates a critical unsupervised-learning principle:

> Cluster IDs are algorithmic assignments. Human interpretation gives them meaning.

### A good cluster-analysis workflow

For each interesting cluster:

```text
1. Sample documents.
2. Read titles/abstracts.
3. Look for recurring semantic themes.
4. Check whether several examples really belong together.
5. Inspect ambiguous examples.
6. Check nearby/outlier documents.
```

Do not label a cluster from one document.

---

## 10. Visualizing clusters in two dimensions

Five dimensions are still impossible to plot directly on a normal screen.

For visualization only, the chapter reduces embeddings again:

```text
384 dimensions
→
2 dimensions
```

with UMAP:

```python
reduced_embeddings = UMAP(
    n_components=2,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
).fit_transform(embeddings)
```

Then a dataframe can store:

```text
x coordinate
y coordinate
title
cluster label
```

and the documents can be plotted.

### What the visualization can tell you

A 2D cluster plot can help you notice:

- large dense groups,
- isolated points,
- relative neighborhoods,
- broad structure,
- possible subclusters.

### What it cannot prove

The chapter explicitly warns that 2D dimensionality reduction loses information.

Two groups may appear:

```text
very close in 2D
```

even if they are more separated in the original embedding space.

Or the reverse.

So:

> A visualization is an exploratory approximation, not ground truth.

[[IMAGE_NEEDED: Cluster visualization with outliers | A 2D scatter plot concept showing several colored document clusters and gray outliers, with a warning callout that 2D positions are an approximation of the original high-dimensional embedding space | Learner should use plots for exploration, not as proof of semantic structure]]

This is why manual cluster inspection remains important.

---

{{exercise:M05.L01.EX01}}

---

## 11. From clustering to topic modeling

At this point, we have groups of semantically similar documents.

But we still need interpretable topic descriptions.

A traditional topic representation might be:

```text
Topic 3:
translation
nmt
machine
neural
bleu
english
```

A human can infer:

```text
Neural Machine Translation
```

The challenge is automatically extracting words that characterize each cluster.

Classic topic-modeling approaches often rely heavily on word-frequency representations such as bag-of-words.

The chapter combines:

```text
semantic clustering
+
bag-of-words-based topic representation
```

through BERTopic.

---

## 12. BERTopic as two major stages

BERTopic can be understood as two broad stages.

### Stage 1 — Discover groups semantically

The chapter reuses the clustering pipeline:

```text
documents
→ embeddings
→ UMAP
→ HDBSCAN
→ clusters
```

This stage answers:

> Which documents belong together?

### Stage 2 — Represent each cluster as a topic

Now BERTopic examines the words occurring within each cluster and identifies which words best characterize that cluster.

This stage answers:

> What is this group about?

The full mental model:

```text
Documents
   ↓
Semantic embeddings
   ↓
Dimensionality reduction
   ↓
Clustering
   ↓
Groups of related documents
   ↓
Cluster-level word weighting
   ↓
Representative keywords
   ↓
Interpretable topics
```

[[IMAGE_NEEDED: BERTopic two-stage pipeline | First stage shows embedding → UMAP → HDBSCAN clustering; second stage shows cluster documents combined and processed with c-TF-IDF to generate ranked topic keywords | Learner should remember semantic grouping and topic representation as related but separable stages]]

---

## 13. Why bag-of-words reappears

Earlier chapters introduced bag-of-words as a simple text representation.

Bag-of-words counts word occurrences.

For a document:

```text
"language models process language"
```

a simplified count representation might be:

```text
language → 2
models   → 1
process  → 1
```

By itself, this ignores semantic context.

So why use it in BERTopic after learning powerful embeddings?

Because bag-of-words has a different strength:

> It is efficient and interpretable for identifying which words occur frequently.

BERTopic combines different tools for different jobs:

```text
embeddings
→ semantic grouping

bag-of-words / c-TF-IDF
→ interpretable topic words
```

This is a recurring lesson in machine learning:

> A modern system does not have to use one model for everything.

---

## 14. Move from document-level counts to cluster-level counts

Ordinary bag-of-words is usually computed per document.

But BERTopic needs to describe a **cluster**.

So think of all documents in one cluster as one combined class-level document.

Suppose Cluster A contains three texts:

```text
speech recognition model
automatic speech system
speech acoustic model
```

At the cluster level:

```text
speech       → high frequency
model        → recurring
recognition  → present
automatic    → present
acoustic     → present
```

The cluster-level frequency is the **class term frequency** part of c-TF-IDF.

Conceptually:

```text
individual documents
        ↓
group documents by cluster
        ↓
aggregate word counts per cluster
```

[[IMAGE_NEEDED: Document TF to class-level TF | Show several documents inside one cluster being merged conceptually into one class-level text, then count words over the whole cluster | Learner should notice that BERTopic represents topics at cluster level rather than treating each document independently]]

---

## 15. c-TF-IDF: find words that matter to one cluster

Raw frequency has a problem.

Words such as:

```text
the
and
of
to
```

can appear everywhere.

A word appearing frequently in every cluster is not very useful for distinguishing one topic.

BERTopic therefore uses **class-based TF-IDF**, or:

```text
c-TF-IDF
```

The high-level idea is:

```text
high weight
=
frequent in this cluster
AND
not equally common across all clusters
```

This means a term like:

```text
translation
```

may receive a strong weight in a machine-translation cluster if it is common there but less dominant elsewhere.

Meanwhile:

```text
the
```

should receive much less discriminative weight because it appears throughout the corpus.

### The intuition matters more than memorizing the formula

Think of c-TF-IDF as asking:

> Which words are especially characteristic of this cluster relative to the other clusters?

The result is a ranked vocabulary for each topic.

[[IMAGE_NEEDED: c-TF-IDF intuition | Show two clusters with word-frequency bars: common stop words are frequent in both and receive low discriminative weight, while a topic-specific word such as “translation” is frequent in one cluster and receives high weight | Learner should understand why frequency alone is not enough]]

---

## 16. Build BERTopic from the components

The chapter reuses the previously defined models:

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    verbose=True,
).fit(
    abstracts,
    embeddings,
)
```

This is important because it demonstrates BERTopic’s modularity.

We already have:

```text
embedding_model
umap_model
hdbscan_model
```

and BERTopic coordinates them while adding topic representation.

### Inspect discovered topics

```python
topic_model.get_topic_info()
```

The chapter shows outputs containing columns such as:

```text
Topic
Count
Name
Representation
```

Examples include themes around:

```text
speech recognition
medical/biomedical NLP
sentiment analysis
machine translation
prompting
sentence embeddings
```

The exact topics are dataset/run dependent.

---

## 17. Understand topic `-1`

BERTopic may show a topic:

```text
-1
```

This is not a normal semantic topic.

It represents documents that HDBSCAN treated as outliers.

This follows directly from the clustering stage.

HDBSCAN says:

```text
"I do not have enough evidence to place this point confidently inside a dense cluster."
```

BERTopic preserves that information.

### What can you do about outliers?

The chapter mentions two broad options:

```text
1. Use a clustering algorithm that forces assignment, such as k-means.
2. Use BERTopic functionality to reduce/reassign outliers.
```

But do not assume outliers are always bad.

Some may represent genuinely rare or unusual documents.

The right decision depends on the application.

---

## 18. Inspect and search topics

To inspect one topic:

```python
topic_model.get_topic(0)
```

The chapter shows topic 0 containing high-ranked words including:

```text
speech
asr
recognition
acoustic
speaker
audio
```

A reasonable interpretation is:

```text
Automatic Speech Recognition
```

### Search for topics semantically

BERTopic can also search for topics:

```python
topic_model.find_topics(
    "topic modeling"
)
```

The chapter reports that topic `22` is highly similar to that query.

Then:

```python
topic_model.get_topic(22)
```

returns words including:

```text
topic
topics
lda
latent
document
modeling
dirichlet
allocation
```

This lets you navigate discovered topics without manually browsing every cluster.

### Verify with documents

The chapter checks whether the BERTopic paper itself belongs to the corresponding topic.

That is a useful habit:

> When a topic looks correct from keywords, verify it against real documents.

---

## 19. BERTopic is modular by design

A major theme of the chapter is modularity.

The pipeline can be viewed like Lego blocks:

```text
Embedding model
      ↓
Dimensionality reduction
      ↓
Clustering
      ↓
Topic representation
```

You can swap components.

For example:

```text
different embedding model
different UMAP settings
different clustering method
different topic representation model
```

The chapter notes that BERTopic can support many variants, including:

- guided topic modeling,
- semi-supervised topic modeling,
- hierarchical topic modeling,
- dynamic topic modeling,
- multimodal topic modeling,
- multi-aspect topic modeling,
- online/incremental topic modeling,
- zero-shot topic modeling.

You do not need to master all variants in this lesson.

The key idea is:

> BERTopic is a framework for composing topic-modeling components, not one rigid algorithm.

[[IMAGE_NEEDED: BERTopic as Lego blocks | Show interchangeable blocks for embedding, reduction, clustering, and topic representation, with example alternatives underneath each block | Learner should notice that components can be swapped independently]]

---

## 20. Explore topics visually

The chapter uses:

```python
topic_model.visualize_documents(
    titles,
    reduced_embeddings=reduced_embeddings,
    width=1200,
    hide_annotations=True,
)
```

This creates an interactive view of topics and documents.

BERTopic also exposes visualizations such as:

```python
topic_model.visualize_barchart()

topic_model.visualize_heatmap(
    n_clusters=30
)

topic_model.visualize_hierarchy()
```

Each visualization answers a different question.

### Bar chart

```text
Which keywords have high weight in each topic?
```

### Heatmap

```text
Which topics appear related?
```

### Hierarchy

```text
Could multiple topics belong to broader parent themes?
```

### Document map

```text
Where are individual documents located relative to topic regions?
```

Remember the earlier warning:

2D visualization remains an approximation.

Use it to explore, not to replace semantic inspection.

---

## 21. Why topic keywords may need refinement

The first BERTopic representation comes from c-TF-IDF.

That is fast and interpretable.

But it is still fundamentally based on word counts and weighting.

It may produce:

- redundant words,
- generic words,
- abbreviations that are useful but obscure,
- terms that do not form a clean human-readable topic description.

The chapter therefore introduces an additional **representation model** stage.

Conceptually:

```text
initial c-TF-IDF topic words
            ↓
representation refinement
            ↓
improved topic description
```

This stage does not need to rerun the entire clustering pipeline.

That is important.

If you have:

```text
1,000,000 documents
100 topics
```

you do not necessarily need an expensive representation model to process one million documents.

You can refine roughly at the topic level.

[[IMAGE_NEEDED: Topic representation refinement | Show documents already clustered, c-TF-IDF producing candidate topic keywords, and an additional representation block reranking/refining those keywords without reclustering documents | Learner should see why topic-level refinement can be much cheaper than document-level processing]]

---

## 22. KeyBERTInspired: semantic keyword reranking

The chapter introduces:

```text
KeyBERTInspired
```

as one representation refinement approach.

The high-level idea uses embeddings to improve keyword ranking.

The chapter describes a process that:

1. identifies representative documents for the topic,
2. forms an average document embedding for the topic,
3. embeds candidate keywords,
4. compares keyword embeddings with the topic representation,
5. reranks the keywords by semantic relevance.

The code:

```python
from bertopic.representation import KeyBERTInspired

representation_model = KeyBERTInspired()

topic_model.update_topics(
    abstracts,
    representation_model=representation_model,
)
```

### Why this can improve readability

c-TF-IDF may identify statistically distinctive terms.

Embedding-based reranking asks an additional question:

> Which candidate terms are semantically representative of this topic?

That can produce cleaner topic descriptions.

### But it has tradeoffs

The chapter gives an important example.

A domain abbreviation such as:

```text
nmt
```

can be highly informative to a domain expert.

An embedding-based representation may fail to model that abbreviation as effectively and remove it.

So “cleaner” does not automatically mean “better for every audience.”

This is why comparing topic representations is valuable.

---

## 23. MMR: reduce redundant keywords

A topic representation might contain:

```text
summarization
summaries
summary
```

All are relevant.

But together they waste limited keyword slots because they convey almost the same idea.

**Maximal Marginal Relevance (MMR)** attempts to balance:

```text
relevance to the topic
+
diversity among selected keywords
```

The chapter uses:

```python
from bertopic.representation import (
    MaximalMarginalRelevance,
)

representation_model = MaximalMarginalRelevance(
    diversity=0.2
)

topic_model.update_topics(
    abstracts,
    representation_model=representation_model,
)
```

The goal is to keep keywords that each contribute new information.

A simplified example:

```text
Before:
summarization
summary
summaries
document
abstract

After diversification:
summarization
document
extractive
rouge
generation
```

The second list may cover more aspects of the topic.

[[IMAGE_NEEDED: MMR keyword diversification | Show a redundant candidate list with several near-duplicate words being filtered into a smaller list containing relevant but more diverse concepts | Learner should notice that MMR trades some redundancy for broader topic coverage]]

---

## 24. Use a generative model to name a topic

Keywords are useful, but humans often prefer a concise label.

For example:

```text
translation
nmt
machine
neural
bleu
```

could become:

```text
Neural Machine Translation
```

A generative model can help produce this label.

The chapter’s key efficiency idea is excellent:

> Do not send every document in the dataset to the generative model. Generate labels once per topic using representative information.

That changes the scale dramatically.

Imagine:

```text
1,000,000 documents
but
100 discovered topics
```

Instead of up to one million generation calls, topic-level labeling may need only around one call per topic.

### What goes into the prompt?

The chapter uses:

```text
representative documents
+
topic keywords
```

A template resembles:

```text
I have a topic containing these documents:

[DOCUMENTS]

The topic is described by these keywords:

[KEYWORDS]

What is this topic about?
```

[[IMAGE_NEEDED: Generative topic labeling | Show one topic cluster producing a small set of representative documents plus top keywords, these entering a generative model once, and a concise human-readable topic label emerging | Learner should understand why generative labeling is applied per topic instead of per document]]

---

## 25. Flan-T5 as a topic-label generator

The chapter uses a text-generation representation model with Flan-T5:

```python
from transformers import pipeline
from bertopic.representation import TextGeneration

prompt = (
    "I have a topic that contains the following documents:\n"
    "[DOCUMENTS]\n\n"
    "The topic is described by the following keywords: '[KEYWORDS]'.\n\n"
    "Based on the documents and keywords, what is this topic about?"
)

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
)

representation_model = TextGeneration(
    generator,
    prompt=prompt,
    doc_length=50,
    tokenizer="whitespace",
)

topic_model.update_topics(
    abstracts,
    representation_model=representation_model,
)
```

The source shows examples such as:

```text
summarization keywords
→ "Summarization"
```

but also broader outputs such as:

```text
"Science/Tech"
```

for a more specific biomedical topic.

This illustrates an important limitation:

> A generated label can be fluent and still be too vague.

Always compare it with the keywords and documents it is supposed to summarize.

---

## 26. Generative labels with a stronger API-hosted model

The chapter also gives a historical example using an API-hosted generative model to create richer labels.

The prompt requests a strict format:

```text
topic: <short topic label>
```

The source reports more detailed outputs for several topics.

However, treat the exact model name and API syntax in the chapter as **source-specific examples from when the chapter was written**.

The transferable lesson is:

```text
topic documents
+
topic keywords
+
clear output instruction
→
generated topic label
```

### Why retain multiple representations?

The chapter explicitly advises keeping multiple perspectives.

For a topic you might retain:

```text
c-TF-IDF keywords
KeyBERTInspired keywords
MMR-diversified keywords
generative label
```

Why?

Because no representation is perfect.

A domain acronym removed by one method may be highly valuable in another.

A generated label may be concise but overly broad.

The raw keywords help you audit the label.

---

## 27. Put the entire system together

Let's trace the complete lesson.

### Stage 1 — Start with unlabeled documents

```text
44,949 research abstracts
```

### Stage 2 — Create semantic embeddings

```text
44,949 × 384
```

Each abstract becomes a vector.

### Stage 3 — Reduce dimensionality for clustering

```text
384 dimensions
→
5 dimensions
```

using UMAP.

### Stage 4 — Discover dense document groups

HDBSCAN identifies clusters and leaves some points as outliers.

```text
cluster 0
cluster 1
...
outlier = -1
```

### Stage 5 — Inspect the clusters

Read representative documents.

Do not infer meaning from IDs alone.

### Stage 6 — Represent each cluster as a topic

BERTopic aggregates word information at cluster level and uses c-TF-IDF to rank representative terms.

```text
cluster
→
weighted topic words
```

### Stage 7 — Improve topic representations

Optional representation models can:

```text
rerank semantically
diversify keywords
generate human-readable labels
```

### Stage 8 — Explore topics

Use:

```text
topic tables
keyword rankings
semantic topic search
document maps
topic relationships
hierarchies
```

### Stage 9 — Validate manually

Read documents.

Check whether:

```text
cluster coherence
topic keywords
generated labels
```

actually make sense.

[[IMAGE_NEEDED: Complete text clustering and topic modeling pipeline | Show unlabeled documents → embedding model → UMAP → HDBSCAN → clusters/outliers → c-TF-IDF → topic keywords → optional KeyBERT/MMR/generative representation blocks → human-readable topics and visualizations | Learner should be able to use this figure as the final mental model for the chapter]]

---

{{exercise:M05.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Clustering is just classification without a training loop.

### Why this is wrong

Classification starts with predefined target labels. Clustering attempts to discover structure without those labels.

---

### Misconception 2

> If two documents appear close on a 2D plot, they must be equally close in the original embedding space.

### Why this is wrong

Dimensionality reduction loses information. A 2D visualization is an approximation.

---

### Misconception 3

> HDBSCAN should always assign every document to a topic.

### Why this is wrong

One of the useful properties of density-based clustering is that uncertain or isolated points can remain outliers.

---

### Misconception 4

> Topic modeling and clustering are exactly the same thing.

### Why this is wrong

Clustering groups documents. Topic modeling additionally attempts to discover and represent interpretable themes.

---

### Misconception 5

> BERTopic uses only BERT.

### Why this is wrong

The chapter presents BERTopic as a modular framework. Its pipeline can combine embedding models, dimensionality reduction, clustering, bag-of-words-derived representations, and other representation models.

---

### Misconception 6

> Bag-of-words became useless once embeddings appeared.

### Why this is wrong

BERTopic uses semantic embeddings for grouping documents and a bag-of-words-derived c-TF-IDF representation for interpretable topic words. Different techniques solve different parts of the pipeline.

---

### Misconception 7

> The most frequent word in a cluster is automatically the best topic word.

### Why this is wrong

Words frequent everywhere may carry little topic-specific information. c-TF-IDF emphasizes terms that are characteristic of one cluster relative to others.

---

### Misconception 8

> A generative topic label is automatically more trustworthy than keywords.

### Why this is wrong

Generated labels can be too broad or misleading. Keeping multiple representations makes interpretation more robust.

---

## Key terminology

| Term | Meaning |
|---|---|
| Unsupervised learning | Learning/discovering structure without predefined target labels |
| Text clustering | Grouping documents based on similarity |
| Topic modeling | Discovering and representing recurring themes in a text collection |
| Document embedding | Dense vector representing a whole document |
| Dimensionality reduction | Compressing high-dimensional representations into fewer dimensions while trying to preserve useful structure |
| UMAP | Dimensionality-reduction method used in the chapter |
| Cluster | Group of data points judged similar by a clustering algorithm |
| Density-based clustering | Clustering based on dense regions of data rather than fixed centroids |
| HDBSCAN | Hierarchical density-based clustering algorithm that can identify outliers |
| Outlier | Data point not confidently assigned to a discovered cluster |
| Bag-of-words | Representation based on word occurrence counts |
| Term frequency | How often a term appears in a representation |
| c-TF-IDF | Class-based TF-IDF weighting used by BERTopic to find cluster-representative words |
| BERTopic | Modular topic-modeling framework combining semantic clustering and topic representation |
| Topic representation | Keywords, labels, or other descriptors explaining what a topic contains |
| Representation model | BERTopic component that refines or generates topic representations |
| KeyBERTInspired | Embedding-based BERTopic representation method used to rerank topic keywords semantically |
| MMR | Maximal Marginal Relevance, used to balance relevance and keyword diversity |
| Cosine similarity | Similarity measure used with embedding vectors |
| Representative document | Document chosen as especially representative of a topic |
| Topic label | Short human-readable description of a topic |
| Sequence packing | Not central here; retained from previous chapter context rather than used in this pipeline |
| Cluster inspection | Human evaluation of documents assigned to a cluster |
| Topic hierarchy | Organization of topics into broader and narrower relationships |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the main difference between supervised classification and clustering?
2. Why are embeddings useful for text clustering?
3. What does `(44949, 384)` mean?
4. What are the three stages in the chapter’s common clustering pipeline?
5. Why reduce dimensionality before clustering?
6. What important information-loss warning applies to dimensionality reduction?
7. Why does the chapter use HDBSCAN instead of requiring k-means?
8. What does `min_cluster_size` influence?
9. What does an HDBSCAN label of `-1` represent?
10. Why should clusters be manually inspected?
11. Why is a 2D UMAP plot only approximate?
12. How is topic modeling different from clustering?
13. What are the two broad stages of BERTopic?
14. Why does BERTopic use bag-of-words-style information after semantic clustering?
15. What does c-TF-IDF try to emphasize?
16. Why is BERTopic considered modular?
17. What can `get_topic()` tell you?
18. What does KeyBERTInspired try to improve?
19. What tradeoff can semantic reranking introduce for domain-specific abbreviations?
20. What problem does MMR address?
21. Why can a generative model be used economically once per topic rather than once per document?
22. What information does the generative topic-label prompt receive?
23. Why should you preserve multiple topic representations?
24. Trace the full pipeline from unlabeled documents to human-readable topics.

---

## Retain this idea

**Text clustering discovers structure before you know the labels. The chapter’s core pipeline converts documents into semantic embeddings, compresses those embeddings with UMAP, and discovers dense groups with HDBSCAN. BERTopic then turns those groups into interpretable topics using c-TF-IDF and optional representation refinements such as semantic reranking, keyword diversification, and generative labels. The strongest workflow does not blindly trust any one cluster ID, plot, keyword list, or generated label—it combines algorithms with human inspection.**
"""
        ),

        "estimated_minutes": 165,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "unsupervised-intuition", "title": "Why clustering matters when nobody gave us labels", "order": 1},
            {"id": "topic-modeling-intuition", "title": "From clusters to topics", "order": 2},
            {"id": "dataset", "title": "The chapter’s dataset: ArXiv Computation and Language", "order": 3},
            {"id": "pipeline", "title": "The common text-clustering pipeline", "order": 4},
            {"id": "document-embeddings", "title": "Step 1 — Embed the documents", "order": 5},
            {"id": "dimensionality", "title": "Why dimensionality reduction comes before clustering", "order": 6},
            {"id": "umap", "title": "Using UMAP", "order": 7},
            {"id": "hdbscan", "title": "Step 3 — Cluster with HDBSCAN", "order": 8},
            {"id": "inspect-clusters", "title": "Never trust a cluster number without reading the documents", "order": 9},
            {"id": "visualization", "title": "Visualizing clusters in two dimensions", "order": 10},
            {"id": "clustering-to-topic-modeling", "title": "From clustering to topic modeling", "order": 11},
            {"id": "bertopic", "title": "BERTopic as two major stages", "order": 12},
            {"id": "bag-of-words", "title": "Why bag-of-words reappears", "order": 13},
            {"id": "class-frequency", "title": "Move from document-level counts to cluster-level counts", "order": 14},
            {"id": "ctfidf", "title": "c-TF-IDF: find words that matter to one cluster", "order": 15},
            {"id": "bertopic-code", "title": "Build BERTopic from the components", "order": 16},
            {"id": "outlier-topic", "title": "Understand topic -1", "order": 17},
            {"id": "inspect-topics", "title": "Inspect and search topics", "order": 18},
            {"id": "modularity", "title": "BERTopic is modular by design", "order": 19},
            {"id": "topic-visualization", "title": "Explore topics visually", "order": 20},
            {"id": "representation-refinement", "title": "Why topic keywords may need refinement", "order": 21},
            {"id": "keybert", "title": "KeyBERTInspired: semantic keyword reranking", "order": 22},
            {"id": "mmr", "title": "MMR: reduce redundant keywords", "order": 23},
            {"id": "generative-labels", "title": "Use a generative model to name a topic", "order": 24},
            {"id": "flan-topic-labels", "title": "Flan-T5 as a topic-label generator", "order": 25},
            {"id": "closed-topic-labels", "title": "Generative labels with a stronger API-hosted model", "order": 26},
            {"id": "full-pipeline", "title": "Put the entire system together", "order": 27},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 28},
            {"id": "terminology", "title": "Key terminology", "order": 29},
            {"id": "self-check", "title": "Self-check", "order": 30},
            {"id": "retain", "title": "Retain this idea", "order": 31},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",

            "title": "Build and Inspect a Semantic Text Clustering Pipeline",

            "lesson_code": "M05.L01",

            "section_id": "visualization",

            "placement": "after_section",

            "description": (
                "Practice the complete embeddings → UMAP → HDBSCAN workflow and "
                "learn to interpret clusters rather than trusting algorithmic IDs."
            ),

            "instructions": (
                "Use a manageable subset of the chapter dataset or another unlabeled "
                "text dataset.\n"
                "1. Encode every document with a sentence-transformer embedding model.\n"
                "2. Print the embedding matrix shape and explain each dimension.\n"
                "3. Reduce the embeddings to 5 dimensions using UMAP.\n"
                "4. Cluster those reduced embeddings using HDBSCAN.\n"
                "5. Report the number of discovered cluster labels and the number of "
                "outlier documents.\n"
                "6. Select at least three non-outlier clusters.\n"
                "7. Read at least three documents from each selected cluster.\n"
                "8. Give each cluster a provisional human-written theme based only "
                "on the inspected documents.\n"
                "9. Reduce the original embeddings to 2D for visualization and plot "
                "the points, distinguishing outliers from clustered points.\n"
                "10. Write a short warning explaining why the 2D plot cannot be treated "
                "as a perfect representation of the original embedding geometry."
            ),

            "expected_output": (
                "A notebook or script containing embedding and reduced-embedding shapes, "
                "cluster labels, outlier count, sampled documents from three clusters, "
                "human-written cluster interpretations, a 2D plot, and a short discussion "
                "of dimensionality-reduction limitations."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "document-embeddings",
                "umap",
                "hdbscan",
                "outlier-analysis",
                "cluster-inspection",
                "visualization-reasoning",
            ],
        },

        {
            "id": "M05.L01.EX02",

            "title": "Build and Compare Topic Representations",

            "lesson_code": "M05.L01",

            "section_id": "full-pipeline",

            "placement": "after_section",

            "description": (
                "Turn semantic clusters into interpretable topics and compare several "
                "representation strategies instead of relying on one output."
            ),

            "instructions": (
                "Starting from a BERTopic model or from the chapter pipeline:\n"
                "1. Fit topics using document embeddings, UMAP, HDBSCAN, and c-TF-IDF.\n"
                "2. Select at least five discovered topics.\n"
                "3. Record the original top c-TF-IDF keywords for each topic.\n"
                "4. Inspect representative documents for each topic and write your own "
                "short human label.\n"
                "5. Apply KeyBERTInspired and record the updated keywords.\n"
                "6. Apply MaximalMarginalRelevance and record the diversified keywords.\n"
                "7. If a generative representation backend is available, create a short "
                "generated topic label using representative documents and keywords. "
                "If not, write the prompt you would use rather than inventing model output.\n"
                "8. Compare the raw, semantic-reranked, diversified, and generated "
                "representations.\n"
                "9. Identify at least one case where a representation removed a useful "
                "domain term, became too broad, or otherwise lost useful information.\n"
                "10. Explain why keeping multiple representations can be preferable "
                "to replacing all earlier representations with the newest one."
            ),

            "expected_output": (
                "A comparison table for at least five topics containing original "
                "c-TF-IDF keywords, KeyBERTInspired keywords, MMR keywords, optional "
                "generated label, human interpretation, representative-document notes, "
                "and a short analysis of representation tradeoffs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "bertopic",
                "ctfidf",
                "topic-inspection",
                "keybert-inspired",
                "mmr",
                "generative-labeling",
                "representation-evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Text Clustering and Topic Modeling — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",
                "section_id": "unsupervised-intuition",
                "question": (
                    "What primarily distinguishes text clustering from supervised text classification?"
                ),
                "options": [
                    "Clustering can only process numbers while classification can process text.",
                    "Clustering discovers groups without predefined target labels, while classification learns predefined labels.",
                    "Classification never uses embeddings.",
                    "Clustering requires more labels than classification.",
                ],
                "correct": 1,
                "explanation": (
                    "The defining difference is whether the target grouping is supplied "
                    "before learning or discovered from the data."
                ),
            },
            {
                "id": "M05.L01.Q02",
                "section_id": "pipeline",
                "question": (
                    "What is the chapter's common three-stage clustering pipeline?"
                ),
                "options": [
                    "Tokenization → generation → fine-tuning",
                    "Embeddings → dimensionality reduction → clustering",
                    "Clustering → tokenization → embeddings",
                    "Prompting → reranking → translation",
                ],
                "correct": 1,
                "explanation": (
                    "Documents are first embedded, then compressed into a lower-dimensional "
                    "space, and finally grouped using a clustering algorithm."
                ),
            },
            {
                "id": "M05.L01.Q03",
                "section_id": "document-embeddings",
                "question": "What does an embedding shape of (44949, 384) mean?",
                "options": [
                    "44,949 clusters containing 384 topics each.",
                    "44,949 documents, each represented by a 384-dimensional vector.",
                    "384 documents and 44,949 labels.",
                    "44,949 Transformer layers.",
                ],
                "correct": 1,
                "explanation": (
                    "The first dimension counts documents and the second is the width "
                    "of each document embedding."
                ),
            },
            {
                "id": "M05.L01.Q04",
                "section_id": "dimensionality",
                "question": (
                    "Why does the chapter reduce embedding dimensionality before clustering?"
                ),
                "options": [
                    "To convert all text back into words.",
                    "To make high-dimensional structure easier for the clustering step to work with.",
                    "To guarantee that no information is lost.",
                    "To force exactly five clusters.",
                ],
                "correct": 1,
                "explanation": (
                    "High-dimensional spaces can be difficult for clustering algorithms, "
                    "so UMAP creates a lower-dimensional representation intended to retain "
                    "useful structure."
                ),
            },
            {
                "id": "M05.L01.Q05",
                "section_id": "hdbscan",
                "question": (
                    "Why is HDBSCAN attractive when the number of natural document groups is unknown?"
                ),
                "options": [
                    "It requires the exact number of clusters in advance.",
                    "It discovers dense groups and can leave isolated documents as outliers.",
                    "It converts documents directly into embeddings.",
                    "It guarantees every cluster has the same number of documents.",
                ],
                "correct": 1,
                "explanation": (
                    "Density-based clustering does not require a fixed number of clusters "
                    "and can explicitly identify noise/outlier points."
                ),
            },
            {
                "id": "M05.L01.Q06",
                "section_id": "visualization",
                "question": (
                    "Why should a 2D UMAP cluster visualization be interpreted cautiously?"
                ),
                "options": [
                    "Because 2D plots cannot contain colors.",
                    "Because dimensionality reduction loses information and can distort distances and cluster separation.",
                    "Because UMAP only works on labeled data.",
                    "Because the plot changes the original cluster assignments automatically.",
                ],
                "correct": 1,
                "explanation": (
                    "Compressing high-dimensional data into two dimensions is inherently "
                    "an approximation, so visual distance is not a perfect reflection of "
                    "the original embedding space."
                ),
            },
            {
                "id": "M05.L01.Q07",
                "section_id": "bertopic",
                "question": "What are the two broad stages of BERTopic described in the lesson?",
                "options": [
                    "Translation and summarization",
                    "Semantic document clustering and topic representation",
                    "Training and deployment",
                    "Tokenization and generation",
                ],
                "correct": 1,
                "explanation": (
                    "BERTopic first groups semantically similar documents and then "
                    "builds an interpretable representation for each discovered cluster."
                ),
            },
            {
                "id": "M05.L01.Q08",
                "section_id": "ctfidf",
                "question": "What is the main intuition behind c-TF-IDF?",
                "options": [
                    "Give the highest score to words that appear frequently everywhere.",
                    "Emphasize words that are frequent in one cluster and relatively distinctive across clusters.",
                    "Remove every rare word.",
                    "Replace all embeddings with token IDs.",
                ],
                "correct": 1,
                "explanation": (
                    "Topic words should characterize the target cluster, not merely be "
                    "common across the entire corpus."
                ),
            },
            {
                "id": "M05.L01.Q09",
                "section_id": "outlier-topic",
                "question": "What does BERTopic topic -1 usually represent in this pipeline?",
                "options": [
                    "The most important topic.",
                    "Documents treated as outliers/noise by HDBSCAN.",
                    "The first topic created by UMAP.",
                    "Documents with negative sentiment.",
                ],
                "correct": 1,
                "explanation": (
                    "HDBSCAN assigns its noise/outlier label to points it does not "
                    "confidently place into a dense cluster."
                ),
            },
            {
                "id": "M05.L01.Q10",
                "section_id": "modularity",
                "question": "What does BERTopic's modularity mean?",
                "options": [
                    "Every component must be a BERT model.",
                    "Major pipeline components can be replaced with alternative compatible methods.",
                    "All topics must use the same human-written label.",
                    "The clustering stage cannot be changed after initialization.",
                ],
                "correct": 1,
                "explanation": (
                    "The embedding, reduction, clustering, and representation stages "
                    "can be configured or replaced, which is a central design feature."
                ),
            },
            {
                "id": "M05.L01.Q11",
                "section_id": "keybert",
                "question": (
                    "What does KeyBERTInspired add to the topic-representation process?"
                ),
                "options": [
                    "A supervised label for every document",
                    "Semantic embedding-based reranking of candidate topic words",
                    "A new tokenizer for every topic",
                    "Forced assignment of all outliers",
                ],
                "correct": 1,
                "explanation": (
                    "The representation method uses semantic similarity between topic/"
                    "representative-document embeddings and candidate keyword embeddings "
                    "to improve ranking."
                ),
            },
            {
                "id": "M05.L01.Q12",
                "section_id": "mmr",
                "question": "What problem is MMR used to reduce in topic keyword lists?",
                "options": [
                    "The number of documents in the dataset",
                    "Redundancy among highly similar keywords",
                    "The embedding dimension",
                    "API rate limits",
                ],
                "correct": 1,
                "explanation": (
                    "MMR balances topic relevance with diversity so the selected words "
                    "cover more distinct information."
                ),
            },
            {
                "id": "M05.L01.Q13",
                "section_id": "generative-labels",
                "question": (
                    "Why is generative topic labeling potentially efficient in BERTopic?"
                ),
                "options": [
                    "The generative model can be used once per topic using representative documents and keywords rather than once per document.",
                    "The generative model does not process any text.",
                    "HDBSCAN generates the labels itself.",
                    "Topic labeling requires no model calls at all.",
                ],
                "correct": 0,
                "explanation": (
                    "After clustering, the expensive generative step can operate on a "
                    "small number of topics rather than the full document collection."
                ),
            },
            {
                "id": "M05.L01.Q14",
                "section_id": "full-pipeline",
                "type": "open",
                "question": (
                    "Explain the complete pipeline from raw unlabeled documents to "
                    "interpretable topic labels. Include embeddings, UMAP, HDBSCAN, "
                    "outliers, c-TF-IDF, optional representation refinement, and human "
                    "inspection. Explain why none of the intermediate outputs should be "
                    "treated as unquestionable ground truth."
                ),
            },
        ],

        "passing_score": 70,
    },
}
