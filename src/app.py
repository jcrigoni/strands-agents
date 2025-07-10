import streamlit as st
from agent import concierge_agent

st.set_page_config(page_title="Concierge Chatbot", page_icon="🤖")

st.title("🤖 Concierge Chatbot")
st.write("Make a restaurant reservation based on weather conditions!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New user input
if prompt := st.chat_input("Ask something..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show spinner while agent is processing
    with st.spinner("Thinking..."):
        response = concierge_agent(prompt)

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
