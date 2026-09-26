CAPSTONE = {
    "title": "Production-Oriented Transformer NLP System",
    "choose_one": ["text classification", "multilingual NER", "summarization", "extractive QA"],
    "stages": [
        "dataset analysis and risk audit",
        "baseline",
        "tokenization and model selection",
        "fine-tuning or adaptation",
        "task-appropriate evaluation",
        "error analysis",
        "controlled improvement experiment",
        "efficiency benchmark",
        "packaging and reproducibility documentation",
    ],
    "acceptance_criteria": [
        "baseline and final system evaluated on the same held-out split",
        "no fabricated metrics",
        "at least one concrete failure category analyzed",
        "model/tokenizer/checkpoint compatibility verified",
        "quality and efficiency trade-offs documented",
        "reproducible inference artifact or script produced",
    ],
}
