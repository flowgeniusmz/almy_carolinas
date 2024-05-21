import streamlit as st
from openai import OpenAI
from archive import tools_class_orig as tools
import json
import time


class Assistant:
    def __init__(self):
        self.thread_id = st.secrets.openai.zthread
        self.assistant_id = st.secrets.openai.assistant_id
        self.openai_client = OpenAI(api_key=st.secrets.openai.api_key)
        self.get_thread_messages()
        self.initial_thread_messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread_id)
        self.tools = tools.Tools()

    def get_thread_messages(self):
        self.thread_messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread_id)

    def create_message(self, role, content):
        self.message = self.openai_client.beta.threads.messages.create(thread_id=self.thread_id, role=role, content=content)
        self.message_id = self.message.id

    def create_run(self):
        self.run = self.openai_client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id)
        self.run_id = self.run.id
        self.run_status = self.run.status

    def retrieve_run(self):
        self.run = self.openai_client.beta.threads.runs.retrieve(run_id=self.run_id, thread_id=self.thread_id)
        self.run_id = self.run.id
        self.run_status = self.run.status

    def wait_on_run(self):
        while self.run_status != "completed":
            st.toast("Processing...")
            time.sleep(2)
            self.retrieve_run()
            if self.run_status == "completed":
                st.toast("Completed")
                self.get_thread_messages()
                self.get_response_message()
                break
            elif self.run.status == "requires_action":
                self.tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
                self.requires_action_type = self.run.required_action.type  # should be submit tool outputs
                self.submit_tool_outputs()
                if self.tool_outputs:
                    self.retrieve_run()

    def submit_tool_outputs(self):
        self.tool_outputs = []
        for tool_call in self.tool_calls:
            toolname = tool_call.function.name
            toolargs = json.loads(tool_call.function.arguments)
            toolid = tool_call.id
            if toolname == "fetch_yelp_data":
                tooloutput = self.tools.fetch_yelp_data(**toolargs)
            elif toolname == "search_tavily":
                tooloutput = self.tools.search_tavily(**toolargs)
            elif toolname == "execute_soql_query":
                tooloutput = self.tools.execute_soql_query(**toolargs)
            elif toolname == "execute_python_code":
                tooloutput = self.tools.execute_python_code(**toolargs)
            else:
                tooloutput = {"error": f"Unknown tool: {toolname}"}

            toolcalloutput = {"tool_call_id": toolid, "output": tooloutput}
            self.tool_outputs.append(toolcalloutput)

    def get_response_message(self):
        for message in self.thread_messages:
            if message.role == "assistant" and message.run_id == self.run_id:
                self.response_message = message.content[0].text.value

    def run_assistant(self, prompt):
        self.create_message(role="user", content=prompt)
        self.create_run()
        self.wait_on_run()
        self.get_response_message()
        return self.response_message