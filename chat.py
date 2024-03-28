import streamlit as st
import time

from src.model import final_function

def main():
    st.title("Bookstore Chat 📚")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.chat_message("assistant"):
        st.markdown("How can I help you? Please enter your question below")

    # Accept user input
    if prompt := st.chat_input("Please enter your question here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    def response_generator(prompt):
        response = final_function(prompt)
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    with st.chat_message("assistant"):
        if st.session_state.messages:
            response = st.write_stream(response_generator(st.session_state.messages[-1]))
    # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
