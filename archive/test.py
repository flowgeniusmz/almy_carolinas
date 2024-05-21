import streamlit as st
from openai import OpenAI

assistantid = "asst_LXiyMQQ4HzOSlxIWfwLFt1S2"
client = OpenAI(api_key=st.secrets.openai.api_key)
thread = client.beta.threads.create(metadata={"username"})

base_url = st.secrets.urlconfig.yelp_search_url 
url = base_url.format(query="dafd", postalcode="aadfad", i="20")
print(url)


#= "https://www.yelp.com/search?find_desc={query}&find_loc={postalcode}&start={i}"