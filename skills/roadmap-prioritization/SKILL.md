---
name: roadmap-prioritization
description: Score and prioritize a backlog of initiatives using a RICE or ICE framework, and write the narrative a roadmap review needs. Use when the user asks to prioritize, rank, or sequence a backlog, or to prep a roadmap review.
---

# Roadmap Prioritization

Turn a backlog into a defensible, sequenced roadmap — the scoring is the easy part;
the narrative explaining *why* the ranking is what it is, and what got explicitly
deprioritized, is what actually survives a roadmap review.

If some initiatives originate from sales call feedback, `sales-call-signal-mining`'s
output (themes already carrying frequency and revenue-exposure data) maps
naturally onto Reach/Impact inputs here — use it as a starting estimate rather
than re-deriving those numbers from scratch.

## Process

1. **Get the backlog and the framework.** Take whatever list of initiatives the
   user provides. Confirm the scoring framework:
   - **RICE** (Reach × Impact × Confidence / Effort) when reach and effort are
     reasonably estimable.
   - **ICE** (Impact × Confidence × Ease) for a faster, rougher pass or when reach
     data doesn't exist yet.
   Default to RICE if the user doesn't specify and the inputs support it.

2. **Score each initiative**, showing the inputs, not just the final number:
   - State the estimate for each factor (e.g. Reach: 2,000 users/quarter) and a
     one-line justification. Don't silently invent numbers that weren't provided or
     inferable — mark unestimated factors as "Unknown" and flag them rather than
     defaulting to a made-up middle value.
   - Compute the score and sort descending.

3. **Sanity-check the raw ranking before presenting it.** A pure score sort can
   produce a bad sequence — e.g. two initiatives that share a dependency but land
   far apart, or a low-scoring item that unblocks several higher ones. Call out
   adjustments and *why* you're making them; don't silently reorder.

4. **Write the roadmap narrative:**
   - **Now / Next / Later** grouping (not just a flat ranked list — a roadmap
     review needs a sequencing story).
   - **Table**: initiative, score, key inputs, one-line rationale.
   - **What's explicitly deprioritized and why** — this is the section stakeholders
     push back on most; give it a real answer per item, not "lower priority."
   - **Confidence and risk flags** — which rankings are solid vs. based on thin
     data, and what would change the ranking if it came in.

## Guardrails

- Don't force a precise score onto an initiative with no usable data — say so, and
  either propose how to get the data or rank it qualitatively with a clear caveat.
- Keep the scoring inputs visible in the output. A ranked list with no visible math
  is not defensible in a review; the moment someone asks "why is X above Y," the
  inputs need to already be on the page.
