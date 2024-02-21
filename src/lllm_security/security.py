from langkit import injections
from whylogs.experimental.core.udf_schema import udf_schema
import whylogs as why

text_schema = udf_schema()

def is_not_prompt_injection(prompt: str) -> bool:  
  profile = why.log({"prompt": prompt}, schema=text_schema).profile().view()
  profile_dict = profile.get_column('prompt.injection').to_summary_dict()['distribution/max']
  
  print(f'Prompt injection score: {profile_dict}')
  
  if profile_dict > 0.5:
    return False
  else:
    return True 
  