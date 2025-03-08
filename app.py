import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_motor import LLMMotor, get_available_models
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

# Initialize LLMMotor with the movie recommendation agent
llm_motor = LLMMotor(api_key)

app = Flask(__name__)
CORS(app)

def validate_message(data: Dict[str, Any]) -> str:
    """Validate incoming message data."""
    if not isinstance(data, dict):
        raise ValueError("Invalid request format")
    
    message = data.get('message')
    if not message or not isinstance(message, str):
        raise ValueError("Message is required and must be a string")
    
    return message

@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Handle incoming messages and generate responses."""
    try:
        message = validate_message(request.json)
        response = llm_motor.generate_response(message)
        return jsonify({"response": response})
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    """Start a new conversation and return the opening message."""
    try:
        opening_message = llm_motor.start_new_conversation()
        return jsonify({"message": opening_message})
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        return jsonify({"error": "Failed to start conversation"}), 500

@app.route('/api/available-models', methods=['GET'])
def get_available_models_route():
    """Get list of available GPT models."""
    try:
        models = get_available_models(api_key)
        return jsonify({"models": models})
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        return jsonify({"error": "Failed to fetch available models"}), 500

@app.route('/api/select-model', methods=['POST'])
def select_model():
    """Select a different GPT model (placeholder for future implementation)."""
    try:
        data = request.json
        model = data.get('model')
        if not model:
            return jsonify({"error": "Model parameter is required"}), 400
        # Implement model selection logic if needed
        return jsonify({"success": True, "message": f"Model {model} selected"})
    except Exception as e:
        logger.error(f"Error selecting model: {str(e)}")
        return jsonify({"error": "Failed to select model"}), 500

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    """Clear the conversation memory."""
    try:
        llm_motor.clear_memory()
        return jsonify({"success": True, "message": "Memory cleared"})
    except Exception as e:
        logger.error(f"Error clearing memory: {str(e)}")
        return jsonify({"error": "Failed to clear memory"}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    """Get movie recommendations based on user input."""
    try:
        message = validate_message(request.json)
        response = llm_motor.generate_response(message)
        return jsonify({'response': response})
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return jsonify({'error': "Failed to generate recommendation"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'movie-recommendation-api'
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with service information."""
    return jsonify({
        'service': 'Movie Recommendation Service',
        'status': 'running',
        'version': '1.0.0',
        'deployment_test': 'This is a deployment test'
    })

@app.route('/test', methods=['GET'])
def test():
    logger.info("Test route accessed")
    return "Test route is working!"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"Starting Flask server on http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)