from src.utils.llm_agent import LLMAgent, OutputFormat

class BusinessStateAgent(LLMAgent):
    def __init__(self):
         super().__init__()
         self.load_config("agents/preprocesser.yaml")