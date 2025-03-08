"""
LLM Motor module for handling movie recommendations using GPT models.
This module provides the core functionality for generating movie recommendations
and managing conversation state.
"""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Optional
from templates.movie_agent import create_movie_recommendation_agent
import logging
import os
import re
import requests

logger = logging.getLogger(__name__)

def create_chat_model(api_key: str, model: str = "gpt-4-0125-preview", temperature: float = 0.7) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance with the specified parameters.
    
    Args:
        api_key (str): OpenAI API key
        model (str): Model identifier (default: gpt-4-0125-preview)
        temperature (float): Temperature parameter for response generation (default: 0.7)
    
    Returns:
        ChatOpenAI: Configured chat model instance
    """
    return ChatOpenAI(
        openai_api_key=api_key,
        model=model,
        temperature=temperature
    )

class LLMMotor:
    """
    Main class for handling movie recommendations and conversation management.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4-0125-preview", temperature: float = 0.7):
        """
        Initialize the LLM motor with specified parameters.
        
        Args:
            api_key (str): OpenAI API key
            model (str): Model identifier (default: gpt-4-0125-preview)
            temperature (float): Temperature parameter for response generation (default: 0.7)
        """
        self.api_key = api_key
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        self.chat_model = create_chat_model(api_key, model, temperature)
        self.movie_agent = create_movie_recommendation_agent(self.chat_model)
        self.memory = ConversationBufferMemory(return_messages=True)
        logger.info(f"Initialized LLMMotor with model: {model}")

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the user's prompt.
        
        Args:
            prompt (str): User's input message
            
        Returns:
            str: Generated response
            
        Raises:
            ValueError: If prompt is empty or invalid
            Exception: For other errors during response generation
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid prompt")
            
        try:
            self.memory.chat_memory.add_user_message(prompt)
            response = self.movie_agent.invoke({"messages": self.memory.chat_memory.messages})
            self.memory.chat_memory.add_ai_message(response.content)
            
            # Extract movie recommendations and enhance with posters and details
            enhanced_response = self._enhance_with_movie_details(response.content)
            
            return enhanced_response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def _enhance_with_movie_details(self, response):
        """Extract movie titles from response and add poster URLs and details."""
        # Simple regex to find movie titles (this can be improved based on your response format)
        movie_titles = re.findall(r'"([^"]+)"', response)
        
        # If no titles found with quotes, try to find titles with common patterns
        if not movie_titles:
            # Look for titles that might be after numbers, colons, or at the beginning of lines
            movie_titles = re.findall(r'(?:^|\d+\.\s+|\:\s+)([A-Z][^\.!?]+?)(?=\s+\(|\s+-|\.|$)', response, re.MULTILINE)
        
        enhanced_data = {"original_response": response, "movies": []}
        
        for title in movie_titles:
            title = title.strip()
            if len(title) > 3:  # Avoid very short matches
                movie_info = self._get_movie_info(title)
                if movie_info:
                    enhanced_data["movies"].append(movie_info)
        
        return enhanced_data
    
    def _get_movie_info(self, title):
        """Get movie information from TMDB API."""
        if not self.tmdb_api_key:
            logging.warning("TMDB_API_KEY not set, skipping movie info retrieval")
            return {"title": title, "poster_url": None, "overview": None}
        
        try:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={self.tmdb_api_key}&query={title}"
            response = requests.get(search_url)
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                movie = data['results'][0]
                poster_path = movie.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                
                return {
                    "title": title,
                    "tmdb_title": movie.get('title'),
                    "poster_url": poster_url,
                    "overview": movie.get('overview'),
                    "release_date": movie.get('release_date'),
                    "vote_average": movie.get('vote_average'),
                    "tmdb_id": movie.get('id')
                }
        except Exception as e:
            logging.error(f"Error fetching movie info for {title}: {str(e)}")
        
        return {"title": title, "poster_url": None, "overview": None}

    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List[Dict[str, str]]: List of messages with role and content
        """
        return [
            {"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
            for msg in self.memory.chat_memory.messages
        ]

    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        try:
            self.memory.clear()
            logger.debug("Conversation memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}")
            raise

    def start_new_conversation(self) -> str:
        """
        Start a new conversation with a welcome message.
        
        Returns:
            str: Opening message
        """
        try:
            self.clear_memory()
            opening_message = "Hello! I'm your movie recommendation assistant. How can I help you find something great to watch today?"
            self.memory.chat_memory.add_ai_message(opening_message)
            return opening_message
        except Exception as e:
            logger.error(f"Error starting new conversation: {str(e)}")
            raise

def get_available_models(api_key: str) -> List[str]:
    """
    Get a list of available GPT models.
    
    Args:
        api_key (str): OpenAI API key
        
    Returns:
        List[str]: List of available model identifiers
        
    Raises:
        Exception: If unable to fetch models
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        return [model.id for model in models.data if model.id.startswith("gpt")]
    except Exception as e:
        logger.error(f"Error fetching available models: {str(e)}")
        raise
