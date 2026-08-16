# StockMind – Agentic Stock Market Assistant

An LLM-powered, tool-augmented financial research assistant and chatbot for stock market research, financial analysis, and document intelligence. Built with **LangGraph**, **LangChain**, **Pinecone**, **FastAPI**, and **Streamlit**.

---

## Overview

**StockMind** is an intelligent conversational agent that provides comprehensive stock market research by combining three distinct information channels:

1. **Personal Knowledge Base (RAG)** – Ingests uploaded PDF and DOCX financial documents (annual reports, earnings transcripts, SEC filings, trading guides) into a Pinecone vector database using Google Generative AI embeddings (`models/gemini-embedding-001`).
2. **Live Web Search** – Uses Tavily Search API for real-time market updates, financial news, and broader macroeconomic context.
3. **Financial Statements Data** – Fetches structured fundamental financial data (income statements, balance sheets, cash flows) directly via the Polygon.io API.

The agent is orchestrated as a **LangGraph state graph** implementing a ReAct tool-use execution loop. A primary LLM (**Google Gemini**) handles reasoning and tool invocation, with automatic failover to a fallback LLM (**Groq**) via LangChain's `.with_fallbacks()` mechanism if rate limits or service disruptions occur.

The system is organized as a monorepo featuring a **FastAPI** backend API and a **Streamlit** frontend interface with modular UI components, containerized via **Docker Compose**, and automated for CI/CD deployment to **Google Cloud Run** through **GitHub Actions**.

---

## Key Features

- **Monorepo Architecture** – Modular separation between FastAPI backend API (`backend/`) and Streamlit web application (`frontend/`).
- **LangGraph Agent Workflow** – Autonomous tool selection (`retriever_tool`, `financials_tool`, `tavilytool`) built with stateful graph nodes and conditional edge transitions.
- **Dual-LLM Automatic Failover** – Resilient model orchestration automatically falling back from primary Google Gemini to Groq upon error or rate limit detection.
- **Pinecone Vector Database Integration** – Serverless index (`stockmind-vdb`, 3072 dimensions) with recursive text splitting, batching (`batch_size=40`), exponential backoff retries, and similarity threshold filtering (`score_threshold=0.5`).
- **Executive Frontend UI** – Tailored Light Theme design with slate navy and copper branding, interactive research capability starter prompt cards, and modular component architecture.
- **Document Processing Pipeline** – Supports uploading PDF and DOCX files through the UI, ingesting them directly into Pinecone for immediate retrieval.
- **Production-Ready Containerization** – Multi-stage Dockerfiles for minimal container image sizes and zero-friction Docker Compose orchestration.
- **Automated CI/CD Deployment** – GitHub Actions workflow building and deploying containers to Google Cloud Run (`asia-south1`) on pushes to `main`.

---

## Tech Stack

