from bentoml import Service
from bentoml.io import Text, JSON
from src.chatbot import load_chain
from src.data_processing import DataPreprocessor
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor

chain = load_chain()
processor = DataPreprocessor(data)

svc = Service(
  'zenno-api-service',
)

@svc.api(input=Text(), output=JSON(), route='api/v1/prompt')
def prompt(prompt: str) -> str:
  resp = chain(prompt)
  print('resp_question:', resp['question'], '\n')
  print('resp_answer:', resp['answer'], '\n')
  print('resp_history:', resp['chat_history'], '\n')
  
  print('\n\nSources:')
  for source in resp['source_documents']:
      print(source.metadata['url'], '\n')
      
  return resp

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/process_data')
def process_data(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.embed_data(data_chunks)
  
  return msg

@svc.api(input=ArrayJSONIODescriptor(), output=Text(), route='api/v1/add_data')
def add_data(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.add_data(data_chunks)
  
  return msg