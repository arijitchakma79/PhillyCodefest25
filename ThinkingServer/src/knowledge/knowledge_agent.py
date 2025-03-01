from src.utils.llm_agent import LLMAgent, OutputFormat

class KnowledgeAgent(LLMAgent):
    def __init__(self):
        instructions = "You are an AI assistant which is responsible of knowledge base which is like an organized large text and answer quetions only using the information from knowledge base in requested format. "
        knowledge = ""

        super().__init__(instructions, False, OutputFormat.TEXT, knowledge)