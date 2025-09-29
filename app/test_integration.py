from .brain import AIBrain

# Test d'intégration complète Brain + Memory
ai = AIBrain()

print("=== TEST INTÉGRATION BRAIN + MEMORY ===")

# Test 1 : Salutations
response1 = ai.get_response("Salut !")
print(f"User: Salut ! → IA: {response1}")

# Test 2 : Question
response2 = ai.get_response("Comment ça va ?")
print(f"User: Comment ça va ? → IA: {response2}")

# Test 3 : Question inconnue
response3 = ai.get_response("Quelle heure est-il ?")
print(f"User: Quelle heure est-il ? → IA: {response3}")

# Test 4 : Vérifier sauvegarde mémoire
conversations = ai.memory.load_conversations()
print(f"\n✅ Conversations sauvegardées : {len(conversations['conversations'])}")

print("\n🤖 Intégration Brain + Memory réussie !")
