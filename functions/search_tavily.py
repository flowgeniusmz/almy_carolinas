import streamlit as st
from tavily import TavilyClient

def search_tavily(query: str = None):
    """
    Searches for information using the TavilyClient.

    Parameters:
    - query (str): The search query string.

    Returns:
    - dict: The search response containing results, raw content, and answer if applicable.
    """
    include_raw_content = True
    max_results = 10
    include_answer = True
    search_depth = "advanced"
    
    # Initialize Tavily client with the API key from Streamlit secrets
    tavily_client = TavilyClient(api_key=st.secrets.tavily.api_key)
    
    # Perform the search with the given parameters
    search_response = tavily_client.search(
        query=query, 
        search_depth=search_depth, 
        include_raw_content=include_raw_content, 
        include_answer=include_answer
    )
    
    # Extract search results from the response
    search_results = search_response['results']
    
    return search_response
