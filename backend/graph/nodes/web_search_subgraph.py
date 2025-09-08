import operator
from typing import Any, Dict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain.schema import Document
from graph.state import GraphState
import time

class WebSearchState(GraphState):
    tavily_results: Document | None = None
    wiki_results: Document | None = None
    documents: List[Document]
    question: str

def tavily_search(state: WebSearchState) -> Dict[str, Any]:
    print(f"---STARTING TAVILY SEARCH at {time.strftime('%H:%M:%S')}---")
    start_time = time.time()
    
    from langchain_community.tools.tavily_search import TavilySearchResults
    web_search_tool = TavilySearchResults(k=3)
    question = state["question"]
    
    docs = web_search_tool.invoke({"query": question})
    results = "\n".join([d["content"] for d in docs])
    
    end_time = time.time()
    print(f"---TAVILY SEARCH COMPLETED at {time.strftime('%H:%M:%S')} (took {end_time - start_time:.2f}s)---")
    
    return {"tavily_results": Document(page_content=results)}

def wikipedia_search(state: WebSearchState) -> Dict[str, Any]:
    print(f"---STARTING WIKIPEDIA SEARCH at {time.strftime('%H:%M:%S')}---")
    start_time = time.time()
    
    from graph.chains.wiki_search import wiki_search
    question = state["question"]
    results = wiki_search(question)
    
    end_time = time.time()
    print(f"---WIKIPEDIA SEARCH COMPLETED at {time.strftime('%H:%M:%S')} (took {end_time - start_time:.2f}s)---")
    
    return {"wiki_results": Document(page_content=results)}

def combine_results(state: WebSearchState) -> Dict[str, Any]:
    print(f"---COMBINING SEARCH RESULTS at {time.strftime('%H:%M:%S')}---")
    documents = state.get("documents", [])
    
    # Wait for both results to be available
    if state.get("tavily_results") is None or state.get("wiki_results") is None:
        raise ValueError("Both search results must be available before combining")
    
    # Get results from both searches
    tavily_doc = state["tavily_results"]
    wiki_doc = state["wiki_results"]
    
    # Add search results to documents
    if documents:
        documents.extend([tavily_doc, wiki_doc])
    else:
        documents = [tavily_doc, wiki_doc]
    
    print("---RESULTS COMBINED---")
    return {"documents": documents}

# Create the web search subgraph
def create_web_search_graph() -> StateGraph:
    workflow = StateGraph(WebSearchState)
    
    # Add nodes for parallel execution
    workflow.add_node("tavily", tavily_search)
    workflow.add_node("wikipedia", wikipedia_search)
    workflow.add_node("combine", combine_results)
    
    # Define the graph edges
    workflow.add_edge(START, "tavily")
    workflow.add_edge(START, "wikipedia")
    workflow.add_edge("tavily", "combine")
    workflow.add_edge("wikipedia", "combine")
    workflow.add_edge("combine", END)
    
    return workflow.compile()