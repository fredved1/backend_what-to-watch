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
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

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
