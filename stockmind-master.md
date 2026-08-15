# StockMind Master Engineering Roadmap & Phase Breakdown

## Overview

This master document outlines the multi-phase refactoring and optimization plan for the **StockMind** codebase. Each phase addresses a focused set of audited architectural, operational, and performance issues while retaining the modular design pattern of the project.

---

## Master Phase Implementation Checklist

- [x] **Phase 1: Core System Prompt, Exception Handling & Config Safety**
  - [x] `SYSTEM_PROMPT` defined in `backend/prompt_library/prompt.py` & injected in `backend/agent/workflow.py`
  - [x] Safe `NoneType` traceback handling in `backend/exception/exceptions.py`
  - [x] Dynamic absolute path resolution in `backend/utils/config_loader.py`
  - [x] Safe module wrapper initialization in `backend/toolkit/tools.py`
  - [x] Phase 1 Handover document created for Phase 2 agent transition

- [ ] **Phase 2: RAG Retriever Tool Optimization & Ingestion Leak Fix**
  - [ ] Detailed, informative docstring for `retriever_tool` in `backend/toolkit/tools.py`
  - [ ] `os.unlink()` temp file cleanup in `backend/data_ingestion/ingestion_pipeline.py`
  - [ ] Lazy vectorstore retriever caching in `backend/toolkit/tools.py`
  - [ ] Phase 2 Handover document created for Phase 3 agent transition

- [ ] **Phase 3: Agent Lifespan Management, Singleton Graph Caching & Cloud Logging**
  - [ ] `@asynccontextmanager` lifespan graph caching in `backend/main.py`
  - [ ] Standard output (`sys.stdout`) log routing in `backend/custom_logging/my_logger.py`
  - [ ] Phase 3 Handover document created for Phase 4 agent transition

- [ ] **Phase 4: Frontend UI Modernization & Local Port Alignment**
  - [ ] Local backend port fallback alignment in `frontend/streamlit_ui.py`
  - [ ] Native `st.chat_message()` and `st.chat_input()` refactor in `frontend/streamlit_ui.py`
  - [ ] Final Master Roadmap Handover & Sign-off completed

---

## Phase 1: Core System Prompt, Exception Handling & Config Safety

### 1. Objectives & Audited Issues
- **Issue 1.1: System Prompt Definition (`backend/prompt_library/prompt.py` & `backend/agent/workflow.py`)**
  - *Problem:* `prompt.py` is currently empty. The agent invokes the LLM without financial guardrails, system instructions, or fallback routing rules.
  - *Solution:* Define a structured financial agent prompt in `prompt.py` and inject it as a `SystemMessage` into the state graph in `workflow.py`.
- **Issue 1.2: Unsafe Traceback Access (`backend/exception/exceptions.py`)**
  - *Problem:* `StockMindException` accesses `exc_tb.tb_lineno` assuming `exc_tb` is non-null. If `exc_tb` is `None`, an `AttributeError` is raised.
  - *Solution:* Add null-checking for `exc_tb` and fallback string representation.
- **Issue 1.3: Relative Path Fragility (`backend/utils/config_loader.py`)**
  - *Problem:* `load_config` opens `"config/config.yaml"` relative to CWD, breaking when scripts are executed outside `backend/`.
  - *Solution:* Resolve `config.yaml` path dynamically using `os.path.dirname(__file__)`.
- **Issue 1.4: Safe Tool Wrapper Instantiation (`backend/toolkit/tools.py`)**
  - *Problem:* `PolygonAPIWrapper` is instantiated at module top-level without error handling if environment variables are missing during initial import.
  - *Solution:* Protect module-level wrapper initialization with fallback logic or lazy instantiation.

### 2. Git Flow Strategy — Phase 1 Start
Run the following commands to initialize the feature branch from latest `main`:

```bash
git checkout main
git fetch origin main
git pull origin main
git checkout -b feature/phase1-prompt-exception-config-refactor
```

### 3. Modular Implementation Plan

#### Component: `backend/prompt_library/prompt.py`
- Define `SYSTEM_PROMPT` containing financial analyst instructions, tool usage guidance (Pinecone retriever vs. Tavily search vs. Polygon financials), formatting expectations, and financial disclaimers.

#### Component: `backend/agent/workflow.py`
- Modify `_chatbot_node` to prepend `SystemMessage(content=SYSTEM_PROMPT)` to the conversation state messages prior to calling `self.llm_with_tools.invoke()`.

