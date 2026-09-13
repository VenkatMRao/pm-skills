# NL data query

Ask a database a question in plain English, get back a plain-language insight —
via the Claude API translating your question to SQL, running it, and summarizing
the result. Works against any database SQLAlchemy can connect to.

Pairs with [`skills/database-chat-insights`](../../skills/database-chat-insights/SKILL.md),
which drives this same tool conversationally from inside Claude Code.

## Safety model

- Every generated query is checked as a single **read-only `SELECT`** before it's
  shown to you. `INSERT`/`UPDATE`/`DELETE`/`DROP`/`ALTER`/etc. are refused
  outright, and multi-statement (`;`-chained) SQL is rejected.
- Nothing runs against the database until you confirm it (or pass `--yes` to run
  without asking — still read-only enforced).
- **This check is a heuristic string check, not a full SQL parser.** It's a
  second line of defense, not the only one. Whenever your database supports it,
  connect with a genuinely **read-only database role**, not an admin credential —
  that's the guarantee that actually matters if the heuristic ever misses
  something.
- Result sets are capped (200 rows by default) before they're even shown to the
  model, so a broad question can't balloon into an enormous prompt.

## Setup

```bash
pip install -r requirements.txt
# plus your database's driver, e.g.:
pip install psycopg2-binary   # Postgres
# pip install pymysql                # MySQL
# pip install snowflake-sqlalchemy   # Snowflake
# pip install sqlalchemy-bigquery    # BigQuery

export ANTHROPIC_API_KEY=sk-ant-...
export NL_DB_URL="postgresql://user:pass@host:5432/dbname"   # or pass --db-url
```

## Usage

**Interactive chat:**

```bash
python3 chat.py
```

```
Connected to postgresql database. Found schema:
- customers(id INTEGER, name TEXT, plan TEXT, signup_date TEXT)
- orders(id INTEGER, customer_id INTEGER, amount REAL, order_date TEXT)

Ask a question in plain language (or 'exit' to quit).

> which plan has the most revenue this quarter?

Generated SQL:
SELECT c.plan, SUM(o.amount) AS revenue
FROM orders o JOIN customers c ON c.id = o.customer_id
WHERE o.order_date >= '2026-04-01'
GROUP BY c.plan ORDER BY revenue DESC LIMIT 200

Run this query? [y/N] y

plan       | revenue
-----------+--------
enterprise | 998.0
pro        | 147.0

Insight: Enterprise plan customers generated the most revenue this quarter
($998), more than 6x the pro plan ($147) despite having fewer customers —
enterprise deal size is doing the work here, not volume.
```

**One-shot question:**

```bash
python3 chat.py --question "how many customers signed up last month?"
```

**Just see the schema** (no API key needed):

```bash
python3 chat.py --schema-only
```

**Generate SQL without running it** — useful for a review step before execution:

```bash
python3 chat.py --question "..." --sql-only
```

**Run a specific, already-approved query** (this is what the Claude Code skill
uses to separate "generate" from "execute"):

```bash
python3 chat.py --execute-sql "SELECT plan, COUNT(*) FROM customers GROUP BY plan" --question "how many customers per plan?"
```

## Try it without a real database

```bash
python3 sample_data/build_sample_db.py
python3 chat.py --db-url sqlite:///sample_data/sample.db
```

## Extending to Snowflake / BigQuery

This is built on SQLAlchemy specifically so it isn't locked to one warehouse.
Install the matching dialect package (`snowflake-sqlalchemy` or
`sqlalchemy-bigquery`) and pass the appropriate connection URL as `--db-url` —
no code changes needed for the common case. If a warehouse's SQL dialect needs
prompting nudges (e.g. Snowflake's date functions, BigQuery's backtick-quoted
table names), add a dialect-specific hint to `SQL_SYSTEM_PROMPT` in `chat.py`.
