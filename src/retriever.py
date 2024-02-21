from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
import pinecone

def create_retriever(api_key: str, pinecone_api_key: str, pinecone_env: str) -> Pinecone:
    """Creates a Pinecone retriever for vector embeddings search.
    Args:
        api_key (str): The OpenAI API key.
        pinecone_api_key (str): The Pinecone API key.
        pinecone_env (str): The Pinecone environment.
    Returns:
        PineconeRetriever: A retriever for vector embeddings search.
    """
    embedding = OpenAIEmbeddings(openai_api_key=api_key)
    # TODO: Index name hardcoded for now
    vectorstore = Pinecone(
      pinecone_api_key=pinecone_api_key, 
      index_name='assuria', 
      embedding=embedding
      )
    
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 1})

    return retriever
