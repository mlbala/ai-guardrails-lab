# AI Guardrails Lab

Hands-on learning repository focused on building guardrails for LLM applications and AI agents. Contains code examples, experiments, and notes from the **Complete AI Security Bootcamp**.

## Topics Covered

- **Guardrails:** Input validation, output filtering, prompt injection defense, and data leakage prevention using NeMo Guardrails, AWS Bedrock Guardrails, and Guardrails AI.
- **AI Agents:** Workflows and tool calling with LangChain, LangGraph, and deep agents; coding workflows with Claude Code.
- **Observability:** Tracing, debugging, and monitoring with LangSmith and Pydantic Logfire.
- **LLM Gateways:** Model routing, fallbacks, and provider management with Portkey and TensorZero.
- **Evaluations:** Answer quality, faithfulness, and hallucination testing with DeepEval.
- **Red Teaming:** Security testing and vulnerability assessment with PyRIT.
- **Performance:** Caching and rate limiting with Redis.

## Goal

Learn to build safer, more reliable AI applications through practical guardrail implementations, evaluations, and monitoring.

## Prerequisites

- Basic Python knowledge
- Familiarity with LLM and Generative AI concepts
- API keys or cloud access for relevant examples

## Repository Structure

```text
ai-guardrails-lab/
├── modules/                       # Course lessons, one folder per module
│   ├── 01_foundations/            # LangChain, LangGraph, debugging, multi-agent, MCP
│   ├── 02_guardrails/             # NeMo Guardrails, Bedrock Guardrails, Guardrails AI
│   ├── 03_observability/          # LangSmith, Pydantic Logfire
│   ├── 04_llm_gateways/           # Portkey, TensorZero, Redis caching and rate limiting
│   ├── 05_evaluations/            # DeepEval
│   ├── 06_red_teaming/            # PyRIT
│   └── 07_deep_agents/            # Deep agents, Claude Code workflows
├── projects/                      # End-to-end projects that combine the modules
│   ├── _template/                 # Copy this to start a new project
│   ├── 01_secure_support_agent/
│   ├── 02_enterprise_llm_gateway/
│   └── 03_red_teaming_eval_suite/
├── src/guardkit/                  # Shared helpers, installed as an editable package
│   ├── config.py                  # Repo paths, .env loading, setup_notebook()
│   ├── llm_factory.py             # get_chat_model("provider:model")
│   ├── observability.py           # enable_langsmith()
│   ├── validators/                # Reusable guardrail validators
│   └── utils/
├── configs/                       # Guardrail, gateway and evaluation configs
├── data/                          # Datasets and sample inputs
├── tests/                         # pytest tests for src/guardkit
├── .env.example                   # Template for the API keys
├── pyproject.toml
└── requirements.txt
```

Each module and project folder has its own README with what it covers and how to run it.

## Getting Started

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                # creates .venv, installs the dependencies and guardkit (editable)
cp .env.example .env   # then fill in your API keys
```

Using pip instead: `pip install -r requirements.txt` (the last line, `-e .`, installs `guardkit`).

## Using guardkit

`guardkit` is the shared package in `src/guardkit/`. Import it as `guardkit` (not `src.guardkit`); it works from any folder once installed.

Every notebook starts with:

```python
from guardkit.config import setup_notebook

ROOT_DIR, DATA_DIR = setup_notebook(required_env=["OPENAI_API_KEY"])
```

It makes the repo root the working directory, loads `.env`, and stops with a clear error if a listed key is missing.

Other helpers, for example in a script:

```python
from guardkit import enable_langsmith, get_chat_model, load_env

load_env(required=["OPENAI_API_KEY"])      # load .env (setup_notebook already does this in notebooks)
model = get_chat_model("openai:gpt-5-mini")  # any "provider:model", e.g. "groq:qwen/qwen3.8-27b"
enable_langsmith()                          # turns on LangSmith tracing if LANGSMITH_API_KEY is set
```

## Running Tests

```bash
uv run pytest
```

## Status

Work in progress — examples and learning notes are added as I progress through the course.

| Module | Topic | Status |
| --- | --- | --- |
| 01 | Foundations: LangChain, LangGraph, debugging, multi-agent, MCP | ✅ Done (16 notebooks, 5 scripts) |
| 02 | Guardrails | Not started |
| 03 | Observability | Not started |
| 04 | LLM gateways | Not started |
| 05 | Evaluations | Not started |
| 06 | Red teaming | Not started |
| 07 | Deep agents | Not started |

Projects (`projects/01`–`03`) start once the matching modules are done.