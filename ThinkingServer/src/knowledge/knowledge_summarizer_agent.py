from src.utils.llm_agent import LLMAgent, OutputFormat

class KnowledgeAgent(LLMAgent):
    def __init__(self):
        super().__init__()
        self.load_config("agents/knowledge_summarizer.yaml")