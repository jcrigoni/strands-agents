import streamlit as st
from agent import concierge_agent

def main():
    st.title("Concierge Chatbot")
    st.write("Ask me anything about restaurant recommendations based on weather conditions!")

    # Create a text input for user questions
    user_input = st.text_input("Your question:")

    if st.button("Send"):
        if user_input:
            # Get the response from the concierge agent
            response = concierge_agent(user_input)
            st.write("Concierge Agent:", response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()