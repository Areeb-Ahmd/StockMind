from setuptools import find_packages, setup

setup(
    name = "stockmind",
    version = "0.0.1",
    description = "StockMind – Agentic Stock Market Assistant",
    author = "Syed Areeb Ahmad",
    author_email = "ahmad.syedareeb7@gmail.com",
    packages = find_packages(),
    install_requires = [
        'langchain',
        'langgraph',
        'tavily-python',
        'polygon',
        'langchain-community',
        'langchain-google-genai',
        'langchain-groq',
        'langchain-pinecone',
        'streamlit',
        'fastapi',
        'uvicorn',
        'pypdf',
        'docx2txt',
        'python-dotenv',
        'pyyaml'
    ]
)