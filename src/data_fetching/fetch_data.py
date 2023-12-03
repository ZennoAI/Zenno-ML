import os
import requests
from dotenv import load_dotenv


load_dotenv()

web_scraper_url = os.getenv("WEB_SCRAPER_URL")
api_key = os.getenv("API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

data = {
    "links": [
"https://assuria.sr/nl/claims/schade-melden-motorrijtuigen/",
"https://assuria.sr/nl/claims/schade-melden-trias/",
"https://assuria.sr/nl/claims/schade-melden-woonhuis/",
"https://assuria.sr/nl/claims/schade-melden-s-o-r/",
"https://assuria.sr/nl/claims/schade-melden-pav/",
"https://assuria.sr/nl/claims/schade-melden-p-o/",
"https://assuria.sr/nl/hypotheken-beleggen/assuria-autofinanciering/",
"https://assuria.sr/nl/hypotheken-beleggen/assuria-hypotheek-pensioen/",
"https://assuria.sr/nl/hypotheken-beleggen/hypotheek-assuria/",
"https://assuria.sr/nl/hypotheken-beleggen/ab-plan/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/wam-verzekering/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/mini-casco/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/casco-verzekering/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/cascodekking-frans-guyana/",
"https://assuria.sr/nl/particulier/verzekeringen/auto/aanvullende-dekkingen/",
"https://assuria.sr/nl/particulier/verzekeringen/zorg/",
"https://assuria.sr/nl/assuria-event-center/",
"https://assuria.sr/nl/klantenservice/",
"https://assuria.sr/nl/klantenservice/vestigingen/",
],
}

data_dir = './data/text_data/assuria_raw/'

def fetch_data():
  """Fetches data from the web scraper API."""

  folder_contents = os.listdir(data_dir)
  if len(folder_contents) != 0:
    print("Data file already exists. Skipping data fetching.")
    return None
  try:
      response = requests.post(web_scraper_url, json=data)
      if response.status_code == 200:
          response_data = response.json()
      else:
          print("Failed to make a POST request. Status code:", response.status_code)

      return response_data
  except requests.exceptions.RequestException as e:
      print("An error occurred while making the request:", e)
      
      
from abc import ABC, abstractclassmethod      

class BaseDataFetcher(ABC):
     def __init__(self, base_url, data_dir):
        self.base_url = base_url
        self.data_dir = data_dir
        
     def fetch_data(self, endpoint, data):
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to make a POST request to {endpoint}. Status code:", response.status_code)
                return None
        except requests.exceptions.RequestException as e:
            print("An error occurred while making the request:", e)
            return None
          
class WebSraperData(BaseDataFetcher):
    """
    Concrete webscraper class that implements the abstract operations of the base
    class.
    """
    def __init__(self, web_scraper_url, data_dir):
        super().__init__(web_scraper_url, data_dir)

    def fetch_data_from_web_scraper(self, data):
        return self.fetch_data("web_scraper", data)
      
class PDFUploadedData(BaseDataFetcher):
    """
    Concrete document uploaded class that implements the abstract operations of the base
    class.
    """
    def __init__(self, uploaded_pdf_url, data_dir):
      super().__init__(uploaded_pdf_url, data_dir)
      
    def fetch_data_from_uploaded_pdfs(self, data):
      return self.fetch_data('upload_pdf', data)