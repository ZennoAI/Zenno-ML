from langchain.prompts import PromptTemplate

def initial_template():
  template =  """Given a customer's query and the current conversation history, generate a response that is helpful, informative, and polite. 
                 The response should be relevant to the customer's query, and it should be tailored to the individual customer's needs. 
                 The response should also be consistent with Uber's brand and values.

                Example:
                Customer: I'm trying to request a ride, but I'm having trouble with the app.
                Chatbot: Hi there! I'm sorry to hear that you're having trouble with the Uber app. Can you please tell me more about the problem you're experiencing?

                Customer: I'm trying to enter my pickup location, but the app keeps crashing.
                Chatbot: Okay, I understand. Are you able to provide me with your pickup location? I can help you to manually request a ride for you.

                Customer: Sure, my pickup location is 123 Main Street, Anytown, CA.
                Chatbot: Okay, thank you. I'm requesting a ride for you now. You should receive a confirmation shortly.

                Customer: Thank you for your help!
                Chatbot: You're welcome! Is there anything else I can help you with today?

                {context}
                Current conversation:
                {chat_history}

                Human: {question}
                AI: 
                """
  prompt_template = PromptTemplate(
    input_variables=['chat_history', 'human_input', 'context'], 
    template=template)
  
  return prompt_template