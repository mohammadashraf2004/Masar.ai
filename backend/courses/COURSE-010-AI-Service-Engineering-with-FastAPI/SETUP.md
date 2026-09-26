# COURSE-010 Setup

1. Review `course_manifest.json`, module projects, lesson source mappings, and manual visual assets.
2. Run `python validate_course.py`.
3. Copy the folder into the appropriate Masar backend seed location only after confirming repository imports.
4. Set `MASAR_COURSE010_TRACK_SLUG` to the intended CareerTrack slug.
5. Run `python seed_course_010.py` inside the real Masar backend.
6. Verify created TrackLevels/Topics/Lessons/Exercises/Quizzes/Projects before exposing them to learners.
7. Add the 29 manual visual assets listed in `assets/visual_assets_manifest.json`; no book images are bundled.

The seed adapter is idempotent for existing topic slugs and child rows, but repository-specific behavior must be integration-tested before production use.
