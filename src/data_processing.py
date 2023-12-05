import re
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

class DataPreprocessor:
    def __init__(self, data=None):
        self.data = data
        
    def process_data(self) -> list:
        """Processes incoming data from the web scraper or pdf upload.
        Returns:
            list: a list of data chunks
        """
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
        """Cleans the text (removes punctuation, extra spaces, etc.)
        Args:
            text (str): text to be cleaned
        Returns:
            str: cleaned text
        """
        cleaned_text = re.sub(r"[^\w\s]", "", text)
        cleaned_text = cleaned_text.lower()
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        return cleaned_text
      

    def split_data(self, cleaned_text, metadata) -> list:
        """Splits the data into chunks.
        Args:
            cleaned_text (_type_): text to be split into chunks
            metadata (_type_): metadata to be added to the chunks
        Returns:
            list: a list of data chunks
        """
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
    
    self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
    pinecone.init(api_key=self.pinecone_api_key, environment=self.pinecone_env)
    
    
  def _try_except_wrapper(self, func, *args, **kwargs):
    """Wraps the function in a try except block.
    Args:
        func (_type_): function to be wrapped
    """
    try:
     return func(*args, **kwargs)
    except Exception as e:
      print(f"Error: {str(e)}")
      
    
  def create_embeddings_index(self, chunks: list) -> str:
    """Creates an embeddings index from the data.
    Args:
        chunks (list): a list of data chunks to create embeddings from
    Returns:
        str: a message indicating the status of the embeddings index creation
    """
    def create_embeddings():
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
                vectorstore = Pinecone(index, self.embeddings, "text")
                vectorstore.add_documents(chunks)
                msg = "Embeddings successfully created."
        else:
            msg = "No split data found. Skipping embedding..."
        return msg
    return self._try_except_wrapper(create_embeddings)
  
  def update_embeddings_index(self, chunks: list) -> str:
    """Updates the embeddings index with new data.
    Args:
        chunks (list): a list of data chunks to update the embeddings index with
    Returns:
        str: a message indicating the status of the embeddings index update
    """
    def update_embeddings():
        index = pinecone.Index("assuria")
        vectorstore = Pinecone(index, self.embeddings, "text")
        vectorstore.add_documents(chunks)
        return 'Successfully added new data to the existing embeddings.'
      
    return self._try_except_wrapper(update_embeddings)
  
  
  def delete_index(self, index_name: str) -> str:
    """Deletes the entire index.
    Args:
        index_name (str): the name of the index to delete
    Returns:
        str: a message indicating the status of the index deletion
    """
    def delete_index():
        # TODO: Index name hardcoded for now
        pinecone.delete_index(index_name)
        
        return 'Successfully deleted the index.'

    return self._try_except_wrapper(delete_index)
  
  
  def delete_embedding(self, url: str) -> str:
    """Deletes a specific embedding.
    Args:
        url (str): the url of the embedding to delete
    Returns:
        str: a message indicating the status of the embedding deletion
    """
    def delete_embedding():
        index = pinecone.Index("assuria")
        index.delete(filter={"url": url})
        return 'Successfully deleted the embedding.'
    return self._try_except_wrapper(delete_embedding)

  
    