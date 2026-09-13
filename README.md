# PM Skills — an AI-augmented Product Management toolkit

I'm a Product Manager who builds and uses AI tools as part of my actual day-to-day
workflow — not as a side experiment. This repo is where that work lives: the
[Claude Code](https://claude.com/claude-code) skills, prompt templates, and small
scripts I reach for to move faster on the recurring, high-friction parts of the job
(synthesizing research, writing specs, prioritizing backlogs, reporting on sprints).

It's public for two reasons:

1. **It's genuinely useful to me.** Every skill and script here solves a problem I
   actually had, and I keep it here so I can pull it into any project.
2. **It's a work sample.** If you're a hiring manager or teammate trying to gauge
   how I think about applying AI to PM work, this repo is a more honest signal than
   a resume bullet — you can read the prompts, run the scripts, and see the
   before/after in the case studies.

> **A note on the content:** the case studies describe real workflows I've used,
> with company-specific details generalized or anonymized. The skills and prompts
> are written to be reusable out of the box — swap in your own product/company
> context where you see `[bracketed placeholders]`.

## What's inside

| Folder | What it is | Use it when |
|---|---|---|
| [`skills/`](skills/) | [Claude Code](https://claude.com/claude-code) skills (`SKILL.md`) — packaged, repeatable workflows Claude follows step by step | You're working inside Claude Code and want a consistent process, not a one-off prompt |
| [`prompts/`](prompts/) | Standalone prompt templates for any chat-based LLM (Claude.ai, ChatGPT, etc.) | You just need a good prompt, not a full tool |
| [`scripts/`](scripts/) | Small, runnable automations (Python) that combine data wrangling with LLM calls | The task is repetitive enough to script, or needs to run outside a chat window |
| [`case-studies/`](case-studies/) | Short write-ups of a real problem, the AI-assisted approach, and the measured outcome | You want the "so what" — evidence these tools actually changed an outcome |

## Highlights

- **[`skills/prd-writer`](skills/prd-writer/SKILL.md)** — turns a rough feature idea
  into a structured PRD by asking the questions a PM should ask before writing one,
  not after.
- **[`skills/roadmap-prioritization`](skills/roadmap-prioritization/SKILL.md)** —
  scores a backlog against a scoring framework (RICE/ICE) and produces the
  narrative a roadmap review actually needs, not just a spreadsheet.
- **[`scripts/verbatim-tagger`](scripts/verbatim-tagger/README.md)** — calls the
  Claude API to theme-tag and sentiment-score hundreds of open-text survey
  responses in minutes instead of a day of manual coding.
- **[`scripts/nl-data-query`](scripts/nl-data-query/README.md)** +
  **[`skills/database-chat-insights`](skills/database-chat-insights/SKILL.md)** —
  ask a database or warehouse a question in plain language and get a
  plain-language insight back, with read-only SQL enforcement and a mandatory
  human confirmation step before any query runs.
- **[`skills/release-notes-draft`](skills/release-notes-draft/SKILL.md)** —
  point it at one or more GitHub PR URLs and get back a release note draft: a
  UAT/SME section (what changed, what to test, known limitations) and a
  customer-facing section, both traceable back to source PRs/issues.
- **[`skills/competitor-watch`](skills/competitor-watch/SKILL.md)** — a
  recurring competitor analysis that researches live each run and saves a
  dated snapshot, so every run after the first leads with what's actually
  *changed* rather than re-presenting a static landscape.
- **[`case-studies/research-synthesis-with-claude.md`](case-studies/research-synthesis-with-claude.md)**
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

Product Manager focused on [your domain/industry]. I use AI tooling to spend less
time on synthesis and reporting mechanics, and more time on judgment calls that
actually need a human. Reach me at `[your email]` / `[your LinkedIn]`.
