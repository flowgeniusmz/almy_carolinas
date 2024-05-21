import streamlit as st
from classes import assistant_class as asst

st.set_page_config(page_title="AlmyAI", layout="wide", initial_sidebar_state="collapsed")
assistant = asst.Assistant()
thread_messages = assistant.initial_thread_messages

chat_container = st.container(height=500, border=True)
with chat_container:
    for msg in thread_messages:
        with st.chat_message(name=msg.role):
            st.markdown(body=msg.content[0].text.value)

if prompt := st.chat_input("Enter request here..."):
    
    with chat_container:
        with st.chat_message(name="user"):
            st.markdown(prompt)
        response_message = assistant.run_assistant(prompt=prompt)
        with st.chat_message("assistant"):
            st.markdown(response_message)
