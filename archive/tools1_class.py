import streamlit as st
from yelpapi import YelpAPI
from tavily import TavilyClient
from openai import OpenAI
from scrapegraphai.graphs import SmartScraperGraph



class Tools():
    def __init__(self):
        self.yelp_client = YelpAPI(api_key=st.secrets.yelp.api_key)
        self.tavily_client = TavilyClient(api_key=st.secrets.tavily.api_key)


    def yelp_search(self, query, zipcode):
        self.yelp_search_response = self.yelp_client.search_query(term=query, location=zipcode)
        
    def tavily_search(self, query):
        self.tavily_search_response = self.tavily_client.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=10)
        self.tavily_search_results = self.tavily_search_response['results']

    def get_scrapegraph(self, query, url):
        self.scrapegraph_config = {
            "llm": {
                "api_key": st.secrets.openai.api_key,
                "model": "gpt-4o",
            },
            "verbose": True,
            "headless": False,
        }
        self.smart_scraper_graph = SmartScraperGraph(prompt=query, source=url, config=self.scrapegraph_config)
        self.smartscrapergraph_response = self.smart_scraper_graph.run()

a = Tools()

#b = a.yelp_search(query="private medical providers", zipcode="27018")
#print(a.yelp_search_response)