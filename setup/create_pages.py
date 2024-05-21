import os
import toml


# Load the secrets.toml file
secrets = toml.load("secrets.toml")

# Extract relevant information
page_paths = secrets["pageconfig"]["page_paths"]
page_titles = secrets["pageconfig"]["page_titles"]

# Ensure the pages directory exists
pages_dir = "pages"
os.makedirs(pages_dir, exist_ok=True)

# Template for the content of each page
page_template = """import streamlit as st
from classes import pagesetup_class as pageclass

page_number = {page_number}
pageclass.PageSetup(page_number=page_number)
"""

# Create a Python file for each page
for page_number, (path, title) in enumerate(zip(page_paths, page_titles)):
    content = page_template.format(page_number=page_number)
    
    with open(os.path.join(pages_dir, path), "w") as file:
        file.write(content)

print("Pages created successfully.")
