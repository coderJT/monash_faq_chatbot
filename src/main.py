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
    # asyncio.run(scrape_url())
    # asyncio.run(scrape_pages())
    # process_data()
    # indexing()
    pass

# UI
st.set_page_config(page_title="Monash Student Chatbot", layout="centered")
st.title("🎓 Monash Student Chatbot")
st.markdown("""
Ask me anything about Monash University policies!  
You can try questions like:

- **"What is my GPA if I received grades: 4 HDs, 2 Ds, and 2 Cs at Year 1 Semester 2, assuming each unit has 4 credit points?"**  
- **"I have graduated and want to receive a physical certificate. What steps should I take?"**  
- **"How can I select my preferred class slots for next semester?"**
""")

# Run setup once
with st.spinner("Setting up backend (first time only)..."):
    run_setup_pipeline()

# Session state to track conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load previous chat conversations
for message in st.session_state.chat_history:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["text"])

# Handle input
user_input = st.chat_input("Type your question here...")

if user_input:
    with st.spinner("Thinking..."):
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = st.write_stream(evaluate(user_input)) 

        st.session_state.chat_history.append({"role": "bot", "text": response})