| Category | Technology | Description / Model |
|---|---|---|
| **Language** | Python 3.11 | Primary runtime environment |
| **Agent Framework** | LangGraph, LangChain | Stateful graph orchestration and ReAct loop |
| **Primary LLM** | Google Gemini | `gemini-3.1-flash-lite` (via `langchain-google-genai`) |
| **Fallback LLM** | Groq | `openai/gpt-oss-120b` (via `langchain-groq`) |
| **Embeddings** | Google AI Embeddings | `models/gemini-embedding-001` (3072 dimensions) |
| **Vector Database** | Pinecone | Index `stockmind-vdb` (Cosine distance, Serverless AWS `us-east-1`) |
| **Web Search** | Tavily Search API | Real-time financial web search (`tavily-python`) |
| **Financial Data** | Polygon.io API | Financial statements data (`PolygonFinancials`) |
| **Backend Framework** | FastAPI & Uvicorn | Async REST API server with lifespan graph initialization |
| **Frontend Framework** | Streamlit | Modular web UI with custom CSS stylesheet |
| **Containerization** | Docker & Docker Compose | Multi-stage production container builds |
| **Cloud Hosting** | Google Cloud Run | Serverless container execution |
| **Artifact Registry** | Google Artifact Registry | Container image repository (`stockmind-repo`) |
| **CI/CD Pipeline** | GitHub Actions | Automated build, push, and Cloud Run deployment |

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD deployment workflow
│
├── backend/
│   ├── Dockerfile              # Multi-stage Dockerfile for FastAPI backend API
│   ├── agent/
│   │   ├── __init__.py
│   │   └── workflow.py         # LangGraph state graph definition & ReAct loop
│   ├── config/
│   │   └── config.yaml         # Configuration for models, retriever, vector DB & tools
│   ├── custom_logging/
│   │   └── my_logger.py        # Logging configuration (Console & File logging)
│   ├── data_ingestion/
│   │   └── ingestion_pipeline.py # Document loader, splitter, and Pinecone ingestion pipeline
│   ├── data_models/
│   │   └── models.py           # Pydantic data schemas (QuestionRequest, RagToolSchema)
│   ├── exception/
│   │   └── exceptions.py       # Custom StockMindException error handler
│   ├── fallback_data/          # Default research PDF and DOCX files
│   │   ├── stock_market.pdf
│   │   ├── stock_market_investing_guide.docx
│   │   └── trading_basics.pdf
│   ├── prompt_library/
│   │   └── prompt.py           # System prompts for agent behavior
│   ├── toolkit/
│   │   └── tools.py            # LangChain tool definitions (Retriever, Tavily, Polygon)
│   ├── utils/
│   │   ├── config_loader.py    # YAML configuration loader
│   │   ├── model_loaders.py    # Primary & Fallback LLM and embedding model loaders
│   │   └── response_formatter.py # Response parser for AIMessage text extraction
│   ├── main.py                 # FastAPI backend entrypoint & REST API endpoints
│   ├── requirements.txt        # Backend Python package dependencies
│   └── setup.py                # Package setup script
│
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml         # Streamlit theme & server configuration
│   ├── assets/                 # Brand logos, provider icons, and social SVG assets
│   │   ├── chatbot_logo.png
│   │   ├── github.svg
│   │   ├── gmail.svg
│   │   ├── linkedin.svg
│   │   ├── pinecone.svg
│   │   ├── polygon.io.jpeg
│   │   └── tavily.svg
│   ├── components/             # Modular Streamlit UI components
│   │   ├── chat.py             # Chat interface & starter prompt capability cards
│   │   ├── footer.py           # Sidebar footer with social links
│   │   ├── header.py           # Top header with logo & brand title
│   │   ├── metrics.py          # Hero research pillars card (Polygon, Pinecone, Tavily)
│   │   └── sidebar.py          # Document upload & knowledge base sidebar
│   ├── static/
│   │   └── css/
│   │       └── theme.css       # Custom Light Theme stylesheet
│   ├── utils/
│   │   └── assets.py           # Base64 image encoding & CSS loader utilities
│   ├── Dockerfile              # Multi-stage Dockerfile for Streamlit UI
│   ├── requirements.txt        # Frontend Python package dependencies
│   └── streamlit_ui.py         # Main Streamlit web application entrypoint
│
├── notebook/
│   └── experiments.ipynb       # Prototyping notebook for RAG and tool testing
├── docker-compose.yml          # Local multi-container development orchestration
├── .dockerignore               # Docker build ignore rules
├── .env.example                # Template for required environment variables
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## Prerequisites & Environment Setup

To run StockMind locally or deploy it to cloud infrastructure, you will need:

- **Docker & Docker Compose** (for containerized execution)
- **Python 3.11+** (if running without Docker)
- API keys for the following 5 services:

| Environment Variable | Provider | Function |
|---|---|---|
| `GOOGLE_API_KEY` | Google AI | Primary LLM (`gemini-3.1-flash-lite`) and Embeddings (`models/gemini-embedding-001`) |
| `GROQ_API_KEY` | Groq | Fallback LLM (`openai/gpt-oss-120b`) |
| `PINECONE_API_KEY` | Pinecone | Vector Database storage and similarity search |
| `TAVILY_API_KEY` | Tavily | Live financial web search tool |
| `POLYGON_API_KEY` | Polygon.io | Fundamental company financial statements tool |

---

## Local Quickstart

