import streamlit as st


def main():
    st.set_page_config(page_title="ChatPDF")
    st.title("ChatPDF - Chat with PDFs 📄")

    user_input = st.text_input("Ask any question related to the pdf")
    st.write(user_input)

    with st.sidebar:
        st.subheader("About")

        docs = st.file_uploader(
            "Upload PDF and click proceed", accept_multiple_files=True
        )

        st.session_state.doc_len = len(docs)
        with st.spinner("Processing..."):
            pass


if __name__ == "__main__":
    main()
