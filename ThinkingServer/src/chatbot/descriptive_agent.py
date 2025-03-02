from src.utils.llm_agent import LLMAgent, OutputFormat

class DescriptiveAI(LLMAgent):
    def __init__(self):
        super().__init__()
        self.load_config("agents/descriptive.yaml")