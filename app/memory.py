# app/memory.py - Gestionnaire de mémoire renforcé
import json
import os
import time
from datetime import datetime

class Memory:
    def __init__(self):
        self.file_path = "data/conversations.json"
        self.ensure_data_structure()
    
    def ensure_data_structure(self):
        """S'assurer que la structure de données existe"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            # Créer le fichier s'il n'existe pas
            if not os.path.exists(self.file_path):
                initial_data = {
                    "conversations": [],
                    "learned_responses": {}
                }
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, ensure_ascii=False, indent=2)
            
            # Vérifier la structure du fichier existant
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Ajouter les clés manquantes si nécessaire
            if "conversations" not in data:
                data["conversations"] = []
            if "learned_responses" not in data:
                data["learned_responses"] = {}
            
            # Sauvegarder si modifié
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ Erreur initialisation mémoire : {e}")
            # Créer un fichier de base en cas d'erreur
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump({"conversations": [], "learned_responses": {}}, f)
            except:
                pass
    
    def load_conversations(self):
        """Charger les conversations avec gestion d'erreurs"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Vérifier la structure
            if not isinstance(data, dict):
                data = {"conversations": [], "learned_responses": {}}
            
            if "conversations" not in data:
                data["conversations"] = []
            if "learned_responses" not in data:
                data["learned_responses"] = {}
            
            return data
            
        except json.JSONDecodeError:
            print("❌ Fichier JSON corrompu, recréation...")
            self.ensure_data_structure()
            return {"conversations": [], "learned_responses": {}}
        except FileNotFoundError:
            print("❌ Fichier non trouvé, création...")
            self.ensure_data_structure()
            return {"conversations": [], "learned_responses": {}}
        except Exception as e:
            print(f"❌ Erreur chargement : {e}")
            return {"conversations": [], "learned_responses": {}}
    
    def save_conversation(self, user_msg, ai_response):
        """Sauvegarder une conversation avec timestamp"""
        try:
            data = self.load_conversations()
            
            # Créer l'entrée de conversation
            conversation_entry = {
                "user": user_msg,
                "ai": ai_response,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Ajouter à la liste
            data["conversations"].append(conversation_entry)
            
            # Limiter à 1000 conversations pour éviter un fichier trop gros
            if len(data["conversations"]) > 1000:
                data["conversations"] = data["conversations"][-1000:]
            
            # Sauvegarder
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ Erreur sauvegarde conversation : {e}")
    
    def get_learned_responses(self):
        """Récupérer les réponses apprises"""
        try:
            data = self.load_conversations()
            return data.get("learned_responses", {})
        except Exception as e:
            print(f"❌ Erreur récupération réponses apprises : {e}")
            return {}
    
    def add_learned_response(self, question, answer):
        """Ajouter une réponse apprise"""
        try:
            data = self.load_conversations()
            question_clean = question.lower().strip()
            
            if question_clean not in data["learned_responses"]:
                data["learned_responses"][question_clean] = []
            
            # Éviter les doublons
            if answer not in data["learned_responses"][question_clean]:
                data["learned_responses"][question_clean].append(answer)
            
            # Sauvegarder
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout réponse apprise : {e}")
            return False
    
    def get_stats(self):
        """Obtenir les statistiques mémoire"""
        try:
            data = self.load_conversations()
            return {
                "conversations_count": len(data.get("conversations", [])),
                "learned_responses_count": len(data.get("learned_responses", {})),
                "file_size": os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0
            }
        except Exception as e:
            print(f"❌ Erreur stats mémoire : {e}")
            return {"conversations_count": 0, "learned_responses_count": 0, "file_size": 0}

# Test du module
if __name__ == "__main__":
    print("=== TEST MODULE MEMORY ===")
    
    try:
        # Test initialisation
        memory = Memory()
        print("✅ Initialisation Memory")
        
        # Test sauvegarde conversation
        memory.save_conversation("test", "réponse test")
        print("✅ Sauvegarde conversation")
        
        # Test récupération
        conversations = memory.load_conversations()
        print(f"✅ Chargement : {len(conversations['conversations'])} conversations")
        
        # Test réponses apprises
        learned = memory.get_learned_responses()
        print(f"✅ Réponses apprises : {len(learned)}")
        
        # Test stats
        stats = memory.get_stats()
        print(f"✅ Stats : {stats}")
        
    except Exception as e:
        print(f"❌ Erreur test : {e}")
    
    print("=== FIN TEST ===")
