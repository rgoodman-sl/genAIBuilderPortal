import streamlit as st
from dotenv import dotenv_values
import sys

# Load environment
env = dotenv_values(".env")
# Streamlit Page Properties
page_title = env["PAGE_TITLE"]
title = env["TITLE"]

def clear_chat_history(page_name):
    """
    Clear chat history for a specific page
    """
    chat_histories = {
        'E-Commerce DB Agent': 'EC_messages',
        'E-Commerce DB Agent_Expandable Log': 'ECE_messages',
        'HR Chatbot': 'HR_messages',
        'University Policy Agent': 'UNI_messages',
        'Deloitte Chatbot': 'DL_messages',
        'Content Reconciliation': 'CREC_messages',
        'Competitor Product Agent': 'CPA_messages',
        'Health Insurance Chatbot': 'UW_messages'
    }
    
    # If the page has a chat history, clear it
    if page_name in chat_histories:
        history_key = chat_histories[page_name]
        if history_key in st.session_state:
            del st.session_state[history_key]

# Set default page to E-Commerce DB Agent
try:
    current_page = sys.argv[4].split('/')[-1].replace('.py', '')
except:
    # Redirect to E-Commerce DB Agent page if no page is specified
    current_page = 'E-Commerce DB Agent'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = current_page
        st.switch_page("pages/E-Commerce DB Agent.py")

# If we're navigating to a new page, clear the previous page's history
if 'previous_page' in st.session_state:
    if st.session_state.previous_page != current_page:
        clear_chat_history(st.session_state.previous_page)

# Store the current page for next time
st.session_state.previous_page = current_page

st.set_page_config(page_title=page_title)
st.title(title)
st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ## SnapLogic GenAI Builder allows you to create LLM-based applications in no time!
    
    ### **👈 Select a demo from the sidebar** to see some examples of what GenAI Builder can do!

    ## Want to learn more?
    - Check out [GenAI Builder](https://www.snaplogic.com/products/genai-builder)
    - Jump into our [documentation](https://docs-snaplogic.atlassian.net/wiki/spaces/SD/overview?homepageId=34537)
    - Ask a question in our [community](https://community.snaplogic.com)
    """
)

# Add a manual clear button to the sidebar for the current page
if current_page != 'GenAI_Demo':
    if st.sidebar.button('Clear Current Chat History'):
        clear_chat_history(current_page)
        st.sidebar.success(f"Chat history cleared for {current_page}")
        st.experimental_rerun()