import streamlit as st
from config import pagesetup as ps, sessionstates as ss
from classes import user_class

# 1. Set Page Config
st.set_page_config(page_title=st.secrets.appconfig.app_name, page_icon=st.secrets.appconfig.app_icon, layout=st.secrets.appconfig.app_layout, initial_sidebar_state=st.secrets.appconfig.app_initial_sidebar)

ps.get_page_styling()

ps.display_background_image()

# 2. Session States
ss.initialize_session_states()

# 3. Set Page Title
ps.set_title_manual(varTitle="AlmyAI", varSubtitle="Login / Registration", varDiv=True)

# 4. Initialize UserFlow
user_flow = user_class.UserFlow()


# 5. Execute UserFlow
if not st.session_state.user['usertype_complete']:
    user_flow.userflow1_usertype_form()
elif not st.session_state.user['userauth_complete']:
    user_flow.userflow2_userauth_form()
else:
    # Redirect to home page if the userflow is complete
    ps.switch_to_homepage()