import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import pinecone

load_dotenv()
api_key = os.getenv("API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")


def create_vector_embeddings() -> Pinecone:
    """
    Fn to create vector embeddings using OpenAI
    and Pinecone as the vector store
    """
    embedding = OpenAIEmbeddings(openai_api_key=api_key)
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    
    # TODO: Index name hardcoded for now
    index = pinecone.Index('assuria')
    vectorstore = Pinecone(index, embedding, "text")
    
    retriever = vectorstore.as_retriever(search_type='similarity',
                                      search_kwargs={'k': 2})

    return retriever