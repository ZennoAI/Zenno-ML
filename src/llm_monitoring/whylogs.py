import os
from dotenv import load_dotenv
from langkit import llm_metrics
from langkit import toxicity
import whylogs as why
from whylogs.api.writer.whylabs import WhyLabsWriter

load_dotenv()
whylab_api_key = os.environ.get("WHYLAB_API_KEY")
whylab_org_id = os.environ.get("WHYLAB_ORG_ID")
whylab_model_id = os.environ.get("WHYLAB_MODEL_ID")

schema = llm_metrics.init()

def log_prompt_response(prompt: str, resp: str):
  """Logs the prompt and response to WhyLabs.

  Args:
      prompt (str): a prompt to generate a response from
      resp (str): a response from the prompt
  """
  telemetry_agent = WhyLabsWriter(
    api_key=whylab_api_key, 
    org_id=whylab_org_id, 
    dataset_id=whylab_model_id
    )
  
  prompt_and_response = {
    'prompt': prompt,
    'response': resp,
  }
  
  profile = why.log(prompt_and_response, schema=schema).profile()
  telemetry_agent.write(profile.view())
  

def is_not_toxic(prompt: str):
  """Checks if the prompt is toxic.

  Args:
      prompt (str): a prompt to generate a response from

  Returns:
      _type_: returns True if the prompt is not toxic, False otherwise
  """
  profile = why.log({'prompt': prompt}, schema=schema).profile().view()
  profile_dict = profile.get_column('prompt.toxicity').to_summary_dict()['distribution/mean']
  
  print(f'Toxic score: {profile_dict}')
  
  if profile_dict > 0.5:
    return True
  else:
    return True