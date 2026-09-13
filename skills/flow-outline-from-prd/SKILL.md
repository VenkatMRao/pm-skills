---
name: flow-outline-from-prd
description: Turn a PRD's prose into a structured step-by-step flow outline with explicit decision branches, ready for a designer to storyboard from directly. Use when the user asks to turn a PRD/spec into a user flow, flow diagram, or storyboard outline.
---

# Flow Outline from PRD

A PRD describes a flow in prose; a designer has to mentally reconstruct the
actual sequence and branch points before they can start sketching. This skill
does that reconstruction explicitly, and — just as importantly — surfaces every
branch the PRD implies but never actually resolves, instead of quietly picking a
plausible behavior and moving on.

## Process

1. **Identify every distinct flow in the PRD.** A PRD covering multiple entry
   points or user types (new vs. returning user, admin vs. member, first-run vs.
   steady-state) usually contains multiple genuinely different journeys. Don't
   flatten them into one linear sequence for simplicity — output each as its
   own flow, and note where one flow leads into another if the PRD implies
   that.

2. **For each flow, extract:**
   - **Entry point** — the trigger or starting screen/state.
   - **Steps** — the ordered sequence of user actions and system responses.
   - **Decision points** — anywhere the PRD implies a branch: an explicit
     condition, a user choice, a validation outcome, or language like "for
     users who already have X" or "assuming Y" that implies a fork even
     without an explicit if/then. Make every implied branch explicit rather
     than leaving it buried in a conditional clause of prose.
   - **Exit points** — every terminal state: success, abandonment, error.

3. **Flag unspecified branches instead of inventing behavior for them.** This
   is the single most valuable output of this skill: when the PRD sets up a
   decision point but doesn't say what happens on one side of it (what a
   validation failure shows, what a returning user sees differently), mark it
   explicitly — `Not specified in PRD — needs a decision` — rather than
   filling in a plausible-sounding guess. A designer working from a guess
   they don't know is a guess is worse off than one working from a flagged
   gap.

4. **Write each flow in a consistent step format:**

   ```
   Flow: <name>
   Entry: <trigger / starting point>

   1. <Step — user action or system response>
      Branch: if <condition> → 3a; else → 2
   2. <Step>
   3. <Step>
      3a. <alternate path> — <where it leads, or an exit>
   4. ...

   Exit states: <success>, <other terminal states>

   Open questions: <every branch or state the PRD didn't specify>
   ```

   Keep steps at the level of what a user sees and does, and how the system
   visibly responds — not implementation detail ("system validates the
   email format," not "backend regex check against the users table").

5. **Offer a diagram version alongside the text outline.** Generate a Mermaid
   `flowchart TD` for each flow directly from the step outline (so the two stay
   in sync — derive the diagram from the outline, don't re-derive it from the
   PRD independently). The text outline is the canonical, detailed version;
   the diagram is a fast-scan companion a designer can glance at before
   reading the detail. If the environment doesn't render Mermaid, include it
   anyway as a code block — the syntax is readable as an outline even
   unrendered.

## When the PRD doesn't support this

If a PRD is too vague to yield a real sequence — no ordering, no triggers, no
sense of what the user actually does step by step — say so directly and name
what's missing, rather than fabricating a plausible-sounding flow the PRD
doesn't actually ground. A short, honest "there isn't enough here to sequence
yet, here's what's missing" is more useful to a designer than a confident flow
built on guesses.

## Guardrails

- Never invent behavior for a branch the PRD doesn't resolve — flag it as an
  open question instead.
- Never merge genuinely distinct user journeys into one flow to make the
  output simpler.
- Keep steps at the user-visible level, not implementation detail.
- Keep the Mermaid diagram and the text outline representing the exact same
  flow — don't let them drift into two different versions of the sequence.
