import json
import streamlit as st
from pymongo import MongoClient
import urllib
import io
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import AgentType, initialize_agent, Tool

import os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("GROQ_API_KEY")

if not api_key:
    st.info("Please add the groq api key to environment variables")

## LLM model
llm = ChatGroq(
    temperature=0,  # Make output deterministic
    streaming=True,
    api_key=api_key,
    model_name="mixtral-8x7b-32768"
)

# mongo client
username=os.getenv("MONGO_ATLAS_USER")
password=os.getenv("MONGO_ATLAS_PASSWORD")
collection_name = 'tours'
database_name = 'amazing'


# Must url encode the username and password
uri = "mongodb+srv://" + urllib.parse.quote(username) + ":" + urllib.parse.quote(password) + "@awscluster1.yerzcf1.mongodb.net/?retryWrites=true&w=majority&appName=AwsCluster1"

client=MongoClient(uri)
db=client[database_name]
collection=db[collection_name]

st.title("talk to MongoDB")

with io.open("sample.txt","r",encoding="utf-8")as f1:
    sample=f1.read()
    f1.close()

prompt="""
        you are a very intelligent AI assitasnt who is expert in identifying relevant questions fro user
        from user and converting into nosql mongodb agggregation pipeline query.
        Note: You have to just return the query as to use in agggregation pipeline nothing else. Don't return any other thing
        Please use the below schema to write the mongodb queries , dont use any other queries.
       schema:
       the mentioned mogbodb collection talks about listing for a hiking tours. The schema for this document represents the structure of the data, describing various properties related to the tours, tour rating, descirption, price, max group and additional features. 
       your job is to get python code for the user question
           Here's a breakdown of the tours collection schema:

    1. **_id**: ObjectId - Unique identifier
    2. **name**: String - Tour name
    3. **maxGroupSize**: Int - Maximum number of people in group
    4. **duration**: Int - Tour duration in days
    5. **price**: Int - Tour price
    6. **difficulty**: String - Tour difficulty level (easy, medium, difficult)
    7. **ratingsAverage**: Double - Average rating (1-5)
    8. **ratingQuantity**: Int - Number of ratings
    9. **summary**: String - Brief tour description
    10. **description**: String - Detailed tour description
    11. **imageCover**: String - Cover image filename
    12. **images**: Array[String] - Tour images filenames
    13. **createdAt**: Date - Tour creation timestamp
    14. **startDates**: Array[Date] - Available tour dates
    15. **__v**: Int - Version key

This schema provides a comprehensive view of the data structure for an tours listing in MongoDB, 
including nested and embedded data structures that add depth and detail to the document.
use the below sample_examples to generate your queries perfectly
sample_example:

Below are several sample user questions related to the MongoDB document provided, 
and the corresponding MongoDB aggregation pipeline queries that can be used to fetch the desired data.
Use them wisely.

sample_question: {sample}
As an expert you must use them whenever required.
Note: You have to just return the query nothing else. Don't return any additional text with the query.Please follow this strictly
input:{question}
output:
"""
query_with_prompt=PromptTemplate(
    template=prompt,
    input_variables=["question","sample"]
)
## LLM Chain
# Convert LLMChain to RunnableSequence
chain = (
    query_with_prompt 
    | llm 
    | StrOutputParser()
)

# if input is not None:
#     button=st.button("Submit")
#     if button:
#         response=chain.invoke({
#             "question":input,
#             "sample":sample
#         })
#         # extract the query from the response
#         query=json.loads(response)
#         # use MongoDB client to execute the query
#         results=collection.aggregate(query)
#         print(query)
#         for result in results:
#             st.write(result)


def transform_input(query: str) -> dict:
    return {
        "question": query,
        "sample": sample  # Make sure sample is in scope
    }

def execute_mongo_query(chain_response: str):
    try:
        # Parse the query from chain response
        query = json.loads(chain_response)
        
        # Execute MongoDB aggregation
        results = collection.aggregate(query)
        
        # Display results in Streamlit
        st.write("### Query Results:")
        for result in results:
            st.write(result)
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse query: {str(e)}")
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")

# Update tool definition
tools = [
    Tool(
        name="MongoDB Query Tool",
        func=lambda x: execute_mongo_query(chain.invoke(transform_input(x))),
        description="Useful for querying MongoDB tours database. Input should be a natural language question about tours.",
        return_direct=True
    )
]

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="Ask anything from the database")

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)

# Update response handling
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(
            user_query,
            callbacks=[streamlit_callback]
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
