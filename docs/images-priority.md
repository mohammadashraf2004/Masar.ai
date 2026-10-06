# Most important images — description for each

One lead figure per lesson (the first image the lesson calls for, usually the diagram that explains the whole lesson), plus the figures the manifests mark as required. The full list of every request is in [images-needed.md](images-needed.md).

Each entry: **lesson** — title, what to draw, and what the learner should notice. `key` is a suggested manifest key.


## COURSE-003_Applied_Deep_Learning — 14 images

1. **M01.L01** — **Feature engineering versus representation learning**  
   _Draw:_ A two-part diagram comparing a traditional ML pipeline where a practitioner manually creates features before a learning algorithm with a deep-learning pipeline where raw data enters a neural network that learns hierarchical features automatically during training  
   _Learner should notice:_ deep learning reduces manual feature design but typically increases dependence on data, training, and computation  
   `key: feature-engineering-versus-representation-learning`
2. **M02.L01** — **Pretrained image-classification inference pipeline**  
   _Draw:_ A diagram showing an input photograph being resized/cropped/normalized into a tensor, passed through a pretrained classifier, producing one score for each ImageNet class, followed by top-k label selection  
   _Learner should notice:_ inference requires both the trained network and the correct input/output processing around it  
   `key: pretrained-image-classification-inference-pipeline`
3. **M03.L01** — **Input-to-intermediate-to-output representations**  
   _Draw:_ A simple neural-network pipeline showing a human-interpretable input on the left, several layers of floating-point intermediate representations in the middle, and a human-usable output on the right  
   _Learner should notice:_ the network repeatedly transforms numeric representations and that the hidden intermediate representations are task-dependent  
   `key: input-to-intermediate-to-output-representations`
4. **M04.L01** — **RGB image channels**  
   _Draw:_ A color image shown alongside separate red, green, and blue intensity maps  
   _Learner should notice:_ a color image is represented as multiple aligned numerical channels rather than one scalar per pixel  
   `key: rgb-image-channels`
5. **M05.L01** — **Mental model of learning**  
   _Draw:_ A loop diagram showing input and target entering a model, model output compared with target through a loss function, gradients flowing backward to parameters, and parameters being updated before the next forward pass  
   _Learner should notice:_ learning is an iterative feedback process driven by prediction error  
   `key: mental-model-of-learning`
6. **M06.L01** — **Same training loop, different model**  
   _Draw:_ A diagram showing input and target entering the familiar training loop, with the model box changing from a linear equation to a neural network while loss, backward pass, optimizer, and validation stay the same  
   _Learner should notice:_ the model architecture changes but the training mechanics remain  
   `key: same-training-loop-different-model`
7. **M07.L01** — **End-to-end bird-vs-airplane classifier**  
   _Draw:_ A pipeline showing CIFAR-10 images entering preprocessing, a neural-network classifier, class scores, loss during training, and predicted bird/airplane labels during inference  
   _Learner should notice:_ the image classification system contains data preparation, model, loss, optimization, and evaluation  
   `key: end-to-end-bird-vs-airplane-classifier`
8. **M08.L01** — **Fully connected image processing versus convolution**  
   _Draw:_ Left side shows a flattened image densely connected to hidden units; right side shows a small kernel applied locally at many positions  
   _Learner should notice:_ convolution reuses the same small set of weights instead of learning independent weights for every pixel-location relationship  
   `key: fully-connected-image-processing-versus-convolution`
9. **M09.L01** — **Prediction versus generation**  
   _Draw:_ Left side shows regression/classification with one input leading to a constrained target; right side shows a text prefix branching into many plausible next-token continuations  
   _Learner should notice:_ generation is handled by modeling a probability distribution rather than selecting one permanently fixed answer  
   `key: prediction-versus-generation`
10. **M10.L01** — **Text generation versus image generation**  
   _Draw:_ Left side shows next-token probability generation; right side shows spatial image generation; both feed into a shared box labeled learn data distribution and sample new examples  
   _Learner should notice:_ different data structures can share the same generative objective  
   `key: text-generation-versus-image-generation`
11. **M11.L01** — **Raw CT data to PyTorch sample**  
   _Draw:_ Raw .mhd/.raw files and candidate CSV metadata flow through loading, coordinate conversion, cropping, tensor conversion, and finally a training-sample tuple  
   _Learner should notice:_ model-ready data is the result of several transformations, not one file-read call  
   `key: raw-ct-data-to-pytorch-sample`
12. **M12.L01** — **Chapter 13 end-to-end training pipeline**  
   _Draw:_ LunaDataset feeds DataLoader batches into a 3D classifier; the training branch computes loss, backward, and optimizer step, while the validation branch computes read-only metrics  
   _Learner should notice:_ this is the first complete train-and-evaluate loop for the CT project  
   `key: chapter-13-end-to-end-training-pipeline`
13. **M13.L01** — **Four binary-classification quadrants**  
   _Draw:_ A clean 2×2 confusion-grid showing true positive, true negative, false positive, and false negative with nodule/non-nodule examples  
   _Learner should notice:_ immediately see that false positives and false negatives are different mistakes with different consequences  
   `key: four-binary-classification-quadrants`
14. **M14.L01** — **Multi-stage CT pipeline with segmentation before classification**  
   _Draw:_ Raw CT slice enters a segmentation model, candidate regions are extracted, then passed into the existing classifier  
   _Learner should notice:_ segmentation answers where while classification answers what  
   `key: multi-stage-ct-pipeline-with-segmentation-before-classificat`

## COURSE-004_Applied_NLP_with_Transformers — 11 images

15. **M01.L01** — **Transformer evolution timeline**  
   _Draw:_ A simple chronological timeline showing the 2017 Transformer paper, ULMFiT, GPT, BERT, and the subsequent expansion of transformer models  
   _Learner should notice:_ modern transformer NLP emerged from the combination of a new architecture and practical transfer-learning methods  
   `key: transformer-evolution-timeline`
16. **M02.L01** — **Transformer text-classification pipeline**  
   _Draw:_ A simple flow from raw tweet to Dataset processing, tokenizer, DistilBERT, classification output, and prediction on new text  
   _Learner should notice:_ text must pass through data preparation and tokenization before the transformer can classify it  
   `key: transformer-text-classification-pipeline`
17. **M01.L02** — **Transformer encoder-decoder overview**  
   _Draw:_ A clean diagram showing input tokens entering an encoder stack, encoder outputs feeding a decoder stack, and the decoder generating output tokens one by one  
   _Learner should notice:_ the encoder processes the source sequence while the decoder produces the target sequence autoregressively  
   `key: transformer-encoder-decoder-overview`
18. **M01.L03** — **IOB2 named entity labeling**  
   _Draw:_ A short sentence with tokens shown in boxes and colored labels underneath for B-PER, I-PER, B-ORG, B-LOC, and O  
   _Learner should notice:_ B marks the start of an entity span, I continues it, and O means the token is not part of an entity  
   `key: iob2-named-entity-labeling`
19. **M01.L04** — **Autoregressive text generation loop**  
   _Draw:_ A step-by-step diagram showing prompt -> language model -> next-token probabilities -> selected token -> append token to prompt -> repeat  
   _Learner should notice:_ one new token is chosen per decoding step and the generated token becomes part of the next input  
   `key: autoregressive-text-generation-loop`
20. **M01.L05** — **Summarization as sequence-to-sequence learning**  
   _Draw:_ A long document entering an encoder-decoder transformer and a short summary coming out, with arrows showing compression from source sequence to target sequence  
   _Learner should notice:_ the output is a newly generated sequence rather than a fixed class label  
   `key: summarization-as-sequence-to-sequence-learning`
21. **M01.L07** — **Two-stage question answering system**  
   _Draw:_ A question enters a retriever that selects relevant documents, then a reader extracts an answer span from one of those documents  
   _Learner should notice:_ document retrieval and answer extraction are separate problems in a practical QA system  
   `key: two-stage-question-answering-system`
