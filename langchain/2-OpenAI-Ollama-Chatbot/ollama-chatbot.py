import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import os

from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With Ollama"

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful massistant . Please  repsonse to the user queries"),
        ("user","Question:{question}")
    ]
)

## #Title of the app
st.title("Enhanced Q&A Chatbot With OpenAI")


## Select the OpenAI model. Another alternative is gemma, mistral
llm=st.sidebar.selectbox("Select Open Source model",["llama3"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.2)
max_tokens = st.sidebar.slider("Max Tokens", min_value=100, max_value=500, value=200)

## MAin interface for user input
st.write("Goe ahead and ask any question")
user_input=st.text_input("You:")


# Update Ollama initialization with parameters
llm=Ollama(
    model=llm,
    temperature=temperature,
    num_ctx=max_tokens  # Ollama uses num_ctx instead of max_tokens
)
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

def generate_response(question):

    answer=chain.invoke({'question':question})
    return answer


if user_input :
    response=generate_response(user_input)
    st.write(response)
else:
    st.write("Please provide the user input")


