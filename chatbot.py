import random
import re
from datetime import datetime

class Chatbot:
    def __init__(self):
        self.intents = {
            "greeting": {
                "keywords": ["hi", "hello", "hey", "greetings", "how are you", "how r u", "what's up", "how's it going"],
                "responses": [
                    "Hello! How can I help you today? 😊",
                    "Hi there! What can I do for you? 🤖",
                    "Hey! How’s it going? 👋"
                ]
            },
            "goodbye": {
                "keywords": ["bye", "goodbye", "see you", "farewell", "catch you later"],
                "responses": [
                    "Goodbye! Have a nice day! 👋",
                    "See you later! Take care! 😊",
                    "Bye! Stay safe! 🛡️"
                ]
            },
            "thanks": {
                "keywords": ["thanks", "thank you", "thx", "thank you so much"],
                "responses": [
                    "You're welcome! 😄",
                    "No problem! 👍",
                    "Happy to help! 😊"
                ]
            },
            "help": {
                "keywords": ["help", "support", "assist", "can you help"],
                "responses": [
                    "I am here to help! What do you need? 🆘",
                    "How can I assist you? 🤔"
                ]
            },
            "smalltalk": {
                "keywords": ["nothing", "fine", "ok", "okay", "good", "bad", "not much", "how are you"],
                "responses": [
                    "Oh, okay. 😌",
                    "Got it.",
                    "Tell me more.",
                    "Hmm, interesting! 🤨",
                    "Cool, what else?"
                ]
            }
        }
        self.fallback_responses = [
            "Sorry, I didn't understand that. Can you please rephrase? 🤷‍♂️",
            "I'm not sure I follow, could you say that differently? 🤔",
            "Hmm, I didn't get that. Can you try again?"
        ]

    def clean_message(self, message):
        message = message.lower()
        message = re.sub(r"[^a-z\s]", "", message)  # Remove punctuation/numbers
        message = message.replace(" u ", " you ")
        message = message.strip()
        return message

    def get_response(self, message):
        message = self.clean_message(message)

        for intent, data in self.intents.items():
            for keyword in data["keywords"]:
                if keyword in message:
                    return random.choice(data["responses"])

        return random.choice(self.fallback_responses)
