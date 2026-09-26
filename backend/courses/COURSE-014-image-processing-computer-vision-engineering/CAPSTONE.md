# COURSE-014 Capstone — Classical-to-Modern Computer Vision System

## Objective

Build one end-to-end visual system that starts from raw image input and demonstrates disciplined use of classical image processing plus at least one modern pretrained vision component.

## Required architecture

Image acquisition → input validation → classical preprocessing → enhancement/restoration → segmentation/detection/structural analysis → measurement/semantic interpretation → optional generative stage → evaluation → structured output.

## Acceptance criteria

- Use at least three classical image-processing operations.
- Handle image dtype/range/channel/coordinate assumptions explicitly.
- Include geometry or frequency-domain reasoning.
- Include an enhancement/restoration decision.
- Include a segmentation, detection, or structural-analysis component.
- Use at least one pretrained modern vision model with its preprocessing contract.
- Include quantitative evaluation when ground truth exists.
- Report runtime/resource evidence where practical.
- Document at least three failure cases.
- If a generative stage is used, explicitly distinguish plausible synthesis from evidence-preserving reconstruction.
- Provide reproducible configuration and example inputs.

## Deliverables

1. Runnable pipeline.
2. Example inputs.
3. Intermediate visualizations.
4. Final outputs.
5. Metrics/evaluation notes.
6. Failure analysis.
7. Technical README.
