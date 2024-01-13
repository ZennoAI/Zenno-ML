import os
from dotenv import load_dotenv
from langkit import llm_metrics
import whylogs as why
from whylogs.api.writer.whylabs import WhyLabsWriter


load_dotenv()
whylab_api_key = os.environ.get("WHYLAB_API_KEY")
whylab_org_id = os.environ.get("WHYLAB_ORG_ID")
whylab_model_id = os.environ.get("WHYLAB_MODEL_ID")

schema = llm_metrics.init()

def log_prompt_respnse(prompt: str, resp: str):
  telemetry_agent = WhyLabsWriter(
    api_key=whylab_api_key, 
    org_id=whylab_org_id, 
    dataset_id=whylab_model_id
    )
  
  prompt_and_response = {
    'prompt': prompt,
    'response': resp['answer'],
  }
  
  profile = why.log(prompt_and_response, schema=schema).profile()
  telemetry_agent.write(profile.view())