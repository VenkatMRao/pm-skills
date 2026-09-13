---
name: terminology-consistency-check
description: Scan product UI text, docs, and marketing content for the same feature or concept being named differently in different places, and produce a canonical terminology map with every inconsistency traced back to its source. Use when the user asks to check terminology/naming consistency, or audit how a feature is referred to across product, docs, help center, and marketing.
---

# Terminology Consistency Check

Find the cases where a feature is called one thing in the product, another in
docs, and a third in marketing — the kind of drift a PM normally only catches by
memory or luck. This is a single full-corpus scan, not a recurring diff: unlike
`competitor-watch` or `backlog-hygiene-audit`, there's no baseline to maintain —
each run just re-scans whatever sources are given.

## Gather sources and confirm scope first

Ask for the sources if not already given — local files/folders (docs,
copy decks, PRDs), URLs (marketing pages, help center, in-app string exports),
or pasted text. Confirm the scope explicitly (e.g. "these 6 pages" vs. "the
whole docs site") before fetching anything — don't crawl an open-ended set of
pages without the user having confirmed that's what they want.

## Process

1. **Extract candidate terms per source.** Look for feature/product-area names:
   capitalized or quoted phrases that name a specific capability, not generic
   English words. Note the exact source and location (file path + line, URL +
   section/heading, or quoted sentence) for every candidate — this traceability
   is what makes the final report actionable rather than just a vague claim.

2. **Cluster candidates into concepts using context, not just string
   matching.** Two differently worded phrases count as the same concept only
   when the surrounding context (what it does, how it's described, adjacent
   screenshots/examples) makes that reasonably clear — not just because the
   words sound similar. When the evidence is suggestive but not solid, report
   it as "possibly the same feature — verify" rather than asserting a merge.
   Equally, don't force two genuinely different features together just because
   this task is looking for matches.

3. **Determine a canonical name per cluster.** Default to whatever the product
   UI itself calls it (that's what the user directly experiences) when UI text
   is among the sources. If UI text isn't available in what was given, present
   the candidate names and ask the user which should be canonical instead of
   guessing — inventing a "correct" name the team hasn't actually agreed on
   isn't this skill's call to make.

4. **Classify severity:**
   - **Customer-facing mismatch** — the same concept is named differently
     across surfaces a single customer could plausibly see in one session
     (e.g. marketing site vs. in-product UI, or in-product UI vs. help
     center). Highest priority — this is what a confused support ticket looks
     like from the outside.
   - **Same-source inconsistency** — one document or page uses two different
     names for the same thing internally. Flag distinctly and treat as
     high-severity even though it's a single source — it signals the
     underlying confusion is deep enough that even one writer didn't stay
     consistent.
   - **Internal-only mismatch** — inconsistency confined to internal docs
     (PRDs, wikis) that customers never see. Still worth fixing, lower
     priority.

5. **Report:**
   - A short section up front listing only customer-facing mismatches and
     same-source inconsistencies — the ones worth acting on first.
   - A full table below: concept, proposed canonical name, variants found
     (with exact source/location for each), severity.
   - A separate list of "possibly the same feature — verify" clusters that
     didn't meet the bar for a confident merge, so the user can resolve the
     ambiguous ones by hand.

6. **Offer, don't act.** Don't edit the source docs to fix the inconsistencies
   unless the user explicitly asks for that as a follow-up — this skill's job
   is to produce the map and the flagged list, not to unilaterally rewrite
   marketing or docs content.

## Guardrails

- Never merge two terms into one concept without real contextual evidence;
  when unsure, report it as unverified rather than as a confirmed finding.
- Never invent a canonical name the team hasn't actually settled on — prefer
  the in-product UI label, or ask.
- Every flagged inconsistency needs an exact, checkable source location — no
  "the docs are inconsistent" without pointing to where.
- Don't fetch or scan beyond the scope the user confirmed.
