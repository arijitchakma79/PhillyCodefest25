from src.agents.interface_ai import InterfaceAI
import os
from src.utils.llm_agent import OutputFormat
import json

agent = ()

def run_cli(agent):
    """Run a command-line interface for interacting with the agent."""
    print("\n===== Travel Assistant Chat =====")
    print("Type 'exit' to quit, 'clear' to clear history, 'json' or 'text' to change format")
    print("================================================\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        elif user_input.lower() == 'clear':
            agent.clear_history()
            print("Chat history cleared!")
            continue
        
        elif user_input.lower() == 'json':
            agent.set_output_format(OutputFormat.JSON)
            print("Output format changed to JSON")
            continue
        
        elif user_input.lower() == 'text':
            agent.set_output_format(OutputFormat.TEXT)
            print("Output format changed to TEXT")
            continue
        
        try:
            response = agent.process_text(user_input)
            
            print("\nAssistant: ", end="")
            
            # Pretty print JSON if it's valid JSON
            try:
                if agent._LLMAgent__output_format == OutputFormat.JSON:
                    json_data = json.loads(response)
                    print(json.dumps(json_data, indent=2))
                else:
                    print(response)
            except json.JSONDecodeError:
                # If it's not valid JSON, just print as is
                print(response)
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Check for API key

    
    # Create the travel assistant
    travel_agent = InterfaceAI()
    
    # Run the CLI
    run_cli(travel_agent)