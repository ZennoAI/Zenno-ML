import os
import bentoml
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from prompt_template import template
from pinecone_init import initialize_vector_db


load_dotenv()
api_key = os.getenv("API_KEY")

def load_chain():
  """Logic for loading the chain"""
  prompt_template = template(

  )
  llm = ChatOpenAI(api_key, temperature=0)

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