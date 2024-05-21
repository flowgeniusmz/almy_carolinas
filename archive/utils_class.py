import streamlit as st
from openai import OpenAI

class Utils():
    def __init__(self):
        self.openai_client = OpenAI(api_key=st.secrets.openai.api_key)

    def get_metadata_object(self, username, password, email, salesforce_id, first_name, last_name, full_name, subsidiary, is_active, thread_id, vector_store_id):
        """
        Returns a metadata object with specified keys and values.

        Parameters:
        - username (str): The username.
        - password (str): The password.
        - email (str): The email address.
        - salesforce_id (str): The Salesforce ID.
        - first_name (str): The first name.
        - last_name (str): The last name.
        - full_name (str): The full name.
        - subsidiary (str): The subsidiary.
        - is_active (bool): The active status.
        - thread_id (str): The thread ID.
        - vector_store_id (str): The vector store ID.

        Returns:
        - dict: The metadata object.
        """

        metadata_object = {
            "username": username,
            "password": password,
            "email": email,
            "salesforce_id": salesforce_id,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "subsidiary": subsidiary,
            "is_active": is_active,
            "thread_id": thread_id,
            "vector_store_id": vector_store_id
        }
        return metadata_object
    
    def create_thread(self, metadata_object=None):
        client = OpenAI(api_key=st.secrets.openai.api_key)
        thread = client.beta.threads.create(metadata = metadata_object)
        thread_id = thread.id
        return thread_id

    def create_vector_store(self, metadata_object=None):
        client = OpenAI(api_key=st.secrets.openai.api_key)
        vstore = client.beta.vector_stores.create(metadata=metadata_object)
        vstore_id = vstore.id
        return vstore_id
    
    def update_thread_metadata(self, thread_id, metadata):
        client = OpenAI(api_key=st.secrets.openai.api_key) 
        client.beta.threads.update(thread_id=thread_id, metadata=metadata)

    def update_vectorstore_metadata(self, vstore_id, metadata):
        client = OpenAI(api_key=st.secrets.openai.api_key) 
        client.beta.vector_stores.update(vector_store_id=vstore_id, metadata=metadata)

    def initial_message(self, thread_id, metadata):
        client = OpenAI(api_key=st.secrets.openai.api_key) 
        message = client.beta.threads.messages.create(role="assistant", content=f"You are the Alma personal Sales Assistant for the following person: {metadata}. Your job is to take their requests and provide the best sales support you can.", thread_id=thread_id)

    def add_assistant_message(self, thread_id, content):
        client = OpenAI(api_key=st.secrets.openai.api_key) 
        message = client.beta.threads.messages.create(role="assistant", thread_id=thread_id, content=content)

utils = Utils()


metadata1 = utils.get_metadata_object(
    username="kevin.notte@almalasers.com",
    password="AlmaEN2833!",
    email="kevin.notte@almalasers.com",
    salesforce_id="0051Y000009vzOyQAI",
    first_name="Kevin",
    last_name="Notte",
    full_name="Kevin Notte",
    subsidiary="Alma Lasers , Inc.",
    is_active="True",
    thread_id="thread_UQT5jdnV7OMlfRbVjbqGJlPA",
    vector_store_id="vs_6N7GM7W975SLKTbPD8CLcnZZ"
)

metadata2 = utils.get_metadata_object(
    username="tim.flood@almalasers.com",
    password="AlmaEX7131!",
    email="tim.flood@almalasers.com",
    salesforce_id="0051Y000009i2PIQAY",
    first_name="Tim",
    last_name="Flood",
    full_name="Tim Flood",
    subsidiary="Alma Lasers , Inc.",
    is_active="True",
    thread_id="thread_n5fpf4LWeJR4HLKCIcViG7BK",
    vector_store_id="vs_6z3AZqs22aBCbMGNMHB2Kmnl"
)

metadata3 = utils.get_metadata_object(
    username="michael.zozulia@almalasers.com",
    password="AlmaPY1836!",
    email="michael.zozulia@almalasers.com",
    salesforce_id="0055d00000DDbsTAAT",
    first_name="Michael",
    last_name="Zozulia",
    full_name="Michael Zozulia",
    subsidiary="Alma Lasers , Inc.",
    is_active="True",
    thread_id="thread_NNXW1Gij8p5yJaKnjeNNEadq",
    vector_store_id="vs_XQgyVdRytHYR2tcS8eOvkp3X"
)

a = """
# REFERENCE GUIDE:
## Salesforce Data
- The most recent Salesforce data for opportunities, leads, accounts, and contacts is provided in CSV files with CODE INTERPRETER TOOL
- The territory to be used is 0MI5d000000sYu6GAE	East - US - NC SC - the users are from the Carolinas Territory

## Zip Code Data
- All zip codes in the carolinas territory is found in Carolinas Zip Code csv file with CODE INTERPRETER TOOL

## USER REQUEST FOR LEADS
- If a user asks for a list of leads - use the TAVILY SEARCH AND FETCH YELP search tools. 
- You will recieve raw content or html content and you will return a table of providers found with any and all contact information. 

## If a user asks for Salesforce data
- Use the SOQL tool and use the salesforce reference guides in FILE SEARCH


"""

b = utils.add_assistant_message(thread_id="thread_NNXW1Gij8p5yJaKnjeNNEadq", content=a)
b = utils.add_assistant_message(thread_id="thread_UQT5jdnV7OMlfRbVjbqGJlPA", content=a)
b = utils.add_assistant_message(thread_id="thread_n5fpf4LWeJR4HLKCIcViG7BK", content=a)