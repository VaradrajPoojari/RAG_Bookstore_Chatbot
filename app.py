import streamlit as st

from src.model import final_function

def main():

    st.set_page_config("Library Assistant")
    st.header("Ask me any questions:")

    input_str = st.text_input("Enter your question here")

    if st.button("Submit"):
        response = final_function(input_str)
        st.success("Answer:")
        st.write(response)

if __name__ == "__main__":
    main()
