# Verbatim tagger

Theme-tags and sentiment-scores open-text survey responses (NPS/CSAT comments,
support tickets, app store reviews) using the Claude API — the manual-coding pass
that normally eats a day of a research or PM's time, done in a couple of minutes.

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
python3 tag_verbatims.py path/to/responses.csv --column response
```

Writes `responses_tagged.csv` alongside the input, with `theme` and `sentiment`
columns added. Override the output path with `-o`, or the model with `--model`
(defaults to `claude-haiku-4-5-20251001` — fast and cheap enough for high-volume
tagging; use a larger model via `--model` if your responses need more nuanced
judgment).

## How it works

Responses are sent to Claude in batches (default 20 per request, tune with
`--batch-size`) with instructions to reuse the same theme label across responses
in the batch that raise the same topic, and to return sentiment as
positive/neutral/negative. Batching keeps theme labels consistent within a batch
and keeps the cost down; very large datasets will have theme labels that drift
slightly batch-to-batch — for a final report, do a quick pass to merge
near-duplicate theme labels (e.g. "pricing concerns" vs. "cost complaint").

## Try it

```bash
python3 tag_verbatims.py sample_data/verbatims.csv --column response
```
