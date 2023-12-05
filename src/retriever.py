from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
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
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    
    # TODO: Index name hardcoded for now
    index = pinecone.Index('assuria')
    vectorstore = Pinecone(index, embedding, "text")
    
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 2})

    return retriever
