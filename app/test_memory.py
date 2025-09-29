from memory import Memory

# Test basique
memory = Memory()
print("Test 1:", memory.load_conversations())

# Test sauvegarde
memory.save_conversation("Salut IA", "Bonjour ! Comment allez-vous ?")
print("Test 2: Conversation sauvegardée")

# Test lecture
conversations = memory.load_conversations()
print("Test 3:", len(conversations["conversations"]), "conversation(s) en mémoire")

print("Memory.py fonctionne !")
