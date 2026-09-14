---
name: sales-call-signal-mining
description: Mine sales call transcripts/notes across many deals for recurring product signal — objections, feature gaps, competitor comparisons, what's working — weighted by deal size and outcome, not just frequency. Use when the user asks to synthesize sales call feedback, find patterns in win/loss reasons, or mine sales calls for product signal.
---

# Sales Call Signal Mining

Sales call feedback usually evaporates into individual reps' memory or scattered
CRM notes. This skill mines it systematically and weights findings by what
actually matters for a roadmap decision — how often something comes up *and*
how much revenue is behind it *and* whether it's actually correlated with deals
being lost — not just which complaint was loudest or most recent.

## Inputs needed

Gather call transcripts, call summaries, or CRM notes across the set of deals
in scope. For each, get as much of this metadata as exists — and be explicit
about what's missing rather than guessing:
- **Account name**, **deal size/ARR**, **stage**, **outcome** (won/lost/open),
  **competitor(s) involved** if any, **rep**.
- Calls missing this metadata can still contribute to frequency signal, but
  say so — they can't contribute to revenue-weighting or won/lost analysis.

## Process

1. **Extract candidate product signal per call**: objections, explicit
   feature gaps raised as blocking, competitor comparisons, praised strengths,
   pricing/packaging friction. Quote directly when the source is a verbatim
   transcript. When the source is a rep's summary rather than a transcript,
   **mark it as the rep's interpretation, not the customer's own words** —
   that distinction matters for how much weight the claim deserves later.

2. **Cluster by underlying theme, not exact wording.** Different reps
   describe the same gap differently. Merge two mentions into one theme only
   when there's real contextual evidence they're the same underlying issue;
   when unsure, report it as "possibly related — verify" rather than forcing
   a merge, the same discipline as `terminology-consistency-check`.

3. **Weight each theme, don't just count it:**
   - **Frequency** — how many distinct deals/reps raised it.
   - **Revenue exposure** — the size/range of deals behind the mentions, not
     just a count.
   - **Won/lost mix** — a theme concentrated in *lost* deals is a stronger
     signal of an actual blocker than one that shows up across both won and
     lost deals, which more likely reflects positioning than a hard gap.

4. **Apply real skepticism to stated loss reasons.** A rep's or a customer's
   stated reason for losing a deal can be a convenient story rather than the
   full truth — "we lost because of missing feature X" is an easier
   explanation than "the discovery process was weak" or "we lost on price."
   Treat a claimed reason as a strong, actionable signal only when it's
   **corroborated across multiple independent deals and reps** — a single
   deal's stated reason is one data point, not a proven cause, and should be
   reported as lower-confidence.

5. **Keep large, one-off asks distinct from recurring themes.** A single huge
   deal's very specific request is worth surfacing, but it isn't the same
   kind of finding as a pattern repeated across many independent deals — label
   it "large-deal-specific ask" rather than blending it into the weighted
   theme ranking, where it would either get overweighted by deal size alone
   or lost among smaller recurring themes.

6. **Report, ranked by weighted significance:**
   - Theme, description, frequency, revenue exposure, won/lost mix,
     confidence (corroborated vs. single-source), and supporting
     quotes/call references (account name, deal size, outcome) for
     traceability.
   - A separate "possibly related — verify" list for weak clusters.
   - A separate "large-deal-specific asks" list, kept out of the main
     ranking.

7. **Note good next steps for the output**: this is well-suited as direct
   input to `roadmap-prioritization` (it already carries frequency and
   revenue-exposure data close to Reach/Impact inputs), and if a theme
   centers on losing to a specific competitor's specific feature, that's
   worth cross-checking against `competitor-watch`'s latest snapshot for that
   competitor.

## Guardrails

- Never present a rep's paraphrase as a direct customer quote — keep the two
  distinguishable.
- Never treat a single deal's stated loss reason as a proven product gap —
  corroboration across independent sources is what elevates a claim from
  anecdote to signal.
- Never merge distinct asks into one theme without real contextual evidence.
- Never let deal size alone override judgment — a large deal's specific ask
  gets surfaced distinctly, not folded into the general ranking as if it were
  a recurring pattern.
- Never fabricate deal metadata that wasn't provided — mark it unknown and
  reflect that in reduced confidence rather than guessing a plausible value.
