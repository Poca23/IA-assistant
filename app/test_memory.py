from .memory import Memory

memory = Memory()
print("Test 1:", memory.load_conversations())

memory.save_conversation("Salut IA", "Bonjour ! Comment allez-vous ?")
print("Test 2: Conversation sauvegardée")

conversations = memory.load_conversations()
print("Test 3:", len(conversations["conversations"]), "conversation(s) en mémoire")

print("Memory.py fonctionne !")
