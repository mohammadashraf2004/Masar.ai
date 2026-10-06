# Inline lesson images

> **Current syntax: `{{image:<key>}}`** (optionally `{{image:<key>|Caption for this spot}}`). `{{figure:<key>}}`
> below is the same marker under its first name and still works. Everything on this page about figures
> applies to images; the additions are in [Images in English and Arabic](#images-in-english-and-arabic).

A lesson is an ordered learning experience. A figure is part of it, placed where it
explains something, not an attachment listed at the end.

```
Course > Module > Lesson > ordered content
                            text  ->  figure  ->  text  ->  figure  ->  text
```

## What a lesson author writes

The lesson body stays Markdown (`lessons.content`). To show a figure, put its key on a
line of its own:

```markdown
LoRA decomposes the trainable update into two low-rank matrices.

{{figure:lora-low-rank-adaptation}}

The original weights stay frozen while the small matrices are trained.
```

* The syntax is `{{figure:<key>}}`. The key is lowercase words joined by hyphens.
* It must be on a line by itself. A marker in the middle of a sentence, a misspelt key
  or a missing brace is a **validation error**, so a typo can never reach a learner.
* A marker inside a fenced code block is code, not a figure (a lesson may show the syntax).
* A lesson never contains a file name, a path or a URL. The key is the only thing that
  ties the lesson to an image, so the files can move (course folder to object storage)
  without touching any lesson.

### Consolidated course files

The canonical course structure may keep a complete lesson in a single discovered
Python file instead of repeating lesson paths in a manifest:

```text
COURSE-NNN_Name/
  course_manifest.json
  modules/
    module_01.py
    module_02.py
```

Each discovered file defines `LESSON_CODE`, `MODULE_ORDER`, `MODULE_TITLE`,
`MODULE_DESCRIPTION`, and `TOPIC`. Files with the same `MODULE_ORDER` become lessons
of the same module and are ordered by `LESSON_CODE`. The `TOPIC` contains the lesson
body, exercises, quiz, and optional project. Embedded questions are promoted to one
module quiz automatically; `module_quizzes.json` is retained only as a source of
stable legacy module and quiz IDs during migration.

Figure placement does not change in this structure: put `{{figure:<key>}}` inside
`TOPIC["lesson"]["content"]`. The loader resolves it through the course's
`assets_manifest.json` exactly as it does for every older layout.

`[[IMAGE_NEEDED: ...]]` is an authoring request, not an image link. It must remain
until an image file and manifest entry exist, then be replaced by a
`{{figure:<key>}}` marker. This prevents missing assets from becoming broken images
in learner content.

## Images in English and Arabic

```markdown
{{image:transformer-flow}}
{{image:transformer-flow|Transformer processing flow}}
```

* One picture, shared. The English body (the lesson's Python module) and the Arabic body
  (`ar/<lesson>.md`) place the **same keys in the same order**; the importer checks it. The text after `|` is
  a caption for that occurrence only and **may differ between languages** (it is translated), so only the key is compared.
* Alt text and caption per language come from the manifest: the Arabic lesson uses `alt_ar` / `caption_ar`,
  the English one `alt_en` / `caption_en` (`alt` / `caption` are the same as the `_en` names). A missing value falls back
  to the other language's; an inline caption beats both.
* The picture lives in the course folder under `assets/` (for example `assets/M01/transformer-flow.png`); it is
  never inside `en/` or `ar/`, and never copied per language. Lessons hold the key, not the path or a URL.
* `[[IMAGE_NEEDED: ...]]` is the opposite marker: *the image does not exist yet*. Both remain valid. Turning a request
  into a link is `seeds/link_images.py` (below); nothing replaces a request automatically.

Manifest entries can be a list (as before) or a map keyed by image key, with or without the `version`/`assets` wrapper:

```json
{ "transformer-flow": { "file": "assets/M01/transformer-flow.png", "lesson": "M01.L01",
    "alt_en": "Transformer processing flow", "alt_ar": "تدفق المعالجة في Transformer",
    "caption_en": "...", "caption_ar": "..." } }
```

| validation | |
|---|---|
| error | an unknown key; a malformed token (not on its own line, bad key, empty caption); a missing or fake image file; a duplicate key (also when the same key is written twice in a map); a path that is absolute, has `..`, a drive letter, a backslash, or leaves the course folder (symlinks included); `lesson` naming a lesson the course does not have; the Arabic body placing different images than the English |
| warning | an image no lesson places; no alt text; a file outside `assets/`; one file under two keys; a file in `assets/` the manifest does not list; `[[IMAGE_NEEDED]]` still in a lesson |

`python seeds/arabic_course_files.py status` prints, for each course with images: found / referenced / missing /
broken references / unused / `IMAGE_NEEDED` left. `python seeds/import_courses.py --validate-only` runs all the checks
above without touching the database, and a normal import refuses to start while any of them fails.

### Turning an `IMAGE_NEEDED` request into a link

```bash
python seeds/link_images.py list --course COURSE-009 --lesson M01.L01      # numbered markers + images not placed yet
python seeds/link_images.py replace --course COURSE-009 --lesson M01.L01 --marker 2 --key rag-ingestion-stack          # preview
python seeds/link_images.py replace --course COURSE-009 --lesson M01.L01 --marker 2 --key rag-ingestion-stack --write
python seeds/link_images.py replace --map links.json --write               # [{"course","lesson","marker","key"}, ...]
```

It never guesses: the key must be in the manifest with its file in place, the marker must be named by number or by a
piece of text that matches exactly one marker, and it must stand on a line of its own. The English module and `ar/<lesson>.md`
change together or not at all; the Arabic `source_hash` is refreshed only if it was current; after writing, the course is validated
again and everything is put back if that finds a new problem. Without `--write` it only prints.

### Placing an image where no request stands

When an image belongs to a concept the lesson teaches but no `IMAGE_NEEDED` marker is there, name the text the image follows:

```bash
python seeds/link_images.py place --map placements.json          # preview; add --write to apply
# [{"course": "COURSE-012", "lesson": "M01.L05", "key": "reflexion-loop",
#   "after": "The solver then tries again with that feedback included in its context.",
#   "after_ar": "ثم يحاول Solver مرة أخرى مع تضمين هذا Feedback داخل Context."}]
```

`after` / `after_ar` are the last line(s) of the English / Arabic block the image follows. Each must appear exactly once in its
lesson and end a block (a blank line follows it); the last line of a code block works too, and the image then follows the
closing fence. Several keys (`"a,b"`) become consecutive lines; an `after` that is itself an image token adds the image as the
next line of that run. `"remove": "key"` takes an image out of its current run first (a move). Nothing but image lines is added or
removed, the same validation and revert-on-new-problem rules as `replace` apply, and an anchor that is not exact is refused.

### Authoring syntax never reaches a learner

Three constructs in a lesson body are authoring syntax. `app/services/content/lesson_blocks.py` parses them into typed blocks and
`app/services/learning/lesson_content.py` decides what each client may show; the stored Markdown is never edited.

| In the lesson | Parsed as | Learner (production) | Author (development) |
|---|---|---|---|
| `{{image:key}}` / `{{figure:key}}` | `image` (or `image_missing`) | the figure | the figure |
| `[[IMAGE_NEEDED: title \| ... ]]` | `author_marker` | nothing | a dashed "Image needed: title" note (title only) |
| `{{exercise:M01.L02.EX04}}` | `ExerciseBlock`, validated against the lesson's exercises | nothing: the lesson page renders the lesson's exercises itself, below the article, paired by `lesson_id` | nothing, or an `exercise_missing` note if the lesson has no exercise at all |

* Markers inside a fenced block or an inline code span are code (a lesson may show the syntax) and are kept; a marker that is not on a line of
  its own, a misspelt one, or an unclosed `IMAGE_NEEDED` is cut out of the prose, and the validator reports the malformed image and exercise
  markers so they get fixed.
* `--validate-only` blocks on an exercise marker that names no exercise of its own lesson (`M01.L02.EX04`, or the same id with the course prefix).
* A body with none of this has `blocks: null` and renders as before; a body whose only content is markers has `blocks: []`, which renders nothing.
* "Production" is `settings.is_production`; the front end additionally drops author notes in a production build.
* In production the lesson response's `content` / `content_ar` are cleaned too (`learner_markdown` in `lesson_blocks.py`): authoring lines are dropped with the one
  blank line that set them off, everything else is kept character for character, and code that shows the syntax is left alone. Outside production they keep the source
  as written. The stored body is never changed and the page renders `blocks`, not this Markdown.

### Arabic alt text and captions

A manifest entry carries `alt` / `caption` (English) and `alt_ar` / `caption_ar` (Arabic). The Arabic lesson gets the Arabic ones, the English lesson the
English ones; either falls back to the other if only one was written, and the image block's `alt_lang` / `caption_lang` say which language it
ended up in, so the client sets `lang` and `dir` from the text actually shown (an Arabic caption with English terms reads right to left; an
English fallback stays left to right). Arabic text explains in Arabic and keeps the technical terms that are normally said in English
(`تدفق آلية Attention في Transformer`). `alt_ar` says briefly what is visible; `caption_ar` says what the learner should notice. Write coordinate pairs as `(1,2)` and
spell out negative numbers (`سالب 127`) or `N×M` sizes in words: digits and minus signs next to Arabic text can be displayed in the wrong order. `--validate-only` and `arabic_course_files.py status` warn (never block) about an image that an Arabic lesson
places without `alt_ar` / `caption_ar`; images no Arabic lesson places are not asked for Arabic text.

### A missing image at read time

If a lesson places a key the course no longer has (removed after import), the API returns an `image_missing` block and the
page shows a "could not be loaded" note instead of dropping the spot silently. Outside production the note also names the key and carries a
`data-missing-image` hook; a production build shows only the generic note and leaves neither in the DOM.

## What a course ships: `assets_manifest.json`

One file per course folder, next to `course_manifest.json`:

```json
{
  "version": 1,
  "course_id": "COURSE-008",
  "assets": [
    {
      "key": "lora-low-rank-adaptation",
      "type": "image",
      "file": "assets/lora-low-rank-adaptation.png",
      "alt": "LoRA adds two small trainable matrices beside a frozen weight matrix",
      "caption": "Low-rank matrices are trained while the original weights stay frozen.",
      "figure_number": "Figure 4.2",
      "source_reference": "Figure 4-2; source file lora.png"
    }
  ],
  "pending": [ { "figure": "Figure 9-2", "title": "...", "lesson_id": "L011-014", "priority": "required" } ]
}
```

| field | required | learners see it |
|---|---|---|
| `key` | yes | no (it is what lessons name) |
| `file` | yes | no. Relative to the course folder; the physical name can stay as it is (`horp_0102.png`, `B21848_3_1.png`, ...) |
| `alt` | yes | screen readers |
| `caption` | no | yes, under the figure |
| `figure_number` | no | yes, before the caption ("Figure 4.2 — ..."). Left unset for figures numbered by their source book, which would mean nothing here |
| `source_reference` | no | never. For authors |
| `type` | no | only `image` |

`pending` lists figures the curriculum calls for that have no image file yet. It is
information for authors and is ignored by the importer.

The importer reads the type, size, hash and dimensions **from the file**, not from the
manifest. Allowed: PNG, JPEG, GIF, WebP, up to 5 MB. SVG is not allowed (it can carry
script, and figures are served from the API's origin).

## Validation (`seeds/import_courses.py --validate-only`)

Errors (nothing is imported):

* a lesson places a key that has no asset ("Lesson L008-014 references 'x' but no corresponding asset exists")
* a marker that is not on its own line / malformed
* an asset with no alt text, a missing file, a file that is not really the type its extension says,
  a `file` that is absolute, has `..`, a drive letter or a backslash, a duplicate or badly formed key,
  a manifest that is not in this format

Warning (not an error):

* an asset no lesson places ("unused asset")

## Import

`import_course` writes each asset to `course_assets` (migration 019), keyed by
`(course, key)`. Re-running updates in place and reports `+created ~updated =unchanged`;
an asset that leaves the manifest is reported as stale and kept.

The lesson text is imported unchanged, markers included. The blocks are made when a lesson
is **read**, not stored, so nothing is duplicated and a corrected caption reaches learners
without touching the lesson.

## API

`GET /tool-courses/{slug}` and `GET /tool-courses/topics/{id}`: a lesson that places at
least one figure carries

```json
"blocks": [
  {"type": "markdown", "content": "LoRA decomposes ..."},
  {"type": "image", "asset_key": "lora-low-rank-adaptation",
   "url": "/learning/courses/course-008/assets/lora-low-rank-adaptation?exp=...&sig=...",
   "alt": "...", "caption": "...", "figure_number": null, "width": 800, "height": 400},
  {"type": "markdown", "content": "The original weights ..."}
],
"blocks_ar": null
```

* A lesson with no figure has `blocks: null` and is rendered from `content`, as it always was.
* `content` is still returned (with the markers) so nothing that reads it breaks; the viewer
  renders the blocks.
* Code, tables, callouts and equations stay inside the Markdown blocks (the existing renderer
  already handles them).
* A locked (paid) lesson has an empty `content` and no blocks, so it has no figure URLs.
* No path, storage key, hash or source reference is ever in a response.

## Serving images

`GET /learning/courses/{slug}/assets/{key}?exp=&sig=`

* The figure is looked up by `(course, key)`. A request never names a file, and a key from one
  course cannot be read through another.
* An `<img>` cannot send an `Authorization` header, so the URL is the credential: an HMAC of
  course, key and expiry made with the server secret. It is only ever put into a lesson response
  the learner may read, is the same for everyone within a day (so it caches) and expires after
  2 to 3 days. A missing, altered or expired signature is refused (422 / 403).
* Response: the stored MIME type, `ETag` (the content hash; `If-None-Match` gives 304),
  `Cache-Control: private, max-age=86400`, `X-Content-Type-Options: nosniff`.
* `backend/courses/` is never exposed as a directory. The local store resolves a database
  `storage_key` and refuses anything that is not a file inside its root.

### Moving to S3 / CloudFront later

Nothing in a lesson changes. Add a store whose `response()` redirects to a signed object URL
(`app/services/assets/store.py`), or change `asset_url()` (`app/services/assets/urls.py`) to
return the CDN URL for the asset's `storage_key`. The browser follows whatever URL the API gives
it (`resolveAssetUrl` in `frontend/src/lib/api.ts` accepts a path or a full URL).

## Browser

`MarkdownLesson` takes `blocks` and renders them in order inside one term-annotation scope (so the
first-mention rule stays per lesson). Figures use `LessonImage`: responsive, aspect ratio kept from
the stored size (no layout jump), lazy loaded, on a light panel that reads in both themes, caption
below. Activating a figure opens an enlarged view (fits the window on a desktop, full width and
scrollable on a phone; Escape, the close button or a tap outside closes it and focus returns).
If an image fails to load the learner sees a note in place of it and the caption stays.

## Adding a figure

1. Put the file in the course folder (any name).
2. Add an entry to that course's `assets_manifest.json` with a semantic `key`, `alt` and `caption`.
3. Put `{{figure:<key>}}` on its own line in the lesson, right after the sentence it explains.
4. `python seeds/import_courses.py --validate-only`, then import.

## What was placed (COURSE-008 to 014)

All 191 committed figures are placed, across 160 lessons. The lesson bodies in these courses
are structured outlines (objective, concepts, workflow, practice, ...), so there is rarely a sentence
that describes one figure; each figure goes at the end of the section that introduces its topic
(for example, after **Concepts**, **System mental model**, **Core topics**, **Engineering model**,
**Learn**), and a lesson with two or three figures spreads them over successive sections instead of
stacking them. The old lists of "visual assets" / "manual visual references" were removed from the
lessons that now show their figures, together with the lesson metadata that duplicated them
(`LESSON_META['visuals']`, `visual_reference`, `FIGURE_REFERENCES`).

* Lessons that call for a figure that has not been supplied still carry their old "add manually" note;
  those figures are listed under `pending` in the manifest.
