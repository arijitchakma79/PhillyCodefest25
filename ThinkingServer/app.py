from flask import Flask, request, jsonify
import requests
import json

from src.chatbot.chatbot import Chatbot
from src.agents.preprocesser_agent import PreprocesserAgent
from src.utils.state_manager import State
from src.utils.llm_agent import OutputFormat
from src.knowledge.knowledge import Knowledge

app = Flask(__name__)

# Initialize the chatbot and preprocesser
chatbot = Chatbot()
preprocesser = PreprocesserAgent()
knowledge = Knowledge()

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

    print(knowledge.get_all_info())
    print(knowledge.get_info("name of the business"))


    return jsonify(result)

    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)