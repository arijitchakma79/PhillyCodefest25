from src.utils.llm_agent import LLMAgent, OutputFormat

class InitialBusinessStateAgent(LLMAgent):
    def __init__(self):
        super().__init__()
        self.load_config("agents/initial_business_state.yaml")