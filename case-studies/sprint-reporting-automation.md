# Cutting sprint reporting from an hour to a few minutes

*Details generalized/anonymized. See [`scripts/sprint-report`](../scripts/sprint-report/) for the underlying tool.*

## Problem

At the end of every sprint, I put together a written summary for stakeholders who
didn't sit in standups: what shipped, what didn't, what's blocked, and who owned
what. The raw data lived in the issue tracker, but turning a board view into a
readable narrative meant manually copying issue statuses and points into a doc,
then writing the summary by hand. It was mechanical work that still took
30-60 minutes every sprint, and it was the kind of task that quietly got skipped
when a sprint ended on a busy day — which meant the update stakeholders relied on
was sometimes the thing that slipped.

## Approach

I wrote a script ([`generate_report.py`](../scripts/sprint-report/generate_report.py))
that takes the CSV export the issue tracker already produces and generates the
structural parts of the report automatically: committed vs. completed points,
what's blocked, what carried over, and a per-assignee breakdown. That removed the
mechanical part of the task — counting points, sorting by status — and left only
the part that actually needs judgment: writing the one or two sentences of
context a stat table can't provide (why something's blocked, what the plan is for
carryover work).

## Outcome

- The mechanical part of sprint reporting went from ~30-45 minutes of manual
  tallying to under a minute of running a script.
- Because the report generates itself from the same export every time, the format
  stayed consistent sprint over sprint, which made trends (completion rate,
  which issues chronically carry over) visible in a way an inconsistently
  hand-written summary hadn't surfaced.
- The task stopped being something that got skipped under time pressure, since
  the effort required dropped below the threshold where skipping felt worth it.

## What I'd change next

The script currently expects a flat CSV export; a natural next step is pulling
directly from the tracker's API so the report can run on a schedule without a
manual export step first.
