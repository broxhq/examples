# @brox/sqlite-query

Inspect and query SQLite databases safely. Read-only by design.

## Install

```bash
brox install @brox/sqlite-query
```

## Requirements

- Python 3.8+
- **Zero external dependencies** — stdlib `sqlite3`

## What the agent can do after installing

- List all tables with row counts and column types
- Describe a specific table's schema with sample rows
- Run SELECT queries and return markdown tables or JSON
- Answer business questions grounded in the actual database

## Safety

- Database is opened with `mode=ro` (read-only URI) — physical write protection
- Query parser rejects INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/REPLACE/ATTACH/DETACH/REINDEX/VACUUM/PRAGMA

## Direct usage

```bash
python3 scripts/query.py app.db
python3 scripts/query.py app.db --table users
python3 scripts/query.py app.db --sql "SELECT id, name FROM users LIMIT 10"
python3 scripts/query.py app.db --sql "..." --json --limit 500
```

## License

MIT
