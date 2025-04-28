# Import libraries
import os
import sys
from dotenv import load_dotenv, find_dotenv
from openai import AzureOpenAI
import streamlit as st
import logging
from logging.handlers import RotatingFileHandler

sys.path.append('..')
from common_utils import *

# Define constants and icons
USER_ICON = 'https://static.vecteezy.com/system/resources/previews/014/194/215/non_2x/avatar-icon-human-a-person-s-badge-social-media-profile-symbol-the-symbol-of-a-person-vector.jpg'
BOT_ICON = 'https://th.bing.com/th/id/R.b978cf9a22395802eb1a6b17f3493584?rik=bfpE0b3W7KrLHQ&riu=http%3a%2f%2fwww.smart-home.com.co%2fImages%2fLogoMicrosoft.png&ehk=SjdKY8seAtRNgdbt6pfOD0%2fyTMe5jPZ1qQcoNcXZk0I%3d&risl=&pid=ImgRaw&r=0'
BOT_ICON = 'https://media.tenor.com/arlZrN0YovkAAAAC/robot-smile.gif'
MSFT_LOGO='microsoft.png'
APP_TITLE="RAG Chat Demo"
MAX_QUESTION_ANSWER_HISTORY = 3

# Función para mostrar mensajes en forma de bocadillo
def get_message_markdown(message, message_role="user"):
    if message_role == "user":
        return f"""
            <div style="display: flex; align-items: center; justify-content: flex-end;">
                <div style="background-color: lightblue; border-radius: 10px; padding: 10px; color: black; text-align: right; margin-left: 65%;">
                    {message}
                </div>
                <img src="{USER_ICON}" alt="User Icon" style="width: 40px; height: 40px; margin-left: 10px;">
            </div>
            """
    else:
        return f"""
            <div style="display: flex; align-items: flex-start;">
                <img src="{BOT_ICON}" alt="Microsoft Logo" style="width: 50px; margin-right: 10px;">
                <div style="background-color: lightgrey; border-radius: 10px; padding: 10px; color: black; text-align: left; margin-right: 35%;">
                    {message}
                </div>
            </div>
            """

def store_message(message, is_user=True):
    message_role = "user" if is_user else "assistant"
    st.session_state.messages.append({"role": message_role, "content": message})

# MAIN
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Load Azure OpenAI and AI Search variables and create clients
    openai_config, ai_search_config = load_config()
    st.session_state.openai_config = openai_config
    st.session_state.ai_search_config = ai_search_config
    st.session_state.history = []

    # Basic logging configuration
    log_file = "rag_chat.log"
    log_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)  # 5 MB per file, 2 backups
    log_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_formatter)
    st.session_state.logger = logging.getLogger()
    st.session_state.logger.setLevel(logging.INFO)
    st.session_state.logger.addHandler(log_handler)
    st.session_state.logger.info("RAG Chat application started.")
    st.session_state.logger.info(f"OpenAI config: {openai_config}")
    # Handler for printing to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    st.session_state.logger.addHandler(console_handler)

# Prepare the web app
st.set_page_config(
    page_title=APP_TITLE,
    layout="centered",
    initial_sidebar_state="auto",
)
st.image(MSFT_LOGO, width=80)
st.title(APP_TITLE)
user_input = st.chat_input("Your question:", key="input")
if user_input:
    store_message(user_input)

    with st.spinner("Generando respuesta..."):
        question = user_input
        print(f"User question: {question}")
        st.session_state.logger.info(f"User question: {question}")
        query = generate_search_query(st.session_state.openai_config["openai_client"],
                               st.session_state.openai_config["aoai_deployment_name"],
                               question,
                               st.session_state.history)
        print(f'Rewritten Question: {query}')
        st.session_state.logger.info(f'Rewritten Question: {query}')

        # Hybrid search
        results, num_results = semantic_hybrid_search(st.session_state.ai_search_config["ai_search_client_docs"],
                                                      st.session_state.openai_config["openai_client"],
                                                      st.session_state.openai_config["aoai_embedding_model"],
                                                      query, 10)
        print(f"query: {query}, num results: {num_results}")
        st.session_state.logger.info(f"query: {query}, num results: {num_results}")
        #show_results(results, query)

        # Valid chunks for the user question
        valid_chunks, num_chunks = get_filtered_chunks(st.session_state.openai_config["openai_client"],
                                                       st.session_state.openai_config["aoai_rerank_model"],
                                                       results, question)

        # Generate answer:
        #answer = generate_answer(st.session_state.openai_config["openai_client"],
        #                         st.session_state.openai_config["aoai_deployment_name"],
        #                         valid_chunks,
        #                         question)
        answer = generate_answer_with_history(st.session_state.openai_config["openai_client"],
                                              st.session_state.openai_config["aoai_deployment_name"],
                                              valid_chunks,
                                              question,
                                              st.session_state.history)
        st.session_state.logger.info(f"Answer: {answer}")
        store_message(answer, is_user=False)

        # check if the number of question and answer pair has reached the limit of N and remove the oldest one
        if len(st.session_state.history) >= MAX_QUESTION_ANSWER_HISTORY:
            st.session_state.history.pop(0)
        st.session_state.history.append({"question": question, "answer": answer})
        print(f"\nhistory: {json.dumps(st.session_state.history, indent=2)}\n")
        st.session_state.logger.info(f"\nhistory: {json.dumps(st.session_state.history, indent=2)}\n")
        print("--------------------------------------------------")

        # Mostrar todos los mensajes almacenados en la sesión
        for message in st.session_state.messages:
            message_role = message["role"]
            message_content = message["content"]

            if message_role in ("user", "assistant", "function") and message_content:
                message_markdown = get_message_markdown(message_content, message_role)
                st.markdown(message_markdown, unsafe_allow_html=True)