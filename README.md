# 🛡️ SentinelAI

> **A Secure, Agentic AI Gateway for Controlled LLM Applications**

SentinelAI is a security-focused AI gateway that combines **FastAPI, LangGraph, LiteLLM, Groq, RAG, ChromaDB, MCP, and deterministic guardrails** into a modular AI system.

The project demonstrates how modern GenAI applications can be built with **intelligent routing, retrieval-augmented generation, controlled tool execution, authentication, observability, and automated testing**.

---

## ✨ Features

* 🤖 **LangGraph Agentic Workflow**
* 🧭 **Intelligent Query Routing**
* 🔐 **API-Key Authentication**
* 🛡️ **Input, Output & Tool Guardrails**
* 🔎 **RAG with ChromaDB**
* 🧠 **Sentence Transformer Embeddings**
* 🧩 **Model Context Protocol (MCP)**
* 📁 **MCP File Server**
* 🗄️ **MCP Database Server**
* ⚡ **LiteLLM Gateway**
* 🚀 **Groq LLM Inference**
* 📊 **Observability & Request Metrics**
* 💻 **Streamlit Frontend**
* 🧪 **Unit & Integration Testing**
* 🐳 **Docker Support**

---

## 🏗️ Architecture

```text
                              ┌─────────────────┐
                              │      User       │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    Streamlit    │
                              │    Frontend     │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │     FastAPI     │
                              │   AI Gateway    │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  API Key Auth   │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Input Guardrail │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    LangGraph    │
                              │ Agent Workflow  │
                              └────────┬────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
             ┌────────────┐     ┌────────────┐     ┌────────────┐
             │ Direct LLM │     │    RAG     │     │    MCP     │
             └──────┬─────┘     └──────┬─────┘     └──────┬─────┘
                    │                  │                  │
                    │                  ▼                  ├──────────────┐
                    │            ┌────────────┐           │              │
                    │            │  ChromaDB  │           ▼              ▼
                    │            │  Vector DB │     ┌───────────┐  ┌───────────┐
                    │            └────────────┘     │File Server│  │DB Server  │
                    │                               └───────────┘  └───────────┘
                    │
                    └──────────────────┬──────────────────────┘
                                       ▼
                              ┌─────────────────┐
                              │    LiteLLM      │
                              │     Gateway     │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │   Groq / LLM    │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Output Guardrail│
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │     Response    │
                              └─────────────────┘
```

---

## 🔄 How It Works

A request flows through multiple controlled layers:

```text
User Query
    │
    ▼
Authentication
    │
    ▼
Input Guardrail
    │
    ▼
LangGraph Router
    │
    ├──► Direct ──► LLM
    │
    ├──► RAG ─────► ChromaDB ──► Context ──► LLM
    │
    └──► MCP ─────► Tool Guard ──► MCP Server
                              │
                              ▼
                           Tool Result
                              │
                              ▼
                             LLM
                              │
                              ▼
                       Output Guardrail
                              │
                              ▼
                           Response
```

---

## 🧠 Core Components

### 🤖 LangGraph Agent

The agent orchestrates three execution paths:

| Route      | Purpose                                      |
| ---------- | -------------------------------------------- |
| **Direct** | Handles general queries using the LLM        |
| **RAG**    | Retrieves relevant information from ChromaDB |
| **MCP**    | Executes authorized external tools           |

This separates routing logic from individual execution workflows.

---

### 🔎 RAG Pipeline

SentinelAI includes a complete Retrieval-Augmented Generation pipeline:

```text
Document
   │
   ▼
Loader
   │
   ▼
Text Chunking
   │
   ▼
Sentence Transformer
   │
   ▼
Embeddings
   │
   ▼
ChromaDB
   │
   ▼
Semantic Retrieval
   │
   ▼
LLM Context
```

Supported document types:

* `.txt`
* `.md`
* `.pdf`

---

### 🧩 MCP Integration

SentinelAI integrates the **Model Context Protocol** to provide controlled access to external tools.

#### 📁 File Server

Available tools:

```text
file_get_project_info
file_get_project_status
```

#### 🗄️ Database Server

Available tools:

```text
db_get_employee
db_get_project_status
db_get_team_members
```

Every tool request passes through authorization and argument validation before execution.

---

## 🛡️ Security & Guardrails

SentinelAI uses deterministic guardrails around the LLM workflow.

### Input Guardrail

Validates user input before agent execution.

### Tool Guardrail

Controls:

* Allowed tool names
* Required arguments
* Argument types
* Employee ID validation
* Project name validation

### Output Guardrail

Checks generated responses for potentially sensitive information, including:

* API-key-like patterns
* Password/secret patterns
* Empty responses

The objective is to keep critical security checks deterministic rather than relying entirely on LLM behavior.

---

## ⚡ LiteLLM Gateway

