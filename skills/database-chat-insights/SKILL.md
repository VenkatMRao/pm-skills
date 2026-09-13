---
name: database-chat-insights
description: Answer a plain-language question against a SQL database/warehouse and turn the result into an insight, with a mandatory human confirmation step before any query runs. Use when the user asks to query, explore, or get insights from a database or data warehouse using natural language.
---

# Database Chat & Insights

Turn a plain-language question into a read-only SQL query, run it only after the
user has seen and approved it, and turn the result into a plain-language insight
— not just a table. This skill drives
[`scripts/nl-data-query/chat.py`](../../scripts/nl-data-query/chat.py) as its
engine; read that script's README for the full safety model before using it
against a real database.

## Non-negotiable safety rule

**Never execute a query the user hasn't seen.** Generating SQL is safe (it
doesn't touch the database); running it is not. Always show the generated SQL in
the conversation and get an explicit go-ahead before executing it — even though
the underlying script *can* run non-interactively with `--yes`, that flag exists
for a human running the script directly at their own terminal, not for this
skill to use on their behalf. If the user says something like "just run whatever
you think is right" for a whole session, confirm that scope once, out loud, before
treating it as standing permission — don't infer blanket approval from a single
"yes."

## Process

1. **Confirm database access.** Check for an `NL_DB_URL` environment variable or
   ask the user for a SQLAlchemy connection string (`postgresql://...`,
   `mysql://...`, `sqlite:///...`, or a Snowflake/BigQuery URL if the matching
   SQLAlchemy dialect package is installed — see the script's README). Also
   confirm `ANTHROPIC_API_KEY` is set. Don't guess or fabricate credentials.

2. **Get the schema** before writing any SQL:
   ```
   python3 scripts/nl-data-query/chat.py --db-url "$NL_DB_URL" --schema-only
   ```
   This needs no API key and doesn't touch data — safe to run without asking.

3. **Generate SQL for the question**, without executing it:
   ```
   python3 scripts/nl-data-query/chat.py --db-url "$NL_DB_URL" --question "<the user's question>" --sql-only
   ```

4. **Show the generated SQL to the user in the conversation** — not just
   "I'm going to query the database," the actual SQL text — and ask them to
   confirm before it runs. If the script refused to generate SQL (a
   `CANNOT_ANSWER:` line, or a rejection for containing a write/DDL keyword),
   relay that reason to the user instead of trying to work around it.

5. **Execute only after explicit approval**, using the exact approved SQL:
   ```
   python3 scripts/nl-data-query/chat.py --db-url "$NL_DB_URL" --execute-sql "<approved SQL>" --question "<original question>" --yes
   ```
   `--yes` is correct here because the human confirmation already happened in
   the conversation in step 4 — it isn't skipping that step, it's skipping the
   script's *own* redundant terminal prompt.

6. **Relay the result.** Share the printed insight, and the table too if it's
   short enough to be useful inline. If the script noted the result was
   truncated (capped at 200 rows), say so — don't present a partial view as
   complete.

## When the question implies a write

If translating the question would require modifying data (e.g. "mark all trial
users as expired"), don't attempt it through this skill. Say clearly that this
workflow is read-only by design, and that a write needs to go through whatever
process the user normally uses for that (a migration, an admin tool, direct DB
access with someone who owns that risk).

## When there's already a database connection available another way

If the user's environment already exposes the database through a different
mechanism (an MCP database server, a `psql`/`bq` CLI already configured), it's
fine to use that instead of the script — but keep the same discipline: inspect
the schema first, write a single read-only `SELECT`, show it and get approval
before running it, and cap/summarize large result sets rather than dumping them
raw into the conversation.
