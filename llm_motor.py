from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
from templates.movie_agent import create_movie_recommendation_agent

def create_chat_model(api_key: str, model: str = "gpt-4-0125-preview", temperature: float = 0.7):
    return ChatOpenAI(
        openai_api_key=api_key,
        model=model,
        temperature=temperature
    )

class LLMMotor:
    def __init__(self, api_key: str, model: str = "gpt-4-0125-preview", temperature: float = 0.7):
        self.chat_model = create_chat_model(api_key, model, temperature)
        self.movie_agent = create_movie_recommendation_agent(self.chat_model)
        self.memory = ConversationBufferMemory(return_messages=True)

    def generate_response(self, prompt: str) -> str:
        self.memory.chat_memory.add_user_message(prompt)
        response = self.movie_agent.invoke({"messages": self.memory.chat_memory.messages})
        self.memory.chat_memory.add_ai_message(response.content)
        return response.content

    def get_chat_history(self) -> List[Dict[str, str]]:
        return [
            {"role": "user" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
            for msg in self.memory.chat_memory.messages
        ]

    def clear_memory(self):
        self.memory.clear()

    def start_new_conversation(self) -> str:
        self.clear_memory()
        opening_message = "Hello! I'm your movie recommendation assistant. How can I help you find something great to watch today?"
        self.memory.chat_memory.add_ai_message(opening_message)
        return opening_message

def get_available_models(api_key: str) -> List[str]:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    models = client.models.list()
    return [model.id for model in models.data if model.id.startswith("gpt")]
