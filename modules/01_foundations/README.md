# Module 01: Foundations

LangChain and LangGraph agent basics that the guardrail modules build on.

| Folder | What it covers |
| --- | --- |
| `01_langchain_agents/` | `create_agent`, model integrations, streaming and batch, tools, messages, structured output, middleware (summarization, model fallback), human in the loop, guardrail middleware (PII, content filters, prompt injection) |
| `02_langgraph_agents/` | `StateGraph` chatbot, ReAct agent with tools, memory and checkpointers, streaming events, human in the loop with `interrupt` |
| `03_debugging/` | LangSmith tracing and LangGraph Studio for `agent.py` (`langgraph.json` reads the repo `.env`) |
| `04_multi_agents/` | Researcher and writer pipeline, and a supervisor multi-agent system (notebook and `supervisor_multi_agent.py`) |
| `05_mcp/` | MCP servers (math over stdio, weather over streamable HTTP) and a LangChain client that routes between them |

## Setup

From the repo root:

```bash
uv sync                # installs the dependencies and guardrails_lab (editable)
cp .env.example .env   # then fill in the keys
```

Keys used in this module: `OPENAI_API_KEY`, `GROQ_API_KEY`, `GOOGLE_API_KEY`, `TAVILY_API_KEY`, `LANGSMITH_API_KEY`.

## Running the scripts

```bash
# LangGraph Studio for the debugging agent
cd modules/01_foundations/03_debugging && uv run langgraph dev

# Supervisor multi-agent system in the terminal
uv run python modules/01_foundations/04_multi_agents/supervisor_multi_agent.py

# MCP: start the weather server first, then the client in a second terminal
uv run python modules/01_foundations/05_mcp/weather.py
uv run python modules/01_foundations/05_mcp/client.py
```
