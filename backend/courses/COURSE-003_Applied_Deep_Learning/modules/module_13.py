"""M13.L01 — Improving Training with Metrics and Augmentation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 14.
Instructor-authored curriculum adaptation.

Quality standard:
- balanced quiz-answer positions
- explicit training/validation best practices
- realistic study-time estimate
- learning checkpoints after dense sections
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M13.L01"
MODULE_ORDER = 13
MODULE_TITLE = "Metrics, Class Balancing & Data Augmentation"
MODULE_DESCRIPTION = (
    "Turn a misleadingly high-accuracy CT classifier into a genuinely useful model by "
    "measuring true/false positives and negatives, computing precision, recall, and F1, "
    "balancing the training data without distorting validation, recognizing overfitting, "
    "and applying domain-aware 3D data augmentation."
)

SOURCE_CHAPTER = 14
SOURCE_PAGES = "Chapter 14 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Improving Training with Metrics and Augmentation",
    "slug": "applied-deep-learning-m13-l01",
    "description": (
        "A practical lesson on evaluating and improving an imbalanced 3D CT classifier using "
        "confusion-matrix concepts, precision, recall, F1, balanced training, overfitting "
        "diagnosis, domain-aware augmentation, and TensorBoard experiment comparison."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.5,
    "skill_tags": [
        "classification-metrics",
        "true-positive",
        "true-negative",
        "false-positive",
        "false-negative",
        "precision",
        "recall",
        "f1-score",
        "class-imbalance",
        "balanced-sampling",
        "overfitting",
        "data-augmentation",
        "affine-grid",
        "grid-sample",
        "3d-augmentation",
        "tensorboard",
        "medical-imaging",
    ],
    "prerequisite_ids": ["M12.L01"],

    "lesson": {
        "title": "Improving Training with Metrics and Augmentation",
        "content": (
            "# Improving Training with Metrics and Augmentation\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M13.L01  \n"
            "> **Source:** *Deep Learning with PyTorch, Second Edition*, Chapter 14.  \n"
            "> **Study expectation:** about **6.5 hours** including metric calculations, code tracing, checkpoints, and exercises.\n\n"
            "Chapter 13 gave us a classifier that *looked* excellent by overall accuracy but was nearly useless in practice: "
            "it learned to call almost everything a non-nodule.\n\n"
            "Chapter 14 fixes that failure in the correct order:\n\n"
            "```text\n"
            "measure the right behavior\n"
            "      ↓\n"
            "understand why the model collapses\n"
            "      ↓\n"
            "balance the training data\n"
            "      ↓\n"
            "detect overfitting\n"
            "      ↓\n"
            "augment limited data\n"
            "      ↓\n"
            "compare experiments with better metrics\n"
            "```\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Define true positives, true negatives, false positives, and false negatives.\n"
            "- Explain why one classification threshold creates precision/recall tradeoffs.\n"
            "- Compute recall from TP and FN.\n"
            "- Compute precision from TP and FP.\n"
            "- Explain why precision or recall alone can be gamed by moving the decision threshold.\n"
            "- Compute and interpret the F1 score as the harmonic mean of precision and recall.\n"
            "- Recognize undefined precision/F1 cases when denominators become zero.\n"
            "- Explain why overall accuracy hid the Chapter 13 failure.\n"
            "- Explain how extreme class imbalance can push a model toward a majority-only solution.\n"
            "- Balance training samples while leaving validation in its natural distribution.\n"
            "- Implement the chapter's ratio-based positive/negative sampling strategy.\n"
            "- Explain why repeated positive examples can still overfit.\n"
            "- Diagnose overfitting by comparing training and validation behavior by class.\n"
            "- Explain how augmentation increases the effective training set without changing class identity.\n"
            "- Apply 3D mirroring, shifts, scaling, rotation, and noise augmentation.\n"
            "- Explain why medical-image augmentation must respect domain geometry.\n"
            "- Explain why caching should happen before random augmentation.\n"
            "- Compare augmentation experiments using TensorBoard and the metrics that matter to the task.\n\n"
            "---\n\n"

            "## 1. From a working pipeline to a useful classifier\n\n"
            "The previous lesson proved that the mechanics worked:\n\n"
            "- data loaded,\n"
            "- the network trained,\n"
            "- validation ran,\n"
            "- metrics were logged.\n\n"
            "But the model's behavior was poor because it exploited the class distribution instead of learning the discrimination we wanted.\n\n"
            "This chapter therefore changes the question from:\n\n"
            "> **Does the training system run?**\n\n"
            "to:\n\n"
            "> **Does the model perform the task in a useful way?**\n\n"
            "That shift is fundamental in applied machine learning.\n\n"
            "---\n\n"

            "## 2. Every binary prediction belongs to one of four outcomes\n\n"
            "For binary classification, ground truth can be positive or negative, and the model prediction can also be positive or negative.\n\n"
            "That produces four cases:\n\n"
            "| Ground truth | Prediction | Name |\n"
            "|---|---|---|\n"
            "| Positive | Positive | True positive (TP) |\n"
            "| Negative | Negative | True negative (TN) |\n"
            "| Negative | Positive | False positive (FP) |\n"
            "| Positive | Negative | False negative (FN) |\n\n"
            '{{image:binary-classification-quadrants}}'
            '\n\n'
            "For the CT project:\n\n"
            "- **TP:** a real nodule correctly flagged as a nodule.\n"
            "- **TN:** a non-nodule correctly rejected.\n"
            "- **FP:** a non-nodule incorrectly flagged as a nodule.\n"
            "- **FN:** a real nodule incorrectly dismissed.\n\n"
            "---\n\n"

            "## 3. The guard-dog metaphor: two different ways to fail\n\n"
            "The chapter uses two guard dogs to make the tradeoff intuitive.\n\n"
            "### Chirpy\n\n"
            "Chirpy barks at nearly everything.\n\n"
            "That means:\n\n"
            "- few burglars are missed,\n"
            "- many harmless events are flagged.\n\n"
            "This is **high recall, poor precision**.\n\n"
            "### Dozer\n\n"
            "Dozer barks only when very sure.\n\n"
            "That means:\n\n"
            "- most alerts are genuinely serious,\n"
            "- many real burglars pass unnoticed.\n\n"
            "This is **high precision, poor recall**.\n\n"
            "The chapter's Chapter 13 classifier behaves more like Dozer: it avoids positive predictions so strongly that it misses the positive class.\n\n"
            "---\n\n"

            "## 4. A classification threshold creates the tradeoff\n\n"
            "The model produces a continuous positive-class score or probability.\n\n"
            "A threshold converts that continuous output into a discrete decision:\n\n"
            "```text\n"
            "score > threshold  -> predict positive\n"
            "score <= threshold -> predict negative\n"
            "```\n\n"
            "Moving the threshold left makes it easier to call something positive:\n\n"
            "- fewer false negatives,\n"
            "- more false positives.\n\n"
            "Moving it right makes positive predictions stricter:\n\n"
            "- fewer false positives,\n"
            "- more false negatives.\n\n"
            "[[IMAGE_NEEDED: Threshold tradeoff between positives and negatives | Overlapping distributions of negative and positive "
            "model scores with a movable vertical threshold; arrows show that moving left raises recall while moving right raises precision | "
            "Learner should notice that threshold changes trade one error type for another]]\n\n"
            "The threshold cannot fix every problem because the positive and negative score distributions can overlap substantially.\n\n"
            "---\n\n"

            "## 5. Recall: how many real positives did we find?\n\n"
            "Recall asks:\n\n"
            "> **Of all truly positive samples, how many did the model detect?**\n\n"
            "Formula:\n\n"
            "```text\n"
            "recall = TP / (TP + FN)\n"
            "```\n\n"
            "To increase recall, reduce false negatives.\n\n"
            "A model can obtain excellent recall by labeling almost everything positive—but that can create many false positives.\n\n"
            "The chapter notes that recall is also called **sensitivity** in some contexts.\n\n"
            "---\n\n"

            "## 6. Precision: how trustworthy are our positive predictions?\n\n"
            "Precision asks:\n\n"
            "> **Of everything the model predicted positive, how many were truly positive?**\n\n"
            "Formula:\n\n"
            "```text\n"
            "precision = TP / (TP + FP)\n"
            "```\n\n"
            "To increase precision, reduce false positives.\n\n"
            "A model can obtain very high precision by predicting positive only in the most obvious cases—but that may miss many real positives.\n\n"
            "[[IMAGE_NEEDED: Precision versus recall denominators | Two small diagrams highlight TP/(TP+FN) for recall and TP/(TP+FP) "
            "for precision using the same TP/FP/FN/TN grid | Learner should notice that both metrics use TP but answer different questions]]\n\n"
            "---\n\n"

            "## 7. Compute TP, TN, FP, and FN from the existing masks\n\n"
            "The previous chapter already computed correct positive and negative predictions.\n\n"
            "The source reframes those counts:\n\n"
            "```python\n"
            "trueNeg_count = neg_correct\n"
            "truePos_count = pos_correct\n\n"
            "falseNeg_count = pos_count - pos_correct\n"
            "falsePos_count = neg_count - neg_correct\n"
            "```\n\n"
            "Once those four counts exist, precision and recall follow directly:\n\n"
            "```python\n"
            "recall = truePos_count / (truePos_count + falseNeg_count)\n"
            "precision = truePos_count / (truePos_count + falsePos_count)\n"
            "```\n\n"
            "This is a powerful pattern: many classification metrics are just different summaries of the same four basic counts.\n\n"

            "### Learning checkpoint 1 — Four outcomes and two ratios\n\n"
            "Given:\n\n"
            "```text\n"
            "TP = 80\n"
            "FN = 20\n"
            "FP = 40\n"
            "TN = 860\n"
            "```\n\n"
            "You should be able to calculate:\n\n"
            "- recall,\n"
            "- precision,\n"
            "- total accuracy,\n"
            "- which error type each metric is sensitive to.\n\n"
            "{{exercise:M13.L01.EX01}}\n\n"
            "---\n\n"

            "## 8. F1: combine precision and recall into one score\n\n"
            "Neither precision nor recall alone captures the full goal.\n\n"
            "The chapter therefore introduces the F1 score:\n\n"
            "```text\n"
            "F1 = 2 × (precision × recall) / (precision + recall)\n"
            "```\n\n"
            "F1 ranges from 0 to 1.\n\n"
            "It is the **harmonic mean** of precision and recall.\n\n"
            "The harmonic mean strongly penalizes a model when one of the two values is much lower than the other.\n\n"
            "[[IMAGE_NEEDED: F1 surface over precision and recall | A conceptual contour/surface plot where the best values occur when both "
            "precision and recall are high and balanced, while regions with one value near zero remain poor | Learner should see why F1 "
            "discourages extreme one-sided behavior]]\n\n"
            "---\n\n"

            "## 9. Why not just average precision and recall?\n\n"
            "Suppose:\n\n"
            "```text\n"
            "precision = 1.0\n"
            "recall    = 0.0\n"
            "```\n\n"
            "The arithmetic mean is `0.5`.\n\n"
            "But a classifier with zero recall is normally not useful for the chapter's purpose.\n\n"
            "Meanwhile:\n\n"
            "```text\n"
            "precision = 0.5\n"
            "recall    = 0.5\n"
            "```\n\n"
            "also averages to `0.5`, despite being a much more balanced classifier.\n\n"
            "The chapter also considers taking the minimum or multiplying precision and recall, then explains why those alternatives lose useful nuance.\n\n"
            "F1 is chosen because it responds meaningfully to tradeoffs between the two rates.\n\n"
            "---\n\n"

            "## 10. Undefined metrics are information, not just annoying warnings\n\n"
            "When the model predicts no positives at all:\n\n"
            "```text\n"
            "TP = 0\n"
            "FP = 0\n"
            "```\n\n"
            "then precision tries to divide by zero:\n\n"
            "```text\n"
            "0 / (0 + 0)\n"
            "```\n\n"
            "The source's early runs therefore produce `nan` for precision and F1.\n\n"
            "That warning is itself diagnostic: the model is in a degenerate state where it refuses to predict the positive class.\n\n"
            "For a production implementation, handle zero denominators explicitly so dashboards remain stable while preserving the meaning of the failure state.\n\n"
            "---\n\n"

            "## 11. Log the metrics that expose the real behavior\n\n"
            "The chapter extends epoch logs to include:\n\n"
            "- overall loss,\n"
            "- overall percent correct,\n"
            "- precision,\n"
            "- recall,\n"
            "- F1,\n"
            "- positive-class loss and accuracy,\n"
            "- negative-class loss and accuracy.\n\n"
            "This turns a misleading line such as:\n\n"
            "```text\n"
            "99.8% correct\n"
            "```\n\n"
            "into a much more truthful diagnosis when recall is zero.\n\n"
            "---\n\n"

            "## 12. Why the original training distribution collapses\n\n"
            "The source describes the candidate dataset as roughly **400 negatives for every positive**.\n\n"
            "At random initialization, roughly half of examples from each class will begin on the wrong side of the decision boundary.\n\n"
            "But there are so many more negatives that the total gradient pressure from incorrectly predicted negatives overwhelms the gradient pressure from positive samples.\n\n"
            "The chapter gives the practical intuition that many all-negative batches can pass before the model even sees a positive sample.\n\n"
            "[[IMAGE_NEEDED: Gradient tug-of-war under 400-to-1 imbalance | A huge group of negative examples pulls model weights strongly "
            "toward negative predictions while a tiny positive group pulls in the opposite direction | Learner should see why random initialization "
            "plus extreme imbalance can rapidly collapse to a majority-only solution]]\n\n"
            "The issue is not that the model lacks capacity. The training signal is badly shaped for early learning.\n\n"
            "---\n\n"

            "## 13. Balance the training stream—not the validation set\n\n"
            "The chapter's goal is to present training batches with comparable positive and negative influence.\n\n"
            "For a one-to-one balance:\n\n"
            "```text\n"
            "+ - + - + - + - ...\n"
            "```\n\n"
            "Because positive examples are scarce, the dataset must reuse them repeatedly during training.\n\n"
            "But validation is deliberately **not balanced**.\n\n"
            "Why?\n\n"
            "Because validation should reflect the naturally imbalanced environment in which the classifier is expected to operate.\n\n"
            "> **Training distribution can be shaped to make learning easier; validation distribution should remain representative of real use.**\n\n"
            "---\n\n"

            "## 14. Why not rely only on a DataLoader sampler?\n\n"
            "PyTorch supports `sampler=...` in `DataLoader`, including tools such as weighted random sampling.\n\n"
            "The source explains a practical limitation: the standard `Dataset` interface exposes only indexed access and length. It does not guarantee a public method that says which indexes belong to which classes.\n\n"
            "If you control the dataset implementation, reshaping the data directly inside the dataset can be clearer than breaking encapsulation to build sampler weights.\n\n"
            "The source therefore chooses dataset-level balancing for this project.\n\n"
            "---\n\n"

            "## 15. Implement ratio-based balancing in `LunaDataset`\n\n"
            "The dataset keeps separate lists:\n\n"
            "```python\n"
            "self.negative_list = [\n"
            "    info for info in self.candidateInfo_list\n"
            "    if not info.isNodule_bool\n"
            "]\n\n"
            "self.pos_list = [\n"
            "    info for info in self.candidateInfo_list\n"
            "    if info.isNodule_bool\n"
            "]\n"
            "```\n\n"
            "`ratio_int` controls how many negative samples are returned for each positive sample.\n\n"
            "For `ratio_int = 2`, the intended pattern is:\n\n"
            "```text\n"
            "dataset index: 0 1 2 3 4 5 6 7 8 ...\n"
            "label:         + - - + - - + - - ...\n"
            "```\n\n"
            "Modulo arithmetic wraps around when the positive list is exhausted so positives can be reused.\n\n"
            "The source also shuffles the positive and negative lists at the start of each epoch.\n\n"
            "{{exercise:M13.L01.EX02}}\n\n"
            "---\n\n"

            "## 16. Epoch size becomes a design choice under resampling\n\n"
            "Once positive samples are intentionally repeated, an epoch no longer has to mean 'visit each unique underlying example exactly once.'\n\n"
            "The source fixes balanced-training dataset length to:\n\n"
            "```text\n"
            "200,000 samples\n"
            "```\n\n"
            "This provides faster feedback than processing the full roughly half-million-example native candidate list every epoch.\n\n"
            "The broader lesson is that **epoch size is an experiment-control choice** when sampling or resampling changes the effective dataset.\n\n"
            "---\n\n"

            "## 17. Balancing immediately changes the learning behavior\n\n"
            "With balanced training, the source reports a dramatic improvement after one epoch:\n\n"
            "```text\n"
            "training precision ≈ 0.94\n"
            "training recall    ≈ 0.92\n"
            "training F1        ≈ 0.93\n"
            "```\n\n"
            "On naturally imbalanced validation data, recall jumps from essentially zero to roughly `0.79` in the shown run.\n\n"
            "That is a major improvement.\n\n"
            "But validation precision remains low because even a small false-positive rate among tens of thousands of negatives creates many false alarms.\n\n"
            "---\n\n"

            "## 18. Tiny negative error rates can still create many false positives\n\n"
            "The chapter gives a concrete example:\n\n"
            "```text\n"
            "negative validation samples ≈ 54,971\n"
            "positive validation samples ≈    136\n"
            "```\n\n"
            "If only 1% of negatives are incorrectly flagged:\n\n"
            "```text\n"
            "54,971 × 0.01 ≈ 550 false positives\n"
            "```\n\n"
            "That is roughly four false positives for every real positive in the entire validation set.\n\n"
            "[[IMAGE_NEEDED: Small false-positive rate on a huge negative class | A large block of 54,971 negative samples with only 1 percent "
            "highlighted as false positives, placed beside 136 true positive cases; the false-positive group is still several times larger | "
            "Learner should notice why precision can remain poor despite 99 percent negative accuracy]]\n\n"
            "This is why imbalanced problems require more careful metrics than overall accuracy.\n\n"

            "### Learning checkpoint 2 — Balance versus reality\n\n"
            "Explain both statements:\n\n"
            "1. **Balanced training is useful.**\n"
            "2. **Balanced validation would be misleading for this project.**\n\n"
            "If you cannot explain why both can be true at the same time, revisit sections 12–18.\n\n"
            "---\n\n"

            "## 19. More training reveals overfitting\n\n"
            "As balanced training continues, training metrics become nearly perfect.\n\n"
            "But validation positive-class performance begins to deteriorate.\n\n"
            "The source highlights a pattern such as:\n\n"
            "```text\n"
            "positive training loss   -> near zero\n"
            "positive validation loss -> rising\n"
            "```\n\n"
            "This divergence is a classic overfitting signal.\n\n"
            "[[IMAGE_NEEDED: Training versus validation positive loss divergence | Two curves over epochs: training positive loss falls toward zero "
            "while validation positive loss turns upward | Learner should identify the point where more training begins to harm generalization]]\n\n"
            "Overall validation loss can hide this because the naturally imbalanced validation set is dominated by negative samples.\n\n"
            "Again, **the right subgroup metric matters**.\n\n"
            "---\n\n"

            "## 20. Overfitting means memorizing specifics instead of learning general properties\n\n"
            "The chapter revisits overfitting with a face-to-age analogy.\n\n"
            "A well-generalizing model learns age-related patterns that transfer to unseen people.\n\n"
            "An overfit model instead learns identifying quirks of the training people and effectively remembers their answers.\n\n"
            "For the CT classifier, only a small number of positive training nodules exist. Repeating them balances the training signal, but repetition does **not** create new biological variation.\n\n"
            "A model with enough capacity can eventually memorize those positive samples.\n\n"
            "---\n\n"

            "## 21. Data augmentation attacks memorization by creating meaningful variation\n\n"
            "Data augmentation synthetically transforms an existing example while trying to preserve its class identity.\n\n"
            "A useful augmentation should be:\n\n"
            "- different enough that it is not trivial to memorize as the same sample,\n"
            "- similar enough that it still represents the same class.\n\n"
            "The effective training set becomes much larger even though the number of original CT scans has not changed.\n\n"
            "[[IMAGE_NEEDED: One nodule producing many augmented views | One original 3D candidate crop branches into mirrored, shifted, "
            "scaled, rotated, and noisy variants, all keeping the same positive label | Learner should notice that augmentation changes "
            "appearance while preserving the task-relevant identity]]\n\n"
            "---\n\n"

            "## 22. Augmentation must respect the domain\n\n"
            "Not every mathematically possible transform is a valid training example.\n\n"
            "The chapter emphasizes using domain knowledge.\n\n"
            "For example, CT voxel spacing is not identical in every axis, so arbitrary 3D rotations that swap the slice-depth axis with in-plane axes would not preserve the same data characteristics.\n\n"
            "The source therefore confines rotation to the in-plane `X-Y` orientation.\n\n"
            "The broader rule is:\n\n"
            "> **Augment invariances the real task should tolerate; do not manufacture physically implausible examples.**\n\n"
            "---\n\n"

            "## 23. Use an affine transform plus `grid_sample`\n\n"
            "The source builds a transformation matrix and resamples the 3D candidate with PyTorch:\n\n"
            "```python\n"
            "affine_t = F.affine_grid(\n"
            "    transform_t[:3].unsqueeze(0).to(torch.float32),\n"
            "    ct_t.size(),\n"
            "    align_corners=False,\n"
            ")\n\n"
            "augmented_chunk = F.grid_sample(\n"
            "    ct_t,\n"
            "    affine_t,\n"
            "    padding_mode='border',\n"
            "    align_corners=False,\n"
            ")\n"
            "```\n\n"
            "`affine_grid` defines where output locations sample from, while `grid_sample` performs the resampling.\n\n"
            "This one mechanism can implement several geometric augmentations by changing the transformation matrix.\n\n"
            "---\n\n"

            "## 24. Cache before random augmentation\n\n"
            "This ordering is critical:\n\n"
            "```text\n"
            "raw CT\n"
            " -> deterministic candidate crop\n"
            " -> CACHE\n"
            " -> random augmentation\n"
            " -> training sample\n"
            "```\n\n"
            "If the augmented output itself were cached, a supposedly random training sample could become frozen and reused identically.\n\n"
            "That would defeat much of the purpose of augmentation.\n\n"
            "This is a broader data-pipeline lesson: **cache deterministic expensive work, not randomness that should change between samples.**\n\n"
            "---\n\n"

            "## 25. Augmentation 1: mirroring\n\n"
            "Mirroring changes orientation without changing voxel values.\n\n"
            "The source randomly flips axes by multiplying diagonal transform entries by `-1`:\n\n"
            "```python\n"
            "for i in range(3):\n"
            "    if random.random() > 0.5:\n"
            "        transform_t[i, i] *= -1\n"
            "```\n\n"
            "Randomness matters. Always returning a flipped sample would create one fixed alternate version rather than an open-ended stream of variation.\n\n"
            "---\n\n"

            "## 26. Augmentation 2: random shifts\n\n"
            "Shifting the candidate helps robustness to imperfect centering.\n\n"
            "The source modifies the translation component of the affine transform:\n\n"
            "```python\n"
            "random_float = random.random() * 2 - 1\n"
            "transform_t[i, 3] = offset_float * random_float\n"
            "```\n\n"
            "Sub-voxel shifts require interpolation, which can introduce small blur effects.\n\n"
            "The chapter uses border padding during sampling, so extreme transforms can also create repeated edge values.\n\n"
            "---\n\n"

            "## 27. Augmentation 3: random scaling\n\n"
            "Scaling changes how large the candidate appears within the crop.\n\n"
            "Conceptually:\n\n"
            "```python\n"
            "transform_t[i, i] *= 1.0 + scale_float * random_float\n"
            "```\n\n"
            "The scale range must remain modest enough that the transformed sample is still representative of the original class.\n\n"
            "---\n\n"

            "## 28. Augmentation 4: in-plane rotation\n\n"
            "Because CT depth spacing differs from in-plane spacing, the chapter rotates only around the head-foot axis, effectively rotating within the `X-Y` plane.\n\n"
            "The rotation matrix is built from sine and cosine:\n\n"
            "```python\n"
            "angle = random.random() * math.pi * 2\n"
            "s = math.sin(angle)\n"
            "c = math.cos(angle)\n\n"
            "rotation_t = torch.tensor([\n"
            "    [ c, -s, 0, 0],\n"
            "    [ s,  c, 0, 0],\n"
            "    [ 0,  0, 1, 0],\n"
            "    [ 0,  0, 0, 1],\n"
            "])\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Valid CT rotation plane | A 3D CT candidate crop with the in-plane X-Y axes highlighted and a rotation arrow "
            "around the head-foot axis, while the anisotropic slice-depth axis is marked as special | Learner should see why rotation is "
            "restricted instead of freely rotating across all 3D axes]]\n\n"
            "---\n\n"

            "## 29. Augmentation 5: Gaussian noise\n\n"
            "Noise augmentation is different from geometric transforms because it directly corrupts voxel values.\n\n"
            "The source uses:\n\n"
            "```python\n"
            "noise_t = torch.randn_like(augmented_chunk)\n"
            "noise_t *= augmentation_dict['noise']\n"
            "augmented_chunk += noise_t\n"
            "```\n\n"
            "Too much noise can overwhelm the real signal and make classification harder for the wrong reason.\n\n"
            "The chapter later observes that the noise-only experiment performs worse at finding nodules than the unaugmented model in the shown runs.\n\n"
            "---\n\n"

            "## 30. Always inspect transformed samples\n\n"
            "Before trusting an augmentation pipeline, visualize examples from each transform and combined transforms.\n\n"
            "You should look for:\n\n"
            "- class-preserving geometry,\n"
            "- candidates remaining inside the crop,\n"
            "- unrealistic borders,\n"
            "- excessive blur,\n"
            "- noise that destroys the nodule signal,\n"
            "- unexpected orientation artifacts.\n\n"
            "The source emphasizes that each `__getitem__` call generates new randomness, so combined augmented samples can differ every time.\n\n"
            "{{exercise:M13.L01.EX03}}\n\n"
            "---\n\n"

            "## 31. Compare augmentation strategies experimentally\n\n"
            "The chapter exposes each augmentation through command-line options and trains separate runs for:\n\n"
            "- balanced baseline,\n"
            "- flip,\n"
            "- shift,\n"
            "- scale,\n"
            "- rotation,\n"
            "- noise,\n"
            "- all augmentations combined.\n\n"
            "TensorBoard then makes it possible to compare:\n\n"
            "- overall correctness,\n"
            "- loss,\n"
            "- F1,\n"
            "- precision,\n"
            "- recall,\n"
            "- especially positive-class behavior.\n\n"
            "This is a strong experimental pattern: **change one training condition, label the run, and compare the metrics that correspond to the real goal.**\n\n"
            "---\n\n"

            "## 32. What the chapter's augmentation experiments show\n\n"
            "The source reports several important observations from the example runs:\n\n"
            "### Combined augmentation\n\n"
            "The fully augmented model finds substantially more positive candidates and resists overfitting better than the unaugmented run.\n\n"
            "### Noise alone\n\n"
            "Noise augmentation performs worse than the unaugmented model for positive identification in the shown experiment.\n\n"
            "### Rotation\n\n"
            "Rotation performs nearly as well as full augmentation on recall and has better precision in the displayed runs, which can lead to a better F1.\n\n"
            "### Chosen direction\n\n"
            "The source keeps the fully augmented model for later work because the use case prioritizes high recall, while F1 remains useful for deciding which epoch is best.\n\n"
            "[[IMAGE_NEEDED: TensorBoard comparison of augmentation runs | Multiple validation curves for balanced baseline, rotation, noise, "
            "and fully augmented models across recall, precision, F1, and positive loss | Learner should notice that different augmentations "
            "affect precision and recall differently and that full augmentation reduces overfitting]]\n\n"
            "The important lesson is not that one transform is universally best. It is that augmentation choices are **task- and data-dependent hypotheses that must be measured**.\n\n"
            "{{exercise:M13.L01.EX04}}\n\n"
            "---\n\n"

            "## 33. Use metrics to choose what to fix next\n\n"
            "This chapter demonstrates a disciplined improvement loop:\n\n"
            "```text\n"
            "observe failure\n"
            " -> define metrics that expose it\n"
            " -> identify the training-data mechanism causing it\n"
            " -> change the data presentation\n"
            " -> observe overfitting\n"
            " -> add realistic variation\n"
            " -> compare experiments\n"
            "```\n\n"
            "At each step, the model is changed only after the existing metrics reveal a reason to change it.\n\n"
            "This is far more effective than randomly adding layers or swapping optimizers without a diagnosis.\n\n"
            "---\n\n"

            "## 34. The complete evaluation-and-improvement blueprint\n\n"
            "```text\n"
            "MODEL OUTPUTS\n"
            "    ↓\n"
            "threshold into positive/negative predictions\n"
            "    ↓\n"
            "TP / TN / FP / FN\n"
            "    ↓\n"
            "precision / recall / F1\n"
            "    ↓\n"
            "diagnose majority-class collapse\n"
            "    ↓\n"
            "balance TRAINING stream\n"
            "keep VALIDATION natural\n"
            "    ↓\n"
            "monitor class-specific train/validation curves\n"
            "    ↓\n"
            "detect overfitting\n"
            "    ↓\n"
            "apply domain-valid random augmentation\n"
            "    ↓\n"
            "compare TensorBoard runs\n"
            "    ↓\n"
            "select improvements based on the task's real priorities\n"
            "```\n\n"
            "### Learning checkpoint 3 — Diagnose before modifying\n\n"
            "Given a model with:\n\n"
            "```text\n"
            "accuracy  = 99.3%\n"
            "precision = 0.21\n"
            "recall    = 0.82\n"
            "```\n\n"
            "you should not summarize it as simply '99.3% accurate.'\n\n"
            "Explain what those numbers imply about false positives and false negatives in an imbalanced dataset, and what additional class-specific plots you would inspect before changing training.\n\n"
            "{{exercise:M13.L01.EX05}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Accuracy is enough if the validation set is large\n\n"
            "A large validation set can still be extremely imbalanced. Majority-class performance can dominate the aggregate number.\n\n"
            "### Misconception 2: High recall means the classifier is good\n\n"
            "A model can obtain perfect recall by predicting everything positive, at the cost of terrible precision.\n\n"
            "### Misconception 3: High precision means the classifier is good\n\n"
            "A model can obtain very high precision by predicting positive only in a tiny set of obvious cases, while missing most positives.\n\n"
            "### Misconception 4: F1 is just ordinary averaging\n\n"
            "F1 is the harmonic mean of precision and recall, chosen specifically to penalize one-sided performance more strongly.\n\n"
            "### Misconception 5: Training and validation should always have identical class balance\n\n"
            "The source intentionally balances training to improve learning while preserving the naturally imbalanced validation distribution.\n\n"
            "### Misconception 6: Repeating rare positive examples solves class imbalance completely\n\n"
            "Repeated positives fix the early gradient imbalance, but the small set can then be memorized, leading to overfitting.\n\n"
            "### Misconception 7: Any random image transformation is useful augmentation\n\n"
            "An augmentation must remain representative of the class and respect domain-specific geometry.\n\n"
            "### Misconception 8: Augmented samples should be cached to save time\n\n"
            "Caching random augmentation can freeze the randomness. The deterministic crop should be cached before augmentation.\n\n"
            "### Misconception 9: More corruption always produces stronger regularization\n\n"
            "The chapter's noise-only run can perform worse because augmentation can make the task too difficult or destroy useful signal.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| True positive (TP) | Positive sample correctly predicted positive. |\n"
            "| True negative (TN) | Negative sample correctly predicted negative. |\n"
            "| False positive (FP) | Negative sample incorrectly predicted positive. |\n"
            "| False negative (FN) | Positive sample incorrectly predicted negative. |\n"
            "| Classification threshold | Score cutoff used to convert a continuous output into a binary decision. |\n"
            "| Recall | `TP / (TP + FN)`; fraction of real positives successfully found. |\n"
            "| Sensitivity | Alternate name for recall in some contexts. |\n"
            "| Precision | `TP / (TP + FP)`; fraction of predicted positives that are truly positive. |\n"
            "| F1 score | Harmonic mean of precision and recall. |\n"
            "| Class imbalance | Strong inequality in the number of examples from different classes. |\n"
            "| Balanced training | Reshaping the training stream so classes contribute more comparably to learning. |\n"
            "| Oversampling | Reusing examples from a minority class more often during training. |\n"
            "| Sampler | DataLoader component controlling which dataset indexes are drawn and in what order. |\n"
            "| Overfitting | Learning training-specific details that do not generalize to unseen data. |\n"
            "| Data augmentation | Creating randomized class-preserving transformations of training samples. |\n"
            "| Affine transform | Linear/translation transformation used for spatial resampling. |\n"
            "| `affine_grid` | PyTorch function constructing a sampling grid from an affine transform. |\n"
            "| `grid_sample` | PyTorch function resampling a tensor using a provided grid. |\n"
            "| Mirroring | Flipping a sample across one or more axes. |\n"
            "| Translation / shift | Moving sample content within the crop. |\n"
            "| Scaling | Enlarging or shrinking the sampled content. |\n"
            "| Rotation | Rotating the sample around a chosen physically valid axis. |\n"
            "| Noise augmentation | Adding random noise directly to voxel values. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. Define TP, TN, FP, and FN for the nodule-classification task.\n"
            "2. Which error does high recall try to minimize?\n"
            "3. Which error does high precision try to minimize?\n"
            "4. Write the recall formula from memory.\n"
            "5. Write the precision formula from memory.\n"
            "6. How does moving the classification threshold left usually affect recall and precision?\n"
            "7. How does moving it right usually affect them?\n"
            "8. Why can neither precision nor recall alone be the final quality metric?\n"
            "9. Write the F1 formula.\n"
            "10. Why is arithmetic averaging of precision and recall weaker for this purpose?\n"
            "11. What does a `nan` precision value mean when no samples were predicted positive?\n"
            "12. Why did Chapter 13's 99.7% accuracy hide catastrophic model behavior?\n"
            "13. Approximately how imbalanced is the source candidate dataset?\n"
            "14. Why can many training batches contain no positive samples under the natural distribution?\n"
            "15. Why does this pull the early model toward predicting negative?\n"
            "16. Why does balancing the training stream help?\n"
            "17. Why is validation deliberately left imbalanced?\n"
            "18. What does `ratio_int=2` mean in the source's sampling pattern?\n"
            "19. Why are positive indexes wrapped with modulo arithmetic?\n"
            "20. Why does the source shorten balanced epochs to 200,000 samples?\n"
            "21. Why can 1% negative error still create hundreds of false positives?\n"
            "22. What train/validation pattern indicates overfitting?\n"
            "23. Why does repeating the same 1,215 positive samples eventually encourage memorization?\n"
            "24. What is the purpose of data augmentation in this context?\n"
            "25. What two properties should a useful augmentation preserve/break?\n"
            "26. Why must augmentation choices use domain knowledge?\n"
            "27. What do `affine_grid` and `grid_sample` do at a high level?\n"
            "28. Why should caching occur before augmentation?\n"
            "29. How does mirroring alter a sample?\n"
            "30. What is a practical benefit of shifting candidates?\n"
            "31. Why are rotations restricted to the X-Y plane in the source implementation?\n"
            "32. Why can too much noise be harmful?\n"
            "33. Why should augmented candidates be visualized before long training runs?\n"
            "34. What does the chapter observe about the fully augmented model's recall?\n"
            "35. What does it observe about noise-only augmentation?\n"
            "36. Why can a rotation-only run have a stronger F1 than a higher-recall run?\n"
            "37. Why does the source keep the fully augmented model despite another run having better F1 in the displayed results?\n"
            "38. What is the chapter's overall model-improvement workflow?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**A model can only be improved intelligently when its metrics expose the failure that matters. For imbalanced classification, "
            "accuracy can hide a useless majority-only strategy. Precision, recall, F1, and class-specific losses reveal the real behavior; "
            "balanced training fixes the early learning signal; and domain-valid augmentation prevents a small minority class from simply being memorized.**\n"
        ),

        "estimated_minutes": 390,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "from-working-to-good", "title": "From working to useful", "order": 1},
            {"id": "four-outcomes", "title": "TP, TN, FP, and FN", "order": 2},
            {"id": "guard-dog-metaphor", "title": "Two ways to fail", "order": 3},
            {"id": "threshold-space", "title": "Classification thresholds", "order": 4},
            {"id": "recall", "title": "Recall", "order": 5},
            {"id": "precision", "title": "Precision", "order": 6},
            {"id": "metric-counts", "title": "Computing classification counts", "order": 7},
            {"id": "f1", "title": "F1 score", "order": 8},
            {"id": "why-not-average", "title": "Why not arithmetic averaging", "order": 9},
            {"id": "undefined-metrics", "title": "Undefined metric cases", "order": 10},
            {"id": "better-logging", "title": "Improved metric logging", "order": 11},
            {"id": "why-imbalance", "title": "Why imbalance causes collapse", "order": 12},
            {"id": "balanced-training", "title": "Balanced training, natural validation", "order": 13},
            {"id": "samplers", "title": "Sampler tradeoffs", "order": 14},
            {"id": "ratio-sampling", "title": "Ratio-based dataset balancing", "order": 15},
            {"id": "shorter-epochs", "title": "Epoch size under resampling", "order": 16},
            {"id": "balanced-results", "title": "Balanced-training results", "order": 17},
            {"id": "false-positive-scale", "title": "False positives at scale", "order": 18},
            {"id": "overfitting-symptoms", "title": "Recognizing overfitting", "order": 19},
            {"id": "what-overfitting-means", "title": "Memorization versus generalization", "order": 20},
            {"id": "augmentation-purpose", "title": "Why data augmentation", "order": 21},
            {"id": "domain-aware-augmentation", "title": "Domain-aware augmentation", "order": 22},
            {"id": "augmentation-pipeline", "title": "Affine-grid augmentation pipeline", "order": 23},
            {"id": "cache-before-augmentation", "title": "Cache before augmentation", "order": 24},
            {"id": "flip", "title": "Mirroring", "order": 25},
            {"id": "shift", "title": "Random shifting", "order": 26},
            {"id": "scale", "title": "Random scaling", "order": 27},
            {"id": "rotate", "title": "In-plane rotation", "order": 28},
            {"id": "noise", "title": "Gaussian noise", "order": 29},
            {"id": "inspect-augmentations", "title": "Inspecting augmented samples", "order": 30},
            {"id": "augmentation-experiments", "title": "Comparing augmentation experiments", "order": 31},
            {"id": "augmentation-results", "title": "Interpreting augmentation results", "order": 32},
            {"id": "metric-driven-iteration", "title": "Metric-driven iteration", "order": 33},
            {"id": "complete-blueprint", "title": "Evaluation and improvement blueprint", "order": 34},
        ],
    },

    "exercises": [
        {
            "id": "M13.L01.EX01",
            "title": "Build a Confusion-Metric Calculator",
            "lesson_code": "M13.L01",
            "section_id": "metric-counts",
            "placement": "after_section",
            "description": "Compute TP/TN/FP/FN, precision, recall, F1, and accuracy from binary labels and probabilities.",
            "instructions": (
                "Create tensors of 20 binary labels and 20 positive-class probabilities. Use a threshold of 0.5 to build predicted labels. "
                "Compute TP, TN, FP, and FN using Boolean masks. Then calculate accuracy, precision, recall, and F1. "
                "Repeat with thresholds 0.25 and 0.75 and explain how the threshold changes FP and FN counts. "
                "Handle any zero denominator explicitly rather than allowing an unexplained NaN."
            ),
            "expected_output": (
                "Metric code, a three-row threshold-comparison table, and an explanation of the precision/recall tradeoff."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["confusion-matrix", "precision", "recall", "f1", "thresholding"],
        },
        {
            "id": "M13.L01.EX02",
            "title": "Implement Ratio-Based Balanced Sampling",
            "lesson_code": "M13.L01",
            "section_id": "ratio-sampling",
            "placement": "after_section",
            "description": "Reproduce the source's dataset-level class balancing logic.",
            "instructions": (
                "Create a synthetic candidate dataset with 100 negatives and 5 positives. Split the records into `negative_list` and `pos_list`. "
                "Implement index mapping for `ratio_int=1` and `ratio_int=2`, including modulo wraparound for positives. "
                "Print the first 18 labels for each ratio and verify the intended class pattern. "
                "Shuffle each class list at the beginning of a simulated epoch and explain why validation should not use this balancing."
            ),
            "expected_output": "Working sampler/index logic, printed class sequences, and an explanation of training versus validation balance.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["class-balancing", "oversampling", "dataset-indexing", "modulo"],
        },
        {
            "id": "M13.L01.EX03",
            "title": "Build and Inspect a 3D Augmentation Pipeline",
            "lesson_code": "M13.L01",
            "section_id": "inspect-augmentations",
            "placement": "after_section",
            "description": "Apply the chapter's spatial and noise transformations to a synthetic 3D candidate.",
            "instructions": (
                "Create a small synthetic 3D tensor containing an asymmetric bright structure so flips and rotations are visible. "
                "Implement options for flip, offset, scale, in-plane rotation, and Gaussian noise using `affine_grid` and `grid_sample` where appropriate. "
                "Generate at least three random outputs for the combined augmentation. Verify output shape is unchanged. "
                "For each transform, explain why it is or is not class-preserving for the CT task described in the chapter."
            ),
            "expected_output": "Working 3D augmentation code, shape checks, several visualized outputs, and a domain-validity explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["affine-grid", "grid-sample", "3d-augmentation", "domain-reasoning"],
        },
        {
            "id": "M13.L01.EX04",
            "title": "Diagnose Overfitting from Experiment Curves",
            "lesson_code": "M13.L01",
            "section_id": "augmentation-results",
            "placement": "after_section",
            "description": "Practice distinguishing optimization progress from generalization failure.",
            "instructions": (
                "Create or use synthetic epoch logs containing training positive loss, validation positive loss, precision, recall, and F1 for 20 epochs. "
                "Make training positive loss decrease steadily while validation positive loss begins rising after an early minimum. "
                "Identify the first clear overfitting region. Then create a second synthetic run representing stronger augmentation where the divergence is delayed. "
                "Explain which epoch you would consider saving and which metrics justify that decision."
            ),
            "expected_output": "Two metric tables/plots, identified overfitting points, and a model-selection explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["overfitting", "validation", "tensorboard-thinking", "model-selection"],
        },
        {
            "id": "M13.L01.EX05",
            "title": "Design the Next Metric and Augmentation Experiment",
            "lesson_code": "M13.L01",
            "section_id": "complete-blueprint",
            "placement": "after_section",
            "description": "Turn the chapter's exercises into an experiment plan.",
            "instructions": (
                ("1. Design a small experiment matrix containing: one alternative class-balance ratio, one stronger/weaker augmentation setting, one augmentation combination, and F1 plus at least one alternative F-beta score from the chapter's exercises.\n"
                 '2. For each run, state the hypothesis, training change, validation metrics to watch, and what result would support or reject the hypothesis.\n'
                 '3. Do not assume in advance which setting will win.')
            ),
            "expected_output": "A concise experiment matrix with hypotheses, controlled changes, metrics, and decision criteria.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["experimental-design", "f-beta", "augmentation", "class-balancing", "metrics"],
        },
    ],

    "quiz": {
        "id": "M13.L01.QZ01",
        "title": "Metrics, Balancing & Augmentation — Knowledge Check",
        "lesson_code": "M13.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M13.L01.Q01",
                "section_id": "four-outcomes",
                "question": "What is a false negative in the nodule-classification task?",
                "options": [
                    "A real nodule predicted as non-nodule.",
                    "A non-nodule predicted as nodule.",
                    "A real nodule predicted as nodule.",
                    "A non-nodule predicted as non-nodule.",
                ],
                "correct": 0,
                "explanation": "A false negative is a truly positive sample that the classifier misses.",
            },
            {
                "id": "M13.L01.Q02",
                "section_id": "recall",
                "question": "Which formula defines recall?",
                "options": [
                    "`TP / (TP + FP)`",
                    "`TP / (TP + FN)`",
                    "`TN / (TN + FP)`",
                    "`(TP + TN) / total`",
                ],
                "correct": 1,
                "explanation": "Recall measures the fraction of true positives that were successfully detected.",
            },
            {
                "id": "M13.L01.Q03",
                "section_id": "precision",
                "question": "Which error directly lowers precision?",
                "options": [
                    "True positives",
                    "True negatives",
                    "False positives",
                    "False negatives only",
                ],
                "correct": 2,
                "explanation": "Precision divides TP by TP+FP, so false positives reduce it.",
            },
            {
                "id": "M13.L01.Q04",
                "section_id": "threshold-space",
                "question": "What usually happens when the positive classification threshold is moved far to the left?",
                "options": [
                    "Precision and recall both necessarily become perfect.",
                    "Recall decreases and false negatives increase.",
                    "Nothing changes because thresholds do not affect predictions.",
                    "Recall tends to rise while false positives can increase.",
                ],
                "correct": 3,
                "explanation": "A lower threshold predicts positive more often, catching more positives but also more negatives.",
            },
            {
                "id": "M13.L01.Q05",
                "section_id": "f1",
                "question": "Why does the chapter use F1?",
                "options": [
                    "It combines precision and recall while penalizing strongly one-sided performance.",
                    "It is identical to overall accuracy.",
                    "It ignores false positives.",
                    "It eliminates the need for a validation set.",
                ],
                "correct": 0,
                "explanation": "F1 is the harmonic mean of precision and recall.",
            },
            {
                "id": "M13.L01.Q06",
                "section_id": "undefined-metrics",
                "question": "Why can precision become undefined when the model predicts no positives?",
                "options": [
                    "Recall is always larger than 1.",
                    "The denominator `TP + FP` becomes zero.",
                    "The model has too many true negatives.",
                    "CrossEntropyLoss returns no logits.",
                ],
                "correct": 1,
                "explanation": "If TP=FP=0, there are no predicted-positive samples and the precision denominator is zero.",
            },
            {
                "id": "M13.L01.Q07",
                "section_id": "why-imbalance",
                "question": "What drives the early majority-only collapse described in the chapter?",
                "options": [
                    "The positive class has much stronger gradients by design.",
                    "Validation updates the training weights.",
                    "The huge number of negative examples dominates the early training signal.",
                    "Data augmentation is applied before caching.",
                ],
                "correct": 2,
                "explanation": "With roughly 400 negatives per positive, negative-driven updates overwhelm the scarce positive signal.",
            },
            {
                "id": "M13.L01.Q08",
                "section_id": "balanced-training",
                "question": "Why is validation not balanced like training?",
                "options": [
                    "Validation cannot contain positive examples.",
                    "PyTorch does not support balanced validation.",
                    "F1 requires only negative samples.",
                    "Validation should represent the naturally imbalanced deployment distribution.",
                ],
                "correct": 3,
                "explanation": "Training is reshaped to aid learning; validation should remain representative of real conditions.",
            },
            {
                "id": "M13.L01.Q09",
                "section_id": "ratio-sampling",
                "question": "Why does the balanced dataset wrap positive indexes with modulo arithmetic?",
                "options": [
                    "Positive examples are scarce and must be reused during the larger balanced training stream.",
                    "Modulo converts CT data to Hounsfield Units.",
                    "It prevents negative examples from being shuffled.",
                    "It computes F1 directly.",
                ],
                "correct": 0,
                "explanation": "The minority positive list is exhausted quickly, so balancing intentionally cycles through it repeatedly.",
            },
            {
                "id": "M13.L01.Q10",
                "section_id": "false-positive-scale",
                "question": "Why can 99% negative-class accuracy still produce poor precision in this dataset?",
                "options": [
                    "Positive labels are always wrong.",
                    "The negative class is so large that even 1% errors can create more false positives than there are true positives.",
                    "Precision ignores true positives.",
                    "Balanced training changes validation labels.",
                ],
                "correct": 1,
                "explanation": "A tiny fraction of a huge majority class can still be a large absolute number of false positives.",
            },
            {
                "id": "M13.L01.Q11",
                "section_id": "overfitting-symptoms",
                "question": "Which pattern most strongly indicates overfitting in the chapter?",
                "options": [
                    "Training and validation losses both improve together.",
                    "Both class losses remain constant.",
                    "Positive training loss improves while positive validation loss worsens.",
                    "Training accuracy begins below validation accuracy.",
                ],
                "correct": 2,
                "explanation": "Improving training behavior alongside degrading unseen behavior indicates memorization rather than generalization.",
            },
            {
                "id": "M13.L01.Q12",
                "section_id": "cache-before-augmentation",
                "question": "Why should deterministic candidate extraction be cached before random augmentation?",
                "options": [
                    "Augmentation only works on CPU.",
                    "Caching must always happen before tensor conversion.",
                    "The validation set must be augmented too.",
                    "Caching after augmentation could freeze one random transformation and remove fresh variation.",
                ],
                "correct": 3,
                "explanation": "The expensive deterministic crop can be reused, while augmentation should remain newly randomized.",
            },
            {
                "id": "M13.L01.Q13",
                "section_id": "rotate",
                "question": "Why does the source restrict rotation to the X-Y plane?",
                "options": [
                    "The CT depth axis has different voxel spacing, so freely mixing axes would not preserve the same data geometry.",
                    "PyTorch cannot rotate 3D tensors.",
                    "Nodules only exist in one slice.",
                    "Rotation is used only for negative examples.",
                ],
                "correct": 0,
                "explanation": "Anisotropic spacing makes the depth axis physically different from the in-plane axes.",
            },
            {
                "id": "M13.L01.Q14",
                "section_id": "noise",
                "question": "What is distinctive about noise augmentation compared with the geometric transforms?",
                "options": [
                    "It changes the class label automatically.",
                    "It directly corrupts voxel values across the sample.",
                    "It cannot be randomized.",
                    "It always improves recall.",
                ],
                "correct": 1,
                "explanation": "Noise modifies the measured values themselves rather than only spatially resampling the candidate.",
            },
            {
                "id": "M13.L01.Q15",
                "section_id": "augmentation-results",
                "question": "What does the source observe about the fully augmented run?",
                "options": [
                    "It has zero recall.",
                    "It is identical to the unaugmented run.",
                    "It finds positive candidates much better and reduces the overfitting behavior seen in the baseline.",
                    "It always has the best precision and F1 among every run.",
                ],
                "correct": 2,
                "explanation": "The full augmentation improves positive detection and overfitting resistance, though another augmentation can have better precision/F1.",
            },
            {
                "id": "M13.L01.Q16",
                "section_id": "metric-driven-iteration",
                "question": "What is the chapter's strongest improvement pattern?",
                "options": [
                    "Add layers whenever accuracy is low.",
                    "Change the optimizer after every epoch.",
                    "Balance validation until its metrics look better.",
                    "Use metrics to diagnose a concrete failure, change training accordingly, and measure the result.",
                ],
                "correct": 3,
                "explanation": "The chapter progresses through diagnosis, targeted intervention, and measured comparison.",
            },
            {
                "id": "M13.L01.Q17",
                "section_id": "complete-blueprint",
                "type": "open",
                "question": (
                    "Explain the complete chain from Chapter 13's misleading 99.7% accuracy to the improved Chapter 14 training setup. "
                    "Your answer should include TP/TN/FP/FN, precision, recall, F1, class balancing, natural validation balance, overfitting, "
                    "data augmentation, caching order, and TensorBoard-based experiment comparison."
                ),
            },
        ],
        "passing_score": 70,
    },
}
