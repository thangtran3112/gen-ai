import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

import os
import dotenv
dotenv.load_dotenv()

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"
POSTGRES="USE_POSTGRES"

radio_opt=["Use local SQLLite Student.db","Connect to you MySQL Database","Use Postgres Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
elif radio_opt.index(selected_opt) == 2:
    db_uri = POSTGRES
    pg_host = st.sidebar.text_input("PostgreSQL Host")
    pg_user = st.sidebar.text_input("PostgreSQL User")
    pg_password = st.sidebar.text_input("PostgreSQL Password", type="password")
    pg_db = st.sidebar.text_input("PostgreSQL Database")
else:
    db_uri=LOCALDB

api_key=os.getenv("GROQ_API_KEY")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key to environment variables")

## LLM model
llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_sqlite() -> SQLDatabase:
    dbfilepath=(Path(__file__).parent/"student.db").absolute()
    print(dbfilepath)
    def creator():
        return sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
    return SQLDatabase(create_engine("sqlite:///", creator=creator))

@st.cache_resource(ttl="2h")
def configure_mysql(mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None) -> SQLDatabase:
    if not (mysql_host and mysql_user and mysql_password and mysql_db):
        st.error("Please provide all MySQL connection details.")
        st.stop()
    return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))  

@st.cache_resource(ttl="2h")
def configure_postgres(pg_host=None,pg_user=None,pg_password=None,pg_db=None) -> SQLDatabase:
    if not (pg_host and pg_user and pg_password and pg_db):
        st.error("Please provide all PostgreSQL connection details.")
        st.stop()
    return SQLDatabase(
        create_engine(
            f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}/{pg_db}"
        )
    )
    
if db_uri==MYSQL:
    db=configure_mysql(mysql_host,mysql_user,mysql_password,mysql_db)
if db_uri==POSTGRES:
    db=configure_postgres(pg_host,pg_user,pg_password,pg_db)
if db_uri==LOCALDB:
    db=configure_sqlite()

## toolkit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)

        

