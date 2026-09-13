#!/usr/bin/env python3
"""Chat with a SQL database/warehouse in plain language and get insights back.

Works against any database SQLAlchemy can connect to (Postgres, MySQL, SQLite
out of the box; Snowflake/BigQuery with the relevant SQLAlchemy dialect package
installed — see README).

Safety model:
- Every generated query is validated as a single read-only SELECT before it is
  shown to you. INSERT/UPDATE/DELETE/DDL statements are refused outright.
- Nothing runs against the database until you (a human, or the Claude Code skill
  relaying your approval) confirms it — see the four run modes below.
- This validation is a heuristic string check, not a real SQL parser, and is not
  a substitute for connecting with a genuinely read-only database credential.
  Use a read-only DB role/user in addition to this script's checks whenever the
  underlying database supports one.

Run modes:
  (no flags)                          Interactive REPL: ask questions one at a
                                       time, confirm each generated query, see
                                       the table + a plain-language insight.
  --question Q                        Same as one REPL turn, non-interactive.
  --question Q --sql-only             Generate SQL for Q and print it. Does not
                                       touch the database.
  --execute-sql "SELECT ..."          Validate and run a specific query (e.g.
                                       one a human already approved), optionally
                                       with --question for insight context.
  --schema-only                       Print the discovered schema and exit.
                                       No ANTHROPIC_API_KEY required.
"""
import argparse
import os
import re
import sys

from sqlalchemy import create_engine, inspect, text

DEFAULT_MODEL = "claude-sonnet-5"
MAX_ROWS = 200
INSIGHT_ROW_SAMPLE = 50

SQL_SYSTEM_PROMPT = """You are a data analyst who writes SQL for a {dialect} database.

Given the schema below and a plain-language question, respond with ONLY the SQL
query needed to answer it. Rules:
- SELECT statements only. Never write INSERT, UPDATE, DELETE, DROP, ALTER,
  TRUNCATE, CREATE, GRANT, or any statement that modifies data or schema.
- Exactly one statement, no semicolon-chained multi-statement SQL.
- Always include a LIMIT clause (max {max_rows} rows) unless the question
  clearly asks for a single aggregate value (e.g. one count or average).
- If the question is ambiguous, or the schema below can't answer it, respond
  with a line starting with "CANNOT_ANSWER:" followed by a one-sentence
  explanation, instead of guessing at a query.

Return only the SQL (or the CANNOT_ANSWER line) — no prose, no markdown fences.

Schema:
{schema}"""

INSIGHT_SYSTEM_PROMPT = """You are a data analyst summarizing a query result for a
product manager. Given the original question, the SQL that answered it, and the
result rows, write a short plain-language summary:
- Lead with the direct answer to the question.
- Call out anything notable (a skew, an outlier, a surprisingly small/large
  number) rather than just restating the table.
- If the note below says the result set was truncated, say so and make clear
  the summary is based on a partial view.
- Don't speculate about causes the data can't support."""

READ_ONLY_PATTERN = re.compile(r"^\s*SELECT\b", re.IGNORECASE)
FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|MERGE|REPLACE|EXEC|CALL)\b",
    re.IGNORECASE,
)


def get_schema_description(engine, max_tables=50):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    lines = []
    for table_name in tables[:max_tables]:
        columns = inspector.get_columns(table_name)
        col_desc = ", ".join(f"{c['name']} {c['type']}" for c in columns)
        lines.append(f"- {table_name}({col_desc})")
    if len(tables) > max_tables:
        lines.append(f"... and {len(tables) - max_tables} more tables (truncated)")
    return "\n".join(lines) if lines else "(no tables found)"


def validate_sql(sql):
    """Heuristic read-only/single-statement check. Returns (is_valid, reason)."""
    sql = sql.strip()
    if not sql:
        return False, "Empty query."
    semicolon_count = sql.count(";")
    if semicolon_count > 1:
        return False, "Multiple statements are not allowed."
    if semicolon_count == 1 and not sql.rstrip().endswith(";"):
        return False, "Multiple statements are not allowed."
    stripped = sql.rstrip(";").strip()
    if ";" in stripped:
        return False, "Multiple statements are not allowed."
    if not READ_ONLY_PATTERN.match(stripped):
        return False, "Only SELECT statements are allowed."
    if FORBIDDEN_KEYWORDS.search(stripped):
        return False, "Query contains a forbidden keyword (data/schema modification)."
    return True, None


def generate_sql(client, model, dialect, schema, question):
    system = SQL_SYSTEM_PROMPT.format(dialect=dialect, schema=schema, max_rows=MAX_ROWS)
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text.strip()


