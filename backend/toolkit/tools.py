import os
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults 
from data_models.models import RagToolSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loaders import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()
try:
    api_wrapper = PolygonAPIWrapper()
    financials_tool = PolygonFinancials(api_wrapper=api_wrapper)
except Exception:
    financials_tool = PolygonFinancials()

model_loader = ModelLoader()
config = load_config()

_retriever_instance = None

def get_retriever():
    global _retriever_instance
    if _retriever_instance is None:
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=pinecone_api_key)
        vector_store = PineconeVectorStore(
            index=pc.Index(config["vector_db"]["index_name"]), 
            embedding=model_loader.load_embeddings()
        )
        _retriever_instance = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": config["retriever"]["top_k"],
                "score_threshold": config["retriever"]["score_threshold"]
            },
        )
    return _retriever_instance

@tool(args_schema=RagToolSchema)
def retriever_tool(question):
    """Search and retrieve relevant context from uploaded stock market financial documents, annual reports, market guides, and custom PDFs/DOCXs stored in the Pinecone vector database."""
    retriever = get_retriever()
    return retriever.invoke(question)

tavilytool = TavilySearchResults(
    max_results=config["tools"]["tavily"]["max_results"],
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    )