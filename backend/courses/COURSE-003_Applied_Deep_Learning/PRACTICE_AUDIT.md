# COURSE-003 Practicality Audit

## Result

The course is intentionally code-first rather than theory-heavy.

- 47 lessons.
- 47 guided code labs: one in every lesson.
- 94 coding exercises: minimum two per lesson.
- 16 module projects/labs.
- 8 portfolio-scale projects.
- Every exercise has starter code and acceptance criteria.
- Validation parses every lesson Python file and every starter-code snippet.

## Exercise design rules used

1. **Build something**: implement a real PyTorch component, helper, trainer, transform, dataset, model, profiler/export flow, or evaluation function.
2. **Prove it works**: use shape/device/dtype assertions, parameter-delta tests, numerical parity, metric checks, or benchmark evidence.
3. **Debug something**: exercises include broken `nn.Module` code, device/dtype mismatches, optimizer coverage, train/eval mistakes, output/loss mismatches, shape failures, and source-code bugs.
4. **Run controlled experiments**: augmentation ablations, scheduler traces, architecture latency/parameter comparisons, packed-sequence benchmarks, AMP/checkpointing memory comparisons, regularization comparisons, and robustness curves.
5. **Avoid passive API drills**: the learner is normally required to return a measurable artifact, report, assertion, benchmark, or before/after comparison.

## Practical progression

- M01–M05: tensor/data/model/training/inference mechanics.
- M06–M09: CNN construction, pretrained models, fine-tuning, augmentation, ensembles.
- M10: variable-length recurrent sequence implementation.
- M11 optional: waveform, log-mel, audio pipeline benchmarking, SpecAugment.
- M12: data sanity, tiny-batch overfit, TensorBoard, hooks, gradient health.
- M13: torch.profiler, pipeline optimization, torch.compile, torch.export and parity checks.
- M14: allocator memory metrics, AMP, activation checkpointing and measured trade-offs.
- M15: MixUp/CutMix/label smoothing plus FGSM robustness curves.
- M16 optional: reconstruction/super-resolution, GAN loop correctness, detection dataset/model contracts.

## Acceptance philosophy

A task is not considered complete because it runs without an exception. Exercises ask for at least one of:

- output-shape or dtype/device contract;
- correct train/eval or gradient behavior;
- model parameter-update/no-update evidence;
- reproducible split or preprocessing contract;
- validation metric under a controlled comparison;
- latency/throughput/memory measurement;
- numerical parity between eager/compiled/exported flows;
- robustness or ablation table.

## Deliberate scope exclusions

Docker/Kubernetes/cloud serving remain for MLOps. Modern Transformer fine-tuning remains for a dedicated Applied NLP / AI Developer course. Distributed PyTorch and modern quantization remain explicit source gaps rather than being invented from BOOK-003.
