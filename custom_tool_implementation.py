from langchain_core.tools import tool
import os
from typing import Optional
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

load_dotenv(override=True)

import os
import random
from dotenv import load_dotenv
from langchain.tools import BaseTool, Tool
from typing import Type, Optional
from pydantic.v1 import BaseModel, Field # Use pydantic v1 for BaseTool compatibility

# Load environment variables (optional, for API keys if using real APIs)
load_dotenv(override=True)



class WeatherInput(BaseModel):
    """Input schema for the Weather Tool."""
    location: str = Field(description="The city name for which to get the weather.")

def get_current_weather(location: str) -> str:
    """
    Simulates fetching current weather for a location.
    In a real application, this would call an external weather API.
    """
    print(f"---> Calling Weather Tool for: {location}")

    try:

        temp_celsius = random.uniform(5.0, 35.0)
        conditions = random.choice(["Sunny", "Cloudy", "Rainy", "Windy", "Snowy (unlikely!)"])
        humidity = random.randint(30, 90)
        return f"The current weather in {location} is {temp_celsius:.1f}°C, {conditions}, with {humidity}% humidity."
    except Exception as e:
        return f"Error fetching weather for {location}: {e}"


class WeatherTool(BaseTool):
    name: str = "weather_checker"
    description: str = "Useful for finding the current weather conditions in a specific city. Input should be a city name."
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, location: str) -> str:
        """Use the tool."""
        return get_current_weather(location)

    async def _arun(self, location: str) -> str:
        """Use the tool asynchronously."""
        return self._run(location) # Simulate async call





def main():
    print("Running main")
    OPEN_WEATHER_API_KEY = os.environ["OPEN_WEATHER_API_KEY"]
    print(OPEN_WEATHER_API_KEY)
    
    weather_tool = WeatherTool()

    tools = [weather_tool]

    agent = create_react_agent("openai:gpt-4.1-mini", tools)
    input_message = {
    "role": "user",
    "content": "What should I wear today in San Francisco?",
}

    for step in agent.stream(
        {"messages": [input_message]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()