22. **M01.L06** — **Transformer production optimization overview**  
   _Draw:_ A large accurate transformer on the left and four optimization paths labeled distillation, quantization, ONNX Runtime, and pruning leading toward a smaller/faster deployment model  
   _Learner should notice:_ several techniques can be combined rather than treated as mutually exclusive choices  
   `key: transformer-production-optimization-overview`
23. **M01.L08** — **Low-label method decision tree**  
   _Draw:_ A decision tree beginning with 'Do you have labeled data?', then branching by amount of labeled data and availability of unlabeled data toward zero-shot, few-shot/embedding methods, domain adaptation/UDA/UST, or ordinary fine-tuning  
   _Learner should notice:_ the correct method depends on the available supervision, not on which technique sounds most advanced  
   `key: low-label-method-decision-tree`
24. **M01.L10** — **Fine-tuning versus training from scratch**  
   _Draw:_ A decision diagram comparing a small domain dataset flowing into pretrained-model fine-tuning versus a massive distinct domain corpus flowing into custom tokenizer training and fresh model pretraining  
   _Learner should notice:_ training from scratch requires both much more data and much more compute  
   `key: fine-tuning-versus-training-from-scratch`
25. **M01.L09** — **Three transformer research directions**  
   _Draw:_ A central transformer branching into three paths labeled scaling, efficient attention, and multimodal/beyond-text learning  
   _Learner should notice:_ the chapter treats these as distinct but complementary ways of extending transformer capability  
   `key: three-transformer-research-directions`

## COURSE-005_Applied_LLM_Engineering — 12 images

26. **M01.L01** — **...**  
   _Draw:_   
   `key: `
27. **M02.L01** — **...**  
   _Draw:_   
   `key: `
28. **M03.L01** — **Autoregressive token generation loop**  
   _Draw:_ Show an initial prompt entering the model, one output token being selected, that token appended to the prompt, and the enlarged sequence entering the model again for the next step  
   _Learner should notice:_ generation is an iterative loop rather than one operation that writes the whole answer at once  
   `key: autoregressive-token-generation-loop`
29. **M04.L01** — **Text classification overview**  
   _Draw:_ Show several example text inputs flowing into a language model/classifier and emerging as labels such as Positive, Negative, Billing Issue, and Shipping Issue  
   _Learner should notice:_ classification converts unstructured text into a small predefined set of labels  
   `key: text-classification-overview`
30. **M05.L01** — **Supervised classification versus unsupervised clustering**  
   _Draw:_ Left side shows labeled documents being assigned to predefined categories; right side shows unlabeled documents automatically forming semantic groups  
   _Learner should notice:_ clustering discovers structure rather than learning predefined labels  
   `key: supervised-classification-versus-unsupervised-clustering`
31. **M06.L01** — **Prompt engineering feedback loop**  
   _Draw:_ Show task requirements → draft prompt → LLM output → evaluate output → revise prompt → repeat  
   _Learner should notice:_ prompt engineering is an optimization loop rather than a one-time wording exercise  
   `key: prompt-engineering-feedback-loop`
32. **M07.L01** — **LLM system building blocks**  
   _Draw:_ Show an LLM in the center connected to model I/O, prompt templates/chains, memory, tools, and agent logic  
   _Learner should notice:_ the language model is one component inside a larger application architecture  
   `key: llm-system-building-blocks`
33. **M08.L01** — **Keyword search versus semantic search**  
   _Draw:_ Show the same query entering two pipelines: keyword search matching shared words and semantic search matching a differently worded but meaning-equivalent passage  
   _Learner should notice:_ semantic relevance does not require exact query terms  
   `key: keyword-search-versus-semantic-search`
34. **M09.L01** — **Multimodal model overview**  
   _Draw:_ Show several modalities—text, image, audio, video, sensors—feeding a multimodal model, with text as one possible output  
   _Learner should notice:_ input modality support and output modality support are separate capabilities  
   `key: multimodal-model-overview`
35. **M10.L01** — **Text to embedding**  
   _Draw:_ Show a document, sentence, and phrase entering an embedding model and each becoming a dense numerical vector  
   _Learner should notice:_ embeddings as learned numerical representations rather than arbitrary encodings  
   `key: text-to-embedding`
36. **M11.L01** — **Frozen versus fine-tuned classifier**  
   _Draw:_ Left side shows frozen BERT feeding a trainable classifier; right side shows both BERT and classification head trainable with backward arrows through the whole network  
   _Learner should notice:_ the difference between fixed feature extraction and end-to-end task adaptation  
   `key: frozen-versus-fine-tuned-classifier`
37. **M12.L01** — **Three-stage LLM training pipeline**  
   _Draw:_ Show an untrained Transformer progressing through pretraining → base model, supervised fine-tuning → instruction/chat model, and preference tuning → aligned model  
   _Learner should notice:_ memorize the different purpose of each stage  
   `key: three-stage-llm-training-pipeline`

## COURSE-006_Production_AI_Engineering — 9 images

38. **M01.L01** — **From traditional ML to AI engineering**  
   _Draw:_ A two-lane diagram comparing the traditional workflow of collecting data and training a task-specific model with the foundation-model workflow of selecting an existing model, adapting it, evaluating it, and integrating it into an application  
   _Learner should notice:_ AI engineering shifts much of the effort from model creation toward model adaptation and product development  
   `key: from-traditional-ml-to-ai-engineering`
39. **M02.L01** — **Foundation-model design map**  
   _Draw:_ A four-part diagram showing training data, architecture/scale, post-training, and sampling all feeding into downstream model behavior  
   _Learner should notice:_ application behavior is influenced by choices made both during training and during inference  
   `key: foundation-model-design-map`
40. **M03.L01** — **Evaluation around failure modes**  
   _Draw:_ A diagram showing an AI application in the center, surrounded by possible failure areas such as factual errors, unsafe outputs, poor retrieval, tool failure, latency, and user dissatisfaction, with evaluation methods mapped to those risks  
   _Learner should notice:_ evaluation should be designed from concrete failure modes rather than generic scores  
   `key: evaluation-around-failure-modes`
41. **M04.L01** — **Evaluation-driven development loop**  
   _Draw:_ A loop showing define criteria -> build prototype -> evaluate -> improve -> deploy -> collect production evidence -> refine criteria  
   _Learner should notice:_ evaluation starts before implementation and continues throughout the application's lifecycle  
   `key: evaluation-driven-development-loop`
42. **M06.L01** — **Instructions versus query-specific context**  
   _Draw:_ A diagram showing a shared system instruction combined with query-specific retrieved/tool-generated context before entering the model  
   _Learner should notice:_ instructions stay relatively stable while context changes for each query  
   `key: instructions-versus-query-specific-context`
43. **M07.L01** — **Prompting versus finetuning**  
   _Draw:_ A side-by-side diagram where prompting changes instructions/context around fixed model weights while finetuning updates some or all model weights  
   _Learner should notice:_ the adaptation happens in different places  
   `key: prompting-versus-finetuning`
44. **M08.L01** — **Dataset engineering lifecycle**  
   _Draw:_ A circular workflow showing define behavior -> acquire/annotate -> synthesize -> verify -> inspect/process -> train/evaluate -> return to curation  
   _Learner should notice:_ dataset engineering is iterative rather than linear  
   `key: dataset-engineering-lifecycle`
45. **M09.L01** — **Three levels of inference optimization**  
   _Draw:_ A layered diagram showing model-level, hardware-level, and service-level optimizations feeding latency and cost outcomes  
   _Learner should notice:_ inference efficiency is a systems problem, not only a model problem  
   `key: three-levels-of-inference-optimization`
46. **M10.L01** — **Progressive AI architecture**  
   _Draw:_ A left-to-right sequence starting with user->model and progressively adding context, guardrails, router/gateway, cache, agent loops, observability, and orchestration  
   _Learner should notice:_ each component is introduced to address a specific production need  
   `key: progressive-ai-architecture`

