#!/usr/bin/env python3
"""Theme-tag and sentiment-score open-text survey responses using the Claude API.

Reads a CSV of open-text responses, sends them to Claude in batches for theme +
sentiment tagging, and writes a new CSV with `theme` and `sentiment` columns
added.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

import anthropic

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_BATCH_SIZE = 20

SYSTEM_PROMPT = """You are tagging open-text survey responses for a product team.

For each response, assign:
- "theme": a short (2-4 word) label for the main topic raised. Reuse the exact
  same label across responses that raise the same topic in this batch — don't
  invent a new phrasing for a theme you've already used.
- "sentiment": one of "positive", "neutral", "negative".

Return ONLY a JSON array, one object per input response, in the same order as
the input, shaped as {"theme": "...", "sentiment": "..."}. No prose, no markdown
code fences, no extra keys."""


def load_responses(csv_path, column):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return rows
    if column not in rows[0]:
        raise SystemExit(
            f"Column '{column}' not found. Available columns: {', '.join(rows[0].keys())}"
        )
    return rows


def tag_batch(client, model, texts):
    numbered = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts))
    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": numbered}],
    )
    raw = message.content[0].text.strip()
    try:
        tags = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Model did not return valid JSON:\n{raw}") from e
    if len(tags) != len(texts):
        raise RuntimeError(
            f"Expected {len(texts)} tags back, got {len(tags)}. "
            "Try a smaller --batch-size."
        )
    return tags


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Path to the CSV of survey responses")
    parser.add_argument(
        "--column",
        default="response",
        help="Column containing the open-text response (default: response)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument(
        "-o", "--output", default=None, help="Output CSV path (default: <input>_tagged.csv)"
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set the ANTHROPIC_API_KEY environment variable before running this script.")

    rows = load_responses(args.csv_path, args.column)
    if not rows:
        raise SystemExit("No rows found in input CSV.")

    client = anthropic.Anthropic()
    texts = [row[args.column] for row in rows]

    all_tags = []
    for start in range(0, len(texts), args.batch_size):
        batch = texts[start : start + args.batch_size]
        print(
            f"Tagging responses {start + 1}-{start + len(batch)} of {len(texts)}...",
            file=sys.stderr,
        )
        all_tags.extend(tag_batch(client, args.model, batch))

    for row, tag in zip(rows, all_tags):
        row["theme"] = tag.get("theme", "")
        row["sentiment"] = tag.get("sentiment", "")

    output_path = args.output or str(
        Path(args.csv_path).with_name(Path(args.csv_path).stem + "_tagged.csv")
    )
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} tagged responses to {output_path}")


if __name__ == "__main__":
    main()
