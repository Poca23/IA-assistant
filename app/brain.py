import json
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .memory import Memory

class AIBrain:
    def __init__(self):
        try:
            self.memory = Memory()
            self.vectorizer = TfidfVectorizer(stop_words=None)
            self.responses = {
                "salut": [
                    "Salut ! Comment ça va ?", 
                    "Bonjour ! Que puis-je faire pour toi ?", 
                    "Hey ! Ravi de te voir !"
                ],
                "comment": [
                    "Ça va bien, merci ! Et toi ?", 
                    "Très bien ! Comment puis-je t'aider ?"
                ],
                "default": [
                    "Je ne comprends pas encore, mais je vais apprendre !", 
                    "Peux-tu reformuler ?", 
                    "Intéressant ! Dis-moi en plus."
                ]
            }
        except Exception as e:
            print(f"❌ Erreur initialisation AIBrain : {e}")
            raise
    
    def clean_input(self, user_input):
        """Nettoyer l'entrée utilisateur"""
        if not user_input:
            return ""
        
        cleaned = user_input.lower().strip()
        
        cleaned = re.sub(r'[^\w\s\-àéèêëîïôöùûüÿç]', '', cleaned)
        
        return cleaned
    
    def get_response(self, user_input):
        """Générer une réponse avec gestion d'erreurs renforcée"""
        try:
            if not user_input or len(user_input.strip()) == 0:
                return "Pardon, je n'ai rien entendu. Pouvez-vous répéter ?"
    
            # 🔹 1️⃣ NOUVEAU : Chercher dans Knowledge Base
            try:
                from .knowledge import KnowledgeBase
                kb = KnowledgeBase()
                
                user_lower = user_input.lower().strip()
                
                # Parcourir toutes les catégories
                for main_cat in ["general", "personal"]:
                    for sub_cat in kb.categories[main_cat]:
                        entries = kb.read_entries(main_cat, sub_cat)
                        
                        for entry in entries:
                            question_lower = entry["question"].lower().strip()
                            
                            # Match exact ou partiel
                            if question_lower == user_lower or question_lower in    user_lower or user_lower in question_lower:
                                response = entry["answer"]
                                self.memory.save_conversation(user_input,   response)
                                return response
            
            except Exception as kb_error:
                print(f"⚠️ Knowledge Base non disponible : {kb_error}")
    
            # 🔹 2️⃣ FALLBACK : Vérifier learned_responses (legacy)
            try:
                learned = self.memory.get_learned_responses()
                user_lower = user_input.lower().strip()
                
                if user_lower in learned and learned[user_lower]:
                    response = random.choice(learned[user_lower])
                    self.memory.save_conversation(user_input, response)
                    return response
                
                for learned_key in learned.keys():
                    if learned_key in user_lower or user_lower in learned_key:
                        if learned[learned_key]:
                            response = random.choice(learned[learned_key])
                            self.memory.save_conversation(user_input, response)
                            return response
            
            except Exception as memory_error:
                print(f"❌ Erreur mémoire : {memory_error}")
    
            # 🔹 3️⃣ FALLBACK FINAL : Patterns par défaut
            cleaned_input = self.clean_input(user_input)
            
            if len(cleaned_input) == 0:
                return "Je n'ai pas bien compris. Pouvez-vous reformuler ?"
            
            response = self._get_pattern_response(cleaned_input)
            
            try:
                self.memory.save_conversation(user_input, response)
            except Exception as save_error:
                print(f"❌ Erreur sauvegarde conversation : {save_error}")
            
            return response
    
        except Exception as e:
            print(f"❌ Erreur get_response : {e}")
            return "Désolée, j'ai rencontré un problème. Pouvez-vous réessayer ?"

    
    def _get_pattern_response(self, cleaned_input):
        """Générer une réponse basée sur des motifs"""
        try:
            if any(word in cleaned_input for word in ["salut", "hello", "bonjour", "hey", "hi"]):
                return random.choice(self.responses["salut"])
            
            elif any(word in cleaned_input for word in ["comment", "ça va", "ca va", "vas tu"]):
                return random.choice(self.responses["comment"])
            
            elif any(word in cleaned_input for word in ["merci", "thank", "thanks"]):
                return "De rien ! Je suis là pour ça !"
            
            elif any(word in cleaned_input for word in ["au revoir", "bye", "à bientôt", "tchao", "ciao"]):
                return "Au revoir ! À bientôt !"
            
            else:
                return random.choice(self.responses["default"])
                
        except Exception as e:
            print(f"❌ Erreur pattern response : {e}")
            return "Je ne comprends pas encore, mais je vais apprendre !"
    
    def get_stats(self):
        """Obtenir les statistiques avec gestion d'erreurs"""
        try:
            conversations = self.memory.load_conversations()
            return {
                'conversations': len(conversations.get('conversations', [])),
                'learned_responses': len(conversations.get('learned_responses', {}))
            }
        except Exception as e:
            print(f"❌ Erreur stats : {e}")
            return {'conversations': 0, 'learned_responses': 0}

if __name__ == "__main__":
    print("=== TEST MODULE BRAIN ===")
    try:
        ai = AIBrain()
        
        test_inputs = ["salut", "comment ça va ?", "merci", "question inconnue"]
        
        for test_input in test_inputs:
            response = ai.get_response(test_input)
            print(f"✅ '{test_input}' → '{response}'")
        
        stats = ai.get_stats()
        print(f"✅ Stats : {stats}")
        
    except Exception as e:
        print(f"❌ Erreur test : {e}")
    
    print("=== FIN TEST ===")
