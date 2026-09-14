---
name: stale-doc-audit
description: Audit PRDs/specs/wikis for stale assumptions — statements that were true when written but no longer hold, verified against current tickets, metrics, and docs rather than just checking last-edited dates. Use when the user asks to find outdated docs, audit doc staleness, or check whether old PRDs/specs still reflect reality.
---

# Stale Doc Audit

A doc's last-edited date is a weak signal — a doc touched last week can still
contain a stale assumption from months ago, and a doc untouched for a year
might still be entirely accurate. This skill checks specific claims a doc makes
against current reality, and uses age only to help prioritize which docs are
worth digging into first, not as the verdict itself.

## Gather sources and confirm scope first

Ask which docs to audit if not given — a folder of PRDs/specs, a Google Drive
folder, a Confluence/Notion space, or a specific list. Confirm scope before
starting; don't attempt to audit an entire wiki unbounded in one pass.

## Process

1. **Extract concrete, checkable claims from each doc** — not the whole
   narrative, just the parts that can go stale:
   - **Metrics/numbers** stated as current fact ("conversion is currently
     2%," "this affects 10% of users").
   - **Dependencies/blockers** referencing a specific ticket, team, or system
     ("blocked by TICKET-123," "waiting on the payments team," "not yet
     supported until X ships").
   - **Status claims** ("currently in beta," "not yet launched," "planned for
     Q2").
   - **References to specific systems/features by name** that might have
     since been renamed, replaced, or deprecated.
   - **Target dates/timelines** that may have already passed.

2. **Verify each claim against a current source of truth** — don't just guess
   based on how old the doc looks:
   - For a referenced ticket/blocker: check its current status (`gh issue
     view`, or the tracker in use — same approach as `backlog-hygiene-audit`).
     If it's resolved/closed, the doc's "blocked by" claim is stale.
   - For a stated metric: if it lives in a database/warehouse, use
     `nl-data-query` / `database-chat-insights` to check the current value.
     Flag a material divergence from what the doc states, and flag separately
     if the metric/table referenced doesn't seem to exist anymore (renamed or
     deprecated).
   - For a referenced system/feature name: check whether it still appears
     under that name in current docs/code — if `terminology-consistency-check`
     has already been run on this corpus, its canonical name map is a fast
     way to spot a doc using a retired name.
   - For a target date: if it's clearly passed, check whether the doc (or a
     linked ticket) shows the work as actually completed. A passed date with
     no completion signal is a real flag; a passed date on work that shipped
     on time just means the doc itself needs a "done" note, which is lower
     stakes.
   - When no source is available to verify a claim, say **"unverified"**
     rather than assuming it's still accurate or assuming it's stale.

3. **Use age and doc-corpus signals only to prioritize, not to conclude.** A
   very old last-edit date, or a doc that's the only one still using
   terminology retired everywhere else, is a reason to look harder at that
   doc first — it's not itself a finding.

4. **Classify each doc:**
   - **Likely stale** — at least one claim directly contradicted by a current
     source (a cited blocker is resolved, a cited metric has materially
     diverged, a referenced system no longer exists under that name).
   - **Possibly stale** — no direct contradiction found, but strong signals
     (very old, isolated terminology, a long-passed target date with no
     completion signal) that make it worth a human look.
   - **Likely current** — no contradictions, and either recently touched or
     nothing suggesting drift.

5. **Report, led by what needs attention:**
   - **Likely stale**, each claim with: what the doc says, what the current
     source shows, and where to look to confirm.
   - **Possibly stale**, with the specific signal that earned the flag.
   - A brief note on **Likely current** docs (count is enough, not full
     detail) so the audit reads as complete rather than selectively negative.

6. **Offer, don't act.** Produce the findings; don't edit, archive, or mark
   docs as deprecated yourself unless the user explicitly asks for that as a
   follow-up.

## Guardrails

- Never call a doc stale on age alone — every "Likely stale" finding needs a
  specific claim contradicted by a specific current source.
- Never treat a doc's silence on a topic as evidence of staleness — only a
  direct or strongly implied contradiction counts.
- When a claim can't be verified against anything accessible, say so plainly
  instead of guessing either way.
- Don't audit an unbounded doc corpus without the user confirming scope first.
