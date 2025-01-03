import streamlit as st
import requests
import time
from dotenv import dotenv_values


# Load environment
env = dotenv_values(".env")
# SnapLogic RAG pipeline
URL = env["SL_EC_TASK_URL"]
BEARER_TOKEN = env["SL_EC_TASK_TOKEN"]
timeout = int(env["SL_TASK_TIMEOUT"])
# Streamlit Page Properties
page_title=env["EC_PAGE_TITLE"]
title=env["EC_TITLE"]


def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

st.set_page_config(page_title=page_title)
st.title(title)

st.markdown(
    """  
    ### This is a E-Commerce DB Agent demo that allows non-technical users to interact with SQL databases 
    Examples 
    - Which product had the highest profit margin in the Q3 2024?
    - Can you update the price of all products in the “tablet” category to include a 15% discount?
    - Compare our new product, iPhone 16, with our top 3 best-selling phones so far?
 """)

# Initialize chat history
if "EC_messages" not in st.session_state:
    st.session_state.EC_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.EC_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me anything")
if prompt:
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.EC_messages.append({"role": "user", "content": prompt})
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
            # st.write(result)
            # with st.chat_message("assistant"):
            #     st.markdown(result)
            if 'answer' in result[0]:
                response=result[0]['answer'].replace("$","\$").replace("NEWLINE ", "**") + "**" + "\n\n"
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.write(response)
                   # typewriter(text=response, speed=10)
                # Add assistant response to chat history
                st.session_state.EC_messages.append({"role": "assistant", "content": response})
            else:
                with st.chat_message("assistant"):
                    st.error(f"❌ Error in the SnapLogic API response")
                    st.error(f"{result['reason']}")
        else:
            with st.chat_message("assistant"):
                st.error(f"❌ Error while calling the SnapLogic API")
        st.rerun()