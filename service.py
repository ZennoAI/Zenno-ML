from bentoml import Service
from bentoml.io import Text, JSON
from src.chatbot import load_chain
from src.data_processing import DataPreprocessor
from src.data_processing import EmbeddingsManager
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor

class APIHandler:
  def __int__(self, data_preprocessor, embeddings_manager):
    self.data_preprocessor = data_preprocessor
    self.embeddings_manager = embeddings_manager

svc = Service(
  'zenno-api-service',
)

@svc.api(input=Text(), output=JSON(), route='api/v1/generate_prompt')
def generate_prompt(prompt: str) -> str:
  chain = load_chain()
  resp = chain(prompt)
  print('resp_question:', resp['question'], '\n')
  print('resp_answer:', resp['answer'], '\n')
  print('resp_history:', resp['chat_history'], '\n')
  
  print('\n\nSources:')
  for source in resp['source_documents']:
      print(source.metadata['url'], '\n')
      
  return resp

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/create_embeddings')
def create_embeddings_index(data: list()) -> str:
  """Creates the embeddings for the data fetched from the web scraper API."""
  handler = APIHandler(DataPreprocessor(data), EmbeddingsManager())
  data_chunks = handler.data_preprocessor.process_data()
  msg = handler.embeddings_manager.create_embeddings(data_chunks)
  
  return msg

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/update_embeddings')
def update_embeddings_index(data: list()) -> str:
  handler = APIHandler(DataPreprocessor(data), EmbeddingsManager())
  data_chunks = handler.data_processor.process_data()
  msg = handler.embeddings_manager.update_embeddings_index(data_chunks)
  
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_embedding',)
def delete_embedding(url: str) -> str:
  handler = APIHandler(None, EmbeddingsManager())
  msg = handler.embeddings_manager.delete_embedding(url)
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_index', )
def delete_index(index_name: str) -> str:
  handler = APIHandler(None, EmbeddingsManager())
  msg = handler.embeddings_manager.delete_index(index_name)
  return msg