### Method 1: Using Docker Compose (Recommended)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Areeb-Ahmd/StockMind.git
   cd StockMind
   ```

2. **Create and Populate Environment File:**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your API keys:
   ```env
   GOOGLE_API_KEY="your-google-gemini-api-key"
   GROQ_API_KEY="your-groq-api-key"
   PINECONE_API_KEY="your-pinecone-api-key"
   TAVILY_API_KEY="your-tavily-api-key"
   POLYGON_API_KEY="your-polygon-api-key"
   ```

3. **Build and Launch Containers:**
   ```bash
   docker compose up --build
   ```

4. **Access the Applications:**
   - **Frontend UI (Streamlit):** [http://localhost:8501](http://localhost:8501)
   - **Backend API (FastAPI):** [http://localhost:8000](http://localhost:8000)
   - **API Healthcheck:** [http://localhost:8000/health](http://localhost:8000/health)

---

### Method 2: Manual Local Setup (Without Docker)

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **Frontend Setup (in a separate terminal):**
   ```bash
   cd frontend
   python -m venv venv
   # Activate virtualenv as above
   pip install -r requirements.txt
   
   # Set backend URL and launch Streamlit
   set BACKEND_URL=http://localhost:8080
   streamlit run streamlit_ui.py --server.port=8501
   ```

---

## Architecture & Data Flow

```
                                 ┌───────────────────────────┐
                                 │   User Query / Document   │
                                 └─────────────┬─────────────┘
                                               │
                                               ▼
                                 ┌───────────────────────────┐
                                 │       Streamlit UI        │
                                 │  (frontend/streamlit_ui)  │
                                 └─────────────┬─────────────┘
                                               │
                                  POST /query  │  POST /upload
                                               ▼
                                 ┌───────────────────────────┐
                                 │      FastAPI Backend      │
                                 │     (backend/main.py)     │
                                 └─────────────┬─────────────┘
                                               │
                                               ▼
                                 ┌───────────────────────────┐
                                 │      LangGraph Agent      │
                                 │   (agent/workflow.py)     │
                                 └─────────────┬─────────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
    ┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────────┐
    │   retriever_tool    │         │     tavilytool      │         │   financials_tool   │
    │  (Pinecone Vector)  │         │   (Tavily Search)   │         │ (Polygon Financials)│
    └─────────────────────┘         └─────────────────────┘         └─────────────────────┘
```

1. **Document Ingestion Workflow:**
   - Users upload PDF or DOCX research files via the Streamlit sidebar.
   - Streamlit forwards files to `POST /upload` on the FastAPI backend.
   - `DataIngestion` processes files using `PyPDFLoader` or `Docx2txtLoader`, splits text using `RecursiveCharacterTextSplitter`, embeds chunks with Google Embeddings, and stores vectors in Pinecone index (`stockmind-vdb`).

2. **Query & Agent Execution Workflow:**
   - User submits a question through the chat interface or capability prompt cards.
   - Streamlit posts the query payload `{"question": "..."}` to `POST /query`.
   - FastAPI invokes the pre-built `LangGraph` graph (`GraphBuilder`).
   - Primary LLM (Google Gemini) evaluates the prompt against system instructions and determines whether to call `retriever_tool`, `financials_tool`, or `tavilytool`.
   - If Google Gemini hits a rate limit or service error, LangChain's fallback automatically routes the query to Groq (`openai/gpt-oss-120b`).
   - Tool outputs are returned to the LLM node, which synthesizes a formatted Markdown answer.

---

## Deployment to Google Cloud Run (CI/CD)

StockMind features an automated **GitHub Actions** deployment pipeline (`.github/workflows/deploy.yml`) that builds multi-stage Docker images for backend and frontend services, pushes them to **Google Artifact Registry**, and deploys them to **Google Cloud Run** (`asia-south1`) on every commit pushed to `main`.

### Setup Steps for Cloud Run Deployment

1. **Enable Google Cloud APIs:**
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
   ```

2. **Create Artifact Registry Repository:**
   ```bash
   gcloud artifacts repositories create stockmind-repo \
     --repository-format=docker \
     --location=asia-south1
   ```

3. **Configure GitHub Repository Secrets:**
   In your GitHub repository, navigate to **Settings → Secrets and variables → Actions** and add:
   - `GCP_PROJECT_ID`: Your GCP project ID (e.g. `stockmind-504615`)
   - `GCP_REGION`: Target region (e.g. `asia-south1`)
   - `GCP_SA_KEY`: Service Account key JSON with Cloud Run Admin, Artifact Registry Writer, and Secret Manager Accessor roles.
   - `GOOGLE_API_KEY`, `GROQ_API_KEY`, `PINECONE_API_KEY`, `TAVILY_API_KEY`, `POLYGON_API_KEY`.

---

## License & Disclaimer

This software is for **educational and research purposes only**. Information provided by StockMind does not constitute financial advice, investment recommendations, or official financial endorsements.

