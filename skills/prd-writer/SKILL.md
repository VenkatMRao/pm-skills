---
name: prd-writer
description: Draft a product requirements document (PRD) from a rough feature idea or notes. Use when the user asks to write, draft, or start a PRD, spec, or feature brief.
---

# PRD Writer

Turn a rough idea into a structured PRD by front-loading the questions a PM should
answer *before* writing, not after — a PRD written without this pass tends to be
vague on success criteria and silent on what's explicitly out of scope.

## Process

1. **Read what's given.** Notes, a Slack thread, a ticket, a one-line ask —
   whatever the user provides. Do not ask them to restate it in a different format.

2. **Ask only the questions the input doesn't already answer**, in one batch, not
   one at a time. At minimum, resolve:
   - **Problem**: Who has this problem, and what do they do today without this
     feature? (If the user can't answer this, that's the real blocker — say so
     before drafting.)
   - **Success metric**: What number moves, and by how much, for this to be worth
     shipping? If there isn't one yet, propose 1-2 candidates instead of leaving it
     blank.
   - **Scope boundary**: What's explicitly *not* included in v1? Under-scoping is
     the most common PRD failure — push for a real answer here, not "TBD."
   - **Constraints**: Any known technical, timeline, or dependency constraints
     already in play?

   Skip a question outright if the input already answers it — don't make the user
   repeat information they already gave you.

3. **Draft the PRD** using this structure:
   - **Title & one-line summary**
   - **Problem statement** — who, what pain, what they do today
   - **Goals** (what success looks like) **/ Non-goals** (explicit scope cuts)
   - **Success metrics** — leading and lagging, with a target where possible
   - **User stories / use cases** — concrete scenarios, not abstractions
   - **Requirements** — functional, grouped by user flow; call out P0 vs P1
   - **Open questions** — anything still unresolved, named explicitly rather than
     buried in the requirements
   - **Risks & dependencies**

4. **Flag weak spots instead of papering over them.** If a success metric is
   genuinely undefined or scope is still fuzzy after asking, write the section as
   "Open question: ___" rather than inventing a plausible-sounding answer. A PRD
   that hides its own gaps is worse than one that names them.

## Output

A single markdown document following the structure above. Match the user's
existing PRD format/template if they share or reference one instead of imposing
this structure.
