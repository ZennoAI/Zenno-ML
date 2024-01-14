import re
import html

def whitelist_prompt_validation(prompt: str)  -> None:
  """Validates the prompt against a whitelist of allowed characters.
  Args:
      prompt (string): a prompt to validate
  """
  pattern = re.compile(r'^[a-zA-Z0-9\.\,\?\!\s]+$')
  
  if not re.match(pattern, prompt):
    raise ValueError('Prompt contains invalid characters. Please try again.')
  
  
  def escape_user_content(user_content: str) -> str:
    """Removes any characters that are not letters, digits, underscores, or whitespace.
    Args:
        user_content (string): user content to be escaped 
    returns:
        string: escaped user content
    """
    escaped_content = re.sub(r'[^\w\s]', '', user_content)
    return escaped_content
  
  
  def sanitize_prompt(prompt: str) -> str:
    """Sanitizes the prompt by replacing < and > with &lt; and &gt;.
    Args:
        prompt (string): prompt to be sanitized
    Returns:
        string: sanitized prompt
    """
    sanitized_prompt = prompt.replace("<", "&lt;").replace(">", "&gt;")
    return sanitized_prompt
  
  
  def generate_dynamic_prompt(user_input: str) -> str:
    """Generates a dynamic prompt from the user input.
    Args:
        user_input (string): user input to generate the prompt from
    Returns:
        string: dynamic prompt
    """
    validated_input = validate_and_escape(user_input)
    dynamic_prompt = f'User input: {validated_input}'
    
    return dynamic_prompt
  
  def validate_and_escape(user_input: str) -> str:
    """Validates and escapes the user input.
    Args:
        user_input (string): user input to be validated and escaped
    Returns:
        string: validated and escaped user input
    """
    escaped_input = html.escape(user_input)
    return escaped_input
  
  
  def prompt_length_validation(prompt: str, max_length=512):
    """Validates the prompt length.
    Args:
        prompt (str): a prompt to validate
        max_length (int, optional): the max length of a prompt. Defaults to 512.
    Raises:
        TypeError: _description_
        ValueError: _description_
        ValueError: _description_
    """
    if not isinstance(prompt, str):
      raise TypeError('Prompt must be a string.')
    
    if not isinstance(max_length, int) or max_length <= 0:
      raise ValueError('Max length must be a positive integer.')
    
    if len(prompt) > max_length:
      raise ValueError(f'Prompt length must be less than {max_length}.')