## COURSE-007_AI_Agents_With_MCP — 8 images

47. **M01.L01** — **Evolution from chatbot to augmented LLM**  
   _Draw:_ A four-stage diagram showing basic LLM chat, RAG with a vector database, function calling with an execution environment, and an augmented LLM with retrieval, tools, and memory  
   _Learner should notice:_ each stage adds capability around the model rather than replacing the model itself  
   `key: evolution-from-chatbot-to-augmented-llm`
48. **M02.L01** — **Host application with LLM and MCP clients**  
   _Draw:_ A diagram showing a user interacting with one host application that contains both an LLM-provider client and an MCP client; the LLM client points to the model API while the MCP client points to an MCP server  
   _Learner should notice:_ the two clients solve different communication problems but are coordinated by the same host  
   `key: host-application-with-llm-and-mcp-clients`
49. **M02.L02** — **Bidirectional MCP client capabilities**  
   _Draw:_ A diagram showing Host + MCP Client in the center, server-provided primitives flowing from MCP Server to Host, and client-provided capabilities sampling/roots/elicitation flowing back toward the server through callbacks  
   _Learner should notice:_ the client becomes an active boundary, not merely a passive connector  
   `key: bidirectional-mcp-client-capabilities`
50. **M03.L01** — **MCP server as a reusable distribution layer**  
   _Draw:_ A before-and-after diagram showing several applications each maintaining custom integrations versus several MCP clients connecting to one reusable MCP server  
   _Learner should notice:_ MCP moves integration knowledge out of each host application and into a reusable server boundary  
   `key: mcp-server-as-a-reusable-distribution-layer`
51. **M03.L02** — **Advanced MCP server capability map**  
   _Draw:_ A two-column diagram with server utilities on one side and client-provided capabilities on the other, both feeding into tools/prompts/resources  
   _Learner should notice:_ utilities improve operation while client capabilities let server workflows obtain external input  
   `key: advanced-mcp-server-capability-map`
52. **M03.L03** — **MCP server production lifecycle**  
   _Draw:_ A pipeline from server implementation through testing, evaluations, security hardening, packaging/deployment, and publication  
   _Learner should notice:_ passing unit tests is only one stage of production readiness  
   `key: mcp-server-production-lifecycle`
53. **M04.L01** — **MCP abstraction stack**  
   _Draw:_ A layered diagram showing application → MCP protocol/session → transport → network/process layer, with one JSON-RPC message flowing downward and upward  
   _Learner should notice:_ the transport does not decide tool semantics; it only carries protocol messages  
   `key: mcp-abstraction-stack`
54. **M05.L01** — **MCP ecosystem beyond the core protocol**  
   _Draw:_ A diagram with Core MCP in the center and branches for registry/discovery, governance/gateways, context management, testing, extensions, and contribution/governance  
   _Learner should notice:_ the core protocol is only one layer of the larger MCP ecosystem  
   `key: mcp-ecosystem-beyond-the-core-protocol`

## COURSE-008_Vision_Language_and_Multimodal_AI_Engineering — 11 images

55. **M01.L01** — **DCT compression intuition**  
   _Draw:_ Show one image block, its DCT coefficient grid with most energy concentrated near the low-frequency corner, a thresholded coefficient grid, and a reconstructed block  
   _Learner should notice:_ visually important structure can often be preserved even after many small high-frequency coefficients are removed  
   `key: dct-compression-intuition`
56. **M01.L02** — **Early image-captioning architecture**  
   _Draw:_ Show an image entering a CNN encoder, the visual feature vector flowing into an RNN/LSTM decoder, and a caption being generated word by word  
   _Learner should notice:_ image captioning as an encoder-decoder mapping from visual representation to language  
   `key: early-image-captioning-architecture`
57. **M01.L03** — **Training paradigms versus training stages**  
   _Draw:_ Create a two-axis diagram. One axis lists HOW: supervised, unsupervised, self-supervised, semi-supervised, contrastive. The other lists WHEN: pretraining, midtraining, post-training, alignment. Show that a stage can use multiple paradigms rather than implying a one-to-one mapping  
   _Learner should notice:_ "contrastive learning" and "pretraining" are not competing terms because they answer different questions  
   `key: training-paradigms-versus-training-stages`
58. **M01.L04** — **Cascaded versus live multimodal interface**  
   _Draw:_ Left: microphone → ASR → transcript → text model → TTS → audio. Right: one stateful live session receiving audio + visual frames + text and returning streamed audio/text/tool events  
   _Learner should notice:_ the number of explicit processing boundaries and where information can be lost in the cascade  
   `key: cascaded-versus-live-multimodal-interface`
59. **M01.L05** — **Post-training roadmap**  
   _Draw:_ Show pretrained VLM branching into SFT, preference alignment, and verifiable-reward optimization, with LoRA/DoRA/QLoRA shown as efficiency tools underneath  
   _Learner should notice:_ distinguish the learning objective from the efficiency method  
   `key: post-training-roadmap`
60. **M01.L06** — **Attention intuition**  
   _Draw:_ Show the words in "The AI community building the future" with stronger arrows from AI to future and community and weaker arrows to less relevant words  
   _Learner should notice:_ attention as weighted information gathering rather than a hard one-to-one lookup  
   `key: attention-intuition`
61. **M01.L07** — **VLM inference pipeline**  
   _Draw:_ Show image → vision encoder → visual tokens merging with prompt tokens before the LLM, followed by prefill and autoregressive decode  
   _Learner should notice:_ the image may be encoded once but its visual tokens remain in the context  
   `key: vlm-inference-pipeline`
62. **M01.L08** — **Document AI task map**  
   _Draw:_ Show one document page branching into direct QA, OCR/parsing, layout analysis, classification, field extraction, retrieval, and multimodal RAG  
   _Learner should notice:_ Document AI is a family of tasks rather than one single model problem  
   `key: document-ai-task-map`
63. **M01.L09** — **Video-language task map**  
   _Draw:_ Show one video branching into classification, embedding-based retrieval, captioning, summarization, and question answering  
   _Learner should notice:_ distinguish label output, vector output, and free-form text output  
   `key: video-language-task-map`
64. **M01.L10** — **Any-to-any multimodal system**  
   _Draw:_ Show text, image, audio, and video entering a multimodal reasoning system with text, image, speech/audio, and video outputs  
   _Learner should notice:_ any-to-any concerns both input and output modalities, not only multimodal perception  
   `key: any-to-any-multimodal-system`
65. **M01.L11** — **Agency spectrum**  
   _Draw:_ Show tool routing → structured tool calling → multistep ReAct agent, with increasing autonomy and increasing complexity/risk  
   _Learner should notice:_ agency is a design continuum  
   `key: agency-spectrum`

## COURSE-009-Enterprise-RAG-Engineering — 10 images

66. **M01.L01** — **Basic RAG architecture**  
   _Draw:_ A user query flowing first to a retrieval component that fetches relevant information from a private knowledge source, then to an LLM that receives both the query and retrieved context and produces the final answer  
   _Learner should notice:_ retrieval happens before generation and that the LLM is grounded by external context  
   `key: basic-rag-architecture`
67. **M01.L02** — **Base RAG stack overview**  
   _Draw:_ Two horizontal flows: ingestion ' 'as source data → parsing → chunking → embedding/indexing → vector ' 'database, and query as user query → query rewriting → embedding/search → ' 'reranking → prompt → generative LLM → answer  
   _Learner should notice:_ ' 'ingestion prepares knowledge ahead of time while the query flow runs for ' 'every request  
   `key: base-rag-stack-overview`
