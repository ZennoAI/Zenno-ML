import bentoml
from src.chatbot import load_chain

chain = load_chain()

svc = bentoml.Service(
  'llm-zenno-service',
)

@svc.api(input=bentoml.io.Text(), output=bentoml.io.Text())
def prompt(prompt: str) -> str:
  # memory = list()
  answer = chain(prompt)
  # memory.extend([prompt, answer['answer']])
  return answer['answer']