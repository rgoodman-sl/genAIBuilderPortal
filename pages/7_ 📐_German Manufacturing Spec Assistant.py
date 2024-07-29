import streamlit as st
import requests
import time

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

st.set_page_config(page_title="GenAI Builder - Chatbot")
st.title("Manufacturing Spec Assistant")

st.markdown(
    """  
    ### This is an Assistant to help users retrieve information from Manufacturing Specifications and Tests.
    Examples: 
    - What are the university values for advertising
    - What is the Code of Conduct?
    - Describe the Community Safety Expectations for Students
    - What are the university provisions regarding alcohol?
    """)

# Document Selection
genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    index=None,
)

st.write("You selected:", genre)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Allow user to select Document
option = st.selectbox(
    "Which Document are you inquiring about?",
    ("MSG_01_HGPL-B.pdf", "MSG_02_HGPT_HGPL_HGDT.pdf", "MSG_04_measurement_test.pdf"),
    index=None,
    placeholder="Select contact Document...",
    
st.write("You selected:", option)
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me anything related to Fordham University Regulations")
if prompt:
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    URL = 'https://abd36121231c84034b34129e798681ad-485346289.eu-west-3.elb.amazonaws.com/api/1/rest/feed-master/queue/ConnectFasterInc/RG/msg/MSG_Retriever%20Task'
    BEARER_TOKEN = 'FXxWoR4LqJOGLJ6OZJeoC8xxHAvRyk7Y'

    data = {"prompt" : prompt}

    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}'
    }

    response = requests.post(
        url=URL,
        data=data,
        headers=headers,
        timeout=180,
        verify=False
    )

    result = response.json()
    #st.write(result)
    response=result[0]['choices'][0]['message']['content']
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #st.markdown(response,unsafe_allow_html=True)
        typewriter(text=response, speed=10)

# Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
