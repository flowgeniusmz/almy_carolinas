import requests
import pandas as pd

def fetch_yelp_data(query, postalcode, start_page, num_pages):
    """
    Fetch data from Yelp search results.

    Parameters:
    - query (str): The search term for Yelp.
    - postalcode (str): The postal code for the search location.
    - start_page (int): The starting page number.
    - num_pages (int): The number of pages to fetch.

    Returns:
    - pd.DataFrame: A dataframe with columns URL, Response Status, Response Text, and Response JSON.
    """
    # Initialize an empty dataframe
    results_df = pd.DataFrame(columns=['URL', 'Response Status', 'Response Text', 'Response JSON'])
    
    # Define the headers
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    # Loop through the specified number of pages
    for i in range(start_page, 20):
        # Construct the URL
        url = f"https://www.yelp.com/search?find_desc={query}&find_loc={postalcode}&start={i}"
        
        # Make the request
        response = requests.get(url, headers=headers)
        
        # Collect the response details
        response_status = response.status_code
        response_text = response.text
        try:
            response_json = response.json()
        except ValueError:
            response_json = None
        
        # Append to the dataframe
        results_df = results_df.append({
            'URL': url,
            'Response Status': response_status,
            'Response Text': response_text,
            'Response JSON': response_json
        }, ignore_index=True)
    
    return results_df

# Example usage
# query = "private+medical+providers"
# postalcode = "60124"
# start_page = 10
# num_pages = 2  # This means it will fetch data for 2 pages

# results_df = fetch_yelp_data(query, postalcode, start_page, num_pages)
# print(results_df)
