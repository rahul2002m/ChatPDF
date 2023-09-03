import os

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader

os.environ["OPENAI_API_KEY"] = ""  # OPENAI_API_KEY


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


def get_vector(chunks):
    return FAISS.from_texts(texts=chunks, embedding=OpenAIEmbeddings())


def get_llm_chain(vectors):
    llm_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
        retriever=vectors.as_retriever(),
        memory=ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        ),
    )
    return llm_chain


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
            vectors = get_vector(doc_chunks)
            st.session_state.llm_chain = get_llm_chain(vectors)


if __name__ == "__main__":
    main()
