import streamlit as st
from yelpapi import YelpAPI
from tavily import TavilyClient
from openai import OpenAI
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph

class Tools():
    def __init__(self):
        """Initialize the Tools class with Yelp and Tavily clients."""
        self.yelp_client = YelpAPI(api_key=st.secrets.yelp.api_key)
        self.tavily_client = TavilyClient(api_key=st.secrets.tavily.api_key)

    def tavily_search(self, query):
        """
        Perform a search using the Tavily API.
        
        Args:
            query (str): The search query.
        
        Returns:
            dict: The search results.
        """
        self.tavily_search_response = self.tavily_client.search(query=query, search_depth="advanced", include_raw_content=True, include_answer=True, max_results=10)
        self.tavily_search_results = self.tavily_search_response['results']
        return self.tavily_search_results

    def get_scrapegraph(self, query, url):
        """
        Get a scrape graph using the SmartScraperGraph.
        
        Args:
            query (str): The query to use in the scrape graph.
            url (str): The URL to scrape.
        
        Returns:
            dict: The response from the SmartScraperGraph.
        """
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
        return self.smartscrapergraph_response

    def yelp_query_search(self, query, zipcode):
        """
        Perform a Yelp search query.
        
        Args:
            query (str): The search term.
            zipcode (str): The location (zipcode) for the search.
        
        Returns:
            dict: The search results.
        """
        self.yelp_search_response = self.yelp_client.search_query(term=query, location=zipcode)
        self.businesses = self.yelp_search_response['businesses']
        return self.yelp_search_response

    def yelp_business_search(self, business_id):
        """
        Perform a Yelp business search query for detailed business information.
        
        Args:
            business_id (str): The Yelp business ID.
        
        Returns:
            dict: The detailed business information.
        """
        self.yelp_business_search_response = self.yelp_client.business_query(id=business_id)
        self.detailed_info = self.yelp_business_search_response
        return self.detailed_info

    def yelp_search(self, query, zipcode):
        """
        Perform a Yelp search and retrieve detailed information for each business.
        
        Args:
            query (str): The search term.
            zipcode (str): The location (zipcode) for the search.
        
        Returns:
            pd.DataFrame: A DataFrame containing detailed information for each business.
        """
        self.business_records = []
        self.yelp_query_search(query=query, zipcode=zipcode)
        for business in self.businesses:
            business_id = business.get('id')
            self.yelp_business_search(business_id=business_id)
            business_record = {
                'id': business.get('id'),
                'alias': business.get('alias'),
                'name': business.get('name'),
                'image_url': business.get('image_url'),
                'is_closed': business.get('is_closed'),
                'url': business.get('url'),
                'review_count': business.get('review_count'),
                'rating': business.get('rating'),
                'latitude': business['coordinates'].get('latitude') if business.get('coordinates') else None,
                'longitude': business['coordinates'].get('longitude') if business.get('coordinates') else None,
                'phone': business.get('phone'),
                'display_phone': business.get('display_phone'),
                'distance': business.get('distance'),
                'address1': business['location'].get('address1') if business.get('location') else None,
                'address2': business['location'].get('address2') if business.get('location') else None,
                'address3': business['location'].get('address3') if business.get('location') else None,
                'city': business['location'].get('city') if business.get('location') else None,
                'zip_code': business['location'].get('zip_code') if business.get('location') else None,
                'country': business['location'].get('country') if business.get('location') else None,
                'state': business['location'].get('state') if business.get('location') else None,
                'display_address': ", ".join(business['location'].get('display_address', [])) if business.get('location') else None,
                'is_claimed': self.detailed_info.get('is_claimed'),
                'cross_streets': self.detailed_info['location'].get('cross_streets') if self.detailed_info.get('location') else None,
                'photos': ", ".join(self.detailed_info.get('photos', [])),
                'hours': self.detailed_info.get('hours', [{}])[0].get('open', []),
                'is_open_now': self.detailed_info.get('hours', [{}])[0].get('is_open_now'),
                'transactions': ", ".join(self.detailed_info.get('transactions', []))
            }
            
            # Add categories to the record
            categories = business.get('categories', [])
            category_aliases = [cat['alias'] for cat in categories]
            category_titles = [cat['title'] for cat in categories]
            business_record['categories_alias'] = ", ".join(category_aliases)
            business_record['categories_title'] = ", ".join(category_titles)

            self.business_records.append(business_record)
        self.yelp_business_records_df = pd.DataFrame(self.business_records)
        return self.yelp_business_records_df

# Example usage
a = Tools()

# Perform a Yelp search and print the resulting DataFrame
b = a.yelp_search(query="private medical providers", zipcode="27018")
print(a.yelp_business_records_df)
