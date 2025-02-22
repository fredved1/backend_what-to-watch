import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_motor import LLMMotor, get_available_models
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

# Initialize LLMMotor with the movie recommendation agent
llm_motor = LLMMotor(api_key)

app = Flask(__name__)
CORS(app)

@app.route('/api/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    response = llm_motor.generate_response(message)
    return jsonify({"response": response})

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    opening_message = llm_motor.start_new_conversation()
    return jsonify({"message": opening_message})

@app.route('/api/available-models', methods=['GET'])
def get_available_models_route():
    models = get_available_models(api_key)
    return jsonify({"models": models})

@app.route('/api/select-model', methods=['POST'])
def select_model():
    data = request.json
    model = data.get('model')
    # Implement model selection logic if needed
    return jsonify({"success": True, "message": f"Model {model} selected"})

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    llm_motor.clear_memory()
    return jsonify({"success": True, "message": "Memory cleared"})

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get recommendation using the LLMMotor
        response = llm_motor.generate_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/', methods=['GET'])
def home():
    return "Movie Recommendation Service is running!"

@app.route('/test', methods=['GET'])
def test():
    logger.info("Test route accessed")
    return "Test route is working!"

if __name__ == '__main__':
    logger.info("Starting Flask server on http://0.0.0.0:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)