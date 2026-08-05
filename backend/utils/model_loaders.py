import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config_loader import load_config
from langchain_groq import ChatGroq

class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()

    def _validate_env(self):
        """
        Validate necessary environment variables.
        """
        required_vars = ["GOOGLE_API_KEY","GROQ_API_KEY"]
        self.groq_api_key=os.getenv("GROQ_API_KEY")
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self):
        """
        Load and return the embedding model.
        """
        print("Loading Embedding model")
        model_name=self.config["embedding_model"]["model_name"]
        return GoogleGenerativeAIEmbeddings(model=model_name)

    def load_llm(self):
        """
        Load and return the primary LLM (Google Gemini) and fallback LLM (Groq).
        """
        print("Loading Primary LLM (Google Gemini)...")
        google_cfg = self.config.get("llm", {}).get("primary") or self.config.get("llm", {}).get("google", {})
        google_model_name = google_cfg.get("model_name", "gemini-3.1-flash-lite")
        primary_llm = ChatGoogleGenerativeAI(
            model=google_model_name,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        print("Loading Fallback LLM (Groq)...")
        groq_cfg = self.config.get("llm", {}).get("fallback") or self.config.get("llm", {}).get("groq", {})
        groq_model_name = groq_cfg.get("model_name", "openai/gpt-oss-120b")
        fallback_llm = ChatGroq(
            model=groq_model_name,
            api_key=self.groq_api_key
        )

        return primary_llm, fallback_llm