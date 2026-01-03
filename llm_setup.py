import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import openai

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
llm_model = "gpt-4o-mini"

llm = ChatOpenAI(temperature=0.7, model=llm_model)
tavily_tool = TavilySearchResults(max_results=3)
