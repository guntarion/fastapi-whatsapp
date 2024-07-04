# src/langchain/kb_processor.py

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

def load_qa_chain():
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local("../faiss_index", embeddings, allow_dangerous_deserialization=True)

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4o"),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    return qa_chain

qa_chain = load_qa_chain()

async def query_data(query: str) -> str:
    # Get the initial response from the knowledge base
    response = qa_chain({"query": query})
    result = response['result'].strip()

    # Create a prompt for OpenAI to generate a friendly response
    prompt = f"""
    You are a chatbot. Please generate a friendly and helpful response, in bahasa Indonesia, for the following information:

    Information: {result}

    Response:
    """

    # Call OpenAI to generate a friendly response
    client = AsyncOpenAI()
    openai_response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful chatbot assistant that provides friendly responses in Bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    print(openai_response)
    friendly_response = openai_response.choices[0].message.content.strip()
    return friendly_response