68. **M01.L03** — **Enterprise RAG scaling map**  
   _Draw:_ Diagram showing data volume, ' 'query load, data complexity, retrieval quality, guardrails, and UX ' 'surrounding a central RAG pipeline  
   _Learner should notice:_ scale ' 'affects several interacting dimensions, not one component  
   `key: enterprise-rag-scaling-map`
69. **M01.L04** — **POC-to-production RAG transition**  
   _Draw:_ A side-by-side diagram ' 'showing a small POC stack on the left and a distributed production stack ' 'with security, monitoring, scaling, staging, and CI/CD on the right  
   _Learner should notice:_ ' 'Learner should notice that production adds operational systems around the ' 'same core RAG logic  
   `key: poc-to-production-rag-transition`
70. **M01.L05** — **DIY RAG versus RAG platform**  
   _Draw:_ Show an application ' 'connected either to many individually managed RAG components or to one ' 'standardized platform API backed by managed components  
   _Learner should notice:_ Notice that the ' 'main difference is ownership of infrastructure complexity, not the ' 'disappearance of the RAG stages  
   `key: diy-rag-versus-rag-platform`
71. **M01.L06** — **RAG evaluation layers**  
   _Draw:_ Show ingestion → retrieval → ' 'generation → user/system outcomes with metrics attached to each layer  
   _Learner should notice:_ ' 'Notice that final answer quality is downstream of multiple independently ' 'measurable stages  
   `key: rag-evaluation-layers`
72. **M01.L07** — **AI agent evolution timeline**  
   _Draw:_ A timeline from Actor Model ' 'and BDI agents through voice assistants, ReAct, tool calling, and modern ' 'LLM agents.  
   _Learner should notice:_ Autonomy predates LLMs; LLMs mainly change flexibility, ' 'language understanding, and planning.  
   `key: ai-agent-evolution-timeline`
73. **M01.L08** — **Conversion vs native multimodal RAG**  
   _Draw:_ Side-by-side ' 'architecture showing non-text data converted to text/JSON versus raw ' 'multimodal embeddings/VLM path  
   _Learner should notice:_ Notice where information is transformed ' 'and where expensive multimodal reasoning occurs  
   `key: conversion-vs-native-multimodal-rag`
74. **M01.L09** — **Example movie knowledge graph**  
   _Draw:_ Show Person and Movie ' 'nodes connected by DIRECTED and ACTED_IN edges  
   _Learner should notice:_ ' 'typed nodes, typed edges, and direction  
   `key: example-movie-knowledge-graph`
75. **M01.L10** — **Late-interaction retrieval**  
   _Draw:_ Compare one-vector-per-chunk ' 'dense retrieval with token-level document vectors matched to query tokens ' 'at query time  
   _Learner should notice:_ accuracy versus storage/memory ' 'trade-off  
   `key: late-interaction-retrieval`

## COURSE-010-AI-Service-Engineering-with-FastAPI — 12 images

76. **M01.L01** — **Generative model training and sampling**  
   _Draw:_ A simple two-stage diagram showing a butterfly-image dataset flowing into model training, followed by a trained model being sampled to produce several new butterfly images with visible variation  
   _Learner should notice:_ the separation between training and inference and that generated outputs are related to, but not identical to, the training examples  
   `key: generative-model-training-and-sampling`
77. **M01.L02** — **FastAPI Swagger UI**  
   _Draw:_ A screenshot or recreated local development view of a FastAPI `/docs` page showing at least two endpoints, their HTTP methods, parameters, and the interactive 'Try it out' workflow  
   _Learner should notice:_ endpoint documentation and interactive testing are generated from the API definitions rather than being written manually  
   `key: fastapi-swagger-ui`
78. **M01.L03** — **RNN versus transformer sequence processing**  
   _Draw:_ Side-by-side diagram: an RNN processing tokens sequentially through a carried state vector, and a transformer processing the whole sequence with attention connections between distant tokens  
   _Learner should notice:_ RNN information flows step-by-step while transformer attention can directly represent long-range token relationships  
   `key: rnn-versus-transformer-sequence-processing`
79. **M01.L04** — **Static type error in an IDE**  
   _Draw:_ A Python editor showing a function annotated to accept an integer timestamp and an incorrect call passing a string, with the type checker highlighting the argument mismatch  
   _Learner should notice:_ the problem is surfaced before the code is run in production  
   `key: static-type-error-in-an-ide`
80. **M01.L05** — **Concurrency versus parallelism timeline**  
   _Draw:_ Three horizontal diagrams showing sequential execution, concurrent interleaved execution on one worker, and parallel execution on several workers/cores  
   _Learner should notice:_ concurrency overlaps progress while parallelism executes work simultaneously on separate compute resources  
   `key: concurrency-versus-parallelism-timeline`
81. **M01.L06** — **Traditional response versus streaming AI response**  
   _Draw:_ Side-by-side timeline showing a normal HTTP request where nothing appears until full completion, versus a streaming request where partial text chunks arrive throughout model generation  
   _Learner should notice:_ streaming improves time-to-first-visible-output without necessarily reducing total generation time  
   `key: traditional-response-versus-streaming-ai-response`
82. **M01.L07** — **Database system hierarchy**  
   _Draw:_ Diagram showing database server → database → schema → table/collection → rows/documents, with SQL and NoSQL branches  
   _Learner should notice:_ different database products still share a broad hierarchy of server, logical databases, structures, and records  
   `key: database-system-hierarchy`
83. **M01.L08** — **Authentication versus authorization**  
   _Draw:_ Two-stage access diagram showing a user first proving identity, then passing a second permission check for a resource/action  
   _Learner should notice:_ knowing who the user is does not automatically grant access  
   `key: authentication-versus-authorization`
84. **M01.L09** — **GenAI attack surface**  
   _Draw:_ A defensive architecture diagram showing user inputs, external documents, model, tools/plugins, downstream systems, and stored sensitive data, with risk markers at prompt injection, malicious external content, unsafe output handling, excessive tool permissions, and resource exhaustion  
   _Learner should notice:_ GenAI security spans inputs, model behavior, outputs, integrations, and infrastructure  
   `key: genai-attack-surface`
85. **M01.L10** — **AI service optimization map**  
   _Draw:_ Diagram splitting optimization goals into performance (latency, throughput, memory, cost) and quality (reliability, structure, alignment), with techniques connected to each side: batching/caching/quantization and structured output/prompting/fine-tuning  
   _Learner should notice:_ each technique addresses a specific bottleneck rather than being a universal improvement  
   `key: ai-service-optimization-map`
86. **M01.L11** — **Unit integration and E2E boundaries**  
   _Draw:_ Three diagrams over one GenAI pipeline: unit boundary around one function, integration boundary around two interacting components, and E2E boundary around the full user workflow  
   _Learner should notice:_ test scope expands from isolated logic to complete workflows  
   `key: unit-integration-and-e2e-boundaries`
87. **M01.L12** — **Deployment options for a GenAI service**  
   _Draw:_ Four branches from one FastAPI/GenAI application to VM, serverless function, managed application platform, and container deployment  
   _Learner should notice:_ deployment choice depends on workload and operational requirements rather than one universal method  
   `key: deployment-options-for-a-genai-service`

## COURSE-011_Cloud_Deployment_and_CI_CD_for_AI_Engineers — 17 images

88. **M08.L01** — **AWS root versus IAM daily-access model**  
   _Draw:_ A diagram showing Root User protected with 2FA and used for account-level control, while an IAM developer user belongs to a developer group with scoped service policies  
   _Learner should notice:_ the separation between account ownership and routine development access  
   `key: aws-root-versus-iam-daily-access-model`
89. **M08.L02** — **EC2 SSH connection anatomy**  
   _Draw:_ A diagram showing local computer + private PEM key → TCP 22 security-group rule → EC2 Elastic IP → Amazon Linux ec2-user shell  
   _Learner should notice:_ the separate roles of private key, network rule, public address, and Linux username  
   `key: ec2-ssh-connection-anatomy`