#### Component: `backend/exception/exceptions.py`
- Update `StockMindException.__init__` to check `if exc_tb is not None:` before extracting line numbers and file names, providing default values when `exc_tb` is unavailable.

#### Component: `backend/utils/config_loader.py`
- Calculate absolute base path relative to `config_loader.py`: `os.path.abspath(os.path.join(os.path.dirname(__file__), "../config/config.yaml"))`.

### 4. Manual Verification & Test Plan
Execute the following verification steps locally before requesting push approval:

```bash
# 1. Test Config Loader from root directory
python -c "from backend.utils.config_loader import load_config; print(load_config())"

# 2. Test Exception Handling with null traceback
python -c "from backend.exception.exceptions import StockMindException; print(str(StockMindException('Test error', sys)))"

# 3. Test Agent Workflow System Prompt Injection
python -c "from backend.agent.workflow import GraphBuilder; g = GraphBuilder(); g.build(); print(g.get_graph())"
```

### 5. Push & Pull Request Strategy — Phase 1 Finish

#### Step 1: Wait for Manual User Approval
> **IMPORTANT:** Do NOT push code to remote until the user manually verifies local execution and explicitly grants approval.

#### Step 2: Push Branch to Remote
Once approved, push the local feature branch to GitHub:

```bash
git add backend/prompt_library/prompt.py backend/agent/workflow.py backend/exception/exceptions.py backend/utils/config_loader.py backend/toolkit/tools.py
git commit -m "refactor(core): implement system prompt, safe exception handling, and dynamic config paths

- Add domain-specific financial system prompt in prompt_library/prompt.py
- Inject SystemMessage in agent/workflow.py graph execution
- Fix unsafe NoneType traceback dereferencing in StockMindException
- Update config_loader.py to resolve config.yaml using absolute file paths
- Add safe initialization wrapper for Polygon API tool in tools.py"
git push origin feature/phase1-prompt-exception-config-refactor
```

#### Step 3: GitHub PR Template for Phase 1
````markdown
# Pull Request: Core System Prompt, Exception Handling & Config Safety Refactor

## PR Title
`refactor(core): add system prompt, safe exception traceback, and absolute config resolution`

## Summary of Changes
- **`backend/prompt_library/prompt.py`**: Added detailed `SYSTEM_PROMPT` for stock market analysis and tool selection guidance.
- **`backend/agent/workflow.py`**: Updated `_chatbot_node` to prepend `SystemMessage` to execution state.
- **`backend/exception/exceptions.py`**: Protected `exc_tb` access against `NoneType` errors.
- **`backend/utils/config_loader.py`**: Resolved `config.yaml` path dynamically using file location rather than CWD.
- **`backend/toolkit/tools.py`**: Protected module-level tool instantiation against missing environment variables.

## Composite & Internal Impact Matrix

| Area / Component | Impact Level | Description of Impact |
|---|---|---|
| AI Search & Chat Agent | High | LLM now operates with explicit financial analyst persona and tool rules |
| Exception Handling | Medium | Prevents silent error masking on system exceptions |
| Configuration Loading | High | Enables CLI scripts and unit tests to run from any working directory |
| Financial Tools | Low | Prevents module import crashes when environment keys are unconfigured |

## Testing & Verification

### Verification Commands Executed
```bash
python -c "from backend.utils.config_loader import load_config; print(load_config())"
python -c "from backend.exception.exceptions import StockMindException; print(str(StockMindException('Test error', sys)))"
python -c "from backend.agent.workflow import GraphBuilder; g = GraphBuilder(); g.build(); print(g.get_graph())"
```

### Execution Summary & Checklist
- [x] Config loads cleanly regardless of execution directory.
- [x] Exception formatter succeeds without `AttributeError` when traceback is missing.
- [x] LangGraph agent compiles and injects system prompt.
````

### 6. Phase Handover & Agent Context Transition Protocol
At the conclusion of Phase 1:
1. Update the **Master Phase Implementation Checklist** in this document marking Phase 1 items as complete (`[x]`).
2. Generate a structured **Phase 1 Handover Summary** for the agent taking on Phase 2, detailing:
   - Modified modules and new exports (`backend.prompt_library.prompt.SYSTEM_PROMPT`).
   - Verified configuration state and baseline tests passed.
   - Key assumptions and preconditions for Phase 2 (RAG Retriever Optimization).

---

## Phase 2: RAG Retriever Tool Optimization & Document Ingestion Leak Fix

