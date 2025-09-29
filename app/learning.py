from .brain import AIBrain
import json
import os
import time

def teach_ai(question, answer):
    """Apprendre une nouvelle réponse à l'IA avec sauvegarde renforcée"""
    try:
        # Validation des entrées
        if not question or not answer:
            print("❌ Question et réponse requises")
            return False
        
        # Créer une nouvelle instance IA
        ai = AIBrain()
        
        # Vérifier que le fichier existe
        if not os.path.exists(ai.memory.file_path):
            print("❌ Fichier conversations.json introuvable")
            return False
        
        # Charger les données actuelles avec gestion d'erreurs
        try:
            with open(ai.memory.file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Fichier JSON corrompu, création d'une nouvelle structure")
            current_data = {"conversations": [], "learned_responses": {}}
        
        # Préparer la question
        question_clean = question.lower().strip()
        
        # Initialiser la structure si nécessaire
        if "learned_responses" not in current_data:
            current_data["learned_responses"] = {}
        
        if "conversations" not in current_data:
            current_data["conversations"] = []
        
        # Ajouter la nouvelle réponse
        if question_clean not in current_data["learned_responses"]:
            current_data["learned_responses"][question_clean] = []
        
        # Éviter les doublons
        if answer not in current_data["learned_responses"][question_clean]:
            current_data["learned_responses"][question_clean].append(answer)
        
        # Sauvegarder avec backup
        backup_path = ai.memory.file_path + '.backup'
        try:
            # Créer une sauvegarde
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            
            # Sauvegarder le fichier principal
            with open(ai.memory.file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            
            # Supprimer le backup si succès
            if os.path.exists(backup_path):
                os.remove(backup_path)
                
        except Exception as save_error:
            print(f"❌ Erreur sauvegarde : {save_error}")
            # Restaurer depuis le backup si possible
            if os.path.exists(backup_path):
                os.rename(backup_path, ai.memory.file_path)
            return False
        
        print(f"✅ IA a appris : '{question}' → '{answer}'")
        return True
        
    except Exception as e:
        print(f"❌ Erreur apprentissage globale : {e}")
        return False

def verify_learning(question):
    """Vérifier qu'une réponse a bien été apprise"""
    try:
        ai = AIBrain()
        learned = ai.memory.get_learned_responses()
        question_clean = question.lower().strip()
        return question_clean in learned and len(learned[question_clean]) > 0
    except:
        return False

# Test rapide d'apprentissage
if __name__ == "__main__":
    print("=== TEST MODULE APPRENTISSAGE ===")
    
    # Test 1 : Apprentissage
    success = teach_ai("test automatique", "réponse automatique")
    print(f"Apprentissage : {'✅' if success else '❌'}")
    
    # Test 2 : Vérification
    if success:
        verified = verify_learning("test automatique")
        print(f"Vérification : {'✅' if verified else '❌'}")
        
        # Test 3 : Réponse IA
        ai = AIBrain()
        response = ai.get_response("test automatique")
        print(f"Réponse IA : {response}")
    
    print("=== FIN TEST ===")
