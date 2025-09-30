import json
import os
import uuid
from datetime import datetime

class KnowledgeBase:
    def __init__(self):
        self.base_path = "data/knowledge"
        self.categories = {
            "general": ["culture", "sciences", "technologies"],
            "personal": ["cuisine", "admin", "sante", "budget"]
        }
        self._ensure_structure()
    
    def _ensure_structure(self):
        """Créer structure si inexistante"""
        for category, subcategories in self.categories.items():
            category_path = os.path.join(self.base_path, category)
            os.makedirs(category_path, exist_ok=True)
            
            for subcategory in subcategories:
                file_path = os.path.join(category_path, f"{subcategory}.json")
                # TOUJOURS recréer si vide ou inexistant
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    self._create_empty_file(file_path, subcategory)
    
    def _create_empty_file(self, file_path, subcategory):
        """Créer fichier JSON vide avec structure"""
        empty_data = {
            "entries": [],
            "metadata": {
                "category": subcategory,
                "total_entries": 0,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(empty_data, f, ensure_ascii=False, indent=2)
        print(f"📝 Fichier créé: {file_path}")
    
    def create_entry(self, category, subcategory, question, answer, tags=None):
        """Créer nouvelle entrée"""
        try:
            file_path = os.path.join(self.base_path, category, f"{subcategory}.json")
            
            # Vérifier si fichier vide AVANT lecture
            if os.path.getsize(file_path) == 0:
                self._create_empty_file(file_path, subcategory)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            new_entry = {
                "id": str(uuid.uuid4())[:8],
                "question": question,
                "answer": answer,
                "tags": tags or [],
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data["entries"].append(new_entry)
            data["metadata"]["total_entries"] = len(data["entries"])
            data["metadata"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return new_entry["id"]
        
        except Exception as e:
            print(f"❌ Erreur création entrée : {e}")
            return None
    
    def read_entries(self, category, subcategory):
        """Lire toutes les entrées"""
        try:
            file_path = os.path.join(self.base_path, category, f"{subcategory}.json")
            
            # Vérifier si fichier vide AVANT lecture
            if os.path.getsize(file_path) == 0:
                self._create_empty_file(file_path, subcategory)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
        
        except Exception as e:
            print(f"❌ Erreur lecture : {e}")
            return {"entries": [], "metadata": {"total_entries": 0}}
