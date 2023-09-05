<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/pdf.svg" width="100" />
<br>ChatPDF
</h1>
<h3>◦ Revolutionize collaboration with ChatPDF✨</h3>
<h3>◦ Developed using &nbsp;&nbsp; <span><b>🐍Python</b></span>&nbsp;&nbsp; | &nbsp;&nbsp; <span>🦜️🔗 <b>LangChain</b></span></h3>
  <p>
    
<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style&logo=Streamlit&logoColor=white" alt="Streamlit" />
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style&logo=OpenAI&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Markdown-000000.svg?style&logo=Markdown&logoColor=white" alt="Markdown" />
  </p>
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#️-features)
- [📂 Project Structure](#-project-structure)
- [🧩 Modules](#-modules)
- [🚀 Getting Started](#-getting-started)
  - [✔️ Prerequisites](#️-prerequisites)
  - [📦 Installation](#-installation)
  - [🎮 Using ChatPDF](#-using-chatpdf)
- [🤝 Contributing](#-contributing)

---


## 📍 Overview

The ChatPDF project is a Streamlit application that allows users to upload PDF and DOCX files and interact with a conversational AI model. It utilizes OpenAI API for conversational interactions and FAISS for fast similarity search. This project's core functionalities include parsing documents, extracting text, generating embeddings for user queries, and providing relevant responses based on document content. Its value proposition lies in simplifying the process of extracting information from documents and facilitating conversational interactions with the content.

---

## ⚙️ Features

| Feature                | Description                           |
| ---------------------- | ------------------------------------- |
| **⚙️ Architecture**     | The system follows a modular design pattern, where different components handle tasks such as file upload, document content extraction, vector conversion, conversational retrieval, and user interaction. The application uses the OpenAI API, FAISS, and various utilities for these tasks. It also incorporates a web interface with Streamlit.    |
| **📖 Documentation**   | The codebase provides clear and comprehensive documentation, explaining the purpose and usage of each component and function. It includes informative comments throughout the code to aid comprehension and maintainability.    |
| **🔗 Dependencies**    | The system relies on external libraries such as OpenAI, FAISS, and Streamlit for key functionalities. These dependencies are clearly listed in the project's requirements.txt file, making project setup and replication easier.    |
| **🧩 Modularity**      | The codebase is well organized into smaller, interchangeable components. Each component handles a specific task, promoting code reuse, maintainability, and ease of testing. The modular approach also allows for easy extension and customization.    |
| **⚡️ Performance**      | The system performance is subject to external factors such as API responses and document sizes. However, the codebase optimizes where possible, utilizing FAISS for efficient similarity search and vector retrieval.     |
| **🔀 Version Control** | The project is managed through Git version control, as evident from the GitHub repository. This enables collaborative development, branch management, and issue tracking. Proper commit history and commenting facilitate code reviews and easy troubleshooting.    |
| **🔌 Integrations**    | The system leverages multiple integrations, primarily with the OpenAI API for conversational interfaces and FAISS for similarity search. Streamlit is used to provide a web interface to users, and further integrations with additional services could be implemented for enhanced functionality.    |

---



## 📂 Project Structure




---

## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                             | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---                                                              | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [app.py](https://github.com/rahul2002m/ChatPDF/blob/main/app.py) | ChatPDF is a Streamlit application that allows users to upload PDF and DOCX files and ask questions about the content. It uses OpenAI API for conversational interactions, FAISS for fast similarity search, and various utilities for parsing and handling documents. It supports functions like parsing DOCX files, extracting textual content from PDFs and DOCX files, splitting text into manageable chunks, generating vectors from chunks using OpenAI embeddings and FAISS, and creating a ConversationalRetrievalChain instance for processing user queries. The main function handles file uploads, user input, and displays bot responses in a Streamlit interface. |

</details>

---

## 🚀 Getting Started

### ✔️ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - `pip install streamlit`
> - `pip install langchain `
> - `pip install openai`
> - `pip install faiss-cpu`
> - `pip install python-docx`
> - `pip install PyPDF2`


### 📦 Installation

1. Clone the ChatPDF repository:
```sh
git clone https://github.com/rahul2002m/ChatPDF
```

2. Change to the project directory:
```sh
cd ChatPDF
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using ChatPDF

```sh
streamlit run app.py
```
---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---
