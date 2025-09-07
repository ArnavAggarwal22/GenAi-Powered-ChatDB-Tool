import streamlit as st
import os
from langchain.sql_database import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit



few_shots = [
    {'Question' : "Who is our most frequent customer based on the number of orders placed??",
     'SQLQuery' : """SELECT "Customer Name" FROM orders GROUP BY "Customer Name" ORDER BY COUNT("Order ID") DESC LIMIT 1;"""},
    {'Question': "Which month had the highest sales for Christmas-related products?",
     'SQLQuery': """SELECT TO_CHAR("Order Date", 'Month') FROM orders WHERE "Products" ILIKE '%Christmas%' GROUP BY TO_CHAR("Order Date", 'Month'), EXTRACT(MONTH FROM "Order Date") ORDER BY SUM("Total") DESC LIMIT 1;"""},
    {'Question': "How many customers have only ever purchased 'Christmas' related items and nothing else",
     'SQLQuery' : """SELECT COUNT(*) FROM (SELECT "Customer ID" FROM orders GROUP BY "Customer ID" HAVING COUNT(*) FILTER (WHERE "Products" ILIKE '%Christmas%') > 0 AND COUNT(*) FILTER (WHERE "Products" NOT ILIKE '%Christmas%') = 0) AS SingleCategoryCustomers;"""}
]

base_instructions = """You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results.
Wrap each column name in double quotes (").

Here are some examples of user questions and their corresponding SQL queries:
"""

formatted_examples = "\n\n".join(
    [f"Question: {example['Question']}\nSQLQuery: {example['SQLQuery']}" for example in few_shots]
)

AGENT_PREFIX = base_instructions + formatted_examples

@st.cache_resource
def create_agent():
    api_key = ""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=api_key, temperature=0)
    
    db_user = ""
    db_password = ""
    db_host = "localhost"
    db_name = "UpharkaroSales"
    db = SQLDatabase.from_uri(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}")

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        prefix=AGENT_PREFIX
    )
    return agent_executor



st.title("ChatDB")

question = st.text_input("Ask a question about your database:")

if question:
    with st.spinner("Thinking..."):
        agent = create_agent()
        response = agent.invoke({"input": question})
        
        st.header("Answer")

        st.write(response['output'])
