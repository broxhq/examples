---
name: sqlite-query
trigger: When the user points you at a SQLite database file (.db, .sqlite, .sqlite3) and asks to inspect its schema, query it, or answer questions about its data.
---

# SQLite Query

You can inspect and read SQLite databases using the `query.py` script. **Read-only by design** — write operations are rejected.

## How to use

The script lives at `<skill-dir>/scripts/query.py`. The database file is opened in read-only mode (`mode=ro`), so you cannot accidentally modify it.

### Step 1: Always start with an overview

When the user gives you a database, **always run the overview first** before answering questions about it:

```bash
python3 <skill-dir>/scripts/query.py <db-path>
```

This lists every table with its row count and column types. You need this map before running meaningful queries.

### Step 2: Describe a specific table

```bash
python3 <skill-dir>/scripts/query.py <db-path> --table <name>
```

Shows full column schema, row count, and the first 5 rows. Use this to understand a table's contents before writing complex queries.

### Step 3: Run a SELECT

```bash
python3 <skill-dir>/scripts/query.py <db-path> --sql "SELECT * FROM users WHERE active = 1"
```

By default the script adds `LIMIT 100` if the query has no LIMIT clause. Override with `--limit N` (max 1000).

### Get JSON output

```bash
python3 <skill-dir>/scripts/query.py <db-path> --sql "SELECT ..." --json
```

Use this when you need to process results programmatically (count, aggregate, transform).

## Examples

> User: "What's in users.db?"

Run `python3 scripts/query.py users.db` — list tables. Then summarize: "The database has 3 tables: users (1,234 rows), orders (5,678 rows), products (89 rows)."

> User: "How many orders did customer 42 place last month?"

1. Run overview to find the `orders` table
2. Describe the table to see columns
3. Run `python3 scripts/query.py db.sqlite --sql "SELECT COUNT(*) FROM orders WHERE customer_id = 42 AND created_at >= date('now','-1 month')"`

> User: "Show me the top 10 products by revenue"

`python3 scripts/query.py db.sqlite --sql "SELECT product_id, SUM(price * qty) AS revenue FROM orders GROUP BY product_id ORDER BY revenue DESC LIMIT 10"`

## Setup requirements

**None.** Python stdlib includes the `sqlite3` module.

## Limits and caveats

- **Read-only**: INSERT/UPDATE/DELETE/DROP/ALTER/CREATE are blocked. If the user needs to modify data, use the `sqlite3` CLI directly.
- **Default limit 100 rows**: Prevents accidental memory blowouts. Override with `--limit` up to 1000.
- **String values truncated at 200 chars in markdown output** — use `--json` for full values.
- **No transactions, no joins across databases**: Single-file inspection only.
- **Encrypted databases (SQLCipher) are not supported.**
