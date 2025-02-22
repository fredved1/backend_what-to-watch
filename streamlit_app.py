"""
Streamlit frontend for the What to Watch movie recommendation service.
This module provides the user interface for interacting with the movie recommendation system.
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:5001')
FEEDBACK_FORM_URL = os.getenv('FEEDBACK_FORM_URL', '#')

# Page configuration
st.set_page_config(
    page_title="What to Watch",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stMarkdown {
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

def get_recommendation(message: str) -> Optional[str]:
    """
    Get movie recommendation from API.
    
    Args:
        message (str): User's input message
        
    Returns:
        Optional[str]: Recommendation response or error message
    """
    try:
        response = requests.post(
            f"{API_URL}/recommend",
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 second timeout
        )
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return "Sorry, the request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to server: {str(e)}")
        return f"Error connecting to server. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "An unexpected error occurred. Please try again."

def initialize_session_state():
    """Initialize the session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def render_chat_interface():
    """Render the chat interface with message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate recommendations."""
    if prompt := st.chat_input("What kind of movie or show are you in the mood for?"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_recommendation(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def render_sidebar():
    """Render the sidebar with feedback button."""
    with st.sidebar:
        st.markdown("### Help us improve!")
        if st.button("Give Feedback"):
            st.markdown(f"Thanks for helping us improve! [Feedback Form]({FEEDBACK_FORM_URL})")

def main():
    """Main application function."""
    try:
        # Initialize session state
        initialize_session_state()

        # Main UI
        st.title("🎬 What to Watch")
        st.markdown("""
        Find your next favorite movie or TV show! Tell me what you like, 
        and I'll recommend something perfect for you.
        """)

        # Render chat interface
        render_chat_interface()

        # Handle user input
        handle_user_input()

        # Render sidebar
        render_sidebar()

        # Footer
        st.markdown("---")
        st.markdown("*Don't forget to rate the recommendations to help us improve!*")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()
