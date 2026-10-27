import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI, tools
from langgraph.graph import START, END
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import  tool
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_tavily import TavilySearch
from dotenv import load_dotenv



def set_env_vars():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()
    # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    # os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    # os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    # os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
    # os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
    # os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
    # os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")

class State(TypedDict):
    """
    A TypedDict to define the structure of the state dictionary.
    """
    messages:Annotated[list[BaseMessage], add_messages]


class Agent:
    """
    A class representing an agent that can process messages and interact with tools.
    """
    def __init__(self):
        self.state_graph = StateGraph(State)


    def llm(self, llm_name:str="gpt-5", temperature:float=0):
        """
        Create and return a ChatOpenAI instance.

        Returns:
            ChatOpenAI: An instance of the ChatOpenAI class.
        """
        return ChatOpenAI(model_name=llm_name, temperature=temperature)
    
    @tool
    def add(a:float, b:float) -> float:
        """
        Add two numbers.

        Always use this tool for any addition, even simple
        ones like 2 + 2. Never add numbers yourself.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of the two numbers.
        """
        return a + b

    @tool
    def web_search(query: str) -> dict:
        """
        Search the web for current information.

        Use this tool only for recent news, current events,
        and questions requiring up-to-date information.
        Do not use it for math (use the add tool for addition),
        general knowledge, or writing tasks you can answer yourself.

        Call this tool only ONCE per question. After you get
        the results, answer using them; do not search again.

        Args:
            query: The search query.
        
        Returns:
            dict: Top 3 Tavily search results

        """
        search = TavilySearch(max_results=3)

        try:
            result = search.invoke({"query": query})
            return result

        except Exception as e:
            return {"error": f"Web search failed: {str(e)}"}

 
    def binding_tools(self, llm, tools: list):
        """
        Bind multiple tools to the LLM and create
        a single ToolNode for execution.
        """

        tool_node = ToolNode(tools)
        llm_with_tools = llm.bind_tools(tools)

        return llm_with_tools, tool_node

    def call_llm_model(self, state:State, llm):
        """ Call llm model wiht state and messages """

        return {"messages":[llm.invoke(state["messages"])]}

    def build_graph(self):
        """
        Build the state graph by binding tools and defining transitions.

        Args:
            llm: The language model to be used.
            tools (list[Tool]): A list of tools to be bound to the state graph.
        """
        llm = self.llm()
        tools = [self.add, self.web_search]
        llm_with_tools, tool_node = self.binding_tools(llm, tools)

        # LLM node must accept graph state
        def llm_node(state: State):
            return self.call_llm_model(state, llm_with_tools)

        self.state_graph.add_node("llm_node", llm_node)
        self.state_graph.add_node("tools", tool_node)

        ## add edges
        self.state_graph.add_edge(START, "llm_node")
        self.state_graph.add_conditional_edges("llm_node", tools_condition)
        self.state_graph.add_edge("tools", "llm_node")

        return self.state_graph.compile()

    def run(self, input_message:str):
        """
        Run the agent with the given input message.

        Args:
            input_message (str): The input message to be processed by the agent.

        Returns:
            dict: The final state of the agent after processing the input message.
        """
        graph=self.build_graph()
        result = graph.invoke({"messages":[HumanMessage(content=input_message)]})
        return result

def create_graph():
    """Create and compile the agent for LangGraph Studio."""
    set_env_vars()
    agent = Agent()
    return agent.build_graph()


# LangGraph Studio entry point
graph = create_graph()

if __name__ == "__main__":
    set_env_vars()
    agent = Agent()
    result = agent.run("What is 2 + 2?")
    for message in result["messages"]:
        message.pretty_print()