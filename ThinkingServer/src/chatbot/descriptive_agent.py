from src.utils.llm_agent import LLMAgent, OutputFormat

class DescriptiveAI(LLMAgent):
    def __init__(self):
        instructions = """
           Only say apple
        """

        knowledge = ""

        super().__init__(instructions, True, OutputFormat.TEXT, knowledge)