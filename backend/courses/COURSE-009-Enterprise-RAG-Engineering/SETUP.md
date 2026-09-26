# Setup / Handoff

1. Copy the COURSE-009 folder under your backend seed workspace.
2. Run `python validate_course.py`.
3. Review `course_manifest.json` and the target CareerTrack mapping.
4. Set `MASAR_COURSE009_TRACK_SLUG`.
5. Run `seed_course_009.py` from an environment where the Masar backend imports resolve.
6. Add the 14 manual visual assets listed in `assets/visual_assets_manifest.json`.
7. Run database-level smoke tests before any production seed.

The seed adapter is intentionally non-destructive: it inserts missing content and skips existing topic content rather than overwriting learner-facing rows.
