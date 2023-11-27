from bentoml import Service
from bentoml.io import Text, JSON
from src.chatbot import load_chain
from src.data_processing import DataPreprocessor
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor

chain = load_chain()
# processor = DataPreprocessor(data)

svc = Service(
  'zenno-api-service',
)

@svc.api(input=Text(), output=JSON(), route='api/v1/generate_prompt')
def generate_prompt(prompt: str) -> str:
  resp = chain(prompt)
  print('resp_question:', resp['question'], '\n')
  print('resp_answer:', resp['answer'], '\n')
  print('resp_history:', resp['chat_history'], '\n')
  
  print('\n\nSources:')
  for source in resp['source_documents']:
      print(source.metadata['url'], '\n')
      
  return resp

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/create_embeddings_index')
def create_embeddings_index(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.create_embeddings_index(data_chunks)
  
  return msg

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/update_embeddings_index')
def update_embeddings_index(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.update_embeddings_index(data_chunks)
  
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_embedding')
def delete_embedding(url: str) -> str:
  processor = DataPreprocessor()
  msg = processor.delete_embedding(url)
  return msg

@svc.api(input=Text(), output=Text(), route='api/v1/delete_index')
def delete_index(index_name: str) -> str:
  processor = DataPreprocessor()
  msg = processor.delete_index(index_name)
  return msg