### 1. Objectives & Audited Issues
- **Issue 2.1: Retriever Tool Docstring & Description (`backend/toolkit/tools.py`)**
  - *Problem:* `retriever_tool` has the description `"""this is retriever tool"""`, confusing the agent LLM.
  - *Solution:* Provide a clear, detailed description explaining that the tool searches vector embeddings of uploaded stock market PDF and DOCX reports.
- **Issue 2.2: Temporary File Disk Leak (`backend/data_ingestion/ingestion_pipeline.py`)**
  - *Problem:* `load_documents()` writes files using `NamedTemporaryFile(delete=False)` and never unlinks `temp_path`.
  - *Solution:* Wrap document parsing in a `try...finally` block that removes `temp_path` with `os.unlink()` after loading.
- **Issue 2.3: Tool Connection & VectorStore Caching (`backend/toolkit/tools.py`)**
  - *Problem:* `retriever_tool` recreates `Pinecone()`, `PineconeVectorStore`, and embedding model instances on every query.
  - *Solution:* Implement lazy singleton caching for Pinecone retriever objects.

### 2. Git Flow Strategy — Phase 2 Start
Run the following commands to initialize the feature branch from latest `main`:

```bash
git checkout main
git fetch origin main
git pull origin main
git checkout -b feature/phase2-retriever-ingestion-leak-fix
```

### 3. Modular Implementation Plan

#### Component: `backend/toolkit/tools.py`
- Update `@tool(args_schema=RagToolSchema)` docstring to:
  ```python
  """Search and retrieve relevant context from uploaded stock market financial documents, annual reports, and trading guides stored in the Pinecone vector database."""
  ```
- Implement cached helper `get_retriever()` so vector store connection is reused across tool calls.

#### Component: `backend/data_ingestion/ingestion_pipeline.py`
- Modify `load_documents` to ensure `os.unlink(temp_path)` is executed in a `finally` block for each parsed file.

### 4. Manual Verification & Test Plan
Execute the following verification steps locally before requesting push approval:

```bash
# 1. Test temporary file cleanup during document ingestion
python -c "from backend.data_ingestion.ingestion_pipeline import DataIngestion; print(DataIngestion)"

# 2. Test retriever tool definition and docstring
python -c "from backend.toolkit.tools import retriever_tool; print(retriever_tool.description)"
```

### 5. Push & Pull Request Strategy — Phase 2 Finish

#### Step 1: Wait for Manual User Approval
> **IMPORTANT:** Do NOT push code to remote until the user manually verifies local execution and explicitly grants approval.

#### Step 2: Push Branch to Remote
Once approved, push the local feature branch to GitHub:

```bash
git add backend/toolkit/tools.py backend/data_ingestion/ingestion_pipeline.py
git commit -m "fix(rag): update retriever tool description, fix temp file leak, and cache vectorstore

- Add detailed docstring to retriever_tool for accurate ReAct agent tool selection
- Ensure temporary files in ingestion_pipeline.py are unlinked in finally block
- Implement lazy singleton caching for Pinecone vectorstore retriever instance"
git push origin feature/phase2-retriever-ingestion-leak-fix
```

#### Step 3: GitHub PR Template for Phase 2
````markdown
# Pull Request: RAG Retriever Tool Optimization & Ingestion Leak Fix

## PR Title
`fix(rag): optimize retriever tool docstring, fix temp file leak, and cache vector store`

## Summary of Changes
- **`backend/toolkit/tools.py`**: Added informative docstring for `retriever_tool` to guide LLM tool routing. Added lazy caching for vector store retriever.
- **`backend/data_ingestion/ingestion_pipeline.py`**: Added explicit `os.unlink(temp_path)` cleanup inside `finally` block during document parsing.

## Composite & Internal Impact Matrix

| Area / Component | Impact Level | Description of Impact |
|---|---|---|
| Vector Search Retriever | High | Agent reliably selects retrieval tool for uploaded document questions |
| Ingestion Pipeline | High | Eliminates disk space leak on file uploads |
| API Performance | Medium | Reuses Pinecone client connection across retrieval calls |

## Testing & Verification

### Verification Commands Executed
```bash
python -c "from backend.toolkit.tools import retriever_tool; print(retriever_tool.description)"
python -c "from backend.data_ingestion.ingestion_pipeline import DataIngestion; print(DataIngestion)"
```

