import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import pinecone

load_dotenv()
api_key = os.getenv("API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")


def initialize_vector_db():
    embedding = OpenAIEmbeddings(openai_api_key=api_key)
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
    index = pinecone.Index('customer')
    vectorstore = Pinecone(index, embedding.embed_query, "text")
    
    retriever = vectorstore.as_retriever(search_type='similarity',
                                      search_kwargs={'k': 4})

    return retriever