90. **M08.L03** — **Network Load Balancer fronting EC2**  
   _Draw:_ A diagram showing a trusted external client reaching an internet-facing AWS Network Load Balancer, which forwards through TCP target groups to the EC2 instance's private IP  
   _Learner should notice:_ the load balancer becomes the public gateway while EC2 is reached as a backend target  
   `key: network-load-balancer-fronting-ec2`
91. **M08.L04** — **Final domain and HTTPS architecture**  
   _Draw:_ A high-level flow showing Browser → custom domain DNS → AWS load-balancer layer → EC2 → Nginx TLS termination → Streamlit container  
   _Learner should notice:_ the custom domain identifies the service while Nginx presents the certificate and proxies to the application  
   `key: final-domain-and-https-architecture`
92. **M08.L05** — **Chapter 5 multi-service architecture**  
   _Draw:_ A diagram showing Nginx with TLS in front of three Docker services: Streamlit on internal 8501, Flask on 8502, and Jenkins on 8080, with external secure ports 8501, 8502, and 8504  
   _Learner should notice:_ the external Jenkins port differs from the internal Jenkins port  
   `key: chapter-5-multi-service-architecture`
93. **M08.L06** — **Port-based URLs versus subdomain URLs**  
   _Draw:_ A before/after diagram. Before: one domain with :8501, :8502, :8504. After: streamlit.domain, flask.domain, jenkins.domain all entering through ports 80/443  
   _Learner should notice:_ service identity moves from the port number into the hostname  
   `key: port-based-urls-versus-subdomain-urls`
94. **M08.L07** — **AWS-to-GCP conceptual migration**  
   _Draw:_ A side-by-side diagram showing the same Streamlit/Flask/Jenkins/Nginx application stack, with AWS EC2/networking on the left and GCP Compute Engine/firewall/static IP on the right  
   _Learner should notice:_ the application architecture is preserved while cloud-specific infrastructure changes  
   `key: aws-to-gcp-conceptual-migration`
95. **M08.L08** — **VM-to-image-to-replicas**  
   _Draw:_ A diagram showing a configured GCP VM disk being preserved, converted into a custom image, then reused to create multiple identical VM instances  
   _Learner should notice:_ the image becomes the reusable machine blueprint  
   `key: vm-to-image-to-replicas`
96. **M08.L09** — **VM deployment versus serverless deployment**  
   _Draw:_ A side-by-side diagram showing VM deployment where the engineer manages OS, Docker, services, scaling, and application versus Cloud Run where the engineer provides a container and Google manages infrastructure and scaling  
   _Learner should notice:_ serverless removes infrastructure-management responsibility rather than eliminating physical servers  
   `key: vm-deployment-versus-serverless-deployment`
97. **M08.L10** — **VM AWS stack versus Fargate stack**  
   _Draw:_ A before/after architecture. Before: EC2 + Docker Compose + Nginx + Flask + Streamlit + Jenkins. After: ALB → ECS Fargate Flask/Streamlit tasks, with ECR and CloudWatch around them  
   _Learner should notice:_ Fargate replaces server/container-host management while ALB replaces Nginx's public routing role  
   `key: vm-aws-stack-versus-fargate-stack`
98. **M01.L01** — **Breaking the wall of confusion**  
   _Draw:_ A before-and-after diagram. On the left, Development and Operations are separated by a wall and exchange a large risky release. On the right, Dev, Ops, QA, Security, and Product collaborate around one continuous delivery flow with shared feedback arrows  
   _Learner should notice:_ DevOps changes the organizational flow and ownership model, not merely the toolset  
   `key: breaking-the-wall-of-confusion`
99. **M02.L01** — **Git three-tree workflow**  
   _Draw:_ A diagram showing Working Directory → Staging Area → Local Repository, with `git add` on the first arrow and `git commit` on the second. Also show `git status` observing the working/staging state  
   _Learner should notice:_ editing a file is not the same as staging it, and staging it is not the same as committing it  
   `key: git-three-tree-workflow`
100. **M03.L01** — **Containers versus virtual machines**  
   _Draw:_ A side-by-side architecture diagram. VM side: hardware/host, hypervisor, multiple guest OS layers, each with libraries and app. Container side: hardware/host OS, container engine, multiple containers sharing the host kernel, each with libraries and app  
   _Learner should notice:_ VMs repeat the guest operating system while containers share the host kernel  
   `key: containers-versus-virtual-machines`
101. **M04.L01** — **Click-ops versus Infrastructure as Code**  
   _Draw:_ A side-by-side diagram. Left side shows a human manually clicking through cloud-console screens to create resources. Right side shows version-controlled Terraform files flowing through Terraform into cloud APIs to create the same resources  
   _Learner should notice:_ IaC turns manual infrastructure steps into repeatable, reviewable configuration  
   `key: click-ops-versus-infrastructure-as-code`
102. **M05.L01** — **Continuous Integration feedback loop**  
   _Draw:_ A loop showing developer commit → push/pull request → CI runner → build → automated tests → pass/fail feedback returning immediately to the developer  
   _Learner should notice:_ CI's main value is fast feedback after small integrations  
   `key: continuous-integration-feedback-loop`
103. **M06.L01** — **From Docker container to Kubernetes orchestration**  
   _Draw:_ A progression diagram showing one Docker container on a laptop, then many containers across multiple servers, followed by Kubernetes managing placement, health, networking, scaling, and updates  
   _Learner should notice:_ orchestration solves lifecycle and scale problems that appear after containerization  
   `key: from-docker-container-to-kubernetes-orchestration`
104. **M07.L01** — **Monitoring versus observability**  
   _Draw:_ A side-by-side diagram. Monitoring side shows predefined dashboards watching CPU, memory, latency, and errors. Observability side shows an engineer starting with an unexpected symptom and exploring correlated logs, metrics, and traces to discover a root cause  
   _Learner should notice:_ monitoring answers predefined questions while observability supports exploratory investigation  
   `key: monitoring-versus-observability`

## COURSE-012_AI_Agents_Foundations — 11 images

105. **M01.L01** — **Reactive LLM versus goal-directed agent**  
   _Draw:_ A side-by-side diagram. Left: User -> LLM -> Text response -> Stop. Right: User goal -> Agent -> Plan -> Tool actions -> Observe results -> Continue/finish  
   _Learner should notice:_ the agent has a continuing control loop instead of a single prompt-response interaction  
   `key: reactive-llm-versus-goal-directed-agent`
106. **M01.L02** — **LLM training versus inference**  
   _Draw:_ A two-part diagram. Left: training text -> tokenization -> prediction -> loss -> backpropagation -> updated weights. Right: prompt -> tokenization -> model -> next-token probabilities -> sampling -> generated token -> repeated generation  
   _Learner should notice:_ training changes model weights, while inference uses the already-trained weights to generate tokens  
   `key: llm-training-versus-inference`
107. **M01.L03** — **Before MCP versus with MCP**  
   _Draw:_ Left: one agent connected to filesystem, database, web API, and SaaS service through four different custom connectors. Right: the agent connects through MCP to reusable servers that wrap those services  
   _Learner should notice:_ MCP standardizes the integration boundary rather than eliminating the underlying services  
   `key: before-mcp-versus-with-mcp`
108. **M01.L04** — **Monolithic agent versus structured multi-agent system**  
   _Draw:_ Left: one overloaded agent with many tools and responsibilities. Right: several specialized agents connected through a clear flow, each with a small tool set  
   _Learner should notice:_ decomposition reduces responsibility per agent but adds coordination boundaries  
   `key: monolithic-agent-versus-structured-multi-agent-system`
109. **M01.L05** — **Decomposition versus planning**  
   _Draw:_ Left: one large goal breaking into several subproblems. Right: the same subproblems connected by arrows showing order, dependencies, and parallel branches  
   _Learner should notice:_ decomposition defines the pieces while planning defines how the pieces fit together  
   `key: decomposition-versus-planning`
