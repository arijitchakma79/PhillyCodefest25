from src.simulation.possible_actions_agent import PossibleActionsAgent
from src.simulation.state_prediction_agent import StatePredictionAgent
import json
import concurrent.futures

class Simulation:
    def __init__(self):
        self.__month_length = 1
        
        self.__state_history = []
        self.__current_month = 0
        
        self.__possible_actions_agent = PossibleActionsAgent()
        self.__state_prediction_agent = StatePredictionAgent()
    
    def run_simulaton(self, initial_state):
        self.__state_history = [[initial_state]]
                
        print("Simulation:")
        for t in range(self.__month_length):
            new_states = []
            current_states = self.__state_history[self.__current_month]
            
            # Collect all state-action pairs
            state_action_pairs = []
            for current_state in current_states:
                actions_json = json.loads(self.__possible_actions_agent.process_text(current_state))
                if "actions" in actions_json:
                    for action in actions_json["actions"]:
                        state_action_pairs.append((current_state, action))
            
            # Process all state-action pairs in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit all tasks
                futures = [
                    executor.submit(
                        self.__state_prediction_agent.process_text,
                        state + " Action: " + action + " Month: " + str(self.__current_month + 1)
                    )
                    for state, action in state_action_pairs
                ]
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(futures):
                    new_state = future.result()
                    new_states.append(new_state)
            
            self.__state_history.append(new_states)
            self.__current_month += 1
        
        return new_states