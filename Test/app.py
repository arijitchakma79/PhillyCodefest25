from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Chatbot response messages
chat_responses = [
    "I'm here to help! What would you like to know?",
    "That’s an interesting question. Let me think about it.",
    "I understand. Here’s what I can tell you.",
    "Could you provide more details?",
]

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("text", "")

    # Select a random chatbot response
    ai_response = random.choice(chat_responses)

    return jsonify({"response": ai_response})

@app.route("/api/process", methods=["GET"])
def process():
    generated_content = {
        "code": "def greet():\n    print('Hello, world!')\n\ngreet()",
        "data": "Sample dataset for analysis",
        "analysis": "This is an example of AI-generated analysis.",
        "results": "Results from the requested process."
    }
    return jsonify(generated_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
