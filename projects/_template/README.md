# Project NN: Name

Copy this folder to `projects/NN_short_name/` and fill in each section.

## Goal

What the app does, who uses it, and what must never go wrong.

## Architecture

The agents, tools and models involved, and how a request flows through them.

## Guardrails

| Layer | Check | Where it runs |
| --- | --- | --- |
| Input | e.g. prompt injection filter | before the agent |
| Tools | e.g. human approval for refunds | around the tool call |
| Output | e.g. PII redaction | after the agent |

## Run

```bash
uv run python projects/NN_short_name/app.py
```

Required keys (in the repo `.env`): ...

## Evaluate

How the guardrails are tested (eval set in `data/`, red-team prompts, metrics), and the latest results.

## Notes

What worked, what didn't, and what to try next.
