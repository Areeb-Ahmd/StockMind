import os
import tempfile
import time
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from utils.model_loaders import ModelLoader
from utils.config_loader import load_config
from pinecone import ServerlessSpec, Pinecone
from uuid import uuid4
import sys
from exception.exceptions import StockMindException
from custom_logging.my_logger import logger

class DataIngestion:
    """
    Class to handle document loading, transformation and ingestion into Pinecone vector store.
    """

    def __init__(self):
        try:
            print("Initializing DataIngestion pipeline...")
            logger.info("Initializing DataIngestion pipeline...")
            self.model_loader = ModelLoader()
            self._load_env_variables()
            self.config = load_config()
        except Exception as e:
            raise StockMindException(e, sys)

    def _load_env_variables(self):
        try:
            load_dotenv()

            required_vars = [
                "GOOGLE_API_KEY",
                "PINECONE_API_KEY"
            ]

            missing_vars = [var for var in required_vars if os.getenv(var) is None]
            if missing_vars:
                raise EnvironmentError(f"Missing environment variables: {missing_vars}")

            self.google_api_key = os.getenv("GOOGLE_API_KEY")
            self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        except Exception as e:
            raise StockMindException(e, sys)

    def load_documents(self, uploaded_files) -> List[Document]:
        try:
            documents = []
            for uploaded_file in uploaded_files:
                file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
                suffix = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path = temp_file.name

                if file_ext == ".pdf":
                    loader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                elif file_ext == ".docx":
                    loader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                else:
                    print(f"Unsupported file type: {uploaded_file.filename}")
            return documents
        except Exception as e:
            raise StockMindException(e, sys)

    def store_in_vector_db(self, documents: List[Document]):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            documents = text_splitter.split_documents(documents)

            pinecone_client = Pinecone(api_key=self.pinecone_api_key)
            index_name = self.config["vector_db"]["index_name"]

            if index_name not in [i.name for i in pinecone_client.list_indexes()]:
                pinecone_client.create_index(
                    name=index_name,
                    dimension=3072,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )

            index = pinecone_client.Index(index_name)
            vector_store = PineconeVectorStore(index=index, embedding=self.model_loader.load_embeddings())
            uuids = [str(uuid4()) for _ in range(len(documents))]

            # Fetch ingestion configs for batching and rate limiting
            ingestion_cfg = self.config.get("ingestion", {})
            batch_size = ingestion_cfg.get("batch_size", 40)
            delay_between_batches = ingestion_cfg.get("delay_between_batches", 5.0)
            max_retries = ingestion_cfg.get("max_retries", 5)
            retry_initial_delay = ingestion_cfg.get("retry_initial_delay", 10.0)

            total_docs = len(documents)
            logger.info(f"Total document chunks to ingest: {total_docs}")
            print(f"Total document chunks to ingest: {total_docs}")

            for i in range(0, total_docs, batch_size):
                batch_docs = documents[i : i + batch_size]
                batch_ids = uuids[i : i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (total_docs + batch_size - 1) // batch_size

                logger.info(f"Ingesting batch {batch_num}/{total_batches} ({len(batch_docs)} chunks)...")
                print(f"Ingesting batch {batch_num}/{total_batches} ({len(batch_docs)} chunks)...")

                retry_count = 0
                current_delay = retry_initial_delay
                while True:
                    try:
                        vector_store.add_documents(documents=batch_docs, ids=batch_ids)
                        break
                    except Exception as batch_err:
                        err_msg = str(batch_err)
                        if ("RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg) and retry_count < max_retries:
                            retry_count += 1
                            logger.warning(
                                f"Rate limit hit on batch {batch_num}/{total_batches}. "
                                f"Retrying ({retry_count}/{max_retries}) after {current_delay}s... Error: {err_msg}"
                            )
                            print(f"Rate limit hit. Retrying ({retry_count}/{max_retries}) in {current_delay}s...")
                            time.sleep(current_delay)
                            current_delay *= 2
                        else:
                            logger.error(f"Failed to ingest batch {batch_num}/{total_batches}: {err_msg}")
                            raise batch_err

                if i + batch_size < total_docs and delay_between_batches > 0:
                    logger.info(f"Waiting {delay_between_batches}s before next batch...")
                    time.sleep(delay_between_batches)

            logger.info("Successfully ingested all document chunks into vector DB.")
            print("Successfully ingested all document chunks into vector DB.")
        except Exception as e:
            raise StockMindException(e, sys)

    def run_pipeline(self, uploaded_files):
        try:
            documents = self.load_documents(uploaded_files)
            if not documents:
                print("No valid documents found.")
                return
            self.store_in_vector_db(documents)
        except Exception as e:
            raise StockMindException(e, sys)

if __name__ == '__main__':
    pass