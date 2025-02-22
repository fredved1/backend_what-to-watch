import streamlit as st
import requests
import json

# Configure the page
st.set_page_config(
    page_title="What to Watch",
    page_icon="🎬",
    layout="centered"
)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# API endpoint
API_URL = "http://localhost:5001"

def get_recommendation(message):
    """Get movie recommendation from API"""
    try:
        response = requests.post(
            f"{API_URL}/recommend",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to server: {str(e)}"

# Main UI
st.title("🎬 What to Watch")
st.markdown("""
Find your next favorite movie or TV show! Tell me what you like, 
and I'll recommend something perfect for you.
""")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
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

# Feedback button in sidebar
with st.sidebar:
    st.markdown("### Help us improve!")
    if st.button("Give Feedback"):
        st.markdown("Thanks for helping us improve! [Feedback Form](your_feedback_form_link)")

# Footer
st.markdown("---")
st.markdown("*Don't forget to rate the recommendations to help us improve!*")
