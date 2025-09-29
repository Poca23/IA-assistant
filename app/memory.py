# app/memory.py - Gestionnaire mémoire IA (10 lignes)
import json
import os

class Memory:
    def __init__(self, file_path="data/conversations.json"):
        self.file_path = file_path
        self.conversations = self.load_conversations()
    
    def load_conversations(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"conversations": [], "learned_responses": {}}
    
    def save_conversation(self, user_input, ai_response):
        self.conversations["conversations"].append({
            "user": user_input,
            "ai": ai_response,
            "timestamp": str(os.times().elapsed)
        })
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.conversations, f, ensure_ascii=False, indent=2)
    
    def get_learned_responses(self):
        return self.conversations.get("learned_responses", {})
