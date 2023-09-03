import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


def get_text(docs):
    doc_text = ""
    for doc in docs:
        pdf_reader = PdfReader(doc)
        for each_page in pdf_reader.pages:
            doc_text += each_page.extractText()
        doc_text += "\n"

    return doc_text


def get_chunks(data):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=250, length_function=len
    )
    text_chunks = text_splitter.split_text(data)
    return text_chunks


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
            doc_text = get_text(docs)
            doc_chunks = get_chunks(doc_text)
            st.write(doc_chunks)


if __name__ == "__main__":
    main()
