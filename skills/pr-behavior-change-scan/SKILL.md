---
name: pr-behavior-change-scan
description: Scan one or more GitHub PR diffs for user-facing behavior changes that aren't mentioned in the PR description or linked ticket, so they get confirmed before merge instead of shipping as a surprise. Use when the user asks to check a PR for unintended/undocumented behavior changes, wants a pre-merge product review of a PR, or asks what a diff actually changes for users. Not a substitute for a full code review (correctness, security, style) — this only looks for user-visible behavior the PR text doesn't already say it changes.
---

# PR Behavior Change Scan

PMs almost never read diffs, so a behavior change that wasn't called out in the
PR description ships unnoticed — the code review caught correctness, nobody
checked whether the *description* actually matches what the code *does*. This
skill closes that specific gap: read the diff, find changes a user or API
consumer would notice, and flag the ones the PR text doesn't already mention.

This runs earlier than `release-notes-draft` (at review time, before merge, on
one PR at a time or a batch of release candidates) rather than at release time
across already-merged PRs. Anything confirmed real here is worth adding to the
PR description immediately — that's also the input `release-notes-draft` reads
later, so fixing it here means the release note doesn't miss it either.

## Process

1. **Pull PR metadata first, not the full diff**: title, body, linked issues
   (`gh pr view <url> --json title,body,files,additions,deletions,closingIssuesReferences`).
   Read the linked issue too (`gh issue view`) — the "documented" bar is
   whichever of the PR description or the ticket already explains the change,
   not the PR description alone.

2. **Triage files before reading full diffs.** Sort the changed files by
   whether they're plausible surface area for user-facing behavior:
   - **Likely surface area** — frontend components/templates, API route
     handlers and response serializers, validation logic, permission/access
     checks, default config values, feature flag defaults, user-facing copy
     /strings, sorting or pagination logic.
   - **Unlikely surface area** — test files, CI config, internal tooling,
     generated files, dependency lockfiles, logging/monitoring, pure
     refactors with no logic change.
   Pull the full diff (`gh pr diff`) only for the likely-surface-area files.
   Skim the unlikely ones just enough to confirm they really are internal —
   don't skip them silently, since a mislabeled file is exactly how a real
   change gets missed.

3. **From the diffs, extract concrete behavior changes**: what a user or API
   consumer would experience differently — a new/removed field in a response,
   a changed default, a validation rule that now accepts/rejects something it
   didn't before, an error message that changed, a permission check that
   loosened or tightened, an altered sort order, a changed empty/error state.
   Describe each as **old behavior → new behavior**, not just "logic changed
   in file X."

4. **Check each one against the PR description and linked ticket.** If it's
   already explained there (even briefly), it's documented — don't flag it,
   just note it was checked. If it isn't mentioned anywhere in the PR text or
   ticket, flag it.

5. **Rate confidence per flagged item.** Static diff reading produces false
   positives — code behind a disabled feature flag, a branch that's
   unreachable, a change that only affects an internal/admin surface. Mark
   each flag **High/Medium/Low** confidence and say why, rather than
   presenting every flag with equal weight.

6. **Report:**
   - **Flagged: undocumented behavior changes** (the main output) — one entry
     per item: old → new behavior, file/line, confidence, and a concrete next
     step ("confirm with the author this was intentional," "add to the PR
     description," "this looks unintentional — worth a second look before
     merge").
   - **Checked and already documented** — a brief count/list, not full detail;
     this section exists so the user trusts the scan was thorough, not that
     it's the focus.
   - **Excluded as non-user-facing** — a short note on what was skipped and
     why, for the same reason.

## Guardrails

- Don't do a general code review here — no correctness, security, or style
  feedback. If something looks like a real bug rather than an undocumented
  behavior change, say so briefly but point the user to a proper code review
  rather than expanding scope.
- Don't flag internal-only changes (admin tooling, logging, refactors with no
  behavior change) as user-facing.
- Don't assume an undocumented change is a mistake — the flag is "confirm
  this was intentional," not an accusation. Many are legitimate small changes
  that just weren't written up.
- Don't skip triaging a file just because it's large — large files are exactly
  where a real behavior change hides among noise.
- State confidence honestly; a Low-confidence flag is still worth surfacing,
  just labeled as needing more verification than a High-confidence one.
