from src.simulation.possible_actions_agent import PossibleActionsAgent
from src.simulation.state_prediction_agent import StatePredictionAgent
import json
import concurrent.futures

class Simulation:
    def __init__(self):
        self.__month_length = 3
        
        self.__state_history = []  # List of states by month
        self.__current_month = 0
        self.__state_tree = {}     # JSON tree structure of states
        
        self.__possible_actions_agent = PossibleActionsAgent()
        self.__state_prediction_agent = StatePredictionAgent()
    
    def __create_state_node(self, state_text):
        """Helper to parse state text into a node with state_description"""
        return {
            "state_description": state_text,
            "next_steps": {}
        }
    
    def __add_state_to_tree(self, tree, path, state_text, action):
        """
        Recursively add a state to the tree at the specified path
        
        Parameters:
        - tree: Current tree or subtree
        - path: List of actions leading to current position
        - state_text: The state text to add
        - action: Current action name
        """
        if not path:
            # We've reached the insertion point
            tree["next_steps"][action] = self.__create_state_node(state_text)
            return
        
        current = path[0]
        if current not in tree["next_steps"]:
            # This shouldn't happen in normal execution, but handle it
            tree["next_steps"][current] = self.__create_state_node("Placeholder")
        
        self.__add_state_to_tree(tree["next_steps"][current], path[1:], state_text, action)
    
    def run_simulaton(self, initial_state):
        # Initialize state history with initial state
        self.__state_history = [[initial_state]]
        
        # Initialize the state tree
        root_action = "Initial_State"
        self.__state_tree = {
            root_action: {
                "state_description": initial_state,
                "next_steps": {}
            }
        }
        
        # Track paths for each state to build tree
        state_paths = {initial_state: [root_action]}
                
        print("Simulation:")
        for t in range(self.__month_length):
            new_states = []
            current_states = self.__state_history[self.__current_month]
            
            # Prepare multithreading data structures
            state_action_pairs = []
            for current_state in current_states:
                actions_json = json.loads(self.__possible_actions_agent.process_text(current_state))
                if "actions" in actions_json:
                    for action in actions_json["actions"]:
                        state_action_pairs.append((current_state, action))
            
            # Process all state-action pairs in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit all tasks
                futures_to_pairs = {
                    executor.submit(
                        self.__state_prediction_agent.process_text,
                        state + " Action: " + action + " Month: " + str(self.__current_month + 1)
                    ): (state, action)
                    for state, action in state_action_pairs
                }
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(futures_to_pairs):
                    parent_state, action = futures_to_pairs[future]
                    try:
                        new_state = future.result()
                        new_states.append(new_state)
                        
                        # Build path and update tree
                        parent_path = state_paths[parent_state]
                        state_paths[new_state] = parent_path + [action]
                        
                        # Add the new state to the tree
                        self.__add_state_to_tree(
                            self.__state_tree[root_action], 
                            parent_path[1:], 
                            new_state, 
                            action
                        )
                    except Exception as e:
                        print(f"Error processing state-action pair: {e}")
            
            self.__state_history.append(new_states)
            self.__current_month += 1
        
        return new_states
    
    def get_state_tree(self):
        """Return the full state tree in JSON format"""
        return self.__state_tree
    
    def get_all_states(self):
        """Return a flattened list of all states for easy calculations"""
        all_states = []
        for month_states in self.__state_history:
            all_states.extend(month_states)
        return all_states
    
    def get_state_tree_json(self):
        """Return the full state tree as a JSON string"""
        return json.dumps(self.__state_tree, indent=2)