### Execution Summary & Checklist
- [x] Retriever tool description is recognized by LangChain agent.
- [x] Temporary files are removed from `/tmp` immediately after parsing.
- [x] Vector store connection reuses cached instance.
````

### 6. Phase Handover & Agent Context Transition Protocol
At the conclusion of Phase 2:
1. Update the **Master Phase Implementation Checklist** in this document marking Phase 2 items as complete (`[x]`).
2. Generate a structured **Phase 2 Handover Summary** for the agent taking on Phase 3, detailing:
   - Reusable vectorstore retriever initialization patterns.
   - Resource cleanup behaviors verified in document ingestion.
   - Key assumptions for Phase 3 (FastAPI Lifespan & Graph Caching).

---

## Phase 3: Agent Lifespan Management, Singleton Graph Caching & Cloud Logging

### 1. Objectives & Audited Issues
- **Issue 3.1: Dynamic Model & Graph Re-instantiation (`backend/main.py` & `backend/agent/workflow.py`)**
  - *Problem:* `GraphBuilder` builds models and state graphs dynamically inside `/query` handler on every HTTP request.
  - *Solution:* Implement FastAPI lifespan context manager (`@asynccontextmanager`) to load and cache the agent graph instance once at server startup.
- **Issue 3.2: Container Logging Adaptation (`backend/custom_logging/my_logger.py`)**
  - *Problem:* `my_logger.py` logs to local timestamped files in `./logs`, which are lost or inaccessible on Google Cloud Run.
  - *Solution:* Configure `StreamHandler(sys.stdout)` alongside optional file logging so logs stream directly to GCP Cloud Logging.

### 2. Git Flow Strategy — Phase 3 Start
Run the following commands to initialize the feature branch from latest `main`:

```bash
git checkout main
git fetch origin main
git pull origin main
git checkout -b feature/phase3-lifespan-caching-cloud-logging
```

### 3. Modular Implementation Plan

#### Component: `backend/main.py`
- Add `@asynccontextmanager` `lifespan` handler to `FastAPI(lifespan=lifespan)`.
- Initialize single global `GraphBuilder` instance during startup and store graph in `app.state.graph`.
- Update POST `/query` to access `request.app.state.graph`.

#### Component: `backend/custom_logging/my_logger.py`
- Update `logging.basicConfig` or logger handlers to add a `logging.StreamHandler(sys.stdout)` so logs appear in standard container output streams.

### 4. Manual Verification & Test Plan
Execute the following verification steps locally before requesting push approval:

```bash
# 1. Test FastAPI app startup and lifespan state compilation
python -c "from backend.main import app; print(app)"

# 2. Test stdout stream logging output
python -c "from backend.custom_logging.my_logger import logger; logger.info('Test stdout logging')"
```

### 5. Push & Pull Request Strategy — Phase 3 Finish

#### Step 1: Wait for Manual User Approval
> **IMPORTANT:** Do NOT push code to remote until the user manually verifies local execution and explicitly grants approval.

#### Step 2: Push Branch to Remote
Once approved, push the local feature branch to GitHub:

```bash
git add backend/main.py backend/custom_logging/my_logger.py
git commit -m "perf(backend): add FastAPI lifespan graph caching and stdout cloud logging

- Implement async lifespan context manager in main.py to cache compiled agent graph
- Reuse app.state.graph across /query requests to eliminate per-request setup latency
- Add StreamHandler to my_logger.py for GCP Cloud Run log compatibility"
git push origin feature/phase3-lifespan-caching-cloud-logging
```

#### Step 3: GitHub PR Template for Phase 3
````markdown
# Pull Request: Agent Lifespan Management & Cloud Logging Adaptation

## PR Title
`perf(backend): cache agent graph in FastAPI lifespan and route logs to stdout`

## Summary of Changes
- **`backend/main.py`**: Added FastAPI lifespan manager to pre-compile and store agent state graph in `app.state.graph`.
- **`backend/custom_logging/my_logger.py`**: Configured `StreamHandler(sys.stdout)` for Cloud Run container logging.

## Composite & Internal Impact Matrix

| Area / Component | Impact Level | Description of Impact |
|---|---|---|
| Query API Endpoint | High | Substantially reduces latency per request by removing object rebuilds |
| Logging Infrastructure | High | Enables real-time log streaming in GCP Cloud Logging |
| Application Lifecycle | Medium | Clean startup/shutdown initialization pattern |

## Testing & Verification

