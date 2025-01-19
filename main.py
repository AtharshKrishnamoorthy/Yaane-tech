import os
from dotenv import load_dotenv
import json
import streamlit as st
from crewai import Crew, Process
from tasks import create_tasks
import logging
from time import sleep
from config import Config

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="LEGAL AGENT",layout="centered")


def process_crime_info(user_input: str) -> str:
    """Process crime information with error handling and retries"""
    max_retries = Config.MAX_RETRIES
    retry_delay = Config.RETRY_DELAY
    
    for attempt in range(max_retries):
        try:
            tasks = create_tasks(user_input)
            crew = Crew(
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                memory=True,
                 embedder={
                       "provider": "huggingface",
                       "config": {
                           "api_url": "sentence-transformers/all-MiniLM-L6-v2",
                       }
                   }
            )
            result = crew.kickoff()
            return result
        except Exception as e:
            logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                sleep(retry_delay * (attempt + 1))
                continue
            raise e

def main():
    st.title("Legal Agent - Indian Crime Information System")
    st.markdown("Provide crime information to get comprehensive legal details")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    messages = st.container()
    
    with messages:
        for message in st.session_state.chat_history:
            st.chat_message(message["role"]).write(message["content"])
    
    if prompt := st.chat_input("Enter crime-related information:"):
        with st.spinner("Analyzing and generating response..."):
            with messages:
                st.chat_message("user").write(prompt)
                st.session_state.chat_history.append(
                    {"role": "user", "content": prompt}
                )
                
                try:
                    response = process_crime_info(prompt)
                    output_info = response.raw
                    st.chat_message("assistant").write(output_info)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": output_info}
                    )
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    logger.error(error_message)
    
    st.markdown("---")
    st.write("Built using Crew AI, LangChain, and Streamlit")

if __name__ == "__main__":
    main()