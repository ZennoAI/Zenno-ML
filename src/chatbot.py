import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory
from langchain.chains.conversation.memory import ConversationSummaryMemory
from src.prompt_template import initial_template, summary_prompt_template
from src.retriever import create_retriever


load_dotenv()
api_key = os.getenv("API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

def init_memory():   
  memory = ConversationSummaryMemory(
    llm=OpenAI(openai_api_key=api_key, temperature=0.0),
    chat_memory=ChatMessageHistory(),
    prompt=summary_prompt_template(),
    input_key='question',
    return_messages=True,
    human_prefix='Human',
    ai_prefix='AI',
    memory_key='chat_history',
    output_key='answer',
  )
  
  return memory

def load_chain():
  """Logic for loading the chain"""
  llm: OpenAI = OpenAI(openai_api_key=api_key,
                                streaming=True,
                                temperature=0.0,
                                max_tokens=1500)
  
  prompt_template = initial_template()

  retriever = create_retriever(api_key, pinecone_api_key, pinecone_env)

  customer_service_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=init_memory(),
    get_chat_history=lambda h: h,
    chain_type='stuff',
    combine_docs_chain_kwargs={'prompt': prompt_template},
    return_source_documents=True,
    verbose=True,
  )

  return customer_service_chain
