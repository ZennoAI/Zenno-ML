import re
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataProcessor:
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
      
      
    


  
    