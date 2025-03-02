import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from enum import Enum

# Load environment variables
load_dotenv()

class OutputFormat(Enum):
    TEXT = "text"
    JSON = "json"

class LLMAgent:
    def __init__(self, instructions="", store_history=True, output_format=OutputFormat.TEXT, knowledge=""):
        self.__client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.__instructions = instructions
        self.__store_history = store_history
        self.__output_format = output_format
        self.__knowledge = knowledge
        self.__chat_history = []
        self.__examples = []

        self.__general_instructions = """
            Make sure you give your answers always in english and english character, no exception!
        """

    def load_config(self, file_path=None):
        """
        Load configuration from a YAML file.
        
        Args:
            file_path (str, optional): Path to the YAML config file.
                                    If None, will look for 'agents/config.yaml' or 'agents/config.yml'
                                    relative to main.py.
        
        Returns:
            bool: True if loading was successful, False otherwise.
        """
        import yaml  # Import yaml module

        
        if file_path is None:
            return False
        
   
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
            
            if not config:
                return False
                
            # Update configuration if properties exist in the loaded config
            if "instructions" in config:
                self.__instructions = config["instructions"]
                
            if "knowledge" in config:
                self.__knowledge = config["knowledge"]
                
            if "store_history" in config and isinstance(config["store_history"], bool):
                self.__store_history = config["store_history"]
                
            if "output_format" in config:
                if config["output_format"] == "JSON":
                    self.set_output_format(OutputFormat.JSON)
                elif config["output_format"] == "TEXT":
                    self.set_output_format(OutputFormat.TEXT)
                    
            return True
        
        except FileNotFoundError:

            print("Couldn't find config file!")
            # Config file not found, but that's okay - we'll use defaults
            return False
        except yaml.YAMLError as e:
            print(f"Warning: Invalid YAML in config file {file_path}: {str(e)}")
            return False
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return False


    def process_text(self, text_input):
        # Construct the system message with instructions
        system_content = self.__instructions + " " + self.__general_instructions
        
        # Add knowledge if provided
        if self.__knowledge:
            system_content += f"\n\nKnowledge: {self.__knowledge}"
            
        # Add output format instructions
        if self.__output_format == OutputFormat.JSON:
            system_content += "\n\nPlease format your response as a valid JSON object."
        
        messages = [
            {"role": "system", "content": system_content}
        ]
        
        # Add examples if they exist
        for example in self.__examples:
            messages.append(example)
        
        # Construct the user message with history if needed
        user_message = text_input
        
        if self.__store_history and self.__chat_history:
            history_text = "Chat History:\n"
            for entry in self.__chat_history:
                if entry["role"] == "user":
                    history_text += f"User: {entry['content']}\n"
                else:
                    history_text += f"Assistant: {entry['content']}\n"
            user_message = f"{history_text}\n\nCurrent request: {text_input}"
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Set response format for API only if JSON is requested
        response_format = None
        if self.__output_format == OutputFormat.JSON:
            response_format = {"type": "json_object"}
        
        response = self.__client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format=response_format,
            max_tokens=3500
        )
        
        response_content = response.choices[0].message.content
        
        # Store the conversation if history is enabled
        if self.__store_history:
            self.__chat_history.append({"role": "user", "content": text_input})
            self.__chat_history.append({"role": "assistant", "content": response_content})
        
        return response_content
    
    def add_example(self, role, content):
        """Add an example to the prompt"""
        self.__examples.append({"role": role, "content": content})
    
    def set_output_format(self, output_format):
        """Set output format to TEXT or JSON enum value"""
        if isinstance(output_format, OutputFormat):
            self.__output_format = output_format
        else:
            raise ValueError("Output format must be an OutputFormat enum value")
    
    def set_knowledge(self, knowledge):
        """Set or update the knowledge base text"""
        self.__knowledge = knowledge

    def clear_knowledge(self):
        self.__knowledge = ""
    
    def toggle_history(self, store_history):
        """Enable or disable chat history storage"""
        self.__store_history = store_history
    
    def clear_history(self):
        """Clear the chat history"""
        self.__chat_history = []
    
    def get_history(self):
        """Get the current chat history"""
        return self.__chat_history
    
    def get_history_text(self):
        history_text = "Chat History:\n"
        for entry in self.__chat_history:
            if entry["role"] == "user":
                history_text += f"User: {entry['content']}\n"
            else:
                history_text += f"Assistant: {entry['content']}\n"
        return history_text