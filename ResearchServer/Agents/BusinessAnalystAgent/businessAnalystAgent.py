import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
import openai
import requests
from dotenv import load_dotenv


dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env"))
load_dotenv(dotenv_path)

# Add this code to test
print(f"Dotenv path: {dotenv_path}")
# Try to access an environment variable, for example OPENAI_API_KEY
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key exists: {api_key is not None}")
# Print first few characters of the key if it exists (for security)
if api_key:
    print(f"First few characters of API key: {api_key[:5]}...")