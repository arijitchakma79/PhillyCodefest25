from flask import Flask, request, jsonify, make_response
import requests
import json

from flask_cors import CORS

from src.chatbot.chatbot import Chatbot
from src.knowledge.preprocesser_agent import PreprocesserAgent
from src.utils.state_manager import State
from src.utils.llm_agent import OutputFormat
from src.knowledge.knowledge import Knowledge
from src.output.output_agent import OutputAgent
from src.simulation.initial_business_state_agent import InitialBusinessStateAgent

from src.simulation.simulation import Simulation 
from src.simulation.summarizer_agent import SummarizerAgent

app = Flask(__name__)

CORS(app)

# Initialize the chatbot and preprocesser
chatbot = Chatbot()
preprocesser = PreprocesserAgent()
knowledge = Knowledge()
output_agent = OutputAgent()
initial_business_state_agent = InitialBusinessStateAgent()
simulation = Simulation()
summarizer_agent = SummarizerAgent()

#CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message and return the response."""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Log the received data
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing required parameter: text'}), 400
        
        text_input = data.get('text', '')
        print(f"Processing input: {text_input}")  # Log the input text
        
        # Process regular chat input
        try:
            response = chatbot.process_input(text_input)
            print(f"Got response: {response}")  # Log the response
            
            # Get current state for the response
            current_state = chatbot.get_current_state().value
            
            return jsonify({
                'response': response,
                'state': current_state
            })
        except Exception as e:
            import traceback
            print(f"Error in chatbot processing: {str(e)}")
            print(traceback.format_exc())  # Print the full stack trace
            return jsonify({'error': str(e)}), 500
    except Exception as e:
        import traceback
        print(f"Error in request processing: {str(e)}")
        print(traceback.format_exc())  # Print the full stack trace
        return jsonify({'error': 'Server error: ' + str(e)}), 500

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
    print(result)

    """response = requests.post(
        url="http://127.0.0.1:5000/pipeline/analyze",
        json=result,
        headers={
            "Content-Type": "application/json",
        }
    )
    
    result = response.json()
    print(result)
    """

    knowledge.add_knowledge(result)
    
    initial_business_state = initial_business_state_agent.process_text(knowledge.get_all_info_text())

    print("-------------------------------------------")
    print("Initial Business State:")
    print(initial_business_state)
    print("-------------------------------------------")
    simulation_results = simulation.run_simulaton(initial_business_state)
    print(simulation_results)
    print(str(simulation.get_state_tree_json()))
    simulation_summary = summarizer_agent.process_text(str(simulation.get_state_tree_json()))
    print("Summary:")
    print(simulation_summary)
    

    print("-------------------------------------------")
    chatbot.descriptive_agent.set_knowledge(knowledge.get_all_info())
    output = json.loads(output_agent.process_text(knowledge.get_all_info_text()))
    output["thinking"] = json.loads(simulation_summary)

    print(output)

    return jsonify(output)

@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Get all accumulated knowledge."""
    return jsonify(knowledge.get_all_info())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3001)