110. **M01.L06** — **External storage versus bounded context**  
   _Draw:_ Show a large database/vector store containing many documents and memories on the left, a retrieval filter in the middle, and a small context window feeding an LLM on the right  
   _Learner should notice:_ retrieval selects a small relevant subset from a much larger store  
   `key: external-storage-versus-bounded-context`
111. **M01.L07** — **Agent evaluation feedback loop**  
   _Draw:_ Show an agent producing outputs, several evaluation sources around it (tests, human, grounding agent, critic), an evaluation store, and an arrow from the stored findings back to system improvement  
   _Learner should notice:_ evaluation creates an improvement loop rather than acting as a one-time test  
   `key: agent-evaluation-feedback-loop`
112. **M01.L08** — **Three agent consumption patterns**  
   _Draw:_ Show three side-by-side architectures: Browser/App with embedded agent; App -> API -> Backend Agent; App/Agent -> MCP/API/A2A -> Containerized Agent Service  
   _Learner should notice:_ agent placement changes the trust boundary and communication path  
   `key: three-agent-consumption-patterns`
113. **M01.L09** — **Three layers of the agentic loop**  
   _Draw:_ Show nested or stacked layers: Layer 1 internal SPAL inside one agent, Layer 2 external task loop around the agent, and Layer 3 orchestrator/collaboration meta loop controlling several agents or task loops  
   _Learner should notice:_ each higher layer expands control beyond the previous loop  
   `key: three-layers-of-the-agentic-loop`
114. **M01.L10** — **Reasoning primitives versus cognitive architecture**  
   _Draw:_ Left: separate boxes for CoT, ReAct, ToT, Reflexion used independently. Right: a cognitive architecture that dynamically selects and monitors these primitives through feedback  
   _Learner should notice:_ the new capability is strategy selection and adaptation, not simply more reasoning  
   `key: reasoning-primitives-versus-cognitive-architecture`
115. **M01.L11** — **Five-layer production checklist**  
   _Draw:_ Stack five horizontal layers labeled Persona, Tools & Actions, Reasoning & Planning, Knowledge & Memory, Evaluation & Feedback. Inside each layer show 3-4 best-practice keywords from the lesson  
   _Learner should notice:_ production quality depends on all five layers rather than one clever prompt  
   `key: five-layer-production-checklist`

## COURSE-013_Applied_Data_Analysis_with_Python — 15 images

116. **M01.L01** — **Raw data to business decision pipeline**  
   _Draw:_ A horizontal workflow showing raw transactions → cleaning → exploration → metrics/models → visualizations → interpretation → business decision  
   _Learner should notice:_ analysis involves multiple linked stages rather than only charts or code  
   `key: raw-data-to-business-decision-pipeline`
117. **M02.L01** — **NumPy shape intuition**  
   _Draw:_ Show a 1D array with shape (6,), a 2D 2×3 matrix with shape (2,3), and a simple 3D block labeled (2,2,3)  
   _Learner should notice:_ shape describes the size of each axis  
   `key: numpy-shape-intuition`
118. **M03.L01** — **Attribute-type decision tree**  
   _Draw:_ A branching diagram: categorical → nominal/ordinal; numeric → interval/ratio; numeric also branching to discrete/continuous  
   _Learner should notice:_ the statistical method starts with understanding the kind of variable  
   `key: attribute-type-decision-tree`
119. **M04.L01** — **Scalar vector matrix tensor hierarchy**  
   _Draw:_ Show a single number, a 1D vector, a 2D grid, and a 3D stack of grids with dimension labels 0D, 1D, 2D, 3D  
   _Learner should notice:_ connect dimensionality with data structure complexity  
   `key: scalar-vector-matrix-tensor-hierarchy`
120. **M05.L01** — **From raw values to visual insight**  
   _Draw:_ Show the same yearly sales values as a small table on the left and a line chart on the right, highlighting the 2021 dip and 2025 peak  
   _Learner should notice:_ why patterns can become easier to recognize visually  
   `key: from-raw-values-to-visual-insight`
121. **M06.L01** — **CSV round-trip**  
   _Draw:_ CSV text file → pd.read_csv() → DataFrame → processing → df.to_csv() → output CSV, with index/header controls labeled  
   _Learner should notice:_ reading and writing as two directions of the same workflow  
   `key: csv-round-trip`
122. **M07.L01** — **Data cleaning decision flow**  
   _Draw:_ Raw messy dataset → EDA → diagnose missing/outliers/inconsistency → choose treatment → validate cleaned dataset, with a warning branch for overcleaning  
   _Learner should notice:_ cleaning as a reasoning workflow rather than a delete-everything process  
   `key: data-cleaning-decision-flow`
123. **M08.L01** — **Tabular versus time-series order**  
   _Draw:_ On the left, ordinary rows that can be shuffled; on the right, dated observations connected in chronological order with arrows showing dependency through time  
   _Learner should notice:_ why temporal order must be preserved  
   `key: tabular-versus-time-series-order`
124. **M09.L01** — **Regression versus classification**  
   _Draw:_ Left side shows points with a fitted numeric prediction line and continuous output; right side shows two colored classes separated by a boundary  
   _Learner should notice:_ immediately distinguish continuous prediction from class assignment  
   `key: regression-versus-classification`
125. **M10.L01** — **High-dimensional reduction concept**  
   _Draw:_ Many original feature axes compressed into a 2D projection while some information is preserved and some is lost  
   _Learner should notice:_ dimensionality reduction as representation, not deletion of arbitrary columns  
   `key: high-dimensional-reduction-concept`
126. **M11.L01** — **Ensemble intuition**  
   _Draw:_ Three different base models making partly different mistakes, then an aggregation block producing a stronger final prediction  
   _Learner should notice:_ error diversification and combination  
   `key: ensemble-intuition`
127. **M12.L01** — **Artificial neuron**  
   _Draw:_ Inputs x1...xn multiplied by weights, summed with bias, passed through activation function, producing output  
   _Learner should notice:_ identify every component of one neuron  
   `key: artificial-neuron`
128. **M13.L01** — **Text-analysis pipeline**  
   _Draw:_ Raw customer reviews flowing through preprocessing, vectorization, model, and insights such as sentiment/spam/topic  
   _Learner should notice:_ the end-to-end role of text analysis  
   `key: text-analysis-pipeline`
129. **M14.L01** — **Image array representations**  
   _Draw:_ Same small image shown as grayscale 2D matrix, RGB 3-channel stack, and RGBA 4-channel stack  
   _Learner should notice:_ connect visible pixels with array dimensions  
   `key: image-array-representations`
130. **M15.L01** — **RNN versus transformer sequence processing**  
   _Draw:_ Left shows sequential token-by-token recurrent processing; right shows all tokens connected through attention in parallel  
   _Learner should notice:_ the transformer motivation  
   `key: rnn-versus-transformer-sequence-processing`

## COURSE-014-image-processing-computer-vision-engineering — 13 images

131. **M01.L01** — **Image as matrix and tensor**  
   _Draw:_ Show one grayscale image beside a 2D intensity matrix and one RGB image beside a 3D H x W x 3 tensor with R, G, and B channels  
   _Learner should notice:_ connect visible pixels to numerical array elements and understand why grayscale is 2D while RGB is 3D  
   `key: image-as-matrix-and-tensor`
132. **M02.L01** — **Image manipulation mental model**  
   _Draw:_ A diagram with one input image branching into pixel-value transforms, geometric-coordinate transforms, and channel/compositing transforms, with 2–3 examples under each branch  
   _Learner should notice:_ many different APIs reduce to a few reusable mathematical ideas  
   `key: image-manipulation-mental-model`
133. **M03.L01** — **Advanced image manipulation concept map**  
   _Draw:_ A diagram connecting value mapping, spatial mapping, interpolation, filtering, masking/compositing, compression, and visualization to example effects such as gamma, homography, blur, vignette, JPEG, and contours  
   _Learner should notice:_ many APIs are implementations of a small number of reusable ideas  
   `key: advanced-image-manipulation-concept-map`
