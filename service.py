from bentoml import Service, io
from bentoml.io import Text, JSON, PandasDataFrame
from src.chatbot import load_chain
from src.data_processing import DataPreprocessor
from src.data import data
from src.array_json_io import ArrayJSONIODescriptor

chain = load_chain()
processor = DataPreprocessor(data)

prompt_svc = Service(
  'llm-zenno-service',
)

process_data_svc = Service(
  'data-processor-service',
)

add_data_svc = Service(
  'data-adder-service',
)

@prompt_svc.api(input=Text(), output=JSON(), route='api/v1/prompt')
def prompt(prompt: str) -> str:
  resp = chain(prompt)
  print('resp_question:', resp['question'], '\n')
  print('resp_answer:', resp['answer'], '\n')
  print('resp_history:', resp['chat_history'], '\n')
  
  print('\n\nSources:')
  for source in resp['source_documents']:
      print(source.metadata['url'], '\n')
      
  return resp

@process_data_svc.api(input=ArrayJSONIODescriptor(), output=Text())
def process_data(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.embed_data(data_chunks)
  
  return msg

@add_data_svc.api(input=ArrayJSONIODescriptor(), output=Text())
def add_data(data: list()) -> str:
  processor = DataPreprocessor(data)
  data_chunks = processor.process_data()
  msg = processor.add_data(data_chunks)
  
  return msg