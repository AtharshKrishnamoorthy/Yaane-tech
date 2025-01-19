from config import Config
from crewai import Agent
from crewai_tools import SerperDevTool
from llm import RateLimitedLLM
from models import CrimeCategories
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def create_search_tool():
    return SerperDevTool(
        api_key=Config.SERPER_API_KEY,
        search_type="search" 
    )


search_tool = create_search_tool()


guard_llm = RateLimitedLLM(
    model="groq/gemma2-9b-it",
    api_key=Config.GROQ_API_KEY
)

sanitize_llm = RateLimitedLLM(
    model="groq/llama-3.1-8b-instant",
    api_key=Config.GROQ_API_KEY
)

classify_llm = RateLimitedLLM(
    model="groq/mixtral-8x7b-32768",
    api_key=Config.GROQ_API_KEY
)

legal_llm = RateLimitedLLM(
    model="gemini/gemini-1.5-pro",
    api_key=Config.GEMINI_API_KEY
)

content_llm = RateLimitedLLM(
    model="gemini/gemini-1.5-flash",
    api_key=Config.GEMINI_API_KEY
)

def get_tool_config():
    """Get the configuration for tools with proper input schemas"""
    return {
        "tools": [search_tool],
        "tool_config": {
            "SerperDevTool": {
                "input_schema": {
                    "search_query": {
                        "type": "string",
                        "description": "The search query to use"
                    }
                }
            }
        }
    }


guard_agent = Agent(
    role='Guard Agent',
    goal='Verify if the provided information is crime-related',
    backstory="""You are an expert at identifying crime-related information. 
    Your task is to verify if user inputs are related to crimes.""",
    verbose=True,
    allow_delegation=False,
    llm=guard_llm
)

sanitization_agent = Agent(
    role='Sanitization Agent',
    goal='Remove sensitive information from crime-related queries',
    backstory="""You are an expert at identifying and removing sensitive personal information 
    while maintaining the essential details of crime-related queries.
    
    Always format your response as:
    Thought: [your reasoning]
    Action: [your action]
    Final Answer: [sanitized information]""",
    verbose=True,
    allow_delegation=False,
    llm=sanitize_llm
)

classification_agent = Agent(
    role='Classification Agent',
    goal='Classify crimes into categories',
    backstory=f"""You are an expert at classifying crimes according to Indian law.
    Use these categories: {CrimeCategories.MAIN_CATEGORIES}
    With subcategories: {CrimeCategories.SUBCATEGORIES}""",
    verbose=True,
    allow_delegation=False,
    llm=classify_llm
)


tool_config = get_tool_config()
legal_expert_agent = Agent(
    role='Legal Expert Agent',
    goal='Provide comprehensive legal information about crimes',
    backstory="""You are a legal expert specializing in Indian criminal law. 
    You provide detailed information about crimes, their severity, applicable laws, 
    reporting procedures, and penalties.""",
    tools=tool_config["tools"],
    tool_config=tool_config["tool_config"],
    verbose=True,
    allow_delegation=True,
    llm=legal_llm
)


content_agent = Agent(
    role='Content Genration Agent',
    goal='Generating legal advisory content for the users.',
    backstory="""You are an experienced legal content generator and legal advisor who takes in the responses and provides a guided advise to the users""",
    verbose=True,
    allow_delegation=False,
    llm=content_llm
)