import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()

web_scraper_url = os.getenv("WEB_SCRAPER_URL")
api_key = os.getenv("API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

def delete_embedding():
  embeddings = OpenAIEmbeddings(openai_api_key=api_key)
  index = pinecone.Index("assuria")
  vectorstore = Pinecone(index, embeddings, "text")
  vectorstore.delete()