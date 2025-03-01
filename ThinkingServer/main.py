import os
import json
from src.utils.llm_agent import OutputFormat
from src.chatbot.chatbot import Chatbot
from src.utils.state_manager import State

def run_cli(chatbot):
    """Run a command-line interface for interacting with the chatbot."""
    print("\n===== Business Idea Assistant =====")
    print("Type 'exit' to quit, 'clear' to clear history, 'json' or 'text' to change format")
    print("Type 'state [statename]' to change state (ideation, processing, feedback)")
    print("================================================\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        elif user_input.lower() == 'clear':
            # Clear history for both agents
            chatbot.descriptive_agent.clear_history()
            chatbot.interface_agent.clear_history()
            print("Chat history cleared!")
            continue
        
        elif user_input.lower() == 'json':
            # Set output format for both agents
            chatbot.descriptive_agent.set_output_format(OutputFormat.JSON)
            chatbot.interface_agent.set_output_format(OutputFormat.JSON)
            print("Output format changed to JSON")
            continue
        
        elif user_input.lower() == 'text':
            # Set output format for both agents
            chatbot.descriptive_agent.set_output_format(OutputFormat.TEXT)
            chatbot.interface_agent.set_output_format(OutputFormat.TEXT)
            print("Output format changed to TEXT")
            continue
        
        elif user_input.lower().startswith('state '):
            # Handle state change command
            state_name = user_input.lower().split('state ')[1].strip()
            
            if state_name == 'ideation':
                chatbot.set_state(State.IDEATION)
                print(f"State changed to: {chatbot.get_current_state().value}")
            elif state_name == 'processing':
                chatbot.set_state(State.PROCESSING)
                print(f"State changed to: {chatbot.get_current_state().value}")
            elif state_name == 'feedback':
                chatbot.set_state(State.FEEDBACK)
                print(f"State changed to: {chatbot.get_current_state().value}")
            else:
                print(f"Unknown state: {state_name}")
            continue
        
        try:
            # Use the chatbot to process the input
            response = chatbot.process_input(user_input)
            
            print("\nAssistant: ", end="")
            
            # Determine which agent was used based on state
            current_state = chatbot.get_current_state()
            current_agent = None
            
            if current_state == State.IDEATION:
                current_agent = chatbot.descriptive_agent
            elif current_state == State.FEEDBACK:
                current_agent = chatbot.interface_agent
            
            # Pretty print JSON if it's valid JSON and we're in a state with an agent
            if current_agent and current_state != State.PROCESSING:
                try:
                    if current_agent._LLMAgent__output_format == OutputFormat.JSON:
                        json_data = json.loads(response)
                        print(json.dumps(json_data, indent=2))
                    else:
                        print(response)
                except (json.JSONDecodeError, AttributeError):
                    # If it's not valid JSON, just print as is
                    print(response)
            else:
                # For PROCESSING state or any other case, just print the response
                print(response)
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = Chatbot()
    
    # Run the CLI with the chatbot
    run_cli(chatbot)