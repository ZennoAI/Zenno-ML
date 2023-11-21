from langchain.prompts import PromptTemplate
import csv

def initial_template():
  template =  """Je bent een behulpzame assistent die werkt voor een grote verzekeringsmaatschappij.
                  Je zult vragen krijgen over verzekeringen en gerelateerde onderwerpen, onder andere.
                  Houd je aan de vraag, geef een uitgebreid antwoord en verzin geen feiten.
                  Als je het antwoord niet weet, zeg dan gewoon dat je het niet weet, verzin geen antwoorden.
                  Als er meerdere puntent zijn, graag het antwoord in bullet points geven.
                  Gebruik de volgende contextstukken om de vraag aan het einde te beantwoorden.

                context: {context}

                Huidige conversatie: {chat_history}
                Mens: {question}
                AI: 
                """
  prompt_template = PromptTemplate(
    input_variables=['chat_history', 'human_input', 'context'], 
    template=template)
  
  return prompt_template

def summary_prompt_template():
  template =  """Vat de gespreksgeschiedenis samen en genereer een reactie die behulpzaam, informatief en beleefd is.
                  Als je het antwoord niet weet, zeg dan gewoon dat je het niet weet, verzin geen antwoorden.
                  summary: {summary}
                  new_lines: {new_lines}
                """
                
  summary_template = PromptTemplate(
    input_variables=['summary', 'new_lines'], template=template
  )              
              
  return summary_template