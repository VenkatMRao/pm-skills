# Turning a multi-day research write-up into an afternoon

*Details generalized/anonymized. See [`prompts/user-research-synthesis.md`](../prompts/user-research-synthesis.md) for the underlying prompt.*

## Problem

After a round of user interviews (typically 6-10 calls), synthesizing raw notes
into a shareable set of themes and recommendations used to take the better part
of two days: re-reading every transcript, manually tagging recurring points,
pulling representative quotes, and then writing up the findings in a way a
non-researcher stakeholder could act on. The bottleneck wasn't judgment — it was
the sheer mechanical effort of holding ten conversations' worth of notes in your
head at once and finding the patterns across them.

## Approach

I use a synthesis prompt ([`prompts/user-research-synthesis.md`](../prompts/user-research-synthesis.md))
that takes raw interview notes for an entire round at once and returns:
frequency-labeled themes with supporting verbatims, explicit disagreement between
participants where it exists, and a "so what" section tying each theme back to a
concrete product implication. I still read every transcript myself first — the
prompt doesn't replace that — but it replaces the slow manual step of
cross-referencing ten sets of notes to find what repeats and what's a one-off, and
it makes it much harder to accidentally overweight the first interview I happened
to read.

## Outcome

- The write-up step went from roughly two days to an afternoon: most of the
  saved time was in the cross-referencing and first-draft-writing steps, not the
  interviewing or the final editorial judgment.
- The output format surfaces the "how many participants said this" number
  automatically, which made it easier to push back internally when a stakeholder
  wanted to act on a single loud comment rather than a genuine pattern.
- Because the prompt explicitly asks for disagreement between participants, the
  write-ups stopped flattening mixed signal into an artificially clean narrative —
  a failure mode the manual process was quietly prone to under time pressure.

## What I'd change next

For larger studies (15+ interviews), a single prompt call starts to strain
context; the natural next step is chunking transcripts and merging themes across
chunks, similar to how [`scripts/verbatim-tagger`](../scripts/verbatim-tagger/)
batches survey responses.