LiteLLM provides a gateway layer between SentinelAI and the underlying model provider.

```text
SentinelAI
     │
     ▼
  LiteLLM
     │
     ▼
   Groq
     │
     ▼
    LLM
```

This provides a consistent interface for model inference while keeping the application architecture separated from the provider-specific implementation.

---

## 📊 Observability

SentinelAI tracks important runtime metrics such as:

* Total requests
* Failed requests
* Average request latency
* Route usage
* Tool usage
* Request IDs

Example:

```json
{
  "requests_total": 10,
  "requests_failed": 1,
  "average_request_duration_ms": 842.31,
  "routes": {
    "direct": 5,
    "rag": 3,
    "mcp": 2
  },
  "tools": {
    "file_get_project_info": 1,
    "db_get_employee": 1
  }
}
```

---

## 📁 Project Structure

```text
SentinelAI/
│
├── backend/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── guardrails/
│   │   ├── input_guard.py
│   │   ├── output_guard.py
│   │   └── tool_guard.py
│   │
│   ├── gateway/
│   │   └── config.yaml
│   │
│   ├── mcp/
│   │   └── client.py
│   │
│   ├── rag/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   └── pipeline.py
│   │
│   ├── auth.py
│   ├── middleware.py
│   ├── observability.py
│   └── main.py
│
├── mcp_servers/
│   ├── file_server.py
│   └── database_server.py
│
├── frontend/
│   └── app.py
│
├── monitoring/
│
├── tests/
│   ├── test_api.py
│   ├── test_agent.py
│   ├── test_guardrails.py
│   ├── test_integration.py
│   └── test_mcp.py
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Tech Stack

| Category         | Technology             |
| ---------------- | ---------------------- |
| Language         | Python                 |
| Backend          | FastAPI                |
| Agent Framework  | LangGraph              |
| LLM Gateway      | LiteLLM                |
| LLM Provider     | Groq                   |
| RAG              | ChromaDB               |
| Embeddings       | Sentence Transformers  |
| Tool Protocol    | MCP                    |
| Frontend         | Streamlit              |
| Authentication   | API Key / Bearer Token |
| Testing          | Pytest                 |
| Containerization | Docker                 |
| Version Control  | Git / GitHub           |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/imymoin/SentinelAI.git
cd SentinelAI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```powershell
copy .env.example .env
```

Configure the required API keys and application settings in `.env`.

> ⚠️ Never commit `.env` or real API keys to GitHub.

---

## ▶️ Running the Application

### Start LiteLLM

```bash
litellm --config backend/gateway/config.yaml --port 4000
```

### Start FastAPI

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Start Streamlit

Open another terminal:

```bash
streamlit run frontend/app.py
```

---

## 🔌 API

### Health Check

```http
GET /health
```

### Chat

```http
POST /chat
Authorization: Bearer <SENTINEL_API_KEY>
Content-Type: application/json
```

Example request:

```json
{
  "query": "Tell me about SentinelAI"
}
```

### Metrics

```http
GET /metrics
```

---

## 🧪 Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Run individual test suites:

```bash
python -m pytest tests/test_api.py -v
python -m pytest tests/test_agent.py -v
python -m pytest tests/test_guardrails.py -v
python -m pytest tests/test_mcp.py -v
python -m pytest tests/test_integration.py -v
```

---

## 🐳 Docker

The repository includes Docker and Docker Compose configuration.

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

> Docker Desktop must be installed and running before using Docker commands on Windows.

---

## 🔐 Security

SentinelAI is designed as a **security-focused AI engineering project**.

Current security mechanisms include:

* API-key authentication
* Input validation
* Tool allowlisting
* Tool argument validation
* Output secret-pattern detection
* Environment-based secret configuration
* Request tracking
* Controlled MCP tool access

For a production deployment, additional hardening should be considered, including:

* HTTPS/TLS
* Rate limiting
* Centralized secret management
* Stronger authorization
* Container hardening
* Centralized logging
* Security evaluations
* Continuous monitoring

---

## 🧪 Engineering Focus

This project was built to explore the engineering challenges involved in combining multiple GenAI components into one reliable system.

Key areas explored:

* Agentic AI architecture
* LLM routing
* RAG
* Vector databases
* MCP tool integration
* AI guardrails
* API security
* Observability
* Automated testing
* Backend architecture
* Containerization

---


## 👨‍💻 Author

### Mohd Yusuf Moin

Interested in **Generative AI, Agentic AI, Python, backend engineering, RAG, and intelligent systems**.

🔗 **GitHub:** https://github.com/imymoin

🔗 **Project:** https://github.com/imymoin/SentinelAI

---

## ⭐ Support

If you find SentinelAI interesting, consider giving the repository a ⭐.

> **SentinelAI — Building safer, more controlled AI systems.**
