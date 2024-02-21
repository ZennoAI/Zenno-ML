import os
from dotenv import load_dotenv
from bentoml import Service
from bentoml.io import Text, JSON
from src.chatbot import load_chain
from src.data_processing import DataProcessor
from src.vector_store import VectorStoreManager
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor 
from src.llm_monitoring.whylogs import log_prompt_response, is_not_toxic
from src.lllm_security.security import is_not_prompt_injection

load_dotenv()

web_scraper_url = os.getenv("WEB_SCRAPER_URL")
api_key = os.getenv("API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


class APIHandler:
  """Handles the API requests.
  """
  def __init__(self, data_processor, embeddings_manager):
    self.data_processor = data_processor
    self.embeddings_manager = embeddings_manager

svc = Service(
  'zenno-api-service',
)

@svc.api(input=Text(), output=JSON(), route='api/v1/prompt_response')
def prompt_response(prompt: str) -> str:
  """Generates a response from the prompt.
  Args:
      prompt (str): a prompt to generate a response from
  Returns:
      str: a response from the prompt
  """
  chain = load_chain()
  
  result = None
  
  if is_not_prompt_injection(prompt):
    if is_not_toxic(prompt):
      result = chain(prompt)
      print('resp_question:', result['question'], '\n')
      print('resp_answer:', result['answer'], '\n')
      print('resp_history:', result['chat_history'], '\n')
      
      print('\n\nSources:')
      for source in result['source_documents']:
          print(source.metadata['url'], '\n')
          
    else:
      result = {'answer': 'Sorry, I cannot answer that question. Please try again.'}
          
  else:
    result = {'answer': 'Sorry, I cannot answer that question. Do you have any other questions I can help you with?.'}
    
  log_prompt_response(prompt, result['answer'])
  
  return result

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/create_embeddings')
def create_embeddings_index(data: list()) -> str:
  """Creates an embeddings index from the data.
  Args:
      data (list): a list of data to create embeddings from
  Returns:
      str: a message indicating the status of the embeddings index creation
  """
  handler = APIHandler(DataProcessor(data), VectorStoreManager(api_key, pinecone_api_key, pinecone_env))
  data_chunks = handler.data_processor.process_data()
  msg = handler.embeddings_manager.create_embeddings(data_chunks)
  
  return msg

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/update_embeddings')
def update_embeddings_index(data: list()) -> str:
  """Updates the embeddings index with new data.
  Args:
      data (list): a list of data to update the embeddings index with
  Returns:
      str: a message indicating the status of the embeddings index update
  """
  handler = APIHandler(DataProcessor(data), VectorStoreManager(api_key, pinecone_api_key, pinecone_env))
  data_chunks = handler.data_processor.process_data()
  msg = handler.embeddings_manager.update_embeddings_index(data_chunks)
  
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_embedding')
def delete_embedding(url: str) -> str:
  """Deletes a specific embedding.
  Args:
      url (str): the url of the embedding to delete
  Returns:
      str: a message indicating the status of the embedding deletion
  """
  handler = APIHandler(None, VectorStoreManager(api_key, pinecone_api_key, pinecone_env))
  msg = handler.embeddings_manager.delete_embedding(url)
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_index')
def delete_index(index_name: str) -> str:
  """Deletes the entire index.
  Args:
      index_name (str): the name of the index to delete
  Returns:
      str: a message indicating the status of the index deletion
  """
  handler = APIHandler(None, VectorStoreManager(api_key, pinecone_api_key, pinecone_env))
  msg = handler.embeddings_manager.delete_index(index_name)
  
  return msg

