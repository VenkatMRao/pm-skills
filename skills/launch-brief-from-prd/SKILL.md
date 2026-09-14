---
name: launch-brief-from-prd
description: Turn a PRD's technical description into a marketing launch brief in benefit language — what it is, who it's for, why it matters, and explicitly what NOT to claim — so the PM edits a draft instead of writing one from scratch every launch. Use when the user asks for a launch brief, marketing brief, or a feature explainer for a campaign/content team.
---

# Launch Brief from PRD

Marketing needs benefit language; a PRD is written in requirements language.
Someone has to do that translation every launch — this skill drafts it so the
PM edits instead of starting blank. The part that matters most isn't the pitch,
though — it's being explicit about what's actually shipping now versus what's
still on the roadmap, since that boundary is exactly where launch messaging
tends to overclaim.

## Process

1. **Identify what's actually shipping in this launch**, not the full PRD
   vision. If the PRD describes multiple phases or a v1/v2 split, draft the
   brief only for what's shipping now — ask which phase if it's ambiguous.
   Conflating the eventual vision with what's actually available is the most
   common way a launch brief turns into an overclaim.

2. **Pull the launch-relevant facts**: what it does, who it's for (the
   segment/use case, not "everyone"), availability (plan tier, rollout
   percentage, region, beta vs. GA), and any stated limitations or explicit
   non-goals from the PRD.

3. **Translate capability into benefit language**, but don't invent a benefit
   the PRD doesn't support. A requirement like "supports batch export up to
   10,000 rows" becomes a benefit like "export your full customer list in one
   pass instead of paging through it" — grounded in what the PRD actually
   says, not embellished into a bigger claim.

4. **Flag every claim that needs real data to back it up** (a speed
   improvement, a percentage, a comparison to the old way of doing it)
   instead of inventing a plausible-sounding number. Mark it
   `[NEEDS DATA: <what's needed>]` so the PM knows exactly what to supply
   before this goes to marketing.

5. **Write a "What NOT to claim" section explicitly** — this is the section
   most launch briefs skip, and the one that prevents the overclaim problem
   before it happens:
   - Anything in the PRD marked as a known limitation, edge case, or
     explicit non-goal.
   - Anything that's true of the roadmap vision but not of what's shipping
     now (the gap identified in step 1).
   - Any claim that would need data to support (from step 4) that hasn't
     been supplied yet — don't let marketing accidentally state it as fact.

6. **Draft the brief**:
   ```
   Launch Brief (DRAFT — for PM review before sharing with marketing)

   Feature: <canonical name — check terminology-consistency-check's map if
   one exists, so this matches what the product/docs actually call it>

   One-line pitch: <benefit-oriented, not a feature description>

   Who it's for: <segment/use case>

   The problem today: <customer-facing framing of the pain point>

   What's new: <2-4 key benefits, each grounded in a specific PRD-stated
   capability>

   How it works: <brief, non-technical>

   Availability: <plan tier, rollout %, region, beta/GA — exactly what's
   true at launch, not the eventual full rollout>

   What NOT to claim: <explicit list, per step 5>

   Needs before this is publish-ready: <data points flagged in step 4,
   anything still pending PM confirmation>
   ```

7. **Note the natural follow-up**: close to actual launch, re-check this
   brief against `release-notes-draft` (or `pr-behavior-change-scan` on the
   relevant PRs) to confirm what's really shipping still matches what this
   brief describes — scope has a way of narrowing between when a brief gets
   written and when a feature actually ships.

## Guardrails

- Never invent a benefit, statistic, or comparison the PRD doesn't actually
  support — flag it as needing data instead.
- Never present the full roadmap vision as what's shipping now — draft only
  the phase that's actually launching.
- Always include the "What NOT to claim" section, even when it feels like
  there's nothing to put there — if that's genuinely true, say so explicitly
  rather than omitting the section.
- This is a draft for the PM to review and correct, not publish-ready copy —
  mark it as such.
