import requests
import json
import sys

class ChatbotClient:
    """Client for interacting with the chatbot server API."""
    
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url
    
    def chat(self, text):
        """Send a message to the chatbot API."""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def get_state(self):
        """Get the current state from the API."""
        response = requests.get(f"{self.base_url}/api/state")
        return response.json()
    
    def set_state(self, state_name):
        """Set the state via the API."""
        response = requests.post(
            f"{self.base_url}/api/state",
            json={"state": state_name},
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def clear(self):
        """Clear history and knowledge via the API."""
        response = requests.post(f"{self.base_url}/api/clear")
        return response.json()
    
    def process(self):
        """Trigger the preprocessor via the API."""
        response = requests.get(f"{self.base_url}/api/process")
        return response.json()
    
    def get_knowledge(self):
        """Get all knowledge from the API."""
        response = requests.get(f"{self.base_url}/api/knowledge")
        return response.json()


def run_cli():
    """Run a command-line interface for interacting with the chatbot server."""
    # Initialize the client
    client = ChatbotClient()
    
    # Check if server is available
    try:
        state = client.get_state()
        current_state = state.get('state', 'unknown')
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the server. Make sure it's running at http://localhost:3000")
        sys.exit(1)
    
    print("\n===== Business Idea Assistant (API Client) =====")
    print("Type 'exit' to quit, 'clear' to clear history")
    print("Type 'state [statename]' to change state (ideation, processing, feedback)")
    print("Type 'process' to run analysis, 'knowledge' to see all knowledge")
    print(f"Current state: {current_state}")
    print("================================================\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        elif user_input.lower() == 'clear':
            # Clear history and knowledge
            result = client.clear()
            print(result.get('message', 'Chat history and knowledge cleared!'))
            continue
        
        elif user_input.lower() == 'process':
            # Run the preprocesser
            try:
                result = client.process()
                print("\nAnalysis result:")
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"Error during processing: {str(e)}")
            continue
        
        elif user_input.lower() == 'knowledge':
            # Get all knowledge
            try:
                result = client.get_knowledge()
                print("\nCurrent knowledge:")
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"Error retrieving knowledge: {str(e)}")
            continue
        
        elif user_input.lower().startswith('state '):
            # Handle state change command
            state_name = user_input.lower().split('state ')[1].strip()
            try:
                result = client.set_state(state_name)
                print(result.get('message', f"State changed to: {state_name}"))
            except Exception as e:
                print(f"Error changing state: {str(e)}")
            continue
        
        try:
            # Send the user input to the chatbot
            result = client.chat(user_input)
            
            # Get the response
            response = result.get('response', 'No response from server')
            current_state = result.get('state', 'unknown')
            
            print(f"\nAssistant ({current_state}): ", end="")
            
            # Try to pretty print JSON if possible
            try:
                json_data = json.loads(response)
                print(json.dumps(json_data, indent=2))
            except (json.JSONDecodeError, TypeError):
                # If it's not valid JSON, just print as is
                print(response)
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    run_cli()