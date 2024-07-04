# src/langchain/ingest.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# Set your OpenAI API key
load_dotenv()

def ingest_data(file_path):
    # 1. Load the document
    loader = TextLoader(file_path)
    documents = loader.load()

    # 2. Split the text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20, length_function=len)
    texts = text_splitter.split_documents(documents)

    # 3. Create embeddings and store them in FAISS
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    # 4. Save the FAISS index
    vectorstore.save_local("faiss_index")  # Save the index to the faiss_index folder

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)  # Get the directory of the script
    file_path = os.path.join(script_dir, "faqvido.txt")  # Build the path to faqvido.txt
    ingest_data(file_path)
    print("Data ingestion complete. FAISS index saved.")