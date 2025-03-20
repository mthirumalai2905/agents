from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agent import create_tool_calling_agent, AgentExecutor
from tools import  search_tool
from tools import wiki_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    source: list[str]
    tools_used: list[str]
    

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=os.getenv("ANTHROPIC_API_KEY"))
parser = PydanticOutputParser(pydantic_object=ReasearchResponse)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
    """
    You are a research assistant that will help generate a research paper.
    Answer the user query and use necessary toools.
    Wrap the output in this format and provide no other text\n{format_instructions}
    """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query} {name}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


tools = [search_tool]
agent = create_tool_calling_agent(
    llm = llm,
    prompt = prompt,
    tools = []
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})
print(raw_response)

try:
    strcutured_response = parser.parse(raw_response)
    print(structured_response)
except Exception as e:
    print(e)
    strcutured_response = None
    
    
