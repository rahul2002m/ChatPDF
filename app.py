"""
ChatPDF

ChatPDF is a Streamlit application that allows users to upload PDF and DOCX files
and then ask questions related to the content of those documents.
The content of the documents is indexed and vectorized to allow for natural
language interactions. The application uses the OpenAI API to power the conversational
interface, FAISS for fast similarity search, and various other utilities to parse
and handle document content.

Functions:
----------
- parse_docx(data: bytes) -> str:
    Parse a DOCX file and return its textual content.

- get_text(docs: list) -> str:
    Extract and combine the textual content of a list of uploaded PDF and DOCX files.

- get_chunks(data: str) -> list:
    Split the provided text into manageable chunks based on characters.

- get_vector(chunks: list) -> FAISS:
    Convert a list of text chunks into vectors using OpenAI embeddings and store them using FAISS.

- get_llm_chain(vectors: FAISS) -> ConversationalRetrievalChain:
    Create a conversational retrieval chain instance ready for processing user queries 
    using the provided set of vectors.

- main() -> None:
    The main function initializes and runs the Streamlit application. It handles 
    the file uploads, user input, and displays bot responses.

If you run this module directly, it will start the Streamlit application where you can
upload PDFs and DOCX files, and then interact with their content using natural language queries.
"""


import os

import streamlit as st
from docx import Document
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader

os.environ["OPENAI_API_KEY"] = ""  # OPENAI_API_KEY


def parse_docx(data):
    """
    Parse and extract text content from a DOCX file.

    Parameters:
    -----------
    data : bytes
        The binary content of the DOCX file.

    Returns:
    --------
    str
        The extracted text content from the DOCX file.
    """
    document = Document(docx=data)
    content = ""
    for para in document.paragraphs:
        data = para.text
        content += data
    return content


def get_text(docs):
    """
    Extract textual content from a list of uploaded PDF files.

    Parameters:
    -----------
    docs : list
        List of uploaded PDF files.

    Returns:
    --------
    str
        The combined textual content of all the provided PDFs.
    """
    doc_text = ""
    for doc in docs:
        if ".pdf" in doc.name:
            pdf_reader = PdfReader(doc)
            for each_page in pdf_reader.pages:
                doc_text += each_page.extractText()
            doc_text += "\n"
        elif ".docx" in doc.name:
            doc_text += parse_docx(data=doc)

    return doc_text


def get_chunks(data):
    """
    Splits the provided text data into manageable chunks.

    Parameters:
    -----------
    data : str
        Text data that needs to be split.

    Returns:
    --------
    list
        A list containing chunks of the provided text data.
    """
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=250, length_function=len
    )
    text_chunks = text_splitter.split_text(data)
    return text_chunks


def get_vector(chunks):
    """
    Generate vectors from text chunks using FAISS vector store and OpenAI embeddings.

    Parameters:
    -----------
    chunks : list
        List of text chunks that need to be vectorized.

    Returns:
    --------
    FAISS
        FAISS vector store containing vectors of the provided text chunks.
    """
    return FAISS.from_texts(texts=chunks, embedding=OpenAIEmbeddings())


def get_llm_chain(vectors):
    """
    Create a conversational retrieval chain using the provided set of vectors.

    Parameters:
    -----------
    vectors : FAISS
        FAISS vector store containing vectors of text chunks.

    Returns:
    --------
    ConversationalRetrievalChain
        A conversational retrieval chain instance ready for processing user queries.
    """
    llm_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
        retriever=vectors.as_retriever(),
        memory=ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        ),
    )
    return llm_chain


def main():
    """
    Main function to initialize the Streamlit application.
    Handles file uploads, user queries, and bot responses.

    Returns:
    --------
    None
    """
    st.set_page_config(page_title="ChatPDF")
    st.title("ChatPDF - Chat with PDFs 📄")

    if not "llm_chain" in st.session_state:
        st.session_state.llm_chain = None

    if not "chat_history" in st.session_state:
        st.session_state.chat_history = []

    if not "doc_len" in st.session_state:
        st.session_state.doc_len = 0

    user_input = st.text_input("Ask any question related to the pdf")

    if user_input and st.session_state.llm_chain:
        bot_response = st.session_state.llm_chain({"question": user_input})
        st.session_state.memory = bot_response["chat_history"]
        for idx, msg in enumerate(st.session_state.memory):
            if idx % 2 == 0:
                with st.chat_message("user"):
                    st.write(msg.content)
            else:
                with st.chat_message("assistant"):
                    st.write(msg.content)

    elif user_input and not st.session_state.llm_chain:
        st.error("Please upload files and click proceed before asking questions")

    with st.sidebar:
        st.subheader("About")

        docs = st.file_uploader(
            "Upload PDF and click proceed", accept_multiple_files=True
        )

        if len(docs) > st.session_state.doc_len:
            st.session_state.doc_len = len(docs)
            with st.spinner("Processing..."):
                doc_text = get_text(docs)
                doc_chunks = get_chunks(doc_text)
                vectors = get_vector(doc_chunks)
                st.session_state.llm_chain = get_llm_chain(vectors)

    with st.chat_message("assistant"):
        st.write("Hello, Please upload your files and click proceed to ask questions.")


if __name__ == "__main__":
    main()
