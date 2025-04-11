# Import libraries
import os
import sys
from dotenv import load_dotenv, find_dotenv
from openai import AzureOpenAI
import streamlit as st

sys.path.append('..')
from common_utils import *

# Define constants and icons
USER_ICON = 'https://static.vecteezy.com/system/resources/previews/014/194/215/non_2x/avatar-icon-human-a-person-s-badge-social-media-profile-symbol-the-symbol-of-a-person-vector.jpg'
BOT_ICON = 'https://th.bing.com/th/id/R.b978cf9a22395802eb1a6b17f3493584?rik=bfpE0b3W7KrLHQ&riu=http%3a%2f%2fwww.smart-home.com.co%2fImages%2fLogoMicrosoft.png&ehk=SjdKY8seAtRNgdbt6pfOD0%2fyTMe5jPZ1qQcoNcXZk0I%3d&risl=&pid=ImgRaw&r=0'
BOT_ICON = 'https://media.tenor.com/arlZrN0YovkAAAAC/robot-smile.gif'
MSFT_LOGO='microsoft.png'
APP_TITLE="RAG Chat Demo"

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
        #query = generate_query(st.session_state.openai_config["openai_client"],
        #                       st.session_state.openai_config["aoai_deployment_name"],
        #                       user_input)
        #print(f'Query REWRITTEN: {query}')
        
        query = user_input

        # Hybrid search
        results, num_results = semantic_hybrid_search(st.session_state.ai_search_config["ai_search_client_docs"],
                                                      st.session_state.openai_config["openai_client"],
                                                      st.session_state.openai_config["aoai_embedding_model"],
                                                      query, 10)
        print(f"query: {query}, num results: {num_results}")
        #show_results(results, query)

        # Valid chunks for the user question
        valid_chunks, num_chunks = get_filtered_chunks(st.session_state.openai_config["openai_client"],
                                                       st.session_state.openai_config["aoai_rerank_model"],
                                                       results, user_input)

        # Generate answer:
        answer = generate_answer(st.session_state.openai_config["openai_client"],
                                 st.session_state.openai_config["aoai_deployment_name"],
                                 valid_chunks, query)
        store_message(answer, is_user=False)

        # Mostrar todos los mensajes almacenados en la sesión
        for message in st.session_state.messages:
            message_role = message["role"]
            message_content = message["content"]

            if message_role in ("user", "assistant", "function") and message_content:
                message_markdown = get_message_markdown(message_content, message_role)
                st.markdown(message_markdown, unsafe_allow_html=True)