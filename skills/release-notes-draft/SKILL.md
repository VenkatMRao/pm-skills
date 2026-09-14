---
name: release-notes-draft
description: Draft release notes from one or more GitHub PR URLs, pulling PR descriptions, commits, diffs, and linked issues via the gh CLI. Produces a UAT/SME section and a customer-facing section for review before anything goes out. Use when the user asks to draft release notes, write up a release from PRs, or prepare notes for UAT sign-off.
---

# Release Notes Draft

Turn a list of merged (or about-to-merge) PRs into a release note draft the user
can hand to business SMEs for UAT, then — after their own approval — to
production users. This skill never sends anything anywhere itself; it produces a
draft clearly marked as a draft, for the user to review, edit, and route.

If the PRs going into this release haven't already been checked for
undocumented behavior changes, consider running `pr-behavior-change-scan` on
them first — anything it surfaces and the user confirms is real should get
added to the PR description before this skill drafts from it, so the release
note doesn't inherit the same gap.

If a `launch-brief-from-prd` draft already exists for this feature, re-check
it against what's actually shipping here — scope narrows between when a
launch brief gets written and when the feature actually ships, and this
skill's PR/ticket data is the source of truth for what's really going out.

## Inputs needed

- One or more GitHub PR URLs from the user.
- A release label (version number, date, or sprint name) — ask if not given
  rather than inventing one.
- `gh` CLI installed and authenticated. If a PR isn't accessible (private repo
  without access, wrong URL), say so and ask rather than guessing its content.

## Process

1. **Pull each PR's metadata**, not the full diff yet:
   ```
   gh pr view <url> --json title,body,number,url,author,baseRefName,headRefName,mergedAt,labels,files,additions,deletions,closingIssuesReferences
   ```
   `closingIssuesReferences` gives linked GitHub issues directly — fetch each
   with `gh issue view <repo> <number> --json title,body,labels` for the "why"
   behind the change when the PR description itself doesn't explain it.

2. **Only pull full diffs selectively**, to avoid burning context on noise:
   - Use the `files` field (path + additions/deletions) as the primary signal
     for *what* changed and *how much*.
   - Pull `gh pr diff <url>` in full only for PRs with a small file count, or
     for specific files likely to carry user-visible meaning (changed
     user-facing strings, API request/response shapes, config defaults,
     migration files). Skip full diffs for large mechanical changes
     (lockfile updates, generated files, formatting-only diffs, test-only
     changes) — the file list already tells you those aren't user-facing.
   - If a PR is large and its description doesn't explain the "why," say so
     as an open question rather than inferring intent from the diff alone.

3. **Group by theme across all PRs, not by PR number.** A release note
   organized as "PR #412, PR #418, PR #421" is useless to an SME or a customer.
   Cluster the changes into New / Improved / Fixed / Breaking or deprecated,
   merging related changes from different PRs into one entry where they serve
   the same user-facing outcome.

4. **Draft the note** in one markdown document with two sections:

   **UAT / SME section** (functional, internal-facing):
   - Header stating this is a draft pending review, the release label, and the
     source PR list (numbers + links) for traceability.
   - **Breaking changes / migration steps**, called out first and prominently
     if any exist — this is the section most likely to get missed and most
     costly to miss.
   - Per change: what changed, which PR(s)/issue(s) it traces to, and an
     explicit **"what to test"** bullet derived from the actual diff/description
     — not invented edge cases the PR doesn't give evidence for.
   - **Known limitations / explicitly out of scope**, if stated in the PR or
     issue.
   - **Open questions** — anything a PR touches that isn't clearly explained,
     named directly rather than glossed over.

   **Customer-facing section** (plain language, benefit-oriented):
   - Grouped as New / Improved / Fixed (omit Breaking/internal unless the
     break is customer-visible, e.g. a removed feature or changed pricing
     behavior — in which case call it out clearly).
   - No ticket numbers, PR links, internal team names, or implementation
     detail — describe outcomes for the user, not the code.
   - Omit anything without user-visible effect (refactors, test coverage,
     internal tooling, dependency bumps) even if it was a large PR.
   - Don't invent marketing language, quantified benefits, or use cases the
     diff/description doesn't actually support.

5. **End with an explicit reminder**: this is a draft based on the code and
   ticket content, not a QA report — actual test results and sign-off still
   need to come from the SMEs doing UAT, and the customer-facing section
   shouldn't go to production users until the user has approved it themselves.

## Guardrails

- Never claim something was tested, verified, or is bug-free — that's the
  point of the UAT step this draft feeds into.
- Never fabricate the reason for a change when the PR/issue doesn't state it;
  write "unclear from the PR — confirm with the author" instead of guessing.
- Keep every UAT-section bullet traceable to a specific PR or issue number so
  an SME (or the engineer who wrote it) can go verify the source.
- Don't dump raw diffs or full commit logs into the output — the draft should
  read as prose an SME can act on, with links back to source for anyone who
  wants the detail.
