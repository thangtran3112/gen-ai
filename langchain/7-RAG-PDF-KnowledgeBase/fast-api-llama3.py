from dataclasses import dataclass
from typing import Optional, List
import os
import time
from pydantic import BaseModel
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

## load the GROQ API Key
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

## If you do not have open AI key use the below Huggingface embedding
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192")
parser=StrOutputParser()

prompt_template=ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate respone based on the question
    <context>
    {context}
    <context>
    Question:{input}

    """
)

@dataclass
class SessionState:
    embeddings: Optional[HuggingFaceEmbeddings] = None
    loader: Optional[PyPDFDirectoryLoader] = None
    docs: Optional[List[Document]] = None
    text_splitter: Optional[RecursiveCharacterTextSplitter] = None
    final_documents: Optional[List[Document]] = None
    vectors: Optional[FAISS] = None

# Initialize typed session state
session_state = SessionState()

def create_vector_embedding():
    if session_state.vectors is None:
        session_state.embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        session_state.loader=PyPDFDirectoryLoader("../pdf-assets") 
        session_state.docs=session_state.loader.load() ## Document Loading
        session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        # Only use the first 100 documents for demonstration purposes
        session_state.final_documents=session_state.text_splitter.split_documents(session_state.docs[:100])
        session_state.vectors=FAISS.from_documents(session_state.final_documents,session_state.embeddings)

create_vector_embedding()
retriever = session_state.vectors.as_retriever()
document_chain=create_stuff_documents_chain(llm,prompt_template)
retrieval_chain=create_retrieval_chain(retriever,document_chain)


response=retrieval_chain.invoke({'input': "When were dogs domesticated?"})
print(response)

# Exposure of the API. Visit http://localhost:8000/docs to see the swagger documentation

app = FastAPI(title="RetrievalChain API with custom PDF document retrieval")

class QueryModel(BaseModel):
    question: str

@app.post("/chat")
def chat_endpoint(query: QueryModel):
    start_time = time.process_time()
    response = retrieval_chain.invoke({"input": query.question})
    elapsed = time.process_time() - start_time
    return {
        "answer": response.get("answer", ""),
        "context": response.get("context", []),
        "processing_time_seconds": elapsed
    }

## Visit http://localhost:8000/docs to see the swagger documentation
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)