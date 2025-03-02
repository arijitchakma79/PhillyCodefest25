from flask import Flask, request, jsonify, make_response
import requests
import json

from flask_cors import CORS

from src.chatbot.chatbot import Chatbot
from src.agents.preprocesser_agent import PreprocesserAgent
from src.utils.state_manager import State
from src.utils.llm_agent import OutputFormat
from src.knowledge.knowledge import Knowledge
from src.output.output_agent import OutputAgent

app = Flask(__name__)

# Initialize the chatbot and preprocesser
chatbot = Chatbot()
preprocesser = PreprocesserAgent()
knowledge = Knowledge()
output_agent = OutputAgent()

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message and return the response."""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required parameter: text'}), 400
    
    text_input = data.get('text', '')
    
    # Process regular chat input
    try:
        response = chatbot.process_input(text_input)
        
        # Get current state for the response
        current_state = chatbot.get_current_state().value
        
        return jsonify({
            'response': response,
            'state': current_state
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get the current state of the chatbot."""
    return jsonify({
        'state': chatbot.get_current_state().value
    })

@app.route('/api/state', methods=['POST'])
def set_state():
    """Set the current state of the chatbot."""
    data = request.get_json()
    
    if not data or 'state' not in data:
        return jsonify({'error': 'Missing required parameter: state'}), 400
    
    state_name = data.get('state', '').lower()
    
    if state_name == 'ideation':
        chatbot.set_state(State.IDEATION)
        return jsonify({
            'message': f"State changed to: {chatbot.get_current_state().value}",
            'state': chatbot.get_current_state().value
        })
    elif state_name == 'processing':
        chatbot.set_state(State.PROCESSING)
        return jsonify({
            'message': f"State changed to: {chatbot.get_current_state().value}",
            'state': chatbot.get_current_state().value
        })
    elif state_name == 'feedback':
        chatbot.set_state(State.FEEDBACK)
        return jsonify({
            'message': f"State changed to: {chatbot.get_current_state().value}",
            'state': chatbot.get_current_state().value
        })
    else:
        return jsonify({'error': f"Unknown state: {state_name}"}), 400

@app.route('/api/clear', methods=['POST'])
def clear():
    """Clear chat history and knowledge"""
    try:
        # Clear history for both agents
        chatbot.descriptive_agent.clear_history()
        chatbot.interface_agent.clear_history()

        chatbot.interface_agent.clear_knowledge()
        chatbot.descriptive_agent.clear_knowledge()
        
        # Clear knowledge base
        knowledge.clear()
        
        return jsonify({
            'message': "Chat history and knowledge cleared!",
            'state': chatbot.get_current_state().value
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['GET'])
def process():
    result = json.loads(preprocesser.process_text(chatbot.interface_agent.get_history_text()))
    
    response = requests.post(
        url="http://127.0.0.1:5000/analyze",
        json=result,
        headers={
            "Content-Type": "application/json",
        }
    )
    
    # Get the JSON response from the other server
    result = response.json()
    
    knowledge.add_knowledge(result)

    chatbot.descriptive_agent.set_knowledge(knowledge.get_all_info())

    output = output_agent.process_text(knowledge.get_all_info_text())

    return jsonify(output)

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Get all accumulated knowledge."""
    return jsonify(knowledge.get_all_info())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)