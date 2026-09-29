import streamlit as st
from workflow import chatbot
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_core.runnables import RunnableConfig

CONFIG: RunnableConfig = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

st.title("Agentic Chatbot with Langgraph")

#Loading converstaion history
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here")

if user_input:
    st.session_state['message_history'].append({'role':'user','content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)
    ai_message = response['messages'][-1].content
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
           message_chunk.content if isinstance(message_chunk, BaseMessage) else message_chunk
           for message_chunk, metadata in chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
            )
        )

        st.session_state['message_history'].append({'role':'assistant','content': ai_message})
        
        