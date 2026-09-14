# PM Skills — an AI-augmented Product Management toolkit

I'm a Senior Product Manager who builds and uses AI tools as part of my actual day-to-day workflow. This repo is where that work lives: the Claude Code skills, prompt templates, and small
scripts I reach for to move faster on the recurring, high-friction parts of the job
(synthesizing research, writing specs, prioritizing backlogs, reporting on sprints).

It's public because **It's genuinely useful to me.** Every skill and script here solves a problem I actually had, and I will be delighted if my fellow PMs can get some value out of this.

> **A note on the content:** the skills, prompts, scripts & case studies describe real workflows I've used, with company-specific details generalized or anonymized to be reusable out of the box — swap in your own product/company context where you see `[bracketed placeholders]`.



## What's inside


| Folder                           | What it is                                                                                   | Use it when                                                                           |
| -------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [skills/](skills/)             | Claude Code skills (`SKILL.md`) — packaged, repeatable workflows Claude follows step by step | You're working inside Claude Code and want a consistent process, not a one-off prompt |
| [prompts/](prompts/)           | Standalone prompt templates for any chat-based LLM (Claude.ai, ChatGPT, etc.)                | You just need a good prompt, not a full tool                                          |
| [scripts/](scripts/)           | Small, runnable automations (Python) that combine data wrangling with LLM calls              | The task is repetitive enough to script, or needs to run outside a chat window        |
| [case-studies/](case-studies/) | Short write-ups of a real problem, the AI-assisted approach, and the measured outcome        | You want the "so what" — evidence these tools actually changed an outcome             |




## Highlights

- [skills/prd-writer](skills/prd-writer/SKILL.md) — turns a rough feature idea into a structured PRD by asking the questions a PM should ask before writing one, not after.
- [skills/roadmap-prioritization](skills/roadmap-prioritization/SKILL.md) - scores a backlog against a scoring framework (RICE/ICE) and produces the narrative a roadmap review actually needs, not just a spreadsheet.
- [scripts/verbatim-tagger](scripts/verbatim-tagger/README.md) - calls the Claude API to theme-tag and sentiment-score hundreds of open-text survey responses in minutes instead of a day of manual coding.
- [scripts/nl-data-query](scripts/nl-data-query/README.md) +
[skills/database-chat-insights](skills/database-chat-insights/SKILL.md) - ask a database or warehouse a question in plain language and get a plain-language insight back, with read-only SQL enforcement and a mandatory human confirmation step before any query runs.
- [skills/release-notes-draft](skills/release-notes-draft/SKILL.md) —
point it at one or more GitHub PR URLs and get back a release note draft: a
UAT/SME section (what changed, what to test, known limitations) and a
customer-facing section, both traceable back to source PRs/issues.
- [skills/pr-behavior-change-scan](skills/pr-behavior-change-scan/SKILL.md)
— a pre-merge check that reads a PR's diff for user-facing behavior changes
the description/ticket never mentions, so they get confirmed before they
ship as a surprise instead of after.
- [skills/metric-shift-correlator](skills/metric-shift-correlator/SKILL.md)
— when a metric suddenly moves, correlates the timing against deploy
history and other likely causes (flags, seasonality, instrumentation
changes) into a ranked hypothesis list — replacing the informal "did
anything ship recently?" Slack message.
- [skills/stale-doc-audit](skills/stale-doc-audit/SKILL.md) — flags
PRDs/specs whose claims (cited blockers, stated metrics, target dates) no
longer match current reality, verified against live sources rather than
just how old the doc looks.
- [skills/weekly-summary](skills/weekly-summary/SKILL.md) — a weekly
update in non-technical language: what got done (from tickets, grouped by
theme not ticket ID), what was decided, current risks/blockers, and how the
week's work connects to the product's OKRs — including honestly flagging
work with no clear OKR link.
- [skills/sales-call-signal-mining](skills/sales-call-signal-mining/SKILL.md)
— mines sales call transcripts/notes across deals for recurring product
signal, weighted by deal size and won/lost outcome rather than just
frequency, with real skepticism applied to stated loss reasons that aren't
corroborated across independent deals.
- [skills/launch-brief-from-prd](skills/launch-brief-from-prd/SKILL.md)
— turns a PRD into a marketing launch brief in benefit language, drafting
only the phase that's actually shipping (not the full roadmap vision) and
including an explicit "what NOT to claim" section so overclaiming gets
caught before it reaches marketing, not after.
- [skills/competitor-watch](skills/competitor-watch/SKILL.md) — a
recurring competitor analysis that researches live each run and saves a
dated snapshot, so every run after the first leads with what's actually
*changed* rather than re-presenting a static landscape.
- [skills/backlog-hygiene-audit](skills/backlog-hygiene-audit/SKILL.md) —
flags tickets with vague/untestable acceptance criteria, and catches scope
creep by diffing a ticket's current state against a saved snapshot of what
was actually approved.
- [skills/terminology-consistency-check](skills/terminology-consistency-check/SKILL.md)
— scans product UI, docs, help center, and marketing content for the same
feature named differently in different places, with every inconsistency
traced back to its exact source.
- [skills/flow-outline-from-prd](skills/flow-outline-from-prd/SKILL.md)
— turns PRD prose into a step-by-step flow outline with explicit decision
branches (plus a Mermaid diagram), so a designer can storyboard directly
instead of reverse-engineering the flow from paragraphs — and flags every
branch the PRD sets up but never resolves.
- [skills/ux-pattern-consistency-audit](skills/ux-pattern-consistency-audit/SKILL.md)
— audits interaction/visual patterns (confirmations, error/empty/loading
states, button placement) across a set of screens for the same kind of
situation being handled differently in different places.
- [case-studies/research-synthesis-with-claude.md](case-studies/research-synthesis-with-claude.md)
— how a synthesis workflow cut a multi-day research write-up down to an
afternoon, with the before/after.



## How I use this repo day to day

Most of what's here gets used in one of three ways:

1. **Inside Claude Code**, as a skill — I say what I need ("write a PRD for X") and
  Claude follows the packaged process in `skills/`.
2. **Pasted into a chat**, as a prompt — for quicker, lower-stakes tasks where I
  don't need the full skill scaffolding, I use a template from `prompts/`.
3. **Run from the terminal**, as a script — for anything that touches a CSV export
  or needs to run outside a chat window, e.g. `scripts/sprint-report`.



## Using the skills in your own Claude Code setup

Copy any folder under `skills/` into your project's `.claude/skills/` directory (or
your global `~/.claude/skills/`), and Claude Code will pick it up automatically.
Each `SKILL.md` is self-contained — frontmatter (`name`, `description`) plus the
instructions Claude follows.

## Structure

```
pm-skills/
├── skills/            Claude Code skills (SKILL.md)
├── prompts/           Tool-agnostic prompt templates
├── scripts/           Runnable Python automations
└── case-studies/      Problem → approach → measured outcome
```



## About me

Senior Product Manager focused on spending less time on day-today tasks like synthesis and reporting mechanics, and more time on customer interactions and judgment calls that actually need a human.
