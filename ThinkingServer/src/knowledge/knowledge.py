from src.knowledge.knowledge_agent import KnowledgeAgent

class Knowledge:
    def __init__(self):
        self.__knowledge_agent = KnowledgeAgent()
        self.__knowledge = []

    def __update_agent_knowledge(self):
        knowledge_text = ""
        for element in self.__knowledge:
            knowledge_text += str(element) + "\n"

        self.__knowledge_agent.set_knowledge(knowledge_text)
        return knowledge_text
    
    def add_knowledge(self, content):
        self.__knowledge.append(content)

    def get_all_info(self):
        return self.__knowledge

    def get_info(self, topic):
        self.__update_agent_knowledge()
        return self.__knowledge_agent.process_text(topic)