134. **M04.L01** — **Sampling versus quantization**  
   _Draw:_ Show a smooth continuous grayscale surface on the left, a spatial sampling grid in the middle, and the same samples restricted to a small number of intensity levels on the right  
   _Learner should notice:_ clearly distinguish discretizing position from discretizing pixel value  
   `key: sampling-versus-quantization`
135. **M05.L01** — **Sliding 2D convolution**  
   _Draw:_ Show a small grayscale image grid, a highlighted 3×3 neighborhood, a 3×3 kernel, element-wise multiplications, their sum, and the resulting output pixel  
   _Learner should notice:_ convolution is repeated local weighted aggregation  
   `key: sliding-2d-convolution`
136. **M06.L01** — **Frequency filtering pipeline**  
   _Draw:_ Show one grayscale image, its centered Fourier magnitude spectrum, a circular filter mask, the masked spectrum, and the reconstructed output  
   _Learner should notice:_ frequency filtering is coefficient selection/attenuation followed by inverse transformation  
   `key: frequency-filtering-pipeline`
137. **M07.L01** — **Image enhancement strategy map**  
   _Draw:_ A diagram grouping enhancement methods by information used: single pixel, global histogram, local neighborhood, non-local patches, multi-scale wavelets, and learned models  
   _Learner should notice:_ enhancement methods differ mainly in what context they use to decide a new pixel value  
   `key: image-enhancement-strategy-map`
138. **M08.L01** — **Image profile and first derivative**  
   _Draw:_ Show a 1D row through alternating dark/bright image regions, the corresponding intensity profile, and derivative spikes at transitions  
   _Learner should notice:_ why edges appear as peaks in first-order derivatives  
   `key: image-profile-and-first-derivative`
139. **M09.L01** — **Image restoration degradation model**  
   _Draw:_ Show clean image f passing through PSF h and additive noise n to produce degraded image g, then a restoration block estimating f-hat  
   _Learner should notice:_ restoration as reversing a modeled forward process  
   `key: image-restoration-degradation-model`
140. **M10.L01** — **Segmentation evolution map**  
   _Draw:_ Show one image flowing through threshold-based regions, watershed regions, superpixels/graphs, CNN semantic map, instance masks, and panoptic output  
   _Learner should notice:_ segmentation evolving from hand-crafted local rules to learned global/object-centric reasoning  
   `key: segmentation-evolution-map`
141. **M11.L01** — **Fixed-label versus promptable segmentation**  
   _Draw:_ Show left: image entering a fixed-class semantic model producing a predefined class map; right: the same image plus point/box/text prompts entering a prompt-conditioned model producing different masks  
   _Learner should notice:_ the prompt changes the requested segmentation without retraining  
   `key: fixed-label-versus-promptable-segmentation`
142. **M12.L01** — **Pixel space to semantic embedding space**  
   _Draw:_ Show several animal images passing through a CNN into high-dimensional vectors, then a 2D conceptual embedding where dogs cluster together, cats cluster together, and unrelated animals are farther apart  
   _Learner should notice:_ representation geometry becomes semantically meaningful  
   `key: pixel-space-to-semantic-embedding-space`
143. **M13.L01** — **Evolution of generative vision**  
   _Draw:_ Show a timeline/flow from cGAN/CVAE → Pix2Pix/CycleGAN → StyleGAN/GFPGAN → DDPM/LDM → Stable Diffusion/SDXL → ControlNet/IP-Adapter → multimodal image APIs  
   _Learner should notice:_ increasingly flexible conditioning and control  
   `key: evolution-of-generative-vision`

## COURSE-015_Voice_AI_Engineering_Real_Time_Voice_Agents — 13 images

144. **M01.L01** — **Five-stage evolution of AI agents**  
   _Draw:_ A left-to-right diagram showing Stage 0 classical agents, Stage 1 foundation models, Stage 2 foundation models plus RAG, Stage 3 tool-using agents, and Stage 4 multi-agent systems  
   _Learner should notice:_ retrieval adds knowledge, tools add action, and multi-agent systems add specialization and collaboration  
   `key: five-stage-evolution-of-ai-agents`
145. **M01.L02** — **Intent-and-slot voice assistant**  
   _Draw:_ A diagram showing several example utterances flowing into one Intent block, with extracted slots such as song_title and artist_name feeding a predefined backend action  
   _Learner should notice:_ the system behaves like a structured form-filling pipeline rather than open-ended contextual reasoning  
   `key: intent-and-slot-voice-assistant`
146. **M01.L03** — **Persona configuration layers**  
   _Draw:_ A diagram showing System Instructions controlling tone/rules and Voice Configuration controlling speech sound, both feeding the same live assistant session  
   _Learner should notice:_ character is produced by multiple configuration layers rather than one prompt alone  
   `key: persona-configuration-layers`
147. **M01.L04** — **Agent framework capability map**  
   _Draw:_ A central Agent Framework box connected to Orchestration, Memory, Tools, Multi-Agent Communication, Human-in-the-Loop, and Streaming/Observability  
   _Learner should notice:_ the framework surrounds the model with operational capabilities rather than replacing the model  
   `key: agent-framework-capability-map`
148. **M01.L05** — **Agent design blueprint**  
   _Draw:_ A central Math Agent connected to Purpose, Tools, Context, Core Instructions, and Execution Examples  
   _Learner should notice:_ agent design combines capability, knowledge, behavior, and demonstrations before coding begins  
   `key: agent-design-blueprint`
149. **M01.L06** — **Monolithic agent vs specialist team**  
   _Draw:_ Left: one huge agent connected to many unrelated tools; right: an orchestrator connected to Grammar, Math, and Summary specialists  
   _Learner should notice:_ why specialization can reduce complexity  
   `key: monolithic-agent-vs-specialist-team`
150. **M01.L07** — **Hard-wired agent vs MCP ecosystem**  
   _Draw:_ Left: one agent directly wired to many APIs/tools with tangled connections; right: Host connected through MCP Clients to independent Git, Filesystem, GitHub, Weather servers  
   _Learner should notice:_ how the standardized boundary removes direct coupling  
   `key: hard-wired-agent-vs-mcp-ecosystem`
151. **M01.L08** — **Overloaded live agent vs layered system**  
   _Draw:_ Left: one live agent connected directly to stock, weather, documents, customer lookup, compliance, and many rules; right: live host delegates to A2A specialists which use MCP tools  
   _Learner should notice:_ why the live layer should not become a domain monolith  
   `key: overloaded-live-agent-vs-layered-system`
152. **M01.L09** — **Technical state vs user-visible state**  
   _Draw:_ Left: backend event graph with listening, tool call, agent delegation, approval, reconnect; right: clean user UI with meaningful labels and controls  
   _Learner should notice:_ UX translates system state into understandable action  
   `key: technical-state-vs-user-visible-state`
153. **M01.L10** — **Evaluation complexity ladder**  
   _Draw:_ Deterministic software -> static LLM -> autonomous tool-using agent -> live multimodal agent, with increasing dimensions of evaluation  
   _Learner should notice:_ why each layer adds new failure modes  
   `key: evaluation-complexity-ladder`
154. **M01.L11** — **Agent sprawl before governance**  
   _Draw:_ Many teams creating separate Math, Grammar, SQL, HR, and Legal agents with inconsistent code structures and direct links  
   _Learner should notice:_ why successful adoption creates governance pressure  
   `key: agent-sprawl-before-governance`
155. **M01.L12** — **Passive chatbot vs acting agent**  
   _Draw:_ Left: chatbot only returns text; right: agent connected to payments, email, database, calendar, files  
   _Learner should notice:_ why tool access increases the consequence of failure  
   `key: passive-chatbot-vs-acting-agent`
