import streamlit as st
import requests
import time
from dotenv import dotenv_values


# Load environment
env = dotenv_values(".env")
# SnapLogic RAG pipeline
URL = env["SL_CPA_TASK_URL"]
BEARER_TOKEN = env["SL_CPA_TASK_TOKEN"]
timeout = int(env["SL_TASK_TIMEOUT"])
namespace = env["SL_CPA_TASK_NAMESPACE"]
# Streamlit Page Properties
page_title=env["CPA_PAGE_TITLE"]
title=env["CPA_TITLE"]


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
    ### This is a Scraped Product Data Demo that allows employees to quickly find information about competing Cycling products
    - Carbon Fiber Frames ?
    - Most expensive grip tape ?
    - weight of carbon fiber bikes ?
 """)

# Initialize chat history
if "cpa_messages" not in st.session_state:
    st.session_state.cpa_messages = []

# Display chat messages from history on app rerun
for message in st.session_state.cpa_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me anything")
if prompt:
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.cpa_messages.append({"role": "user", "content": prompt})
    with st.spinner("Working..."):
        params={'namespace': namespace}
        data = {"prompt" : prompt}
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
        response = requests.post(
            url=URL,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,
            verify=False
        )

        if response.status_code==200:
            result = response.json()
            with st.chat_message("assistant"):
                typewriter(text=response, speed=10)
          #  if ['entity'][0]['completion'] in result:
             #   response=result['entity'][0]['completion'].replace("NEWLINE ", "**") + "**"
           #      #Display assistant response in chat message container
            #    with st.chat_message("assistant"):
             #       typewriter(text=response, speed=10)
                 #Add assistant response to chat history
              #  st.session_state.cpa_messages.append({"role": "assistant", "content": response})
         #   else:
          #      with st.chat_message("assistant"):
           #         st.error(f"❌ Error in the SnapLogic API response")
                    
        else:
            with st.chat_message("assistant"):
                st.error(f"❌ Error while calling the SnapLogic API")
