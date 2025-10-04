import json
import os
from datetime import datetime
from .knowledge import KnowledgeBase

class ImportHandler:
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def validate_json(self, file_content):
        """Valider la structure du JSON uploadé"""
        try:
            data = json.loads(file_content)
            
            # Vérifier structure minimale
            if not isinstance(data, dict):
                return False, "Le fichier doit contenir un objet JSON"
            
            if "entries" not in data:
                return False, "Clé 'entries' manquante"
            
            if not isinstance(data["entries"], list):
                return False, "'entries' doit être une liste"
            
            # Vérifier chaque entrée
            for entry in data["entries"]:
                if not all(k in entry for k in ["question", "answer"]):
                    return False, "Chaque entrée doit avoir 'question' et 'answer'"
            
            return True, "Structure valide"
            
        except json.JSONDecodeError as e:
            return False, f"JSON invalide : {str(e)}"
        except Exception as e:
            return False, f"Erreur validation : {str(e)}"
    
    def import_from_json(self, file_content, category, subcategory):
        """Importer les données depuis un fichier JSON"""
        try:
            # Valider d'abord
            is_valid, message = self.validate_json(file_content)
            if not is_valid:
                return False, message, 0
            
            data = json.loads(file_content)
            imported_count = 0
            
            # Importer chaque entrée
            for entry in data["entries"]:
                # ✅ CORRECTION : Passer question et answer séparément
                self.kb.create_entry(
                    category, 
                    subcategory, 
                    entry["question"],
                    entry["answer"]
                )
                imported_count += 1
            
            return True, f"Import réussi : {imported_count} entrée(s)", imported_count
            
        except Exception as e:
            return False, f"Erreur import : {str(e)}", 0