156. **M01.L13** — **AgentOps automated factory**  
   _Draw:_ Developer commit enters CI/CD conveyor belt through validate, test, build, Dev, Staging, evaluate, register, approve, Production  
   _Learner should notice:_ deployment as an assembly line rather than one command  
   `key: agentops-automated-factory`

## COURSE-016_Machine_Learning_Systems_and_MLOps_Engineering — 17 images

157. **M01.L01** — **Components of a production ML system**  
   _Draw:_ A clean systems diagram showing business requirements, user or API interface, data stack, model development, deployment infrastructure, prediction serving, monitoring, and model/data updates as connected components  
   _Learner should notice:_ the ML algorithm is only one component inside a larger feedback-driven system  
   `key: components-of-a-production-ml-system`
158. **M02.L01** — **From business objective to ML metric**  
   _Draw:_ A layered diagram showing a business goal at the top, followed by a product goal, an ML objective, and finally model/system metrics  
   _Learner should notice:_ model metrics are proxies for a higher-level goal, not the final goal themselves  
   `key: from-business-objective-to-ml-metric`
159. **M03.L01** — **End-to-end data engineering pipeline for ML**  
   _Draw:_ A left-to-right diagram showing data sources feeding serialization formats, data models, storage/processing systems, inter-service dataflow, feature generation, and finally an ML model  
   _Learner should notice:_ the model is only one consumer at the end of a larger data pipeline  
   `key: end-to-end-data-engineering-pipeline-for-ml`
160. **M04.L01** — **Iterative training-data lifecycle**  
   _Draw:_ A cycle showing sampling, labeling, training, evaluation, discovering data issues, and updating the data before looping back  
   _Learner should notice:_ training-data creation continues as the model and environment evolve  
   `key: iterative-training-data-lifecycle`
161. **M05.L01** — **Learned versus engineered features**  
   _Draw:_ A two-part diagram showing raw text/image going directly into a deep model that learns representations, alongside contextual metadata such as user, thread, and behavioral information being explicitly engineered into features  
   _Learner should notice:_ representation learning reduces but does not eliminate feature engineering  
   `key: learned-versus-engineered-features`
162. **M06.L01** — **Model selection as a multidimensional trade-off**  
   _Draw:_ A radar or matrix-style comparison of two model candidates across predictive quality, training cost, inference latency, data requirement, deployability, and interpretability  
   _Learner should notice:_ the highest-accuracy model is not automatically the best production choice  
   `key: model-selection-as-a-multidimensional-trade-off`
163. **M07.L01** — **Demo deployment versus production deployment**  
   _Draw:_ A simple model-plus-API box on the left and a production system on the right containing load balancing, monitoring, alerts, model versions, feature pipelines, and multiple clients  
   _Learner should notice:_ exposing an endpoint is only one small part of production deployment  
   `key: demo-deployment-versus-production-deployment`
164. **M08.L01** — **Post-deployment ML lifecycle**  
   _Draw:_ A circular flow from deployment to monitoring, detection, diagnosis, correction/retraining, and redeployment  
   _Learner should notice:_ production ML is a continuing feedback process rather than a final release  
   `key: post-deployment-ml-lifecycle`
165. **M09.L01** — **Continual-learning production loop**  
   _Draw:_ A circular production pipeline showing fresh data and feedback feeding candidate training, evaluation, promotion, deployment, and monitoring  
   _Learner should notice:_ continual learning requires an end-to-end update system, not merely a training function  
   `key: continual-learning-production-loop`
166. **M10.L01** — **Infrastructure as the foundation of the ML lifecycle**  
   _Draw:_ A stack where model development, deployment, monitoring, and continual learning sit above shared infrastructure  
   _Learner should notice:_ earlier ML-system practices depend on enabling infrastructure beneath them  
   `key: infrastructure-as-the-foundation-of-the-ml-lifecycle`
167. **M10.L02** — **Humans around an ML system**  
   _Draw:_ An ML system connected to end users, business stakeholders, data scientists, platform engineers, subject-matter experts, and wider society  
   _Learner should notice:_ system quality depends on technical and human relationships  
   `key: humans-around-an-ml-system`
168. **M11.L01** — **Continuous delivery feedback loop**  
   _Draw:_ A circular process from code/model change to build, test, package, deploy, observe, and improve  
   _Learner should notice:_ feedback and improvement are built into the release process  
   `key: continuous-delivery-feedback-loop`
169. **M12.L01** — **Observability questions around a production ML system**  
   _Draw:_ A deployed ML service surrounded by logs, metrics, alerts, model-quality signals, and data-drift signals  
   _Learner should notice:_ observability exists to explain system state, not merely collect data  
   `key: observability-questions-around-a-production-ml-system`
170. **M13.L01** — **AWS MLOps abstraction ladder**  
   _Draw:_ A ladder from raw infrastructure/building blocks through containers and serverless to managed AI APIs and full ML platforms  
   _Learner should notice:_ higher levels remove more operational work while lower levels provide more control  
   `key: aws-mlops-abstraction-ladder`
171. **M14.L01** — **Azure ML interface map**  
   _Draw:_ Azure ML at the center connected to Studio, Designer, notebooks, AutoML, CLI, and Python SDK, all reaching shared models, data, compute, and deployment services  
   _Learner should notice:_ different interfaces operate on the same underlying lifecycle  
   `key: azure-ml-interface-map`
172. **M15.L01** — **GCP MLOps technology ecosystem**  
   _Draw:_ Google Cloud surrounded by Kubernetes, TensorFlow, Go, BigQuery, and Vertex AI, with arrows showing portability beyond one cloud  
   _Learner should notice:_ the source's emphasis on widely adopted technologies rather than only proprietary services  
   `key: gcp-mlops-technology-ecosystem`
173. **M16.L01** — **Shell script to Python growth path**  
   _Draw:_ A tiny one-purpose shell script on the left and a larger Python CLI with logging, tests, modules, and dependencies on the right  
   _Learner should notice:_ tool choice changes as complexity and maintainability needs grow  
   `key: shell-script-to-python-growth-path`


## Marked required in the course manifests

These come from source-book figure lists, so there is only a title and the lessons they belong to (no drawing brief). Redraw them as original diagrams.


### COURSE-010-AI-Service-Engineering-with-FastAPI — 1

- Loading and using models on every request (L010-015)

### COURSE-011_Cloud_Deployment_and_CI_CD_for_AI_Engineers — 5

- Cloud Run service metrics dashboard (L011-014)
- Adjusting load-balancer routing rules (L011-016)
- ECS security group (L011-022)
- ALB listener rules final result (L011-023)
- ECS/Fargate cluster (L011-025)

### COURSE-016_Machine_Learning_Systems_and_MLOps_Engineering — 25

- Components of an ML system (L016-001)
- Latency/throughput and batching (L016-004)
- Iterative ML system cycle (L016-008)
- Row-major vs column-major data (L016-011)
- Request-driven services (L016-016)
- Event broker communication (L016-016)
- Reservoir sampling (L016-019)
- Weak-supervision labeling functions (L016-022)
- Uncertainty-based active learning (L016-023)
- Time-based train/validation/test split (L016-032)
- Data parallelism vs model parallelism (L016-039)
- Model calibration curves (L016-043)
- Batch prediction architecture (L016-046)
- Online prediction with batch features (L016-046)
- Online prediction with batch and streaming features (L016-046)
- Separate training and inference pipelines (L016-048)
- Drift and time-window selection (L016-059)
- Cumulative metric hiding sudden degradation (L016-059)
- Monitoring artifacts across the ML pipeline (L016-060)
- Champion/challenger continual-learning process (L016-066, L016-071)
- Stateless vs stateful training (L016-067)
- Measuring value of fresher training data (L016-070)
- Infrastructure layers for ML (L016-076)
- ML workflow represented as a DAG (L016-080)
- Artifacts tracked by a model store (L016-083)
