# Scripts

Small, runnable Python automations for tasks that are repetitive enough to script
or need to run outside a chat window. Each subfolder is self-contained with its
own README, sample data, and (where needed) `requirements.txt`.

| Script | What it does | Needs an API key? |
|---|---|---|
| [`sprint-report/`](sprint-report/README.md) | Turns a Jira/Linear CSV export into a markdown sprint summary (velocity, completed vs. carried over, risks) | No |
| [`verbatim-tagger/`](verbatim-tagger/README.md) | Theme-tags and sentiment-scores open-text survey responses using the Claude API | Yes (`ANTHROPIC_API_KEY`) |
| [`nl-data-query/`](nl-data-query/README.md) | Ask a SQL database/warehouse a question in plain language and get a read-only query plus a plain-language insight back | Yes (`ANTHROPIC_API_KEY`) |
