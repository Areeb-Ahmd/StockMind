# Agentic Trading Bot

An LLM-powered, tool-augmented chatbot for stock market research and financial analysis, built with LangGraph, LangChain, and a Retrieval-Augmented Generation (RAG) pipeline backed by Pinecone.

## Overview

This project implements a conversational AI agent that can answer questions about the stock market by combining three information sources:

1. **Private knowledge base** -- Users upload PDF or DOCX documents (e.g. trading guides, market reports) which are chunked, embedded, and stored in a Pinecone vector database. A retriever tool performs similarity search over this knowledge base at query time.
2. **Live web search** -- A Tavily search tool provides the agent with up-to-date information from the internet.
3. **Financial data API** -- A Polygon.io financials tool gives the agent access to company financial data (income statements, balance sheets, etc.).

The agent is orchestrated as a **LangGraph state graph** with a ReAct-style tool-use loop: the LLM decides which tools to call (if any), the tool results are fed back, and the LLM produces a final answer. A primary LLM (Google Gemini) is used with automatic failover to a fallback LLM (Groq) if the primary encounters errors or rate limits.

The system is exposed via a **FastAPI** backend with two endpoints (`/upload` and `/query`) and a **Streamlit** frontend that provides a chat interface with document upload capabilities.

## Key Features

- **RAG pipeline** with PDF and DOCX ingestion, recursive text splitting, and Pinecone vector storage with configurable batch sizes and rate-limit retry logic.
- **Multi-tool agent** powered by LangGraph that autonomously selects between a vector store retriever, Tavily web search, and Polygon.io financial data based on the user's question.
- **Dual-LLM architecture** with automatic failover from Google Gemini (primary) to Groq (fallback) using LangChain's `with_fallbacks`.
- **Configurable parameters** via a central YAML config file for embedding models, LLM providers, retriever thresholds, ingestion batching, and tool settings.
- **Streamlit chat UI** with a sidebar for document upload and a conversational message history.
- **FastAPI REST API** for programmatic access to document ingestion and querying.
- **Structured logging** with timestamped log files written to a `logs/` directory.
- **Custom exception handling** with detailed tracebacks (file name, line number, error message).

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Agent Framework | LangGraph, LangChain |
| Primary LLM | Google Gemini (via `langchain-google-genai`) |
| Fallback LLM | Groq (via `langchain-groq`) |
| Embeddings | Google Generative AI Embeddings (`gemini-embedding-001`) |
| Vector Database | Pinecone (via `langchain-pinecone`) |
| Web Search | Tavily (via `tavily-python`) |
| Financial Data | Polygon.io (via `polygon` + LangChain `PolygonFinancials`) |
| Backend API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Document Parsing | PyPDF (`pypdf`), Docx2txt (`docx2txt`) |
| Configuration | YAML (`PyYAML`), python-dotenv |

## Project Structure

```
.
├── agent/
│   └── workflow.py            # LangGraph state graph definition (chatbot + tool nodes)
├── config/
│   └── config.yaml            # Central configuration (models, retriever, ingestion, tools)
├── custom_logging/
│   └── my_logger.py           # Logging setup with timestamped log files
├── data_ingestion/
│   └── ingestion_pipeline.py  # Document loading, chunking, and Pinecone ingestion
├── data_models/
│   └── models.py              # Pydantic schemas (QuestionRequest, RagToolSchema)
├── exception/
│   └── exceptions.py          # Custom TradingBotException with traceback details
├── fallback_data/             # Sample documents (PDFs, DOCX) for the knowledge base
├── notebook/
│   └── experiments.ipynb      # Jupyter notebook for experimentation
├── prompt_library/
│   └── prompt.py              # Placeholder for prompt templates (currently empty)
├── toolkit/
│   └── tools.py               # Tool definitions (retriever, Tavily search, Polygon financials)
├── utils/
│   ├── config_loader.py       # YAML config file loader
│   ├── model_loaders.py       # Embedding and LLM model initialization
│   └── response_formatter.py  # Extracts clean text from LLM response content
├── main.py                    # FastAPI application (POST /upload, POST /query)
├── streamlit_ui.py            # Streamlit chat frontend
├── setup.py                   # Package setup configuration
└── requirements.txt           # Python dependencies
```

## Prerequisites

- **Python 3.x** (the project uses a standard `venv`; no specific version is pinned)
- API keys for the following services:

