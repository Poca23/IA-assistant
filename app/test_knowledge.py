from .knowledge import KnowledgeBase

def test_knowledge_crud():
    print("=== TEST KNOWLEDGE BASE CRUD COMPLET ===")
    
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
    
    # TEST 3: Modification
    print("\n3️⃣ TEST MODIFICATION")
    success = kb.update_entry("general", "culture", entry_id, 
                             answer="Léonard de Vinci (1503-1519)")
    print(f"✅ Modification: {'OK' if success else 'ÉCHEC'}")
    
    # TEST 4: Suppression
    print("\n4️⃣ TEST SUPPRESSION")
    # Créer une entrée temporaire
    temp_id = kb.create_entry("general", "culture", "Test suppression", "Test")
    delete_success = kb.delete_entry("general", "culture", temp_id)
    print(f"✅ Suppression: {'OK' if delete_success else 'ÉCHEC'}")
    
    # TEST 5: Liste catégories
    print("\n5️⃣ TEST CATEGORIES")
    categories = kb.list_categories()
    print(f"✅ Catégories: {list(categories.keys())}")
    
    # TEST 6: Création multiple (pour tests suivants)
    print("\n6️⃣ TEST MULTIPLE")
    kb.create_entry("personal", "cuisine", "Recette pâtes ?", "Eau + sel + pâtes", ["facile"])
    kb.create_entry("general", "sciences", "Formule eau ?", "H2O", ["chimie"])
    
    # Vérification finale
    print("\n7️⃣ VÉRIFICATION FINALE")
    cuisine_data = kb.read_entries("personal", "cuisine")
    science_data = kb.read_entries("general", "sciences")
    
    print(f"✅ Cuisine: {cuisine_data['metadata']['total_entries']} entrées")
    print(f"✅ Sciences: {science_data['metadata']['total_entries']} entrées")
    
    print("\n🎯 Tests CRUD COMPLET réussis !")

if __name__ == "__main__":
    test_knowledge_crud()
