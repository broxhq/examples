#!/usr/bin/env python3
"""Inspect and query SQLite databases.

Modes:
    query.py <db>                          # list tables + schema
    query.py <db> --table <name>           # show table schema + row count + 5 sample rows
    query.py <db> --sql "<SELECT ...>"    # run a query, output markdown table
    query.py <db> --sql "..." --json      # output as JSON array
    query.py <db> --sql "..." --limit N   # safety cap (default 100, max 1000)

Read-only: rejects INSERT/UPDATE/DELETE/DROP/ALTER/CREATE.
"""
import json
import os
import re
import sqlite3
import sys


WRITE_KEYWORDS = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|attach|detach|reindex|vacuum|pragma)\b",
    re.IGNORECASE,
)


def truncate(value, max_len: int = 200) -> str:
    s = "" if value is None else str(value)
    if len(s) > max_len:
        return s[:max_len] + "…"
    return s


def render_markdown_table(headers: list[str], rows: list[tuple]) -> str:
    if not headers:
        return "(empty result)"
    parts = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        parts.append("| " + " | ".join(truncate(c).replace("|", "\\|") for c in row) + " |")
    return "\n".join(parts)


def overview(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    tables = [r[0] for r in cur.fetchall()]
    if not tables:
        print("(no tables)")
        return

    print(f"## Tables ({len(tables)})")
    for name in tables:
        cur.execute(f"SELECT COUNT(*) FROM \"{name}\"")
        count = cur.fetchone()[0]
        cur.execute(f"PRAGMA table_info(\"{name}\")")
        cols = cur.fetchall()
        col_summary = ", ".join(f"{c[1]} {c[2]}" for c in cols)
        print(f"\n### {name} ({count} rows)")
        print(f"columns: {col_summary}")


def describe_table(conn: sqlite3.Connection, name: str) -> None:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name = ?", (name,))
    if not cur.fetchone():
        sys.stderr.write(f"table not found: {name}\n")
        sys.exit(1)

    cur.execute(f"PRAGMA table_info(\"{name}\")")
    cols = cur.fetchall()
    print(f"## {name}")
    print()
    print("### Schema")
    print(render_markdown_table(
        ["column", "type", "notnull", "default", "pk"],
        [(c[1], c[2], c[3], c[4] if c[4] is not None else "", c[5]) for c in cols],
    ))

    cur.execute(f"SELECT COUNT(*) FROM \"{name}\"")
    count = cur.fetchone()[0]
    print(f"\nrows: {count}")

    cur.execute(f"SELECT * FROM \"{name}\" LIMIT 5")
    rows = cur.fetchall()
    headers = [d[0] for d in cur.description]
    print(f"\n### First {len(rows)} rows")
    print(render_markdown_table(headers, rows))


def run_sql(conn: sqlite3.Connection, sql: str, limit: int, as_json: bool) -> None:
    if WRITE_KEYWORDS.search(sql):
        sys.stderr.write("write operations are not allowed. Use a SELECT-only query.\n")
        sys.exit(1)

    if "limit" not in sql.lower():
        sql = sql.rstrip("; \n\t") + f" LIMIT {limit}"

    cur = conn.cursor()
    try:
        cur.execute(sql)
    except sqlite3.Error as e:
        sys.stderr.write(f"SQL error: {e}\n")
        sys.exit(1)

    if cur.description is None:
        print("(no rows returned)")
        return

    headers = [d[0] for d in cur.description]
    rows = cur.fetchall()

    if as_json:
        json.dump(
            [dict(zip(headers, [None if v is None else v for v in row])) for row in rows],
            sys.stdout,
            ensure_ascii=False,
            default=str,
            indent=2,
        )
        sys.stdout.write("\n")
    else:
        print(render_markdown_table(headers, rows))


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.stderr.write(__doc__)
        sys.exit(0 if args else 1)

    db_path = args[0]
    if not os.path.isfile(db_path):
        sys.stderr.write(f"database not found: {db_path}\n")
        sys.exit(1)

    table = None
    sql = None
    as_json = False
    limit = 100

    i = 1
    while i < len(args):
        a = args[i]
        if a == "--table":
            table = args[i + 1]
            i += 2
        elif a == "--sql":
            sql = args[i + 1]
            i += 2
        elif a == "--json":
            as_json = True
            i += 1
        elif a == "--limit":
            limit = min(1000, int(args[i + 1]))
            i += 2
        else:
            sys.stderr.write(f"Unknown argument: {a}\n")
            sys.exit(1)

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        if sql:
            run_sql(conn, sql, limit, as_json)
        elif table:
            describe_table(conn, table)
        else:
            overview(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
