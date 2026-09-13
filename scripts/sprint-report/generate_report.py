#!/usr/bin/env python3
"""Generate a markdown sprint summary from a Jira/Linear CSV export.

Expected CSV columns: Key, Summary, Status, Story Points, Assignee.
Extra columns are ignored.
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

DONE_STATUSES = {"done", "closed", "resolved", "completed"}


def load_issues(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def points(issue):
    raw = issue.get("Story Points", "").strip()
    try:
        return float(raw)
    except ValueError:
        return 0.0


def is_done(issue):
    return issue.get("Status", "").strip().lower() in DONE_STATUSES


def is_blocked(issue):
    return "block" in issue.get("Status", "").strip().lower()


def generate_report(issues, sprint_name):
    total_points = sum(points(i) for i in issues)
    done = [i for i in issues if is_done(i)]
    done_points = sum(points(i) for i in done)
    carried = [i for i in issues if not is_done(i)]
    blocked = [i for i in issues if is_blocked(i)]

    by_assignee = defaultdict(lambda: {"total": 0.0, "done": 0.0, "count": 0})
    for i in issues:
        assignee = i.get("Assignee", "").strip() or "Unassigned"
        by_assignee[assignee]["total"] += points(i)
        by_assignee[assignee]["count"] += 1
        if is_done(i):
            by_assignee[assignee]["done"] += points(i)

    completion_pct = (done_points / total_points * 100) if total_points else 0

    lines = [f"# Sprint report: {sprint_name}", ""]
    lines.append(f"- **Committed:** {total_points:g} pts across {len(issues)} issues")
    lines.append(f"- **Completed:** {done_points:g} pts ({completion_pct:.0f}%)")
    lines.append(
        f"- **Carried over:** {len(carried)} issue(s), "
        f"{sum(points(i) for i in carried):g} pts"
    )
    lines.append("")

    if blocked:
        lines.append("## Blocked")
        for i in blocked:
            lines.append(
                f"- **{i.get('Key', '')}** — {i.get('Summary', '')} "
                f"({i.get('Assignee', 'Unassigned') or 'Unassigned'})"
            )
        lines.append("")

    carried_not_blocked = [i for i in carried if not is_blocked(i)]
    if carried_not_blocked:
        lines.append("## Carried over")
        for i in carried_not_blocked:
            lines.append(
                f"- **{i.get('Key', '')}** — {i.get('Summary', '')} — "
                f"_{i.get('Status', '')}_ ({i.get('Assignee', 'Unassigned') or 'Unassigned'})"
            )
        lines.append("")

    lines.append("## By assignee")
    lines.append("| Assignee | Issues | Points committed | Points done | Completion |")
    lines.append("|---|---|---|---|---|")
    for assignee, d in sorted(by_assignee.items(), key=lambda kv: -kv[1]["total"]):
        pct = (d["done"] / d["total"] * 100) if d["total"] else 0
        lines.append(
            f"| {assignee} | {d['count']} | {d['total']:g} | {d['done']:g} | {pct:.0f}% |"
        )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Path to the Jira/Linear CSV export")
    parser.add_argument(
        "--sprint-name",
        default=None,
        help="Label for the report header (defaults to the CSV filename)",
    )
    parser.add_argument(
        "-o", "--output", help="Write report to this file instead of stdout"
    )
    args = parser.parse_args()

    issues = load_issues(args.csv_path)
    if not issues:
        raise SystemExit("No rows found in input CSV.")

    sprint_name = args.sprint_name or Path(args.csv_path).stem
    report = generate_report(issues, sprint_name)

    if args.output:
        Path(args.output).write_text(report + "\n", encoding="utf-8")
        print(f"Wrote report to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
