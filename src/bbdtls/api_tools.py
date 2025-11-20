from tavily import TavilyClient
import os

# tavily search
def tavily_search(query, **kwargs):
    """
    Search tavily API
    @param query: search query
    @param kwargs: other keyword arguments
    @return: search results
    """
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    response = tavily_client.search(query, **kwargs)
    return response