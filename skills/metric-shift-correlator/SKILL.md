---
name: metric-shift-correlator
description: When a metric suddenly moves, correlate the timing against deploy/PR history (and other likely causes) to produce a first-pass hypothesis list, instead of an informal "did anything ship recently?" in Slack. Use when the user asks why a metric moved, wants to investigate a spike/drop, or needs candidate causes before looping in an engineer.
---

# Metric Shift Correlator

Produces hypotheses to verify, not a diagnosis. Correlation-in-time with a
deploy is a lead worth checking, not proof of causation — this skill's job is
to narrow down what an engineer should check first, not to declare a PR guilty.

## Inputs needed

- **The metric shift**: what moved, the direction/magnitude, and the time
  window it happened in. If the user gives a full timeseries instead of a
  window, do a rough before/after comparison to locate the likely inflection
  point — but if it's ambiguous, confirm the window with the user rather than
  silently picking one. Everything else in this investigation anchors on this
  window, so it's worth getting right before proceeding.
  - If the metric lives in a database/warehouse, use `nl-data-query` /
    `database-chat-insights` to pull the daily/hourly series for the relevant
    range rather than asking the user to export it by hand.
- **Which systems plausibly touch this metric** — ask which repo(s)/services
  are relevant if not obvious (a conversion metric probably touches checkout
  and pricing services, not the internal admin tool).

## Process

1. **Widen the window slightly** beyond the exact inflection point in both
   directions — a change that landed a day or two before the metric moved is
   still a candidate (delayed effects, gradual rollouts), and looking a bit
   past the shift helps confirm whether the metric held at its new level or
   was a blip.

2. **Pull deploy/PR history for the window**, per relevant repo:
   `gh pr list --state merged --search "merged:<start>..<end>"`, then look at
   title, description, and changed files for each. Rank candidates by:
   - **Timing proximity** to the inflection point.
   - **Plausible mechanism** — do the files/areas touched actually relate to
     the metric (e.g. checkout-flow files for a conversion metric), not just
     "something merged that day."
   - **Whether the PR description itself hints at relevance** (mentions the
     feature area, a config default, a threshold).

3. **Explicitly check for non-deploy causes** — these don't show up in git
   history at all, and skipping them is the most common way this kind of
   investigation goes wrong:
   - **Feature flags** toggled without a deploy — ask whether flag changes
     are tracked anywhere and, if so, check that log too.
   - **Marketing/pricing/campaign changes** — a traffic or conversion shift
     with no code change behind it often traces here instead.
   - **Seasonality** — day-of-week, holiday, or recurring cyclical pattern
     that would explain the move without any change at all.
   - **Third-party dependency issues** — an outage or behavior change in a
     payment processor, CDN, or other external service.
   - **Instrumentation/tracking changes** — the metric's *measurement*
     changed (an analytics tagging update, a query definition change), not
     the underlying user behavior. This is worth checking early — it's a
     common false alarm.

4. **Write the hypothesis list, ranked, each with:**
   - What changed and when, relative to the inflection point.
   - Why it's plausible (the mechanism — how this could move this specific
     metric, not just "it's close in time").
   - A concrete way to verify it (e.g. "check whether the metric reverted
     when this flag was rolled back," "confirm with [PR author] whether this
     touches the affected flow," "check if the timing lines up to the hour,
     not just the day").

5. **If nothing correlates well, say so plainly.** Don't stretch a weak
   candidate to look like an answer. Suggest next steps instead: widen the
   window further, check systems not yet considered, or hand this to an
   engineer for a deeper investigation this scan can't do (log diving,
   infrastructure metrics, A/B test allocation changes).

## Guardrails

- Never state a PR "caused" the shift — frame every finding as correlated in
  time and mechanistically plausible, pending confirmation by whoever owns
  that system.
- Never frame a finding around blaming an engineer — keep it about the
  change, not the person who made it.
- Don't skip non-code causes just because deploy history is the easiest data
  to pull — they're often the actual answer.
- Confirm the shift window with the user before investing effort in
  correlating against it.
- If the scan turns up nothing convincing, report that clearly rather than
  presenting a weak correlation as a likely cause.
