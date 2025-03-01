import os
from dotenv import load_dotenv


# Load environment variables
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path)

class Config:
    """Configuration settings for Flask app"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG = True

