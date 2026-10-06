"""M01.L07 — Question Answering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 7.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L07"
MODULE_ORDER = 1
MODULE_TITLE = "Transformer Foundations"
MODULE_DESCRIPTION = (
    "Build practical question-answering systems by combining transformer readers "
    "with retrieval, long-context handling, evaluation, domain adaptation, and "
    "retrieval-augmented generation."
)

SOURCE_CHAPTER = 7
SOURCE_PAGES = "Chapter 7"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Question Answering",
    "slug": "applied-nlp-transformers-m01-l07-question-answering",
    "description": (
        "Learn extractive question answering, span prediction, sliding-window handling for "
        "long contexts, retriever-reader architectures, BM25 and DPR retrieval, QA evaluation, "
        "domain adaptation, and the transition from extractive QA to retrieval-augmented generation."
    ),
    "order": 7,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.25,
    "skill_tags": [
        "question-answering",
        "extractive-qa",
        "span-classification",
        "bm25",
        "dense-passage-retrieval",
        "retriever-reader",
        "rag",
        "haystack",
        "domain-adaptation",
        "evaluation",
        "module-01",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
    ],

    "lesson": {
        "title": "Question Answering",

        "content": (
            "# Question Answering\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L07  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 7. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain extractive question answering as answer-span prediction.\n"
            "- Distinguish closed-domain and open-domain QA.\n"
            "- Explain how SQuAD-style QA examples are structured.\n"
            "- Tokenize question-context pairs correctly.\n"
            "- Explain start and end logits from a QA head.\n"
            "- Handle unanswerable questions.\n"
            "- Use sliding windows for contexts longer than the model limit.\n"
            "- Explain the retriever-reader architecture.\n"
            "- Compare sparse BM25 retrieval with dense DPR retrieval.\n"
            "- Evaluate retrievers with recall@k and readers with EM/F1.\n"
            "- Explain why the retriever places an upper bound on end-to-end QA quality.\n"
            "- Explain domain adaptation from SQuAD to SubjQA.\n"
            "- Distinguish extractive QA from generative QA.\n"
            "- Explain the basic idea behind retrieval-augmented generation (RAG).\n"
            "\n"
            "---\n"
            "\n"

            "## 1. What is question answering?\n"
            "\n"
            "Search systems often do more than return documents. They may return a short answer "
            "snippet directly.\n"
            "\n"
            "A common architecture is:\n"
            "\n"
            "```text\n"
            "user question\n"
            "    ↓\n"
            "retrieve relevant documents\n"
            "    ↓\n"
            "extract or generate an answer\n"
            "```\n"
            "\n"
            "The chapter focuses first on **extractive QA**.\n"
            "\n"
            "In extractive QA, the answer must be a span that already appears in a document.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Question: Is the watch waterproof?\n"
            "Context:  This watch is waterproof at 30m depth.\n"
            "Answer:   waterproof at 30m\n"
            "```\n"
            "\n"
            "There are other QA forms too:\n"
            "\n"
            "- community QA,\n"
            "- long-form QA,\n"
            "- QA over tables,\n"
            "- generative QA,\n"
            "- multimodal QA.\n"
            "\n"
            "[[IMAGE_NEEDED: Two-stage question answering system | "
            "A question enters a retriever that selects relevant documents, then a reader "
            "extracts an answer span from one of those documents | "
            "Learner should notice that document retrieval and answer extraction are separate "
            "problems in a practical QA system]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Build QA from customer reviews\n"
            "\n"
            "The chapter uses the **SubjQA** dataset to build an electronics-review QA system.\n"
            "\n"
            "SubjQA contains customer reviews from six domains, including electronics, books, "
            "restaurants, movies, grocery, and travel-related reviews.\n"
            "\n"
            "The electronics subset contains questions such as:\n"
            "\n"
            "```text\n"
            "How is the battery?\n"
            "Is sound clear?\n"
            "Is it a wireless keyboard?\n"
            "```\n"
            "\n"
            "This dataset is challenging because many questions are **subjective**. A phrase "
            "such as 'poor quality' does not have one universal definition.\n"
            "\n"
            "A QA example commonly contains:\n"
            "\n"
            "| Field | Meaning |\n"
            "|---|---|\n"
            "| question | User question |\n"
            "| context | Review/document |\n"
            "| answer text | Correct answer span |\n"
            "| answer start | Character offset where the answer begins |\n"
            "\n"
            "Some questions are intentionally **unanswerable** and contain an empty answer.\n"
            "\n"
            "The chapter's electronics split is relatively small, which makes transfer learning "
            "especially important.\n"
            "\n"
            "### Closed-domain versus open-domain QA\n"
            "\n"
            "**Closed-domain QA** searches within a narrow domain, such as one product category.\n"
            "\n"
            "**Open-domain QA** searches over a much broader knowledge source.\n"
            "\n"
            "The chapter's product-review system is a closed-domain example.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Why SQuAD matters\n"
            "\n"
            "The Stanford Question Answering Dataset (SQuAD) helped establish the standard "
            "question + passage + answer-span format used in extractive QA.\n"
            "\n"
            "SQuAD 1.1 contains answerable questions whose answers occur in the passage.\n"
            "\n"
            "SQuAD 2.0 adds questions that look relevant but cannot be answered from the passage.\n"
            "\n"
            "That matters because a robust QA system must sometimes say:\n"
            "\n"
            "```text\n"
            "No answer is supported by this context.\n"
            "```\n"
            "\n"
            "The chapter starts from a MiniLM model already fine-tuned on SQuAD 2.0 rather "
            "than training a QA head from scratch, because the SubjQA training set is small.\n"
            "\n"
            "This is a useful transfer-learning pattern:\n"
            "\n"
            "```text\n"
            "general language pretraining\n"
            "        ↓\n"
            "large QA dataset fine-tuning\n"
            "        ↓\n"
            "smaller target-domain adaptation\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Extractive QA is span classification\n"
            "\n"
            "The model does not directly generate the answer text.\n"
            "\n"
            "Instead, it predicts:\n"
            "\n"
            "- the most likely **start token**, and\n"
            "- the most likely **end token**.\n"
            "\n"
            "Suppose the tokenized context is:\n"
            "\n"
            "```text\n"
            "[this] [watch] [is] [waterproof] [at] [30m] [depth]\n"
            "```\n"
            "\n"
            "A correct answer may correspond to:\n"
            "\n"
            "```text\n"
            "start = waterproof\n"
            "end   = 30m\n"
            "```\n"
            "\n"
            "The QA head produces two scores for every input token:\n"
            "\n"
            "```text\n"
            "token position\n"
            "   ├── start score\n"
            "   └── end score\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Extractive QA span-classification head | "
            "Question and context tokens enter a transformer encoder; each token hidden state "
            "feeds a small QA head that produces start and end logits, with the selected answer "
            "span highlighted inside the context | "
            "Learner should notice that the answer is defined by two token positions]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Tokenize question-context pairs\n"
            "\n"
            "For BERT-like models, the tokenizer formats a QA input approximately as:\n"
            "\n"
            "```text\n"
            "[CLS] question tokens [SEP] context tokens [SEP]\n"
            "```\n"
            "\n"
            "Example:\n"
            "\n"
            "```python\n"
            "from transformers import AutoTokenizer\n"
            "\n"
            "model_ckpt = 'deepset/minilm-uncased-squad2'\n"
            "tokenizer = AutoTokenizer.from_pretrained(model_ckpt)\n"
            "\n"
            "question = 'How much music can this hold?'\n"
            "context = (\n"
            "    'An MP3 is about 1 MB/minute, so about 6000 hours '\n"
            "    'depending on file size.'\n"
            ")\n"
            "\n"
            "inputs = tokenizer(\n"
            "    question,\n"
            "    context,\n"
            "    return_tensors='pt',\n"
            ")\n"
            "```\n"
            "\n"
            "Some BERT-like models also provide `token_type_ids`, which distinguish question "
            "tokens from context tokens.\n"
            "\n"
            "The key idea is that the model receives the **question and candidate evidence "
            "together**.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Turn start/end logits into an answer\n"
            "\n"
            "A question-answering model returns two logit vectors:\n"
            "\n"
            "```python\n"
            "from transformers import AutoModelForQuestionAnswering\n"
            "import torch\n"
            "\n"
            "model = AutoModelForQuestionAnswering.from_pretrained(model_ckpt)\n"
            "\n"
            "with torch.no_grad():\n"
            "    outputs = model(**inputs)\n"
            "\n"
            "start_logits = outputs.start_logits\n"
            "end_logits = outputs.end_logits\n"
            "```\n"
            "\n"
            "If there are 28 input tokens, both vectors have 28 scores.\n"
            "\n"
            "A simple demonstration is:\n"
            "\n"
            "```python\n"
            "start_idx = torch.argmax(start_logits)\n"
            "end_idx = torch.argmax(end_logits) + 1\n"
            "\n"
            "answer_ids = inputs['input_ids'][0][start_idx:end_idx]\n"
            "answer = tokenizer.decode(answer_ids)\n"
            "```\n"
            "\n"
            "For the chapter's example, this extracts:\n"
            "\n"
            "```text\n"
            "6000 hours\n"
            "```\n"
            "\n"
            "In a real QA pipeline, postprocessing is more careful than simply taking two "
            "independent argmax values. It should ensure that:\n"
            "\n"
            "- the answer lies inside the context rather than the question,\n"
            "- the start comes before the end,\n"
            "- the span length is sensible,\n"
            "- impossible-answer cases are handled.\n"
            "\n"
            "{{exercise:M01.L07.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Handle unanswerable questions\n"
            "\n"
            "A robust QA model must not invent a span just because it is forced to choose one.\n"
            "\n"
            "SQuAD 2.0-style models use a special mechanism for predicting that no answer is "
            "supported by the passage. In the chapter's pipeline example, an unanswerable "
            "question can produce an empty answer.\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "qa = pipeline(\n"
            "    'question-answering',\n"
            "    model=model,\n"
            "    tokenizer=tokenizer,\n"
            ")\n"
            "\n"
            "result = qa(\n"
            "    question='Why is there no data?',\n"
            "    context=context,\n"
            "    handle_impossible_answer=True,\n"
            ")\n"
            "```\n"
            "\n"
            "The system may return:\n"
            "\n"
            "```text\n"
            "answer = ''\n"
            "```\n"
            "\n"
            "Knowing when **not** to answer is a fundamental QA capability.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Long contexts: use a sliding window\n"
            "\n"
            "Question answering is especially sensitive to truncation.\n"
            "\n"
            "If you keep only the beginning of a long review, the answer might be removed.\n"
            "\n"
            "The standard solution described in the chapter is a **sliding window**.\n"
            "\n"
            "Instead of one long context, create several overlapping windows:\n"
            "\n"
            "```text\n"
            "question + context tokens\n"
            "\n"
            "window 1: [--------------------]\n"
            "window 2:          [--------------------]\n"
            "window 3:                    [--------------------]\n"
            "```\n"
            "\n"
            "The overlap is controlled by the **stride**.\n"
            "\n"
            "```python\n"
            "tokenized = tokenizer(\n"
            "    question,\n"
            "    long_context,\n"
            "    return_overflowing_tokens=True,\n"
            "    max_length=100,\n"
            "    stride=25,\n"
            ")\n"
            "```\n"
            "\n"
            "The repeated overlap reduces the chance that an answer crossing a window boundary "
            "is lost.\n"
            "\n"
            "[[IMAGE_NEEDED: Sliding window for long-context QA | "
            "A long token sequence with the question shown separately and several overlapping "
            "context windows beneath it; the answer span lies near a boundary but is fully "
            "captured in at least one window | "
            "Learner should notice why overlap/stride is necessary instead of simple truncation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. From one passage to thousands: the retriever-reader architecture\n"
            "\n"
            "So far we assumed the correct context was already known.\n"
            "\n"
            "Real users normally provide only a question.\n"
            "\n"
            "If a product has hundreds of reviews, sending every review through the reader "
            "would be too slow.\n"
            "\n"
            "Modern QA therefore separates the work:\n"
            "\n"
            "### Retriever\n"
            "\n"
            "Finds the most relevant documents/passages for the query.\n"
            "\n"
            "### Reader\n"
            "\n"
            "Runs deeper reading comprehension on the smaller retrieved set and extracts "
            "answer spans.\n"
            "\n"
            "```text\n"
            "Question\n"
            "   ↓\n"
            "Retriever\n"
            "   ↓ top-k passages\n"
            "Reader\n"
            "   ↓\n"
            "Answer candidates\n"
            "```\n"
            "\n"
            "Optional reranking or postprocessing stages can be inserted between or after "
            "these components.\n"
            "\n"
            "[[IMAGE_NEEDED: Retriever-reader QA architecture | "
            "Question -> document store -> retriever -> top-k documents -> optional reranker -> "
            "reader -> answer candidates, with clear separation of retrieval and reading stages | "
            "Learner should notice that retrieval reduces the amount of text the expensive "
            "reader must process]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Document store and metadata filters\n"
            "\n"
            "The chapter uses Haystack and an Elasticsearch document store.\n"
            "\n"
            "A document store contains:\n"
            "\n"
            "- text passages,\n"
            "- document IDs,\n"
            "- metadata used for filtering.\n"
            "\n"
            "For product QA, metadata is crucial. A user asking about one camera should not "
            "receive evidence from reviews of a different product.\n"
            "\n"
            "A stored document may conceptually look like:\n"
            "\n"
            "```python\n"
            "{\n"
            "    'text': '<review text>',\n"
            "    'meta': {\n"
            "        'item_id': '<product-id>',\n"
            "        'question_id': '<question-id>',\n"
            "        'split': 'train',\n"
            "    },\n"
            "}\n"
            "```\n"
            "\n"
            "Retrieval can then be filtered by `item_id` before ranking results.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Sparse retrieval with BM25\n"
            "\n"
            "The first retriever in the chapter is based on **BM25**.\n"
            "\n"
            "BM25 is a sparse lexical retrieval method. It scores documents largely according "
            "to term matching, term frequency, inverse document frequency, and document-length "
            "normalization.\n"
            "\n"
            "Its strengths include:\n"
            "\n"
            "- fast indexing and retrieval,\n"
            "- strong lexical matching,\n"
            "- mature search-engine support.\n"
            "\n"
            "Its weakness is that semantic matches may be missed when the query and document "
            "use different words.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Query:    Is it good for reading?\n"
            "Review:   the larger screen makes books easier to read\n"
            "```\n"
            "\n"
            "The exact wording differs even though the meaning is closely related.\n"
            "\n"
            "The chapter retrieves the top documents and then lets a QA reader extract "
            "answer spans from them.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. The reader extracts answers from retrieved passages\n"
            "\n"
            "The chapter uses a MiniLM SQuAD 2.0 reader.\n"
            "\n"
            "Its job is not to search the whole corpus. The retriever has already reduced the "
            "candidate set.\n"
            "\n"
            "Given a query and several candidate passages, the reader predicts answer spans "
            "and ranks answer candidates.\n"
            "\n"
            "An end-to-end result can look like:\n"
            "\n"
            "```text\n"
            "Question: Is it good for reading?\n"
            "\n"
            "Answer 1: I mainly use it for book reading\n"
            "Answer 2: the larger screen ... makes for easier reading\n"
            "Answer 3: it is great for reading books when no light is available\n"
            "```\n"
            "\n"
            "This demonstrates why retrieval and reading complement each other:\n"
            "\n"
            "- the retriever narrows the search space,\n"
            "- the reader performs detailed answer extraction.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Evaluate the retriever with recall@k\n"
            "\n"
            "The retriever determines which documents the reader gets to see.\n"
            "\n"
            "If the relevant passage is not retrieved, even a perfect reader cannot answer "
            "correctly.\n"
            "\n"
            "That is why the chapter emphasizes **retriever recall**.\n"
            "\n"
            "Recall@k asks:\n"
            "\n"
            "> For how many questions does at least one relevant document appear among the "
            "top k retrieved documents?\n"
            "\n"
            "The chapter obtains roughly **Recall@3 = 0.95** in one BM25 evaluation setup.\n"
            "\n"
            "Increasing `k` usually improves recall, but creates a cost:\n"
            "\n"
            "```text\n"
            "higher k\n"
            "  → more relevant passages likely found\n"
            "  → more passages sent to the reader\n"
            "  → higher reader latency\n"
            "```\n"
            "\n"
            "This is a system-level trade-off, not just a retrieval metric.\n"
            "\n"
            "{{exercise:M01.L07.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Dense Passage Retrieval (DPR)\n"
            "\n"
            "Sparse retrieval relies heavily on lexical overlap.\n"
            "\n"
            "Dense retrieval instead maps questions and passages into learned dense vectors.\n"
            "\n"
            "DPR uses two transformer encoders:\n"
            "\n"
            "- a **question encoder**,\n"
            "- a **passage encoder**.\n"
            "\n"
            "The training goal is to make relevant question-passage pairs have high similarity "
            "and irrelevant pairs have lower similarity.\n"
            "\n"
            "```text\n"
            "question ──► question encoder ──► vector q\n"
            "\n"
            "passage  ──► passage encoder  ──► vector p\n"
            "\n"
            "relevance ≈ similarity(q, p)\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: DPR bi-encoder architecture | "
            "A question enters one BERT-like encoder and a passage enters another; each produces "
            "a dense vector and their similarity determines relevance | "
            "Learner should notice that the question and passage are encoded separately, "
            "which enables efficient retrieval over many stored passage vectors]]\n"
            "\n"
            "In the chapter's SubjQA experiment, DPR does **not** outperform BM25 in recall. "
            "This is an important lesson: dense retrieval is not automatically better. Domain "
            "fit and retriever training matter.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Evaluate the reader with EM and F1\n"
            "\n"
            "Two common extractive-QA reader metrics are:\n"
            "\n"
            "### Exact Match (EM)\n"
            "\n"
            "The normalized prediction must exactly match a reference answer.\n"
            "\n"
            "### F1-score\n"
            "\n"
            "Measures token overlap between prediction and reference using the harmonic mean "
            "of precision and recall.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Reference: 6000 hours\n"
            "Prediction: about 6000 hours\n"
            "```\n"
            "\n"
            "EM is 0 because the strings differ after normalization.\n"
            "\n"
            "F1 can still be high because most answer tokens overlap.\n"
            "\n"
            "But F1 can also overestimate bad answers. If the model predicts:\n"
            "\n"
            "```text\n"
            "about 6000 dollars\n"
            "```\n"
            "\n"
            "some tokens overlap even though the meaning is wrong.\n"
            "\n"
            "Therefore the chapter recommends considering **both EM and F1**, rather than "
            "trusting one metric alone.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Domain adaptation: SQuAD is not customer reviews\n"
            "\n"
            "A model fine-tuned on SQuAD performs much worse on SubjQA than on its original "
            "benchmark.\n"
            "\n"
            "Why?\n"
            "\n"
            "- Wikipedia is formal and factual.\n"
            "- Customer reviews are informal.\n"
            "- SubjQA questions and answers are often subjective.\n"
            "- The language distribution is different.\n"
            "\n"
            "The chapter adapts the MiniLM reader by further fine-tuning it on SubjQA.\n"
            "\n"
            "The useful transfer path is:\n"
            "\n"
            "```text\n"
            "pretrained MiniLM\n"
            "      ↓\n"
            "fine-tune on large SQuAD QA data\n"
            "      ↓\n"
            "fine-tune again on small SubjQA domain data\n"
            "```\n"
            "\n"
            "This substantially improves SubjQA performance.\n"
            "\n"
            "The chapter also compares this against directly fine-tuning the base MiniLM model "
            "on SubjQA alone. The direct approach performs worse, supporting the value of the "
            "large intermediate QA training stage when target-domain data is scarce.\n"
            "\n"
            "[[IMAGE_NEEDED: QA domain-adaptation path | "
            "A three-stage pipeline from pretrained MiniLM to SQuAD fine-tuning to SubjQA "
            "fine-tuning, contrasted with a shorter direct MiniLM-to-SubjQA path that performs "
            "worse in the chapter | "
            "Learner should notice the benefit of task transfer before small-domain adaptation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Evaluate the entire QA pipeline\n"
            "\n"
            "Evaluating the reader with the correct context already provided is easier than "
            "real production QA.\n"
            "\n"
            "In the real system:\n"
            "\n"
            "```text\n"
            "question\n"
            "   ↓\n"
            "retriever may return imperfect passages\n"
            "   ↓\n"
            "reader must answer from those passages\n"
            "```\n"
            "\n"
            "When the chapter evaluates retriever + reader together, end-to-end EM/F1 are lower "
            "than the reader-only SQuAD-style evaluation.\n"
            "\n"
            "This exposes one of the most important principles in the chapter:\n"
            "\n"
            "> **Component quality does not automatically equal system quality.**\n"
            "\n"
            "You should evaluate:\n"
            "\n"
            "- retriever recall,\n"
            "- reader EM/F1 with known-good contexts,\n"
            "- end-to-end EM/F1 with retrieved contexts,\n"
            "- latency and top-k trade-offs.\n"
            "\n"
            "[[IMAGE_NEEDED: QA component versus end-to-end evaluation | "
            "A diagram with separate metric boxes under retriever (Recall@k), reader (EM/F1 with "
            "gold contexts), and full system (end-to-end EM/F1 + latency) | "
            "Learner should notice that every layer needs its own evaluation as well as a final "
            "system-level evaluation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Go beyond extractive QA with RAG\n"
            "\n"
            "Extractive QA can only return spans that already exist in the retrieved passages.\n"
            "\n"
            "Sometimes the answer should synthesize evidence from several places into a new "
            "sentence. This motivates **generative QA**.\n"
            "\n"
            "The chapter introduces **Retrieval-Augmented Generation (RAG)**.\n"
            "\n"
            "RAG replaces the extractive reader with a generator.\n"
            "\n"
            "```text\n"
            "Question\n"
            "   ↓\n"
            "Dense retriever (DPR)\n"
            "   ↓ relevant documents\n"
            "Seq2seq generator\n"
            "   ↓\n"
            "generated answer\n"
            "```\n"
            "\n"
            "The generator can be a sequence-to-sequence transformer such as BART or T5.\n"
            "\n"
            "The chapter distinguishes:\n"
            "\n"
            "### RAG-Sequence\n"
            "\n"
            "Uses retrieved-document evidence at the sequence level to generate the answer.\n"
            "\n"
            "### RAG-Token\n"
            "\n"
            "Can effectively draw on different retrieved documents while generating different "
            "tokens, enabling more flexible evidence synthesis.\n"
            "\n"
            "[[IMAGE_NEEDED: RAG architecture | "
            "Question -> dense retriever -> top-k passages -> sequence-to-sequence generator -> "
            "generated answer, with the retrieval stage visually connected to generation | "
            "Learner should notice that RAG grounds generation in retrieved external documents "
            "rather than generating from the language model alone]]\n"
            "\n"
            "The chapter's example shows that RAG can produce reasonable answers, especially "
            "for more factual questions, but subjective questions can still confuse it.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. A practical hierarchy for QA systems\n"
            "\n"
            "The chapter's conclusion recommends an incremental approach to real-world QA.\n"
            "\n"
            "A useful hierarchy is:\n"
            "\n"
            "```text\n"
            "1. Build strong search/retrieval\n"
            "          ↓\n"
            "2. Add extractive QA\n"
            "          ↓\n"
            "3. Consider generative QA only when needed\n"
            "```\n"
            "\n"
            "Why this order?\n"
            "\n"
            "- Search alone already provides user value.\n"
            "- Extractive QA is easier to inspect because the answer comes directly from evidence.\n"
            "- Generative QA is more flexible but introduces more subtle failure modes.\n"
            "\n"
            "[[IMAGE_NEEDED: QA hierarchy of needs | "
            "A three-level pyramid with retrieval/search at the base, extractive QA in the middle, "
            "and generative QA/RAG at the top | "
            "Learner should notice that strong retrieval is foundational and generative QA "
            "should build on a reliable evidence pipeline]]\n"
            "\n"
            "The chapter also points toward future directions such as:\n"
            "\n"
            "- multimodal QA over text, tables, and images,\n"
            "- QA over knowledge graphs,\n"
            "- synthetic question generation for data augmentation.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: A QA model searches the entire corpus by itself\n"
            "\n"
            "> Give the transformer a question and it will automatically find the right document.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "An extractive reader expects a question and context. A retriever is usually needed "
            "to select relevant documents first.\n"
            "\n"
            "### Misconception 2: Truncating long QA contexts is harmless\n"
            "\n"
            "> If the document is too long, keeping the beginning is good enough.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The answer may occur near the end. Sliding windows preserve coverage across the "
            "full context.\n"
            "\n"
            "### Misconception 3: Dense retrieval is always better than BM25\n"
            "\n"
            "> Transformer embeddings automatically beat lexical retrieval.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "In the chapter's SubjQA experiment, DPR does not improve recall over BM25. "
            "Retrieval quality depends on the data and domain adaptation.\n"
            "\n"
            "### Misconception 4: A strong reader guarantees a strong QA system\n"
            "\n"
            "> If reader F1 is high, the end-to-end system will also be high.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The reader can only work with retrieved evidence. Retrieval errors propagate "
            "downstream and reduce full-system quality.\n"
            "\n"
            "### Misconception 5: Generative QA is always better than extractive QA\n"
            "\n"
            "> If a generator can synthesize answers, it should replace search and extraction.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Generative QA is more flexible but has subtler failure modes. The chapter recommends "
            "building strong retrieval and extractive capabilities first.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Question answering (QA) | System that answers natural-language questions from evidence or model knowledge |\n"
            "| Extractive QA | Returns an answer span directly from a context document |\n"
            "| Generative QA | Generates a new answer sequence from retrieved evidence |\n"
            "| Span classification | Predicting answer start and end token positions |\n"
            "| Start logit | Score indicating how likely a token is to begin the answer |\n"
            "| End logit | Score indicating how likely a token is to end the answer |\n"
            "| Unanswerable question | Question whose answer is not supported by the context |\n"
            "| Sliding window | Overlapping chunks used to process contexts longer than the model limit |\n"
            "| Stride | Number of overlapping tokens between adjacent windows |\n"
            "| Retriever | Component that selects relevant documents/passages |\n"
            "| Reader | Component that extracts an answer from retrieved text |\n"
            "| Document store | Searchable storage layer for documents and metadata |\n"
            "| BM25 | Sparse lexical retrieval scoring method |\n"
            "| DPR | Dense Passage Retrieval using separate question and passage encoders |\n"
            "| Recall@k | Fraction of questions with relevant evidence among top-k retrieved documents |\n"
            "| Exact Match | Strict normalized answer-string equality metric |\n"
            "| F1 | Token-overlap metric balancing precision and recall |\n"
            "| Domain adaptation | Further training a model on target-domain data |\n"
            "| RAG | Retrieval-Augmented Generation; generates answers using retrieved evidence |\n"
            "| RAG-Sequence | RAG formulation operating with document evidence at sequence level |\n"
            "| RAG-Token | RAG formulation allowing document evidence to vary across generated tokens |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What makes extractive QA different from ordinary text classification?\n"
            "2. What do the start and end logits represent?\n"
            "3. Why must QA systems support unanswerable questions?\n"
            "4. Why is a sliding window preferable to naive truncation?\n"
            "5. What is the role of the retriever?\n"
            "6. What is the role of the reader?\n"
            "7. Why can increasing top-k improve recall but worsen latency?\n"
            "8. How does DPR differ from BM25?\n"
            "9. Why should both EM and F1 be tracked?\n"
            "10. Why does SQuAD fine-tuning not transfer perfectly to SubjQA?\n"
            "11. Why does reader-only evaluation overestimate end-to-end system performance?\n"
            "12. How does RAG differ from an extractive retriever-reader pipeline?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A practical QA system is an evidence pipeline: retrieve the right passages, "
            "process long contexts safely, extract or generate an answer, and evaluate every "
            "stage separately. Retrieval quality sets the ceiling, domain adaptation improves "
            "the reader, and RAG extends the same evidence-first design from extraction to "
            "generation.**\n"
        ),

        "estimated_minutes": 135,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "qa-overview", "title": "What is question answering?", "order": 1},
            {"id": "subjqa", "title": "Build QA from customer reviews", "order": 2},
            {"id": "squad", "title": "Why SQuAD matters", "order": 3},
            {"id": "span-classification", "title": "Extractive QA is span classification", "order": 4},
            {"id": "tokenizing-qa", "title": "Tokenize question-context pairs", "order": 5},
            {"id": "qa-logits", "title": "Turn logits into an answer", "order": 6},
            {"id": "unanswerable", "title": "Handle unanswerable questions", "order": 7},
            {"id": "long-context", "title": "Long contexts and sliding windows", "order": 8},
            {"id": "retriever-reader", "title": "Retriever-reader architecture", "order": 9},
            {"id": "document-store", "title": "Document store and metadata", "order": 10},
            {"id": "bm25", "title": "Sparse retrieval with BM25", "order": 11},
            {"id": "reader", "title": "Reader answer extraction", "order": 12},
            {"id": "retriever-eval", "title": "Evaluate retriever recall", "order": 13},
            {"id": "dpr", "title": "Dense Passage Retrieval", "order": 14},
            {"id": "reader-eval", "title": "Evaluate reader EM and F1", "order": 15},
            {"id": "domain-adaptation", "title": "Domain adaptation", "order": 16},
            {"id": "whole-pipeline", "title": "Evaluate the whole QA pipeline", "order": 17},
            {"id": "generative-qa", "title": "Generative QA and RAG", "order": 18},
            {"id": "qa-hierarchy", "title": "Practical QA hierarchy", "order": 19},
        ],
    },

    "exercises": [
        {
            "id": "M01.L07.EX01",
            "title": "Trace an Extractive Answer Span",
            "lesson_code": "M01.L07",
            "section_id": "qa-logits",
            "placement": "after_section",
            "description": (
                "Practice reasoning from question/context tokens to valid answer start and end positions."
            ),
            "instructions": (
                "1. Use the context: 'The battery lasts around ten hours on one charge.'\n"
                "2. Use the question: 'How long does the battery last?'\n"
                "3. Tokenize the answer conceptually into words/tokens.\n"
                "4. Identify the start token and end token for the answer span.\n"
                "5. Explain why selecting an answer token from the question itself would be invalid.\n"
                "6. State two constraints a production QA postprocessor should enforce."
            ),
            "expected_output": (
                "A short token-span trace identifying 'around'/'ten' as a possible start and "
                "'hours' as the end depending on tokenization, plus constraints such as context-only "
                "selection and start <= end."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "extractive-qa",
                "span-classification",
                "start-end-logits",
            ],
        },
        {
            "id": "M01.L07.EX02",
            "title": "Tune Retrieval Depth",
            "lesson_code": "M01.L07",
            "section_id": "retriever-eval",
            "placement": "after_section",
            "description": (
                "Practice the recall-versus-latency trade-off when choosing how many documents "
                "to send from a retriever to a reader."
            ),
            "instructions": (
                "Suppose your retriever has the following results:\n"
                "k=1 -> recall 0.72, reader latency 40 ms\n"
                "k=3 -> recall 0.94, reader latency 105 ms\n"
                "k=5 -> recall 0.97, reader latency 165 ms\n"
                "k=10 -> recall 0.99, reader latency 320 ms\n\n"
                "1. Explain why recall improves with k.\n"
                "2. Explain why end-to-end latency also increases.\n"
                "3. Choose a reasonable k for a real-time ecommerce QA system and justify it.\n"
                "4. State what additional end-to-end metric you would inspect before finalizing the choice."
            ),
            "expected_output": (
                "A reasoned trade-off discussion, likely favoring an elbow point such as k=3 "
                "or k=5 rather than automatically choosing the maximum k, plus end-to-end EM/F1 "
                "and latency measurement."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "retriever-recall",
                "latency-tradeoffs",
                "system-evaluation",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L07.QZ01",
        "title": "Question Answering — Knowledge Check",
        "lesson_code": "M01.L07",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L07.Q01",
                "section_id": "span-classification",
                "question": "What does an extractive QA head usually predict?",
                "options": [
                    "One sentiment label for the whole document.",
                    "The start and end token positions of an answer span.",
                    "A document embedding only.",
                    "A complete generated paragraph with no source passage.",
                ],
                "correct": 1,
                "explanation": (
                    "Extractive QA is commonly framed as span classification, with one score "
                    "for each possible answer-start token and one for each answer-end token."
                ),
            },
            {
                "id": "M01.L07.Q02",
                "section_id": "long-context",
                "question": (
                    "Why is a sliding window useful for long QA contexts?"
                ),
                "options": [
                    "It deletes every token after the first sentence.",
                    "It creates overlapping model-sized context chunks so answers later in the "
                    "document are not lost to truncation.",
                    "It changes the task into image classification.",
                    "It guarantees that every question is answerable.",
                ],
                "correct": 1,
                "explanation": (
                    "Overlapping windows preserve coverage of long documents while respecting "
                    "the model's maximum input length."
                ),
            },
            {
                "id": "M01.L07.Q03",
                "section_id": "retriever-eval",
                "question": (
                    "Why does retriever recall place an upper bound on the QA system?"
                ),
                "options": [
                    "The reader can only extract an answer from evidence it receives.",
                    "Recall changes the tokenizer vocabulary.",
                    "Readers do not use documents.",
                    "Higher recall always reduces latency.",
                ],
                "correct": 0,
                "explanation": (
                    "If the relevant document is never retrieved, the reader does not have "
                    "the evidence required to extract the correct answer."
                ),
            },
            {
                "id": "M01.L07.Q04",
                "section_id": "dpr",
                "question": "What is the main idea behind DPR?",
                "options": [
                    "Represent both queries and passages as dense learned vectors using separate encoders.",
                    "Count only exact keyword frequencies without neural encoders.",
                    "Generate answers without retrieving any documents.",
                    "Store every document as a one-hot class label.",
                ],
                "correct": 0,
                "explanation": (
                    "DPR uses a bi-encoder setup that embeds questions and passages separately "
                    "and retrieves passages by vector similarity."
                ),
            },
            {
                "id": "M01.L07.Q05",
                "section_id": "generative-qa",
                "type": "open",
                "question": (
                    "Design a QA system for a large product-review catalog. Explain how you "
                    "would choose between BM25 and DPR, handle long reviews, evaluate retrieval "
                    "and reading separately, adapt the reader to the product domain, and decide "
                    "whether extractive QA or RAG should be the final answer layer."
                ),
            },
        ],

        "passing_score": 70,
    },
}
