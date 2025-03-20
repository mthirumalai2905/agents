from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Saves the provided data to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)

# Initialize DuckDuckGo search tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="searchWeb",
    func=search.run,
    description="Search the web for information",
)

# Initialize Wikipedia API wrapper and search tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Example usage
query = "Artificial Intelligence"
wiki_result = wiki_tool.run(query)
search_result = search_tool.run(query)

# Save the results
save_to_txt(f"Wikipedia Result:\n{wiki_result}\n\nWeb Search Result:\n{search_result}")
print("Results saved to research_output.txt")
