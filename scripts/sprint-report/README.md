# Sprint report generator

Turns a Jira/Linear CSV export into a markdown sprint summary: velocity,
completion rate, what's blocked, what carried over, and a per-assignee breakdown.
No API key or dependencies — standard library only.

## Usage

```bash
python3 generate_report.py path/to/export.csv --sprint-name "Sprint 24"
```

Write to a file instead of stdout:

```bash
python3 generate_report.py path/to/export.csv -o sprint-24-report.md
```

## Input format

A CSV with these columns (extra columns are ignored):

| Column | Required | Notes |
|---|---|---|
| `Key` | No | Issue identifier, e.g. `APP-101` |
| `Summary` | No | Issue title |
| `Status` | Yes | Anything containing "done"/"closed"/"resolved"/"completed" counts as done; anything containing "block" is flagged as blocked |
| `Story Points` | Yes | Numeric; blank or non-numeric treated as 0 |
| `Assignee` | No | Blank rows are grouped under "Unassigned" |

Most issue trackers (Jira, Linear, GitHub Projects) can export a sprint/board view
to CSV directly — rename the columns to match, or adjust the column names at the
top of `generate_report.py`.

## Try it

```bash
python3 generate_report.py sample_data/sprint_export.csv --sprint-name "Sprint 24"
```
