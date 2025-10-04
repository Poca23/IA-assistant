# app/test_sync_import.py
from .sync_import import SyncImport

def test_validation():
    """Test validation JSON"""
    sync = SyncImport()
    
    # JSON valide
    valid_json = '''
    {
        "entries": [
            {
                "question": "Test ?",
                "answer": "Réponse test",
                "tags": ["test"]
            }
        ]
    }
    '''
    
    is_valid, msg, data = sync.validate_json(valid_json)
    print(f"✅ Validation: {is_valid} - {msg}")
    assert is_valid
    
    # JSON invalide
    invalid = '{"entries": "pas une liste"}'
    is_valid, msg, _ = sync.validate_json(invalid)
    print(f"❌ Invalid: {is_valid} - {msg}")
    assert not is_valid
    
    print("\n🎯 Tests validation OK !")

if __name__ == "__main__":
    test_validation()
