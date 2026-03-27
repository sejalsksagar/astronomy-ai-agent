import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")

# --- Tool: Save User Query ---
def add_query_to_state(tool_context: ToolContext, query: str) -> dict:
    """Stores user query in state."""
    tool_context.state["QUERY"] = query
    logging.info(f"[State updated] QUERY: {query}")
    return {"status": "success"}

# --- Wikipedia Tool (for astronomy facts) ---
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# --- 1. Research Agent ---
astronomy_researcher = Agent(
    name="astronomy_researcher",
    model=model_name,
    description="Fetches astronomy-related information using Wikipedia.",
    instruction="""
    You are an astronomy research assistant.

    Your job:
    - Read the user's QUERY
    - Use the Wikipedia tool to fetch relevant astronomy information
    - Focus on concepts like planets, stars, black holes, galaxies, space missions, etc.
    - Extract clear, useful facts

    QUERY:
    { QUERY }
    """,
    tools=[wikipedia_tool],
    output_key="research_data"
)

# --- 2. Explanation Agent ---
astronomy_explainer = Agent(
    name="astronomy_explainer",
    model=model_name,
    description="Converts research into simple explanations.",
    instruction="""
    You are an astronomy expert who explains concepts in a simple and engaging way.

    Your job:
    - Take the RESEARCH_DATA
    - Explain it in beginner-friendly language
    - Keep it concise (under 150 words)
    - Use examples or analogies if helpful

    RESEARCH_DATA:
    { research_data }
    """
)

# --- Workflow ---
astronomy_workflow = SequentialAgent(
    name="astronomy_workflow",
    description="Handles astronomy queries by researching and explaining them.",
    sub_agents=[
        astronomy_researcher,
        astronomy_explainer
    ]
)

# --- Root Agent ---
root_agent = Agent(
    name="astronomy_assistant",
    model=model_name,
    description="Entry point for astronomy queries.",
    instruction="""
    You are an Astronomy Assistant 

    - Greet the user briefly
    - Ask what astronomy topic they want to learn about
    - When the user provides a query:
        1. Use 'add_query_to_state' tool
        2. Then pass control to 'astronomy_workflow'
    """,
    tools=[add_query_to_state],
    sub_agents=[astronomy_workflow]
)
