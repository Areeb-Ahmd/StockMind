from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from langchain_core.messages import HumanMessage
from agent.workflow import GraphBuilder
from data_models.models import QuestionRequest
from utils.response_formatter import extract_text_content

router = APIRouter(tags=["Chat Workflow"])

@router.post("/query")
async def query_chatbot(request: QuestionRequest, req: Request):
    try:
        graph = getattr(req.app.state, "graph", None)
        if graph is None:
            graph_service = GraphBuilder()
            graph_service.build()
            graph = graph_service.get_graph()

        result = graph.invoke({"messages": [HumanMessage(content=request.question)]})

        if isinstance(result, dict) and "messages" in result and result["messages"]:
            raw_content = result["messages"][-1].content
            final_output = extract_text_content(raw_content)
        else:
            final_output = str(result)

        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
