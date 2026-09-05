# SentinelAI

SentinelAI is a secure AI gateway built with FastAPI, LangGraph, LiteLLM, Groq, RAG, ChromaDB, MCP and deterministic guardrails.

## Architecture

```text
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ API Key Auth │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │Input Guardrail│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LangGraph   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Direct LLM      RAG          MCP
                           │             │
                           ▼             ▼
                       ChromaDB     File/Database
                           │             │
                           └──────┬──────┘
                                  │
                                  ▼
                           LiteLLM Gateway
                                  │
                                  ▼
                               Groq LLM
                                  │
                                  ▼
                           Output Guardrail
                                  │
                                  ▼
                                User# SentinelAI
