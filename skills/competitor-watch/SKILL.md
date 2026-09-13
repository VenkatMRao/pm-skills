---
name: competitor-watch
description: Run a full competitor analysis using live web research, and diff it against the most recent saved analysis to surface what's actually changed. Use when the user asks to run or update a competitor analysis, check what's new with competitors, or wants an ongoing competitive tracking workflow — as opposed to a one-off synthesis of research they already have (see the competitive-analysis skill for that).
---

# Competitor Watch

A recurring competitor analysis: research each competitor fresh, save the
findings, and — on every run after the first — lead with what's changed since
the last saved snapshot instead of re-presenting a static landscape. The value
of running this repeatedly is the delta, not the snapshot.

## Before the first research call: a safety check

This workflow saves potentially sensitive competitive intelligence to local
files. Before writing anything, check whether the current working directory
looks like a public or shared repository (a public GitHub remote, or a repo
clearly meant to be shared externally — e.g. a portfolio repo). If it does,
**stop and tell the user**, and ask where they'd actually like this saved
instead, rather than silently committing real competitor research into a
public place.

## History storage convention

Use a `competitor-analysis/` directory at the root of the current project
(create it if the user confirms this is an appropriate place):

```
competitor-analysis/
  <competitor-slug>/
    2026-09-14.md       # one dated snapshot per run
    2026-08-01.md
  changelog.md           # running log: one entry per run, summarizing deltas
```

- Never edit or delete a past snapshot — every run adds a new dated file. The
  point of the history is an honest, auditable trail; overwriting it defeats
  that.
- `changelog.md` is a convenience index — a few lines per run ("2026-09-14:
  Competitor X dropped its free tier; Competitor Y shipped SSO") — so trends
  are skimmable without opening every dated file.

## Process

1. **Establish scope.** If `competitor-analysis/` already exists, read it to
   recover the competitor list, the dimensions previously tracked, and the
   most recent snapshot per competitor — don't make the user re-specify what's
   already on record. If it doesn't exist, this is a first run: ask which
   competitors to track and confirm the dimensions that matter (typically
   pricing, core feature set, positioning/messaging, and notable news —
   funding, leadership, launches — adjust to what the user says actually
   matters for their decisions).

2. **Research each competitor live.** Use web search/fetch against competitor
   sites (pricing pages, changelogs/release notes, product pages), recent news
   and press releases, and review sites where easily accessible. For every
   material claim, note the source URL and that it was checked today —
   competitive facts (pricing, features) go stale fast, and the source trail
   is what makes a later "did this actually change" check possible. If a
   dimension can't be found for a competitor, mark it "unknown," don't guess.

3. **Diff against the baseline**, if one exists, per competitor:
   - **Changed**: lead with this — what's different from the last snapshot,
     and cite both the old and new values (e.g. "Pricing: was $49/mo flat →
     now $39/mo + usage tiers").
   - **New**: anything that's appeared with no prior counterpart (a new
     product line, a new stated integration).
   - **Unchanged**: brief, not the focus — a short list is enough.
   - **Missing from current research**: something in the old snapshot that
     current research didn't turn up. Flag as "removed, or could not
     reverify" — absence of evidence from a web search isn't proof it's gone,
     say so rather than asserting a removal you didn't confirm.
   - On a first run (no baseline), skip this section and say explicitly that
     this snapshot is the new baseline for future comparisons.

4. **Write the full analysis**, structured for the decision it's meant to
   inform (ask what that is if unclear — a roadmap bet, a pricing call, a
   positioning pitch — same framing question as the `competitive-analysis`
   skill):
   - **What changed since last time** — first and most prominent section
     after a first run exists; this is the section repeat use is for.
   - **Comparison table** across the agreed dimensions, current values.
   - **Per-competitor notes** — 2-4 sentences: where they're clearly ahead,
     where they're weak, what that implies.
   - **Strategic implications** — concrete recommendations the delta
     supports, not a generic landscape recap.
   - **Sources** — every URL used, so claims are checkable.
   - **What we still don't know** — gaps in this run's research.

5. **Save the snapshot and update the changelog** — one new dated file per
   competitor with this run's full findings, plus a short changelog entry
   summarizing the deltas found.

## Guardrails

- Don't state something as fact when it's inference (competitor strategy,
  unannounced roadmap, financial health) — mark it as inference distinctly
  from sourced claims.
- Don't treat your own general knowledge as current — a competitor's pricing
  or feature set from training data can be outdated; prefer freshly fetched
  sources for anything the analysis will lean on, and say when something is
  from general knowledge rather than a live check.
- Don't force a recommendation the evidence doesn't support just to make the
  analysis feel conclusive — "no material change this cycle" is a legitimate,
  useful output.
- Keep snapshots append-only. If the user asks to "clean up" old snapshots,
  confirm explicitly before deleting anything — that history is the entire
  point of this skill over a one-off analysis.
