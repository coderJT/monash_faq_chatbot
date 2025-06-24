import streamlit as st
import asyncio
import playwright_setup

from source_urls_scraper import scrape_url
from url_details_scraper import scrape_pages
from clean_scraped_result import process_data
from build_index import indexing
from query_rag import evaluate  # This function should take user query as input

# Ensure async setup steps only run once
@st.cache_resource
def run_setup_pipeline():
    asyncio.run(scrape_url())
    asyncio.run(scrape_pages())
    process_data()
    indexing()

# UI
st.set_page_config(page_title="Monash Student Chatbot", layout="centered")
st.title("🎓 Monash Student Chatbot")
st.markdown("Ask me anything about Monash University policies!")

# Run setup once
with st.spinner("Setting up backend (first time only)..."):
    run_setup_pipeline()

# Session state to track conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Handle input
user_input = st.chat_input("Type your question here...")
if user_input:
    with st.spinner("Thinking..."):
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        with st.chat_message("assistant"):
            response = st.write_stream(evaluate(user_input)) 

        st.session_state.chat_history.append({"role": "bot", "text": response})
