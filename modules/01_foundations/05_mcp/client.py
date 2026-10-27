from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

client=MultiServerMCPClient({
    "math":{
        "command":"python",
        # "args":["mathserver.py"],
        "args":[os.path.join(os.path.dirname(__file__), "mathserver.py")],
        "transport":"stdio"
    },
    "weather":{
        "url":"http://127.0.0.1:8000/mcp",
        "transport":"streamable_http",
    }
})

model = ChatGroq(model="qwen/qwen3.8-27b")


async def call_math(question:str) -> str:
    """Answer the question with only the math server tools"""
    tools = await client.get_tools(server_name="math")
    agent = create_agent(model, tools=tools)
    response = await agent.ainvoke({"messages":[{"role":"user", "content":question}]})
    return response['messages'][-1].content


async def call_weather(question:str) -> str:
    """Answer the question with only the weather server tools"""
    tools = await client.get_tools(server_name="weather")
    agent = create_agent(model, tools=tools)
    response = await agent.ainvoke({"messages":[{"role":"user", "content":question}]})
    return response['messages'][-1].content


async def orchestrate(question:str) -> str:
    """Send weather questions to the weather helper, everything else to the math helper"""
    weather_words = ["weather", "temperature", "rain", "forecast", "humidity", "wind"]

    if any(word in question.lower() for word in weather_words):
        print("-> weather server")
        return await call_weather(question)

    print("-> math server")
    return await call_math(question)


async def main():
    while True:
        user_input = input("\nYou: ").strip()

        ## End option
        if user_input.lower() in ["exit", "quit", "end"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            print("Response: ", await orchestrate(user_input))
        except Exception as e:
            print("Error: ", e)


asyncio.run(main())
