---
name: ux-pattern-consistency-audit
description: Audit interaction and visual patterns (confirmation flows, error/empty/loading states, button placement, formatting) across a set of screens for inconsistency — how the product handles the same kind of situation differently in different places. Use when the user asks to audit UX/design pattern consistency, or find where similar interactions are handled differently across the product. For naming/terminology drift specifically, use terminology-consistency-check instead.
---

# UX Pattern Consistency Audit

Finds places where the product handles the same *kind* of situation
differently — one screen confirms a delete with a modal, another deletes
instantly on click; one form shows errors inline, another only in a toast. This
is a visual/interaction check, not a naming check — for the same feature being
*called* different things in different places, use `terminology-consistency-check`
instead; the two pair well together but look at different failure modes.

## Gather sources and confirm scope first

Ask for the screens to audit if not given — screenshots (image files, which can
be read directly), Figma frame exports, or a live app to capture via browser
automation if that's available in the environment. Also ask whether a
documented design system or pattern library exists — if it does, it's the
canonical reference to audit *against*, not just another data point. Confirm
scope (which flows/screens) before starting; don't try to audit an entire
product unbounded in one pass.

## Pattern categories to check

Use these as a starting checklist, not an exhaustive requirement — adjust to
what's actually relevant to the screens given:

- **Destructive-action confirmation** — modal vs. inline vs. none, for
  delete/remove/cancel-type actions.
- **Error display** — inline field errors vs. toast vs. banner, and whether
  the tone/specificity of error copy is consistent.
- **Empty states** — illustration + CTA vs. plain text vs. nothing.
- **Loading states** — spinner vs. skeleton vs. progress bar, and whether the
  choice correlates with load duration consistently.
- **Navigation conventions** — back button placement, breadcrumb use,
  modal close-button position.
- **Action hierarchy** — primary/secondary button placement and ordering
  (e.g. is "Cancel" always on the same side relative to the primary action?).
- **Formatting** — dates, times, numbers, currency — same format everywhere?

## Process

1. **Record how each screen implements each relevant pattern**, with the
   exact source (file/frame name, or a description specific enough to
   relocate it). Don't summarize before you've actually looked at each
   screen — a pattern audit built from assumption defeats the point.

2. **Compare across screens** (and against the documented design system, if
   one was given) to find where the same kind of situation is handled
   differently. For each inconsistency found, capture: which screens/sources
   are involved, exactly how each one differs, and — when a design system
   exists — which one (if any) matches the documented standard.

3. **Don't flag intentional differentiation as inconsistency.** Two screens
   can reasonably use different patterns because their contexts genuinely
   differ (a full-page confirmation for account deletion vs. a lightweight
   inline undo for removing one list item). When a difference could plausibly
   be intentional, report it as "possibly intentional — verify" rather than a
   flat inconsistency, and say what context difference might justify it.

4. **Classify severity:**
   - **High** — the inconsistency touches safety or trust: a destructive
     action confirmed in some places and not others, an error state that
     doesn't clearly communicate what happened in some places but does in
     others. This is where real user harm (accidental data loss, confusion
     during a failure) can happen.
   - **Medium** — affects perceived polish/coherence but not safety: button
     placement, spacing/layout drift, inconsistent loading indicators.
   - **Low** — minor stylistic variation, plausibly intentional or low-stakes.

5. **Recommend a standard, don't invent one.** If a documented design system
   exists, recommend aligning to it. If not, recommend the pattern already
   used most often across the audited screens, labeled explicitly as "most
   common current pattern, no documented standard" rather than presented as
   an established rule — and say clearly when there's no clear majority and
   this is a decision the team still needs to make.

6. **Report, high severity first:**
   - A short section up front with only High-severity findings.
   - A full table below: pattern category, screens involved, what differs,
     severity, recommendation, whether a design-system standard exists.
   - A separate "possibly intentional — verify" list for the ambiguous cases.

7. **Offer, don't act.** This produces findings and recommendations, not
   design changes — don't edit screens/specs or declare a new standard
   unilaterally; that's a call for the design team and the user to make.

## Guardrails

- Never flag a difference as inconsistent without checking whether the
  contexts genuinely differ enough to justify it.
- Never invent a "correct" pattern when no design system exists — recommend
  the most common current pattern, labeled as such, or say it's undecided.
- Every finding needs a traceable source (which screens/frames), not a vague
  "some screens do X."
- Stay in scope: interaction/visual patterns, not naming/terminology — hand
  naming drift to `terminology-consistency-check`.
