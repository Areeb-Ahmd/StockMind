# StockMind – Agentic Stock Market Assistant

An LLM-powered, tool-augmented chatbot for stock market research and financial analysis, built with LangGraph, LangChain, and a Retrieval-Augmented Generation (RAG) pipeline backed by Pinecone.

## Overview

This project implements a conversational AI agent that can answer questions about the stock market by combining three information sources:

1. **Private knowledge base** -- Users upload PDF or DOCX documents (e.g. trading guides, market reports) which are chunked, embedded, and stored in a Pinecone vector database. A retriever tool performs similarity search over this knowledge base at query time.
2. **Live web search** -- A Tavily search tool provides the agent with up-to-date information from the internet.
3. **Financial data API** -- A Polygon.io financials tool gives the agent access to company financial data (income statements, balance sheets, etc.).

The agent is orchestrated as a **LangGraph state graph** with a ReAct-style tool-use loop: the LLM decides which tools to call (if any), the tool results are fed back, and the LLM produces a final answer. A primary LLM (Google Gemini) is used with automatic failover to a fallback LLM (Groq) if the primary encounters errors or rate limits.

The system is containerized as a monorepo with a **FastAPI** backend (`backend/`) and a **Streamlit** frontend (`frontend/`), deployed automatically to **Google Cloud Run** via **GitHub Actions CI/CD**.

## Key Features

- **Monorepo architecture** with clean separation between FastAPI backend and Streamlit UI.
- **Multi-stage Docker builds** for optimized, small production container images.
- **Docker Compose** integration for zero-friction local multi-container development.
- **Automated CI/CD** via GitHub Actions deploying to Google Cloud Run (`asia-south1`) on pushes to `main`.
- **RAG pipeline** with PDF and DOCX ingestion, recursive text splitting, and Pinecone vector storage with configurable batch sizes and rate-limit retry logic.
- **Multi-tool agent** powered by LangGraph that autonomously selects between a vector store retriever, Tavily web search, and Polygon.io financial data.
- **Dual-LLM architecture** with automatic failover from Google Gemini (primary) to Groq (fallback) using LangChain's `with_fallbacks`.

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.11 |
| Agent Framework | LangGraph, LangChain |
| Primary LLM | Google Gemini (via `langchain-google-genai`) |
| Fallback LLM | Groq (via `langchain-groq`) |
| Embeddings | Google Generative AI Embeddings (`gemini-embedding-001`) |
| Vector Database | Pinecone (via `langchain-pinecone`) |
| Web Search | Tavily (via `tavily-python`) |
| Financial Data | Polygon.io (via `polygon` + LangChain `PolygonFinancials`) |
| Backend API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Containerization | Docker (Multi-Stage), Docker Compose |
| Cloud Infrastructure | Google Cloud Run, Artifact Registry, Secret Manager |
| CI/CD Pipeline | GitHub Actions |

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment workflow
│
├── backend/
│   ├── Dockerfile              # Multi-stage Dockerfile for FastAPI backend
│   ├── agent/
│   │   └── workflow.py        # LangGraph state graph definition
│   ├── config/
│   │   └── config.yaml        # Configuration parameters
│   ├── custom_logging/
│   │   └── my_logger.py       # Custom logger setup
│   ├── data_ingestion/
│   │   └── ingestion_pipeline.py # Document ingestion pipeline
│   ├── data_models/
│   │   └── models.py          # Pydantic schemas
│   ├── exception/
│   │   └── exceptions.py      # Custom StockMindException
│   ├── fallback_data/         # Knowledge base fallback documents
│   ├── prompt_library/
│   │   └── prompt.py          # System prompt definitions
│   ├── toolkit/
│   │   └── tools.py           # Retriever, Tavily, & Polygon tools
│   ├── utils/
│   │   ├── config_loader.py   # YAML config loader
│   │   ├── model_loaders.py   # LLM and Embedding loaders
│   │   └── response_formatter.py
│   ├── main.py                 # FastAPI backend entrypoint (REST API)
│   ├── requirements.txt        # Backend Python dependencies
│   └── setup.py                # Package setup script
│
├── frontend/
│   ├── Dockerfile              # Multi-stage Dockerfile for Streamlit UI
│   ├── streamlit_ui.py         # Streamlit chat interface
│   ├── requirements.txt        # Frontend Python dependencies
│   └── .streamlit/
│       └── config.toml         # Streamlit server config
│
├── docker-compose.yml          # Local multi-container development orchestration
├── .dockerignore               # Docker build ignore rules
├── .env.example                # Template for required environment variables
├── .gitignore                  # Git ignore rules
└── README.md
```

## Prerequisites

- **Docker & Docker Compose** (for local containerized execution)
- **Python 3.11+** (if running without Docker)
- API keys for the following services:

| Environment Variable | Service | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | Google AI (Gemini) | Primary LLM and embedding model |
| `GROQ_API_KEY` | Groq | Fallback LLM |
| `PINECONE_API_KEY` | Pinecone | Vector database storage and retrieval |
| `TAVILY_API_KEY` | Tavily | Web search tool |
| `POLYGON_API_KEY` | Polygon.io | Financial data tool |

---

## Local Quickstart with Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Areeb-Ahmd/StockMind.git
   cd StockMind
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your actual 5 API keys.

3. **Launch local containers:**
   ```bash
   docker compose up --build
   ```

4. **Access services:**
   - **Frontend UI**: [http://localhost:8501](http://localhost:8501)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **Backend Healthcheck**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Deployment to Google Cloud Run (CI/CD)

The project includes a complete **GitHub Actions** CI/CD pipeline (`.github/workflows/deploy.yml`) that automatically builds multi-stage Docker images and deploys them to **Google Cloud Run** (`asia-south1`) whenever new code is pushed to the `main` branch.

### Deployment Prerequisites & GCP Setup

1. **GCP Project**: `stockmind-504615`
2. **Enable Required APIs**:
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
   ```
