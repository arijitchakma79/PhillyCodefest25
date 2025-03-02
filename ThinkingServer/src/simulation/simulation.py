from src.simulation.possible_actions_agent import PossibleActionsAgent
from src.simulation.state_prediction_agent import StatePredictionAgent
import json
import concurrent.futures
import re

class Simulation:
    def __init__(self, top_states_count=3):
        self.__month_length = 3
        self.__top_states_count = top_states_count  # Number of top states to keep
        
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
    
    def __extract_metrics(self, state_text):
        """
        Extract revenue and funding from state text
        Returns a tuple of (revenue, funding) or (0, 0) if not found
        """
        revenue = 0
        funding = 0
        
        # Using regex to find revenue and funding in the state text
        revenue_match = re.search(r'revenue[:\s]+[$]?(\d+(?:\.\d+)?)[KMB]?', state_text, re.IGNORECASE)
        funding_match = re.search(r'funding[:\s]+[$]?(\d+(?:\.\d+)?)[KMB]?', state_text, re.IGNORECASE)
        
        if revenue_match:
            revenue_str = revenue_match.group(1)
            try:
                revenue = float(revenue_str)
                # Handle K, M, B suffixes if present
                if 'K' in revenue_match.group(0):
                    revenue *= 1000
                elif 'M' in revenue_match.group(0):
                    revenue *= 1000000
                elif 'B' in revenue_match.group(0):
                    revenue *= 1000000000
            except ValueError:
                revenue = 0
        
        if funding_match:
            funding_str = funding_match.group(1)
            try:
                funding = float(funding_str)
                # Handle K, M, B suffixes if present
                if 'K' in funding_match.group(0):
                    funding *= 1000
                elif 'M' in funding_match.group(0):
                    funding *= 1000000
                elif 'B' in funding_match.group(0):
                    funding *= 1000000000
            except ValueError:
                funding = 0
        
        return (revenue, funding)
    
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
            current_states = self.__state_history[self.__current_month]
            
            # 1. Rank current states by revenue and funding
            state_metrics = []
            for state in current_states:
                revenue, funding = self.__extract_metrics(state)
                # Calculate a simple score (can be adjusted with weights if needed)
                score = revenue + funding
                state_metrics.append((state, score))
            
            # Sort states by score (highest first) and take top n states
            state_metrics.sort(key=lambda x: x[1], reverse=True)
            top_states = [state for state, _ in state_metrics[:self.__top_states_count]]
            
            print(f"Month {t+1}: Selecting top {len(top_states)} states out of {len(current_states)}")
            
            # 2. Process only the top states
            new_states = []
            state_action_pairs = []
            
            for current_state in top_states:
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
    
    def assign_knowledge(self, knowledge):
        self.__possible_actions_agent.set_knowledge(knowledge)
        self.__state_prediction_agent.set_knowledge(knowledge)