from .brain import AIBrain

ai = AIBrain()

print("=== TEST INTÉGRATION BRAIN + MEMORY ===")

response1 = ai.get_response("Salut !")
print(f"User: Salut ! → IA: {response1}")

response2 = ai.get_response("Comment ça va ?")
print(f"User: Comment ça va ? → IA: {response2}")

response3 = ai.get_response("Quelle heure est-il ?")
print(f"User: Quelle heure est-il ? → IA: {response3}")

conversations = ai.memory.load_conversations()
print(f"\n✅ Conversations sauvegardées : {len(conversations['conversations'])}")

print("\n🤖 Intégration Brain + Memory réussie !")
