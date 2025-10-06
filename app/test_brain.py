from .brain import AIBrain

ai = AIBrain()
print("Test 1:", ai.get_response("Salut"))
print("Test 2:", ai.get_response("Comment ça va ?"))
print("Brain.py fonctionne !")

# Tester learned_responses
ai.memory.add_learned_response("1 + 1 = ?", "2")
response = ai.get_response("1 + 1 = ?")
print(f"✅ Test learned: '1 + 1 = ?' → '{response}'")
assert response == "2", f"❌ Attendu '2', reçu '{response}'"