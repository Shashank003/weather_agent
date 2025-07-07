#2) Develop an agent to suggest a clothing for today in a given city, based on the weather:


#Input/ query:  Assign it in a variable to be fed into the agent to get back the recommendation
#Output: Printed in console

#Weather API / Weather MCP

#Things to consider: a) Single/2 agents b) Tools to use
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain import hub
from langchain_community.chat_models import ChatOpenAI
load_dotenv(override=True)

def main():
    print("Running main")
    OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API_KEY"]

    
    weather = OpenWeatherMapAPIWrapper(openweathermap_api_key="bd5e378503939ddaee76f12ad7a97608")
    tools = [weather.run]

    agent = create_react_agent("openai:gpt-4.1-mini", tools)
    input_message = {
    "role": "user",
    "content": "What should I wear today in Alaska?",
}

    for step in agent.stream(
        {"messages": [input_message]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()


