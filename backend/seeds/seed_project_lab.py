"""Sync Project Lab content (app/services/project_lab/definitions) into the DB.

Idempotent: re-running updates titles, instructions, hints and validator
settings in place and never touches learner attempts. Requires the career
tracks (seed.py) first.

    python -m seeds.seed_project_lab
"""
from app.db.schema_guard import require_migrated_schema
from app.db.session import SessionLocal


def main() -> None:
    import app.main  # noqa: F401 - resolves every model relationship
    from app.services.project_lab.definitions import PROJECTS
    from app.services.project_lab.service import sync_definitions

    session = SessionLocal()
    try:
        report = sync_definitions(session, PROJECTS)
        for kind, count in report.items():
            print(f"  {kind:<10} +{count}")
        print("Project Lab content synced.")
    finally:
        session.close()


if __name__ == "__main__":
    require_migrated_schema()
    main()
