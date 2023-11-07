import bentoml
from chatbot import load_chain

llm_runner = bentoml.Runner(
  load_chain,
  name='customer_service_chain',

)

svc = bentoml.Service(
  'llm-zenno-serive',
  runners=[llm_runner],
)

@svc.api(input=bentoml.io.Text(), outpu=bentoml.io.Text())
async def prompt(input_text: str) -> str:
  answer = await llm_runner.generate.async_run(input_text)
  return answer[0]['generated_text']