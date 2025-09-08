from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

def wiki_search(query: str) -> str:
    wikipedia = WikipediaAPIWrapper(
        top_k_results=3,
        doc_content_chars_max=3000
    )
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)
    return wiki_tool.run(query) 