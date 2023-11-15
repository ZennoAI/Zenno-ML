import os
import re
import aiohttp
import asyncio
import openai
import pinecone
import requests
from langchain.document_loaders import DirectoryLoader, TextLoader, JSONLoader
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
    def __init__(self, data):
        self.data = data
        

    def process_data(self):
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

    def clean_text(self, text):
        """Perform basic text cleaning and normalization."""
        #Remove special characters and punctuation
        cleaned_text = re.sub(r"[^\w\s]", "", text)

        # Convert text to lowercase
        cleaned_text = cleaned_text.lower()

        #Remove extra whitespace
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        return cleaned_text
      

    def split_data(self, cleaned_text, metadata):
        """Splits the text into chunks for embedding."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64, separators=["\n\n", "\n"]
        )
        
        split_texts = text_splitter.split_text(cleaned_text)
        split_document = text_splitter.create_documents(split_texts, [metadata])
        
        return split_document
      

    def embed_data(self, chunks):
        """Embeds the data using the OpenAI embeddings model."""
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
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
            
    def add_data(self):
      """Adds more data to the existing embeddings."""
      embeddings = OpenAIEmbeddings(openai_api_key=api_key)
      index = pinecone.Index("assuria")
      vectorstore = Pinecone(index, embeddings, "text")
      vectorstore.add_texts(self.data)
      return 'Data added successfully'