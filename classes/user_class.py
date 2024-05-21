import streamlit as st
from datetime import datetime
from config import pagesetup as ps
from supabase import create_client

class User:
    def __init__(self):
        self.initialize_user_attributes()

    def initialize_user_attributes(self):
        self.authenticated = False
        self.username = None
        self.password = None
        self.email = None
        self.firstname = None
        self.lastname = None
        self.fullname = None
        self.subsidiary = None
        self.threadid = None
        self.vectorid = None
        self.sfid = None
        self.userrole = None

    def initialize_clients(self):
        self.supabase_client = create_client(supabase_key=st.secrets.supabase.api_key_admin, supabase_url=st.secrets.supabase.url)
        self.select_string = f"{st.secrets.supabase.username_column}, {st.secrets.supabase.password_column}, {st.secrets.supabase.vstoreid_column}, {st.secrets.supabase.threadid_column}, {st.secrets.supabase.userrole_column}, {st.secrets.supabase.firstname_column}, {st.secrets.supabase.lastname_column}, {st.secrets.supabase.fullname_column}, {st.secrets.supabase.subsidiary_column}, {st.secrets.supabase.active_column}, {st.secrets.supabase.sfid_column}, {st.secrets.supabase.email_column}"
        
    def authenticate_user(self, username, password):
        self.username = username
        self.password = password
        response = self.supabase_client.table(st.secrets.supabase.users_table).select(self.select_string).eq(st.secrets.supabase.username_column, self.username).eq(st.secrets.supabase.password_column, self.password).execute()
        if response.data:
            self.authenticated = True
            self.user_data = response.data[0]
            self.threadid = self.user_data[st.secrets.supabase.threadid_column]
            self.vectorid = self.user_data[st.secrets.supabase.vstoreid_column]
            self.sfid = self.user_data[st.secrets.supabase.sfid_column]
            self.active = self.user_data[st.secrets.supabase.active_column]
            self.subsidiary = self.user_data[st.secrets.supabase.subsidiary_column]
            self.email = self.user_data[st.secrets.supabase.email_column]
            self.userrole = self.user_data[st.secrets.supabase.userrole_column]
            self.firstname = self.user_data[st.secrets.supabase.firstname_column]
            self.lastname = self.user_data[st.secrets.supabase.lastname_column]
            self.fullname = self.user_data[st.secrets.supabase.fullname_column]
            self.update_session_state()
            ps.switch_to_homepage()
            
    def display_userauth_form(self):
        userauth_container = ps.container_styled2(varKey="userauthcontainer")
        with userauth_container:
            userauth2_container = ps.container_styled3(varKey="userauth2container")
            with userauth2_container:
                userauth_columns = st.columns([1, 20, 1])
                with userauth_columns[1]:
                    st.text_input(label="Username", key="username")
                    st.text_input(label="Password", type="password", key="password")
                    st.button(label="Submit",key="checkexistinguser",on_click=self.authenticate_user, args=(st.session_state.username, st.session_state.password),type="primary")

    def update_session_state(self):
        st.session_state.username = self.username
        st.session_state.password = self.password
        st.session_state.email = self.email
        st.session_state.firstname = self.firstname
        st.session_state.lastname = self.lastname
        st.session_state.fullname = self.fullname
        st.session_state.active = self.active
        st.session_state.sfid = self.sfid
        st.session_state.threadid = self.threadid
        st.session_state.vectorid = self.vectorid
        st.session_state.subsidiary = self.subsidiary
        st.session_state.userrole = self.userrole
        st.session_state.authenticated = self.authenticated
