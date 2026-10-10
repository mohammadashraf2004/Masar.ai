"""Fingerprint every table of a database, so a rehearsal can prove no existing record changed.

Run it against a RESTORED COPY (never the live database): save a snapshot, perform the step being
rehearsed (alembic upgrade, course import, legacy backfill), then compare.

    python deploy/rehearsal/snapshot.py save    --dsn postgresql://user:pw@host/db snapshot.json
    python deploy/rehearsal/snapshot.py compare --dsn postgresql://user:pw@host/db snapshot.json [--ignore t1,t2]

Each table is reduced to its row count and an order-independent digest of its rows. `compare` recomputes
the digest using only the columns the snapshot knew, so a migration may add columns without raising a
finding, while a changed value in an old column, a different row count, a vanished table or a dropped
column does. Exit status 1 means at least one finding; read each one: some are expected (alembic_version
always moves; the credit_packages table gains the four packs in migration 039).

The connection is opened read-only. Requires psycopg2 (already in the API image).
"""
import argparse
import json
import sys

import psycopg2


def tables(cur):
    cur.execute("select table_name from information_schema.tables where table_schema='public' "
                "and table_type='BASE TABLE' order by 1")
    return [row[0] for row in cur.fetchall()]


def columns(cur, table):
    cur.execute("select column_name from information_schema.columns where table_schema='public' "
                "and table_name=%s order by ordinal_position", (table,))
    return [row[0] for row in cur.fetchall()]


def fingerprint(cur, table, cols):
    select = ", ".join(f'"{column}"' for column in cols)
    cur.execute(
        "select count(*), coalesce(md5(string_agg(h, '' order by h)), '') from "
        f'(select md5(t::text) as h from (select {select} from "{table}") t) s'
    )
    rows, digest = cur.fetchone()
    return {"rows": rows, "digest": digest}


def save(cur, path):
    snapshot = {}
    for table in tables(cur):
        cols = columns(cur, table)
        snapshot[table] = {"columns": cols, **fingerprint(cur, table, cols)}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=1)
    print(f"saved {len(snapshot)} tables, {sum(entry['rows'] for entry in snapshot.values())} rows")
    return 0


def compare(cur, path, ignore):
    with open(path, encoding="utf-8") as handle:
        before = json.load(handle)
    now = set(tables(cur))
    findings, identical = [], 0
    for table, old in before.items():
        if table in ignore:
            continue
        if table not in now:
            findings.append(f"{table}: table vanished ({old['rows']} rows)")
            continue
        present = set(columns(cur, table))
        kept = [column for column in old["columns"] if column in present]
        gone = [column for column in old["columns"] if column not in present]
        if gone:
            findings.append(f"{table}: columns gone {gone}")
            continue
        got = fingerprint(cur, table, kept)
        if got["rows"] != old["rows"]:
            findings.append(f"{table}: rows {old['rows']} -> {got['rows']}")
        elif got["digest"] != old["digest"]:
            findings.append(f"{table}: content changed (same row count {got['rows']})")
        else:
            identical += 1
    print(f"identical tables: {identical}; findings: {len(findings)}; new tables: {sorted(now - set(before))}")
    for finding in findings:
        print("  FINDING", finding)
    return 1 if findings else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("save", "compare"))
    parser.add_argument("snapshot", help="snapshot file to write (save) or read (compare)")
    parser.add_argument("--dsn", required=True, help="postgresql://user:password@host:port/database of a RESTORED COPY")
    parser.add_argument("--ignore", default="", help="comma-separated tables to skip when comparing")
    args = parser.parse_args()
    connection = psycopg2.connect(args.dsn)
    connection.set_session(readonly=True)
    cur = connection.cursor()
    ignore = {name for name in args.ignore.split(",") if name}
    sys.exit(save(cur, args.snapshot) if args.mode == "save" else compare(cur, args.snapshot, ignore))


if __name__ == "__main__":
    main()
