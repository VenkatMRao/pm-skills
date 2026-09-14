---
name: weekly-summary
description: Generate a weekly summary in non-technical language — what got done this week (from tickets), what decisions were made, current risks/blockers, and how the week's work moves the product's OKRs. Use when the user asks for a weekly update, weekly status, or wants to summarize the week for stakeholders against OKRs.
---

# Weekly Summary

Four things, every week: what happened (in plain language, not ticket-speak),
what was decided, what's currently at risk or blocked, and how the week
connects to the OKRs the product is actually accountable for. Don't add
sections beyond these four plus a short header — this is meant to be a fast,
focused read, not a comprehensive report.

## Before the first run: the same safety check as other recurring skills

This summary can contain internal decisions and business context. Before
saving anything locally, check whether the current working directory looks
like a public/shared repository. If it does, stop and ask the user where
they'd actually like these saved instead.

## Inputs needed

- **The week's date range** — confirm it rather than assuming; "this week"
  is ambiguous across time zones and work weeks.
- **Ticket source** — however the team tracks work: GitHub Issues/PRs (`gh`
  CLI), Jira, Linear, or a pasted list. Scope to tickets closed or
  meaningfully advanced within the date range.
- **Decision source** — meeting notes, a Slack export, a decision log, or
  whatever the user has. If nothing is provided beyond tickets, say so
  explicitly in the output: decisions made only verbally or in an untracked
  meeting won't show up unless something documents them, and it's important
  the reader knows the decisions section isn't necessarily complete rather
  than assuming it is.
- **The current OKRs** — ask for them if not already given (pasted, or a
  path/doc to read). Don't invent or infer OKRs that haven't actually been
  stated.
- **Risk/blocker context beyond tickets**, if the user has it (standup notes,
  a risk register, something a lead flagged in Slack). Ticket status alone
  only catches blockers that got explicitly marked as such in the tracker —
  it won't catch a risk that's known but not yet logged anywhere (a
  dependency on a team member who's about to be out, an external vendor
  that's gone quiet). Ask, rather than assuming tickets are the full picture.

## History convention

Save each week's summary to `weekly-summaries/<start-date>_<end-date>.md` in
the current project. Before writing a new one, check whether last week's file
exists — reading it lets you write with continuity ("following up on last
week's decision to...") instead of every summary reading as if it's the first
one ever produced. Never overwrite a past week's file.

## Process

1. **Gather this week's tickets** and group them by theme/initiative, not by
   ticket ID — a summary organized as "TICKET-412, TICKET-418" is exactly the
   kind of ticket-speak this skill exists to avoid. Translate each into what
   actually changed for the user or the business, not what changed in the
   code. If a ticket's actual outcome isn't clear from its title/description,
   say so rather than guessing at a plausible-sounding impact.

2. **Gather decisions made this week** from whatever sources were given
   (meeting notes, Slack, ticket comments, description changes that clearly
   reflect a decision — e.g. "decided to go with approach X instead of Y").
   State each decision plainly: what was decided, and — if evident from the
   source — why. Don't infer a decision from a ticket simply changing status;
   only report it as a decision when the source actually shows one being
   made.

3. **Gather current risks and blockers.** Pull tickets explicitly marked
   blocked/at-risk in the tracker, plus anything from the risk context the
   user provided. For each: what's blocked, why, since when, and — if known
   — what's needed to unblock it or who owns resolving it. Distinguish a
   **blocker** (something is stopped, concretely, right now) from a
   **risk** (nothing's stopped yet, but something could derail the work if it
   doesn't get attention) — don't collapse the two into one undifferentiated
   list. If ticket status is the only source available, say so: a clean
   "no blockers" from tickets alone doesn't mean there are no real risks,
   only that none were logged as one.

4. **Map this week's work and decisions to the OKRs.** For each Key Result:
   - What this week's work contributes toward it, if anything — phrased as
     contribution/intent ("this work is aimed at improving X"), not as a
     measured result, unless there's actual data showing movement.
   - If a Key Result is metric-based and the data lives in a database/
     warehouse, use `nl-data-query` / `database-chat-insights` to check
     current progress rather than guessing at where the number stands.
   - If nothing this week traces to a given Key Result, say so plainly — this
     is useful signal (either the OKR isn't being actively worked, or the
     work underway isn't visibly connected to it) rather than something to
     paper over.
   - Note, without judgment, any completed work this week that doesn't trace
     to any stated OKR — worth surfacing, not necessarily worth flagging as a
     problem.

5. **Write the summary**, in plain, non-technical language throughout:
   ```
   Weekly Summary: <date range>

   What happened this week
   <grouped by theme, plain language, ticket refs in parentheses for
   traceability>

   Decisions made this week
   <each decision, plainly stated, with the why if known>
   (If no decision source was provided: note that only decisions visible in
   ticket history are reflected here.)

   Risks & blockers
   <Blockers: what's stopped, why, since when, what/who unblocks it>
   <Risks: what could derail things if unaddressed>
   (Note if this is sourced from tracker status only, since that likely
   understates the real picture.)

   OKR impact
   <per Key Result: what contributed, or that nothing did>

   Work without a clear OKR link
   <if any — stated neutrally, not as a criticism>
   ```

6. **Save it** to the history location, and mention if it follows up on
   anything from last week's file — including whether a previously listed
   blocker/risk is now resolved, still open, or has gotten worse.

## Guardrails

- Keep the "what happened" section in outcomes language a non-technical
  stakeholder can act on — no implementation detail, no unexplained jargon.
- Never state or imply a decision happened without a source showing it did.
- Never claim a Key Result moved by a specific amount unless there's actual
  data behind that number — contribution and measured impact are different
  claims, don't blur them.
- Don't invent OKRs, and don't force a tenuous connection between a piece of
  work and a Key Result just to give every item a home.
- Don't invent a risk that isn't evidenced by something the user or the
  tracker actually surfaced — a plausible-sounding risk that isn't real just
  adds noise.
- Don't blur "blocked" and "at risk" together — they call for different
  responses from the reader.
- Don't add sections beyond what happened, decisions, risks/blockers, and OKR
  impact.
