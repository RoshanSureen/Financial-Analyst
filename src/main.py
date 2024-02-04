import os
import time
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import json
import time
import crud
import utils

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI")

# Streamlit UI for sidebar configuration
st.sidebar.title("Configuration")

client = None
assitant_id = None
# if entered_api_key:
with st.spinner('Initializing OpenAI assitant...'):
    client = crud.initialize_openai_client(OPENAI_API_KEY)
    assistant = crud.create_assitant(client)
    assitant_id = utils.extract_assitant_desc(assistant)['id']
    

# Sidebar for selecting the assistant
assistant_option = st.sidebar.selectbox(
    "Select an Assistant",
    ("Financial Assistant", "PDF Analyzer")
)

if assistant_option == "Financial Assistant":
    st.title("Financial Assistants :bar_chart:")

    # Description
    st.markdown("""
        This assistant is your go-to resource for financial insights and advice. Here's what you can do:
        - :page_facing_up: **Analyze financial statements** to understand your company's health.
        - :chart_with_upwards_trend: **Track market trends** and make informed investment decisions.
        - :moneybag: Receive tailored **investment advice** to maximize your portfolio's performance.
        - :bulb: **Explore various financial scenarios** and plan strategically for future ventures.

        Simply enter your financial query below and let the assistant guide you with actionable insights.
    """)
    user_query = st.text_input("Enter your financial query:")

    if st.button('Get Financial Insight') and client:
        with st.spinner('Fetching your financial insights...'):
            thread = crud.create_thread(client=client)
            run = crud.submit_message(client, assitant_id, thread, user_query)
            run = crud.wait_on_run(client, run, thread)
            response_messages = crud.get_response(client, thread)
            response = utils.pretty_print(response_messages)
            st.text_area("Response:", value=response, height=300)

elif assistant_option == "PDF Analyzer":
    st.title("PDF Analyzer  :mag:")

    # Description for PDF Analyzer
    st.markdown("""
        Use this tool to extract valuable information from PDF documents. Ideal for:
        - :page_facing_up: **Analyzing text and data** within PDFs for research or business insights.
        - :mag_right: **Extracting specific information** from large documents quickly.
        - :clipboard: Converting **PDF content into actionable data** to inform decision-making.
        - :bookmark_tabs: Gaining insights from **financial reports, research papers, or legal documents** in PDF format.

        Upload a PDF file and enter your specific query related to the document.
    """)

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    user_query = st.text_input("Enter your query about the PDF:")

    if uploaded_file is not None and user_query:
        with st.spinner('Analyzing PDF...'):
            temp_dir = "temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                file_response = client.files.create(
                    file=open(temp_file_path, "rb"),
                    purpose="assistants",
                )
                assistant = client.beta.assistants.update(
                    assitant_id,
                    file_ids=[file_response.id],
                )
                thread = crud.create_thread(client)
                run = crud.submit_message(client, assitant_id, thread, user_query)
                run = crud.wait_on_run(client, run, thread)
                response_messages = crud.get_response(client, thread)
                response = utils.pretty_print(response_messages)
                st.text_area("Response:", value=response, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Show a message if the API key is not entered
if not client:
    st.warning("Please enter your OpenAI API key in the sidebar to use the app.")



