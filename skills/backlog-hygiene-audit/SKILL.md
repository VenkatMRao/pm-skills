---
name: backlog-hygiene-audit
description: Audit a set of backlog tickets/specs for vague or missing acceptance criteria, and for scope drift — tickets that have quietly changed since they were approved/committed, which nobody is diffing. Use when the user asks to audit backlog hygiene, check acceptance criteria quality, or find scope creep across tickets.
---

# Backlog Hygiene Audit

Two independent checks per ticket: whether its acceptance criteria are actually
usable, and whether its current scope still matches what was approved when it
was committed. The second check is the one nobody does manually — it requires
comparing "ticket now" against "ticket at approval," which this skill tracks
across runs the same way `competitor-watch` tracks competitor snapshots.

## Before writing anything locally: the same safety check as competitor-watch

Backlog ticket content can be sensitive. Before creating any local audit files,
check whether the current working directory looks like a public or shared
repository. If it does, stop and ask the user where they'd actually like this
saved instead.

## Scope of the audit

Ask which tickets to audit if not given — a sprint, an epic, a specific list of
IDs/URLs, or "everything currently In Progress or Ready for Dev." Don't default
to auditing an entire unbounded backlog; that produces a report too long for
anyone to act on.

## Baseline storage convention

```
backlog-audit/
  <ticket-id>/
    baseline.md    # the approved snapshot this ticket is diffed against
    history.md      # append-only log of findings from each audit run
```

- `baseline.md` is the comparison anchor. It's only replaced when the user
  explicitly confirms a scope change was an intentional re-approval (see step
  4) — never updated silently, or the audit stops meaning anything.
- `history.md` is append-only — never overwrite a past finding. It's the trail
  that shows whether hygiene is improving or the same tickets keep drifting.

**Prefer the tracker's own edit history over a locally-seeded baseline when
it's reasonably accessible** — e.g. Jira's issue changelog API, or GitHub's
`userContentEdits` history on an issue — since it's authoritative and doesn't
depend on remembering to run this audit at the moment of approval. Fall back to
a local baseline file when the tracker doesn't expose that easily (most
GitHub-issue and Linear setups, or when the user is pasting ticket content
directly).

## Process

1. **Fetch each ticket's current state**: title, description, acceptance
   criteria (however that's captured — a dedicated field, a checklist, or
   prose in the description), estimate/points, status, labels. Use whatever
   the tracker is — `gh issue view` for GitHub Issues, a Jira/Linear API or
   export, or content the user pastes directly.

2. **Check acceptance criteria quality** (no baseline needed for this part):
   - **Missing** — no AC section or testable conditions at all.
   - **Vague** — present, but not independently testable (e.g. "should handle
     edge cases," "works well on mobile" with nothing specific). Say exactly
     *what's* untestable about it — "vague" on its own isn't actionable
     feedback.
   - **Adequate** — specific, testable conditions someone could actually check
     off.
   For Missing/Vague tickets, only draft proposed AC when the ticket
   description gives enough real detail to do so responsibly — and label it
   clearly as **"proposed — needs PM confirmation,"** never presented as
   already agreed. If there isn't enough in the ticket to propose AC
   responsibly, say so instead of guessing at scope the ticket doesn't state.

3. **Check for scope drift against the approval baseline:**
   - **Determine the approval point.** A ticket usually starts rough and firms
     up before it's actually committed — don't treat the ticket's original
     creation as the approval baseline by default. If using native tracker
     history, use the state at (or shortly after) the status change that means
     "committed" for this team (e.g. moved to "Ready for Dev" / "Committed") —
     ask the user which status transition counts as approval if it isn't
     obvious from the workflow.
   - **No baseline yet** (first audit of this ticket, and no usable native
     history): save current state as `baseline.md` and note explicitly that
     this run is establishing the reference point — there's nothing to diff
     yet.
   - **Baseline exists**: diff current description/AC/points against it and
     classify each difference:
     - *Material scope change* — added/removed/changed requirements or
       behavior. This is the actual scope-creep signal.
     - *Cosmetic change* — wording, formatting, typo fixes. Not creep; don't
       flag it as such.
     - *Estimate mismatch* — points unchanged despite material scope growth
       (or scope shrank but points didn't move). Flag as "re-estimate needed"
       regardless of whether the scope change itself is a problem.
   - **Append the finding to `history.md`** — every run's result, not just the
     flagged ones, so "no drift this run" is also on the record.

4. **Offer re-baselining, but only on explicit confirmation.** If a material
   change looks like an intentional, already-agreed scope change rather than
   creep, ask the user whether to update `baseline.md` to the current state so
   future audits measure from the new approved point. Never do this
   automatically — silently moving the goalposts defeats the point of the
   audit.

5. **Report, led by what needs attention.** Don't bury three flagged tickets in
   a table of forty fine ones:
   - A short section up top listing only tickets needing action, each with a
     one-line reason and recommended next step (rewrite AC, re-estimate,
     confirm scope change with stakeholder, etc.).
   - The full table below: ticket | AC status | drift status | recommended
     action, for everything audited.

## Guardrails

- Never flag "vague" without saying specifically what's missing or
  untestable.
- Never treat a ticket's earliest draft as its approval baseline without
  checking whether it was still being scoped at that point.
- Never auto-update a baseline — re-baselining requires the user's explicit
  yes.
- Never flag a wording/typo-only edit as scope creep.
- Don't audit an unbounded backlog by default — get an explicit scope first.
