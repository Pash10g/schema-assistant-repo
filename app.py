from openai import OpenAI
from typing_extensions import override
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock 
import streamlit as st
assistant_id = 'asst_3z6eylu26SneliNF8bqeJRLV'

client = OpenAI()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'thread' not in st.session_state:
    st.session_state.thread = client.beta.threads.create()





def ai_chat(prompt, messages):
    
    message = client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
        )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread.id,
        assistant_id=assistant_id)

   
    while not run.status == "completed":
        
        run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread.id,
        assistant_id=assistant_id)


    resp_messages = client.beta.threads.messages.list(
    thread_id=st.session_state.thread.id,
  )
    for current_part in resp_messages.data[0].content:
        if current_part.type == "text":
            messages.markdown(current_part.text.value)
        


    st.session_state.messages.append({"role": "assistant", "content": resp_messages.data[0].content[0].text.value})


    
    # return streamed_resp

st.markdown('## Chat with the Schema Design Assistant')
if st.button("New Chat"):
        st.session_state.messages=[]
        st.session_state.thread = client.beta.threads.create()
messages = st.container(height=500)

       

for message in st.session_state.messages:
    with messages.chat_message(message["role"]):
        messages.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Be creative, lets design great MongoDB applications together..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with messages.chat_message("user"):
        messages.markdown(prompt)
        
    with messages.chat_message("assistant"):
        with st.spinner("I'm thinking..."):
            response = ai_chat(prompt, messages)

