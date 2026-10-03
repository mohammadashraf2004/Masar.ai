"""The course endpoint must not join lessons x exercises x quizzes x projects in one statement.

`GET /tool-courses/{slug}` used to eager-load a topic's four collections with `joinedload`, which
returns one row per combination: a COURSE-011 module of 21 lessons, 42 exercises and 21 quizzes is
~18,000 rows each carrying the lesson bodies, and a single request took the API past 2 GB and killed
it. One query per collection returns each row once.
"""
from sqlalchemy import event

from app.db.session import engine
from tests.curriculum_fixtures import make_spec
from tests.learning_fixtures import learn_catalog, learn_client, learn_db, logs_enabled, register  # noqa: F401
from app.services.curriculum import importer
from seeds import curriculum as cfg


def _rows_fetched_per_statement(client, url, headers):
    counts = []

    def after(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT") and cursor.rowcount >= 0:
            counts.append(cursor.rowcount)

    event.listen(engine, "after_cursor_execute", after)
    try:
        response = client.get(url, headers=headers)
    finally:
        event.remove(engine, "after_cursor_execute", after)
    assert response.status_code == 200, response.text
    return response, counts


def test_a_large_module_is_read_with_a_row_count_that_grows_with_its_size_not_its_square(learn_client, learn_db, learn_catalog):
    spec = make_spec("COURSE-001", modules=2, lessons=12)  # 12 lessons, 24 exercises, 12 quizzes per module
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    importer.import_course(learn_db, spec, definitions["COURSE-001"])
    learn_db.commit()
    who = register(learn_client)

    response, counts = _rows_fetched_per_statement(learn_client, "/api/v1/tool-courses/course-001", who["headers"])
    topics = response.json()["topics"]
    assert [len(t["lessons"]) for t in topics] == [12, 12]
    assert [len(t["exercises"]) for t in topics] == [24, 24]
    # a cartesian join would return 12 x 24 x 12 = 3,456 rows per topic
    assert max(counts) <= 60, sorted(counts)[-5:]

    topic_id = topics[0]["id"]
    response, counts = _rows_fetched_per_statement(learn_client, f"/api/v1/tool-courses/topics/{topic_id}", who["headers"])
    assert len(response.json()["lessons"]) == 12
    assert max(counts) <= 60, sorted(counts)[-5:]
