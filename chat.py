import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf=r"C:\work\portfolio-website\Oussama_cv.pdf"):
    pdf = PdfReader(pdf)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    with open("bio.txt", "r") as f:
        bio_text = f.read()
    combined_text = bio_text + "\n\n" + "this is oussama's resume :\n" +text
    return combined_text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
   #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    def extract_after_word(text, word):
        pos = text.find(word)
        
        if pos != -1:
           
            return text[pos + len(word):].strip()
        else:
           
            return "Word not found in the string"


    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", extract_after_word(message.content, "Human:")), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat my resume",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with my resume :books:")
    user_question = st.text_input("Ask a question about oussama:")
    if user_question:
        raw_text = get_pdf_text()

                # get the text chunks
        text_chunks = get_text_chunks(raw_text)

                # create vector store
        vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
        st.session_state.conversation = get_conversation_chain(
                    vectorstore)
        user_prompt = f"""You are an AI assistant dedicated to assisting oussama in his job search by providing recruiters with relevant and concise information. 
    If you do not know the answer, politely admit it and let recruiters know how to contact oussama to get more information directly from him. 
    Don't put a breakline in the front of your answer.
    Human: {user_question}
    """
        handle_userinput(user_prompt)





if __name__ == '__main__':
    main()