| Environment Variable | Service | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | Google AI (Gemini) | Primary LLM and embedding model |
| `GROQ_API_KEY` | Groq | Fallback LLM |
| `PINECONE_API_KEY` | Pinecone | Vector database storage and retrieval |
| `TAVILY_API_KEY` | Tavily | Web search tool |
| `POLYGON_API_KEY` | Polygon.io | Financial data tool |

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Areeb-Ahmd/Agentic-Trading-Bot.git
   cd Agentic-Trading-Bot
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   This will also install the project itself in editable mode (via `-e .` in `requirements.txt`), which runs `setup.py` and installs the package as `agentic-trading-bot`.

## Configuration

### Environment Variables

Create a `.env` file in the project root with your API keys:

```env
GOOGLE_API_KEY="your-google-api-key"
GROQ_API_KEY="your-groq-api-key"
PINECONE_API_KEY="your-pinecone-api-key"
TAVILY_API_KEY="your-tavily-api-key"
POLYGON_API_KEY="your-polygon-api-key"
```

The application loads these via `python-dotenv` at startup. All five keys are required for full functionality.

### YAML Configuration

Model parameters, retriever settings, and ingestion behavior are configured in `config/config.yaml`:

```yaml
vector_db:
  index_name: "agentic-trading-bot-vdb"

ingestion:
  batch_size: 40
  delay_between_batches: 5.0
  max_retries: 5
  retry_initial_delay: 10.0

retriever:
  top_k: 3
  score_threshold: 0.5

embedding_model:
  provider: "google"
  model_name: "models/gemini-embedding-001"

llm:
  primary:
    provider: "google"
    model_name: "gemini-3.1-flash-lite"
  fallback:
    provider: "groq"
    model_name: "openai/gpt-oss-120b"

tools:
  tavily:
    max_results: 5
```

## Usage

### 1. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

The API server starts on `http://localhost:8000` by default with two endpoints:

- **`POST /upload`** -- Accepts multipart file uploads (PDF, DOCX). Files are parsed, chunked, embedded, and stored in Pinecone.
- **`POST /query`** -- Accepts a JSON body `{"question": "your question"}` and returns `{"answer": "..."}` from the agent.

### 2. Launch the Streamlit UI

In a separate terminal:

```bash
streamlit run streamlit_ui.py
```

The Streamlit app connects to the FastAPI backend at `http://localhost:8000`. Use the sidebar to upload documents and the main chat area to ask questions.

### Example API usage with curl

```bash
# Upload documents
curl -X POST http://localhost:8000/upload \
  -F "files=@stock_market.pdf" \
  -F "files=@trading_basics.pdf"

# Query the agent
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the NIFTY 50 index?"}'
```

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

1. **Document ingestion**: Users upload PDF or DOCX files via the `/upload` endpoint or the Streamlit sidebar. The `DataIngestion` pipeline loads the documents, splits them into 1000-character chunks (with 200-character overlap) using `RecursiveCharacterTextSplitter`, embeds them with Google's `gemini-embedding-001` model, and stores the vectors in a Pinecone serverless index. Ingestion is batched with configurable rate-limit retry logic (exponential backoff).

2. **Query processing**: When a user sends a question, the FastAPI backend constructs a LangGraph `StateGraph` with two nodes -- a **chatbot node** (the LLM) and a **tools node** (`ToolNode` with all three tools). The graph starts at the chatbot node.

3. **Tool selection**: The LLM (Google Gemini, with Groq as fallback) decides whether to invoke tools based on the question. LangGraph's `tools_condition` routes to the tools node if the LLM produces tool calls, or to the end if it produces a final answer.

4. **Tool execution**: The `ToolNode` executes the selected tools:
   - **`retriever_tool`**: Queries the Pinecone vector store using similarity search with a score threshold.
   - **`tavilytool`**: Performs an advanced web search via the Tavily API.
   - **`financials_tool`**: Fetches company financial data from Polygon.io.

5. **Response generation**: Tool results are sent back to the chatbot node. The LLM synthesizes a final answer incorporating the tool outputs. The response is extracted using `extract_text_content` (which handles both plain strings and structured content blocks) and returned to the user.

## Disclaimer

This project is intended for **educational and research purposes only**. It does not constitute financial advice, and no part of this software should be used to make real trading or investment decisions. The authors are not responsible for any financial losses incurred from the use of this software. Always consult a qualified financial advisor before making investment decisions.

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

<!-- TODO: No LICENSE file found in the repository. Add a LICENSE file and update this section. -->

This project does not currently include a license file. Please contact the author for licensing information.

## Author

**Syed Areeb Ahmad** -- ahmad.syedareeb7@gmail.com
