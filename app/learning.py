# app/learning.py - Module apprentissage IA (15 lignes)
from .brain import AIBrain
import json

def teach_ai(question, answer):
    """Apprendre une nouvelle réponse à l'IA"""
    ai = AIBrain()
    
    # Ajouter la réponse apprise
    learned = ai.memory.get_learned_responses()
    question = question.lower().strip()
    
    if question not in learned:
        learned[question] = []
    learned[question].append(answer)
    
    # Sauvegarder dans le fichier JSON
    ai.memory.conversations["learned_responses"] = learned
    with open(ai.memory.file_path, 'w', encoding='utf-8') as f:
        json.dump(ai.memory.conversations, f, ensure_ascii=False, indent=2)
    
    print(f"✅ IA a appris : '{question}' → '{answer}'")

# Test rapide d'apprentissage
if __name__ == "__main__":
    teach_ai("ton nom", "Je m'appelle Claire-IA !")
    
    # Tester la nouvelle réponse
    ai = AIBrain()
    response = ai.get_response("ton nom")
    print(f"Test: {response}")
