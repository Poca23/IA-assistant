from .brain import AIBrain
import json
import os
import time

def teach_ai(question, answer):
    """Apprendre une nouvelle réponse à l'IA avec sauvegarde renforcée"""
    try:
        if not question or not answer:
            print("❌ Question et réponse requises")
            return False
        
        ai = AIBrain()
        
        if not os.path.exists(ai.memory.file_path):
            print("❌ Fichier conversations.json introuvable")
            return False
        
        try:
            with open(ai.memory.file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Fichier JSON corrompu, création d'une nouvelle structure")
            current_data = {"conversations": [], "learned_responses": {}}
        
        question_clean = question.lower().strip()
        
        if "learned_responses" not in current_data:
            current_data["learned_responses"] = {}
        
        if "conversations" not in current_data:
            current_data["conversations"] = []
        
        if question_clean not in current_data["learned_responses"]:
            current_data["learned_responses"][question_clean] = []
        
        if answer not in current_data["learned_responses"][question_clean]:
            current_data["learned_responses"][question_clean].append(answer)
        
        backup_path = ai.memory.file_path + '.backup'
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            
            with open(ai.memory.file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, ensure_ascii=False, indent=2)
            
            if os.path.exists(backup_path):
                os.remove(backup_path)
                
        except Exception as save_error:
            print(f"❌ Erreur sauvegarde : {save_error}")
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

if __name__ == "__main__":
    print("=== TEST MODULE APPRENTISSAGE ===")
    
    success = teach_ai("test automatique", "réponse automatique")
    print(f"Apprentissage : {'✅' if success else '❌'}")
    
    if success:
        verified = verify_learning("test automatique")
        print(f"Vérification : {'✅' if verified else '❌'}")
        
        ai = AIBrain()
        response = ai.get_response("test automatique")
        print(f"Réponse IA : {response}")
    
    print("=== FIN TEST ===")
