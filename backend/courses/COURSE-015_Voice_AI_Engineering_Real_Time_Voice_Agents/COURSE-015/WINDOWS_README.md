# Windows extraction note

This export uses short, stable filesystem names to avoid Windows `0x80010135: Path too long` errors.

- Root folder: `COURSE-015`
- Module folders: `M015-01` ... `M015-08`
- Lesson files: `L015-001.py` ... `L015-064.py`
- Human-readable lesson titles and slugs remain inside each lesson's metadata and manifests.
- `__pycache__` and `.pyc` files are intentionally excluded from the archive.

If Windows still reports a path-length issue, extract the ZIP close to the drive root, for example `C:\Masar\COURSE-015`.