### Verification Commands Executed
```bash
python -c "from backend.main import app; print(app)"
python -c "from backend.custom_logging.my_logger import logger; logger.info('Test stdout logging')"
```

### Execution Summary & Checklist
- [x] Agent state graph compiles once during application startup.
- [x] `/query` endpoint successfully executes using cached graph instance.
- [x] Logs stream cleanly to stdout.
````

### 6. Phase Handover & Agent Context Transition Protocol
At the conclusion of Phase 3:
1. Update the **Master Phase Implementation Checklist** in this document marking Phase 3 items as complete (`[x]`).
2. Generate a structured **Phase 3 Handover Summary** for the agent taking on Phase 4, detailing:
   - Server lifecycle state (`app.state.graph`).
   - Logging stream configurations verified.
   - Key assumptions for Phase 4 (Frontend UI Modernization & Local Port Alignment).

---

## Phase 4: Frontend UI Modernization & Local Port Alignment

### 1. Objectives & Audited Issues
- **Issue 4.1: Local Port Default Consistency (`frontend/streamlit_ui.py` & `docker-compose.yml`)**
  - *Problem:* `streamlit_ui.py` defaults `BASE_URL` fallback to `http://localhost:8000`, while local backend scripts run on port `8080`.
  - *Solution:* Standardize local development fallback port configuration across frontend and backend.
- **Issue 4.2: Streamlit Native Chat UI Upgrade (`frontend/streamlit_ui.py`)**
  - *Problem:* Chat messages use plain markdown strings instead of Streamlit native `st.chat_message()` components.
  - *Solution:* Modernize rendering using `st.chat_message("user")` and `st.chat_message("assistant")`.

### 2. Git Flow Strategy — Phase 4 Start
Run the following commands to initialize the feature branch from latest `main`:

```bash
git checkout main
git fetch origin main
git pull origin main
git checkout -b feature/phase4-frontend-ui-port-alignment
```

### 3. Modular Implementation Plan

#### Component: `frontend/streamlit_ui.py`
- Update default `BACKEND_URL` fallback logic to `http://localhost:8080` (or matching environment default).
- Refactor message history rendering loop to use `with st.chat_message(chat["role"]): st.write(chat["content"])`.
- Use `st.chat_input()` for user message submission.

### 4. Manual Verification & Test Plan
Execute the following verification steps locally before requesting push approval:

```bash
# 1. Verify Streamlit UI script syntax
python -m py_compile frontend/streamlit_ui.py
```

### 5. Push & Pull Request Strategy — Phase 4 Finish

#### Step 1: Wait for Manual User Approval
> **IMPORTANT:** Do NOT push code to remote until the user manually verifies local execution and explicitly grants approval.

#### Step 2: Push Branch to Remote
Once approved, push the local feature branch to GitHub:

```bash
git add frontend/streamlit_ui.py
git commit -m "style(frontend): modernize Streamlit chat UI and align default backend port

- Update fallback BACKEND_URL default port to match backend default
- Refactor chat history rendering to native st.chat_message components
- Replace custom form input with native st.chat_input"
git push origin feature/phase4-frontend-ui-port-alignment
```

#### Step 3: GitHub PR Template for Phase 4
````markdown
# Pull Request: Modernize Streamlit Chat UI & Align Default Port

## PR Title
`style(frontend): upgrade to native Streamlit chat components and update backend port default`

## Summary of Changes
- **`frontend/streamlit_ui.py`**: Replaced custom HTML/Markdown chat loops with native `st.chat_message` and `st.chat_input`. Updated default backend fallback URL to port 8080.

## Composite & Internal Impact Matrix

| Area / Component | Impact Level | Description of Impact |
|---|---|---|
| Streamlit UI | High | Sleek, native UI experience with proper assistant/user avatar blocks |
| Local DX | Medium | Prevents connection refused errors when running frontend and backend locally |

## Testing & Verification

### Verification Commands Executed
```bash
python -m py_compile frontend/streamlit_ui.py
```

### Execution Summary & Checklist
- [x] Streamlit script compiles cleanly without syntax errors.
- [x] Chat history renders using native Streamlit chat bubbles.
````

### 6. Phase Handover & Agent Context Transition Protocol
At the conclusion of Phase 4:
1. Update the **Master Phase Implementation Checklist** in this document marking all phases as complete (`[x]`).
2. Generate a **Final Master Project Handover Summary** confirming that all audited issues across the 4 phases have been resolved, verified, and merged.
