import streamlit as st
import requests
import time
from dotenv import dotenv_values


# Load environment
env = dotenv_values(".env")
# SnapLogic RAG pipeline
URL = env["SL_ECE_TASK_URL"]
BEARER_TOKEN = env["SL_ECE_TASK_TOKEN"]
timeout = int(env["SL_TASK_TIMEOUT"])
# Streamlit Page Properties
page_title=env["ECE_PAGE_TITLE"]
title=env["ECE_TITLE"]


def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

st.set_page_config(page_title=page_title)

# Create a container for the header
header_container = st.container()
with header_container:
    st.title(title)
    st.markdown(
        """  
        ### This is a E-Commerce DB Agent demo that allows non-technical users to interact with SQL databases 
        Examples 
        - Which product had the highest profit margin in the Q3 2024?
        - Can you update the price of all products in the "tablet" category to include a 15% discount?
        - Compare our new product, iPhone 16, with our top 3 best-selling phones so far?
    """)

# Initialize chat history
if "ECE_messages" not in st.session_state:
    st.session_state.ECE_messages = []

# Create a container for all messages
messages_container = st.container()

# Display chat messages from history on app rerun
with messages_container:
    for message in st.session_state.ECE_messages:
        with st.chat_message(message["role"]):
            msg_container = st.container()
            with msg_container:
                st.markdown(message["content"])
            if "debug_log" in message:
                expander_container = st.container()
                with expander_container:
                    with st.expander("Show Agent's Process"):
                        st.markdown(message["debug_log"])

# React to user input
prompt = st.chat_input("Ask me anything")
if prompt:
    with messages_container:
        st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.ECE_messages.append({"role": "user", "content": prompt})
    with st.spinner("Working..."):
        data = {"prompt" : prompt}
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
        response = requests.post(
            url=URL,
            data=data,
            headers=headers,
            timeout=timeout,
            verify=False
        )

        if response.status_code==200:
            result = response.json()
            if 'summary' in result[0]:
                response_text = result[0]['short_response'].replace("$","\$").replace("NEWLINE ", "**") + "**" + "\n\n"
                log = result[0]['summary'].replace("$","\$").replace("NEWLINE ", "**") + "**" + "\n\n"
                # Add assistant response to chat history
                st.session_state.ECE_messages.append({
                    "role": "assistant", 
                    "content": response_text,
                    "debug_log": log
                })
            else:
                st.session_state.ECE_messages.append({
                    "role": "assistant",
                    "content": f"❌ Error in the SnapLogic API response\n{result.get('reason', 'Unknown error')}",
                    "debug_log": result
                })
        else:
            st.session_state.ECE_messages.append({
                "role": "assistant",
                "content": "❌ Error while calling the SnapLogic API",
                "debug_log": {
                    "status_code": response.status_code,
                    "response": response.text
                }
            })
        st.rerun()