3. **Create Artifact Registry Repository**:
   ```bash
   gcloud artifacts repositories create stockmind-repo \
     --repository-format=docker \
     --location=asia-south1
   ```
4. **Configure Secrets in GitHub Repository**:
   Add the following under **GitHub Repo → Settings → Secrets and variables → Actions**:
   - `GCP_PROJECT_ID`: `stockmind-504615`
   - `GCP_REGION`: `asia-south1`
   - `GCP_SA_KEY`: JSON service account key with Cloud Run Admin, Artifact Registry Writer, and Secret Manager Accessor permissions.
   - `GOOGLE_API_KEY`, `GROQ_API_KEY`, `PINECONE_API_KEY`, `TAVILY_API_KEY`, `POLYGON_API_KEY`.

---

## How It Works

```
User Question
     │
     ▼
┌──────────┐    POST /query     ┌──────────────────┐
│ Streamlit │ ──────────────────▶│  FastAPI Backend  │
│    UI     │                    │    (main.py)      │
└──────────┘                    └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  LangGraph Agent  │
                                │  (workflow.py)    │
                                └────────┬─────────┘
                                         │
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
                   ┌────────────┐ ┌───────────┐ ┌──────────────┐
                   │  Retriever │ │  Tavily   │ │   Polygon    │
                   │  (Pinecone)│ │  Search   │ │  Financials  │
                   └────────────┘ └───────────┘ └──────────────┘
```

1. **Document Ingestion**: Users upload PDF or DOCX files via Streamlit or `/upload`. The `DataIngestion` pipeline processes, chunks, embeds using Gemini embeddings, and stores vectors in Pinecone.
2. **ReAct Agent Execution**: Questions sent to `/query` invoke a LangGraph state graph. Google Gemini (or Groq fallback) decides which tool (`retriever_tool`, `tavilytool`, `financials_tool`) to call.
3. **Response Synthesis**: Tool findings are passed back to the LLM to format a final markdown answer.

---

## License & Disclaimer

This project is intended for **educational and research purposes only**. It does not constitute financial advice.
