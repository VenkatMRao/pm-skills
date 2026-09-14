# Skills

[Claude Code](https://claude.com/claude-code) skills — each folder is a
self-contained `SKILL.md` with frontmatter (`name`, `description`) and the process
Claude follows. Drop any folder into `.claude/skills/` (project) or
`~/.claude/skills/` (global) to use it.

| Skill | Use it for |
|---|---|
| [`prd-writer`](prd-writer/SKILL.md) | Drafting a PRD from a rough idea, with the scoping questions asked up front |
| [`competitive-analysis`](competitive-analysis/SKILL.md) | Turning competitor research *you already have* into a comparison with an actual recommendation (one-off, no research or history) |
| [`competitor-watch`](competitor-watch/SKILL.md) | Full competitor analysis with live web research, saved as a dated snapshot each run so it can lead with what's *changed* since last time |
| [`backlog-hygiene-audit`](backlog-hygiene-audit/SKILL.md) | Flagging tickets with vague/missing acceptance criteria, and catching scope drift by diffing current ticket state against its approval baseline |
| [`terminology-consistency-check`](terminology-consistency-check/SKILL.md) | Finding a feature named differently across product, docs, help center, and marketing, traced back to source |
| [`flow-outline-from-prd`](flow-outline-from-prd/SKILL.md) | Turning PRD prose into a step-by-step flow outline with explicit decision branches, ready for a designer to storyboard from |
| [`ux-pattern-consistency-audit`](ux-pattern-consistency-audit/SKILL.md) | Finding where the same kind of situation (confirmations, errors, empty/loading states) is handled differently across screens |
| [`roadmap-prioritization`](roadmap-prioritization/SKILL.md) | Scoring a backlog (RICE/ICE) and writing the sequencing narrative for a roadmap review |
| [`database-chat-insights`](database-chat-insights/SKILL.md) | Answering a plain-language question against a database/warehouse — read-only, with mandatory confirmation before any query runs |
| [`release-notes-draft`](release-notes-draft/SKILL.md) | Drafting release notes from GitHub PR URLs — a UAT/SME section plus a customer-facing section, ready for your review before going anywhere |
| [`pr-behavior-change-scan`](pr-behavior-change-scan/SKILL.md) | Pre-merge check: scans a PR's diff for user-facing behavior changes the description/ticket doesn't mention |
| [`metric-shift-correlator`](metric-shift-correlator/SKILL.md) | When a metric moves, correlates the timing against deploy history and other likely causes into a ranked hypothesis list |
| [`stale-doc-audit`](stale-doc-audit/SKILL.md) | Flags PRDs/specs whose claims (blockers, metrics, target dates) no longer match current reality, verified against live sources rather than just last-edited date |
| [`weekly-summary`](weekly-summary/SKILL.md) | A weekly update in non-technical language: what got done (from tickets), what was decided, current risks/blockers, and how it moves the product's OKRs |
| [`sales-call-signal-mining`](sales-call-signal-mining/SKILL.md) | Mines sales call transcripts/notes across deals for recurring product signal, weighted by deal size and won/lost outcome, not just frequency |
| [`launch-brief-from-prd`](launch-brief-from-prd/SKILL.md) | Turns a PRD into a marketing launch brief in benefit language, with an explicit "what NOT to claim" section to prevent overclaiming |