def generate_insight(client, model, question, sql, columns, rows, truncated):
    preview = "\n".join(
        ", ".join(f"{col}={val}" for col, val in zip(columns, row))
        for row in rows[:INSIGHT_ROW_SAMPLE]
    )
    note = "TRUNCATED: yes, more rows exist than shown" if truncated else "TRUNCATED: no"
    user_content = (
        f"Question: {question or '(not provided)'}\n\n"
        f"SQL: {sql}\n\n"
        f"Result columns: {', '.join(columns)}\n"
        f"{note}\n"
        f"Result rows ({min(len(rows), INSIGHT_ROW_SAMPLE)} of {len(rows)} shown):\n{preview}"
    )
    message = client.messages.create(
        model=model,
        max_tokens=512,
        system=INSIGHT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text.strip()


def run_query(engine, sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = result.fetchmany(MAX_ROWS + 1)
    truncated = len(rows) > MAX_ROWS
    return columns, [tuple(r) for r in rows[:MAX_ROWS]], truncated


def print_table(columns, rows, max_display=20):
    if not rows:
        print("(no rows)")
        return
    widths = [
        max(len(str(c)), max((len(str(r[i])) for r in rows), default=0))
        for i, c in enumerate(columns)
    ]
    print(" | ".join(str(c).ljust(w) for c, w in zip(columns, widths)))
    print("-+-".join("-" * w for w in widths))
    for row in rows[:max_display]:
        print(" | ".join(str(v).ljust(w) for v, w in zip(row, widths)))
    if len(rows) > max_display:
        print(f"... ({len(rows) - max_display} more rows not shown)")


def get_anthropic_client():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set the ANTHROPIC_API_KEY environment variable before running this script.")
    import anthropic

    return anthropic.Anthropic()


def handle_question(engine, client, model, dialect, schema, question, auto_confirm, sql_only):
    sql = generate_sql(client, model, dialect, schema, question)

    if sql.startswith("CANNOT_ANSWER:"):
        print(sql)
        return

    valid, reason = validate_sql(sql)
    if not valid:
        print(f"Refusing to run generated query: {reason}\nGenerated SQL was:\n{sql}")
        return

    if sql_only:
        print(sql)
        return

    print(f"\nGenerated SQL:\n{sql}\n")
    if not auto_confirm:
        confirm = input("Run this query? [y/N] ").strip().lower()
        if confirm != "y":
            print("Skipped.")
            return

    execute_and_report(engine, client, model, question, sql)


def execute_and_report(engine, client, model, question, sql):
    try:
        columns, rows, truncated = run_query(engine, sql)
    except Exception as e:
        print(f"Query failed: {e}")
        return

    print()
    print_table(columns, rows)
    print()

    insight = generate_insight(client, model, question, sql, columns, rows, truncated)
    print(f"Insight: {insight}")


def main():
    parser = argparse.ArgumentParser(
        description="Chat with a SQL database in plain language and get insights back.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--db-url",
        default=os.environ.get("NL_DB_URL"),
        help="SQLAlchemy connection string, e.g. postgresql://user:pass@host/db (or set NL_DB_URL)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--question", default=None, help="Ask a single question and exit instead of starting the REPL")
    parser.add_argument("--sql-only", action="store_true", help="With --question: print the generated SQL only, don't run it")
    parser.add_argument("--execute-sql", default=None, help="Skip generation and run this exact SQL (still validated as read-only)")
    parser.add_argument("--schema-only", action="store_true", help="Print the discovered schema and exit (no API key needed)")
    parser.add_argument("--yes", action="store_true", help="Skip the confirmation prompt before running a query (still read-only enforced)")
    args = parser.parse_args()

    if not args.db_url:
        raise SystemExit("Pass --db-url or set NL_DB_URL to a SQLAlchemy connection string.")

    engine = create_engine(args.db_url)
    dialect = engine.dialect.name

    if args.schema_only:
        print(get_schema_description(engine))
        return

    schema = get_schema_description(engine)
    client = get_anthropic_client()

    if args.execute_sql:
        valid, reason = validate_sql(args.execute_sql)
        if not valid:
            raise SystemExit(f"Refusing to run this query: {reason}")
        if not args.yes:
            print(f"About to run:\n{args.execute_sql}\n")
            confirm = input("Run this query? [y/N] ").strip().lower()
            if confirm != "y":
                print("Skipped.")
                return
        execute_and_report(engine, client, args.model, args.question, args.execute_sql)
        return

    if args.question:
        handle_question(engine, client, args.model, dialect, schema, args.question, args.yes, args.sql_only)
        return

    print(f"Connected to {dialect} database. Found schema:\n{schema}\n")
    print("Ask a question in plain language (or 'exit' to quit).\n")
    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question or question.lower() in {"exit", "quit"}:
            break
        handle_question(engine, client, args.model, dialect, schema, question, args.yes, sql_only=False)
        print()


if __name__ == "__main__":
    main()
