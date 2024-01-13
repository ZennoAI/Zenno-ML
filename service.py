import os
from dotenv import load_dotenv
from bentoml import Service
from bentoml.io import Text, JSON
from src.chatbot import load_chain
from src.data_processing import DataProcessor
from src.vector_store import VectorStoreManager
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor
from langkit import llm_metrics
import whylogs as why
from whylogs.api.writer.whylabs import WhyLabsWriter

load_dotenv()

web_scraper_url = os.getenv("WEB_SCRAPER_URL")
api_key = os.getenv("API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
whylab_api_key = os.environ.get("WHYLAB_API_KEY")
whylab_org_id = os.environ.get("WHYLAB_ORG_ID")
whylab_model_id = os.environ.get("WHYLAB_MODEL_ID")

schema = llm_metrics.init()

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
  resp = chain(prompt)
  
  telemetry_agent = WhyLabsWriter(api_key=whylab_api_key, org_id=whylab_org_id, dataset_id=whylab_model_id)
  prompt_and_response = {
    'prompt': prompt,
    'response': resp['answer'],
  }
  
  profile = why.log(prompt_and_response, schema=schema).profile()
  telemetry_agent.write(profile.view())
  
  print('resp_question:', resp['question'], '\n')
  print('resp_answer:', resp['answer'], '\n')
  print('resp_history:', resp['chat_history'], '\n')
  
  print('\n\nSources:')
  for source in resp['source_documents']:
      print(source.metadata['url'], '\n')
      
  return resp

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

