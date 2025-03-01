from enum import Enum

class State(Enum):
    """Simple enum to track workflow states"""
    IDEATION = "ideation"
    PROCESSING = "processing"
    FEEDBACK = "feedback"


class StateManager:
    """
    Simple state manager to track current state and handle transitions.
    Used to determine which agent should receive user input.
    """
    
    def __init__(self, initial_state=State.IDEATION):
        """Initialize with a default state"""
        self.current_state = initial_state
    
    def get_current_state(self):
        """Return the current state"""
        return self.current_state
    
    def transition_to(self, new_state):
        """Change to a new state"""
        if isinstance(new_state, State):
            self.current_state = new_state
            return True
        return False