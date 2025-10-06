# app/learning.py
from .knowledge import KnowledgeBase

def teach_ai(question: str, answer: str) -> bool:
    """
    Enseigne une réponse simple à l'IA
    Stocke maintenant dans knowledge/personal/quick.json
    """
    try:
        kb = KnowledgeBase()
        
        # Créer dans catégorie "Personal" > sous-catégorie "Quick"
        success = kb.create_entry(
            main_category="personal",
            sub_category="quick",
            question=question,
            answer=answer,
            tags=["apprentissage-rapide"]  # Tag automatique
        )
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur teach_ai : {e}")
        return False
