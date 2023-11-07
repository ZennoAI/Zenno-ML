import os
import bentoml
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from src.prompt_template import initial_template
from src.pinecone_init import initialize_vector_db
from langchain.llms import OpenLLM


load_dotenv()
api_key = os.getenv("API_KEY")

def load_chain():
  """Logic for loading the chain"""
  llm: ChatOpenAI = ChatOpenAI(openai_api_key=api_key,
                                streaming=True,
                                temperature=0.0)
  
  prompt_template = initial_template()

  retriever = initialize_vector_db()

  customer_service_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    combine_docs_chain_kwargs={'prompt': prompt_template},
    return_source_documents=True,
    verbose=True,
    chain_type='stuff'
  )

  return customer_service_chain
