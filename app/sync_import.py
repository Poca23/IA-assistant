# app/sync_import.py
import json
from datetime import datetime
from typing import Dict, List, Tuple
from .knowledge import KnowledgeBase

class SyncImport:
    """Gestion import avancé avec validation"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
    
    def validate_json(self, content: str) -> Tuple[bool, str, Dict]:
        """
        Valider format JSON
        Returns: (is_valid, message, data)
        """
        try:
            data = json.loads(content)
            
            # Vérifier structure
            if "entries" not in data:
                return False, "❌ Clé 'entries' manquante", {}
            
            if not isinstance(data["entries"], list):
                return False, "❌ 'entries' doit être une liste", {}
            
            if len(data["entries"]) == 0:
                return False, "⚠️ Aucune entrée trouvée", {}
            
            # Valider chaque entrée
            required_fields = ["question", "answer"]
            for i, entry in enumerate(data["entries"]):
                for field in required_fields:
                    if field not in entry:
                        return False, f"❌ Entrée {i}: champ '{field}' manquant", {}
            
            return True, f"✅ {len(data['entries'])} entrées valides", data
            
        except json.JSONDecodeError as e:
            return False, f"❌ JSON invalide: {str(e)}", {}
        except Exception as e:
            return False, f"❌ Erreur: {str(e)}", {}
    
    def detect_duplicates(self, category: str, subcategory: str, 
                         new_entries: List[Dict]) -> Dict:
        """
        Détecter doublons
        Returns: {"duplicates": [...], "new": [...]}
        """
        existing = self.kb.read_entries(category, subcategory)
        existing_questions = {e["question"].lower() for e in existing["entries"]}
        
        duplicates = []
        new = []
        
        for entry in new_entries:
            question_lower = entry["question"].lower()
            if question_lower in existing_questions:
                duplicates.append(entry)
            else:
                new.append(entry)
        
        return {
            "duplicates": duplicates,
            "new": new,
            "total": len(new_entries)
        }
    
    def preview_import(self, content: str, category: str, 
                      subcategory: str) -> Dict:
        """
        Aperçu avant import
        Returns: statistiques et preview
        """
        is_valid, message, data = self.validate_json(content)
        
        if not is_valid:
            return {"valid": False, "message": message}
        
        # Détection doublons
        dup_info = self.detect_duplicates(category, subcategory, 
                                         data["entries"])
        
        return {
            "valid": True,
            "message": message,
            "total": dup_info["total"],
            "new": len(dup_info["new"]),
            "duplicates": len(dup_info["duplicates"]),
            "preview": data["entries"][:5],  # 5 premiers
            "entries_to_import": dup_info["new"]
        }
    
    def merge_import(self, category: str, subcategory: str, 
                    entries: List[Dict], mode: str = "add") -> Dict:
        """
        Importer avec fusion intelligente
        mode: 'add' (ajouter) ou 'replace' (remplacer)
        """
        try:
            imported = 0
            skipped = 0
            
            for entry in entries:
                # Ajouter métadonnées si manquantes
                if "tags" not in entry:
                    entry["tags"] = []
                
                # Import selon mode
                if mode == "add":
                    self.kb.create_entry(
                        category, subcategory,
                        entry["question"],
                        entry["answer"],
                        entry["tags"]
                    )
                    imported += 1
                elif mode == "replace":
                    # TODO: logique replace si besoin
                    pass
            
            return {
                "success": True,
                "imported": imported,
                "skipped": skipped,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
