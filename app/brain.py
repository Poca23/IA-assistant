# app/brain.py - Cœur IA avec mémoire intégrée (20 lignes)
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .memory import Memory

class AIBrain:
    def __init__(self):
        self.memory = Memory()
        self.vectorizer = TfidfVectorizer()
        self.responses = {
            "salut": ["Salut ! Comment ça va ?", "Bonjour ! Que puis-je faire pour toi ?", "Hey ! Ravi de te voir !"],
            "comment": ["Ça va bien, merci ! Et toi ?", "Très bien ! Comment puis-je t'aider ?"],
            "default": ["Je ne comprends pas encore, mais je vais apprendre !", "Peux-tu reformuler ?", "Intéressant ! Dis-moi en plus."]
        }
    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Recherche dans les réponses apprises
        learned = self.memory.get_learned_responses()
        if user_input in learned:
            response = random.choice(learned[user_input])
        else:
            # Réponses par motifs simples
            if any(word in user_input for word in ["salut", "hello", "bonjour"]):
                response = random.choice(self.responses["salut"])
            elif any(word in user_input for word in ["comment", "ça va"]):
                response = random.choice(self.responses["comment"])
            else:
                response = random.choice(self.responses["default"])
        
        # Sauvegarder la conversation
        self.memory.save_conversation(user_input, response)
        return response
