from src.chatbot.descriptive_agent import DescriptiveAI
from src.chatbot.interface_agent import InterfaceAI
from src.utils.state_manager import StateManager, State

class Chatbot:
    """
    Chatbot interface that manages different agents based on the current state.
    Routes user inputs to the appropriate agent based on the state.
    """
    
    def __init__(self):
        """Initialize chatbot with agents and state manager"""
        self.state_manager = StateManager()
        self.descriptive_agent = DescriptiveAI()
        self.interface_agent = InterfaceAI()
        
    def process_input(self, user_input):
        """
        Process user input based on the current state
        
        Args:
            user_input (str): The text input from the user
            
        Returns:
            str: Response to the user
        """
        current_state = self.state_manager.get_current_state()
        
        # If state is processing, return a standard message
        if current_state == State.PROCESSING:
            return "I'm still processing your request. Please wait a moment."
        
        # Route to the appropriate agent based on state
        if current_state == State.IDEATION:
            response = self.interface_agent.process_text(user_input)
        elif current_state == State.FEEDBACK:
            response = self.descriptive_agent.process_text(user_input)
        else:
            # Default fallback
            response = "I'm not sure how to process this input in the current state."
        
        return response
    
    def set_state(self, new_state):
        """
        Change the current state of the chatbot
        
        Args:
            new_state (State): The new state to transition to
            
        Returns:
            bool: True if transition was successful, False otherwise
        """
        return self.state_manager.transition_to(new_state)
    
    def get_current_state(self):
        """
        Get the current state of the chatbot
        
        Returns:
            State: The current state
        """
        return self.state_manager.get_current_state()