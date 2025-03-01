from src.utils.llm_agent import LLMAgent, OutputFormat

class KnowledgeAgent(LLMAgent):
    def __init__(self):
        instructions = ""
        knowledge = ""

        super().__init__(instructions, False, OutputFormat.JSON, knowledge)

class Knowledge:
    def __init__(self):
        pass