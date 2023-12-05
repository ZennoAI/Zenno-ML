import os
import re
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()

web_scraper_url = os.getenv("WEB_SCRAPER_URL")
api_key = os.getenv("API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


class DataPreprocessor:
    def __init__(self, data=None):
        self.data = data
        

    def process_data(self) -> list:
        """Processes the data fetched from the web scraper API."""
        if self.data:
            metadata = {}
            chunks = []
            for res in self.data:
                metadata['title'] = res.get('title')
                metadata['url'] = res.get('url')
                content = res["content"]

                cleaned_text = self.clean_text(content)
                chunks.extend(self.split_data(cleaned_text, metadata))
            return chunks
        else:
            print("No new data from the web scraper. Skipping data processing.")

    def clean_text(self, text: str) -> str:
        """Perform basic text cleaning and normalization.
           Removes special characters, punctuation, and extra whitespace.
           
           arg: text: str
        """
        cleaned_text = re.sub(r"[^\w\s]", "", text)
        cleaned_text = cleaned_text.lower()
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        return cleaned_text
      

    def split_data(self, cleaned_text, metadata) -> list:
        """Splits the text into chunks for embedding."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64, separators=["\n\n", "\n"]
        )
        
        split_texts = text_splitter.split_text(cleaned_text)
        split_document = text_splitter.create_documents(split_texts, [metadata])
        
        return split_document
    
class EmbeddingsManager():
  def __init__(self, api_key, pinecone_api_key, pinecone_env):
    self.api_key = api_key
    self.pinecone_api_key = pinecone_api_key
    self.pinecone_env = pinecone_env
    
  def create_embeddings_index(self, chunks: list) -> str:
    """Embeds the data using the OpenAI embeddings model."""
    embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
    pinecone.init(api_key=self.pinecone_api_key, environment=self.pinecone_env)
    # TODO Index name hardcoded for now
    index_name = "assuria"
    msg = ''

    if chunks:
        if index_name in pinecone.list_indexes():
            msg = "Embeddings already exist. Skipping embedding...."
        else:
          # TODO upload the embeddings in batches
            print("Creating embeddings...")
            pinecone.create_index(name=index_name, metric="cosine", dimension=1536)
            index = pinecone.Index(index_name)
            vectorstore = Pinecone(index, embeddings, "text")
            vectorstore.add_documents(chunks)
            msg = "Embeddings succesfully created."
    else:
        msg = "No split data found. Skipping embedding..."
    return msg
  
  def update_embeddings_index(self, chunks: list) -> str:
    """Adds more data to the existing embeddings.
      
      args: chunks: list
    """
    
    embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
    index = pinecone.Index("assuria")
    vectorstore = Pinecone(index, embeddings, "text")
    vectorstore.add_documents(chunks)
    msg = 'Successfully added new data to the existing embeddings.'
    
    return msg
  
  def delete_index(self, index_name: str) -> str:
    """Delete the entire index.
    
       args: index_name: str
    """
    # TODO: Index name hardcoded for now
    pinecone.delete_index(index_name)
    msg = 'Successfully deleted the index.'
    
    return msg
  
  def delete_embedding(self, url: str) -> str:
    """Delete a specific embedding
      
      args: url: str
    """
    
    index = pinecone.Index("assuria")
    index.delete(
    filter={"url": url})
    msg = 'Successfully deleted the embedding.'
    # vectorstore = Pinecone(index, embeddings, "text")
    # vectorstore.delete(filter={'metadata.url': url})
    return msg
      
  
    