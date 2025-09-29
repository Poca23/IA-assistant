# app/brain.py - Cœur IA (15 lignes)
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AIBrain:
    def __init__(self):
        self.responses = {
            "salut": ["Salut ! Comment ça va ?", "Bonjour ! Que puis-je faire pour toi ?"],
            "default": ["Je ne comprends pas encore, mais je vais apprendre !", "Peux-tu reformuler ?"]
        }
    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        if "salut" in user_input or "bonjour" in user_input:
            return random.choice(self.responses["salut"])
        return random.choice(self.responses["default"])

