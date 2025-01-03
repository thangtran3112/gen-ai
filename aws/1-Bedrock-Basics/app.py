from typing import List
import boto3
import streamlit as st
from langchain_core.documents import Document

## We will be suing Titan Embeddings Model To generate Embedding

from langchain_aws.embeddings.bedrock import BedrockEmbeddings
from langchain_aws.chat_models.bedrock import ChatBedrock
## Data Ingestion

import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

# Vector Embedding And Vector Store

from langchain_community.vectorstores import FAISS

## LLm Models
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

VECTOR_STORE_FOLDER = "faiss_index"

## Bedrock Clients
bedrock=boto3.client(service_name="bedrock-runtime")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",client=bedrock)


## Data ingestion
def data_ingestion() -> List[Document]:
    """Load and split PDF documents from data directory.
    
    Returns:
        List[Document]: List of document chunks after splitting
    """
    loader: PyPDFDirectoryLoader = PyPDFDirectoryLoader("data")
    documents: List[Document] = loader.load()

    # In our testing Character split works better with this PDF data set
    text_splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, 
        chunk_overlap=1000
    )
    
    docs: List[Document] = text_splitter.split_documents(documents)
    return docs

## Vector Embedding and vector store

def get_vector_store(docs):
    vectorstore_faiss=FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    vectorstore_faiss.save_local(VECTOR_STORE_FOLDER)

def get_claude_llm():
    ##create the Anthropic Model
    llm=ChatBedrock(model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",client=bedrock,
                model_kwargs={'max_tokens':512})
    
    return llm

def get_llama3_llm():
    ##create the Anthropic Model
    llm=ChatBedrock(model_id="us.meta.llama3-2-11b-instruct-v1:0",client=bedrock,
                model_kwargs={'max_tokens':512})
    
    return llm

prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explanations. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def get_response_llm(llm,vectorstore_faiss,query):
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer = qa.invoke({"query": query})
    return answer['result']


def main():
    st.set_page_config("Chat PDF")
    
    st.header("Chat with PDF using AWS Bedrock 💁")

    user_question = st.text_input(
        "Ask a Question from the PDF Files",
        placeholder="Example: When dogs were domesticated?"
    )

    with st.sidebar:
        st.title("Update Or Create Vector Store:")
        
        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Done")

    # Define available models
    model_options = ["Claude Sonnet 3.5", "Llama 3.2"]
    selected_model = st.selectbox("Select Model", model_options)

    if st.button("Get Response"):
        with st.spinner("Processing..."):
            if selected_model == "Claude Sonnet 3.5":
                llm = get_claude_llm()
            elif selected_model == "Llama 3.2":
                llm = get_llama3_llm()

            faiss_index = FAISS.load_local(
                VECTOR_STORE_FOLDER, 
                bedrock_embeddings, 
                allow_dangerous_deserialization=True
            )
            
            st.write(get_response_llm(llm, faiss_index, user_question))
            st.success("Done")

if __name__ == "__main__":
    main()














