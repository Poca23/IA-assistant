from .knowledge import KnowledgeBase

def test_knowledge_crud():
    print("=== TEST KNOWLEDGE BASE CRUD ===")
    
    kb = KnowledgeBase()
    
    # TEST 1: Création
    print("\n1️⃣ TEST CRÉATION")
    entry_id = kb.create_entry(
        category="general",
        subcategory="culture",
        question="Qui a peint La Joconde ?",
        answer="Léonard de Vinci",
        tags=["art", "renaissance"]
    )
    print(f"✅ Entrée créée ID: {entry_id}")
    
    # TEST 2: Lecture
    print("\n2️⃣ TEST LECTURE")
    data = kb.read_entries("general", "culture")
    print(f"✅ Entrées trouvées: {data['metadata']['total_entries']}")
    if data["entries"]:
        print(f"   Premier: {data['entries'][0]['question']}")
    
    # TEST 3: Création multiple
    print("\n3️⃣ TEST MULTIPLE")
    kb.create_entry("personal", "cuisine", "Recette pâtes ?", "Eau + sel + pâtes", ["facile"])
    kb.create_entry("general", "sciences", "Formule eau ?", "H2O", ["chimie"])
    
    # TEST 4: Vérification
    print("\n4️⃣ VÉRIFICATION")
    cuisine_data = kb.read_entries("personal", "cuisine")
    science_data = kb.read_entries("general", "sciences")
    
    print(f"✅ Cuisine: {cuisine_data['metadata']['total_entries']} entrées")
    print(f"✅ Sciences: {science_data['metadata']['total_entries']} entrées")
    
    print("\n🎯 Tests CRUD Knowledge réussis !")

if __name__ == "__main__":
    test_knowledge_crud()
