# Feature spec / PRD review

**Use when:** you have a draft spec or PRD and want a critical pass before it goes
to engineering or a review meeting — catching the gaps a fresh reader would
question, before they do.

**Input:** the full draft spec/PRD.

---

```
Review this draft spec/PRD as a skeptical but constructive reviewer — the kind of
review that saves the actual review meeting from turning into a gap-finding
session. Specifically check for:

1. **Success metrics**: Is there a measurable definition of success? If it's
   vague ("improve engagement") or missing, say so directly rather than assuming
   it's implied.
2. **Scope boundaries**: Is it clear what's explicitly out of scope for v1? Vague
   scope is the single most common cause of spec-related rework — flag it hard.
3. **Edge cases**: What happens for the user who doesn't fit the happy path
   (empty states, errors, permission edge cases, existing users vs. new)?
4. **Dependencies**: Does this rely on another team, system, or in-flight
   project that isn't named? Silent dependencies are the ones that blow up
   timelines.
5. **Internal consistency**: Do the requirements section and the stated goals
   actually match? Flag anything in the requirements that doesn't map back to a
   stated goal, and any goal with no requirement serving it.

For each issue: quote or point to the specific section, explain concretely what
could go wrong if it ships as-is, and suggest a fix — don't just flag it and move
on. If a section is genuinely solid, say so; don't manufacture issues to seem
thorough.

Spec:

[PASTE DRAFT SPEC/PRD HERE]
```
