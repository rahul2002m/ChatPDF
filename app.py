"""
ChatPDF: Conversational Interface for PDF Files.

This application allows users to upload PDF files, processes the textual content,
and enables users to ask questions related to the content of the PDF. The app
then provides answers to these questions by using a conversational language model.

Attributes:
-----------
imported modules:
    - os: Provides a way of using operating system dependent functionality.
    - streamlit: Framework for creating web apps with Python.
    - docx.Document: For parsing and extracting text from DOCX files.
    - langchain: Series of modules for conversational retrieval chains, chat models, embeddings,
                text splitters and vector stores.
    - PyPDF2.PdfReader: Used to extract text from PDF files.
    - templates: Contains predefined chat user interface templates.

Functions:
----------
- parseDocx(data: bytes) -> str:
    Parses a DOCX file and extracts the text content.

- get_text(docs: list) -> str:
    Extracts textual content from a list of uploaded PDF files.

- get_chunks(data: str) -> list:
    Splits the provided text data into manageable chunks.

- get_vector(chunks: list) -> FAISS:
    Generates vectors from text chunks using the FAISS vector store and OpenAI embeddings.

- get_llm_chain(vectors: FAISS) -> ConversationalRetrievalChain:
    Creates a conversational retrieval chain using a given set of vectors.

- create_user_chat_strip(user_input: str) -> None:
    Displays the user's message on the Streamlit interface.

- create_bot_chat_strip(bot_response: str) -> None:
    Displays the bot's response on the Streamlit interface.

- main() -> None:
    The main function that initializes the Streamlit application, handles file uploads,
    user queries, and bot responses.

Usage:
------
Run the code to initialize the Streamlit application. Use the sidebar to upload PDF files,
then ask questions related to the content of the uploaded PDFs in the text input box.
The bot will provide answers based on the content of the uploaded documents.
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
from templates import bot_template, css, user_template

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


def create_user_chat_strip(user_input):
    """
    Display the user's message on the Streamlit interface.

    Parameters:
    -----------
    user_input : str
        The text content of the user's message.

    Returns:
    --------
    None
    """
    st.write(user_template.replace("{{message}}", user_input), unsafe_allow_html=True)


def create_bot_chat_strip(bot_response):
    """
    Display the bot's response on the Streamlit interface.

    Parameters:
    -----------
    bot_response : str
        The text content of the bot's response.

    Returns:
    --------
    None
    """
    st.write(bot_template.replace("{{message}}", bot_response), unsafe_allow_html=True)


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

    st.write(css, unsafe_allow_html=True)

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
                create_user_chat_strip(msg.content)
            else:
                create_bot_chat_strip(msg.content)

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

    st.write(
        bot_template.replace(
            "{{message}}",
            "Hello, Please upload your files and click proceed to ask questions.",
        ),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
