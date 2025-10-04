# app/test_sync_export.py
"""
Tests unitaires module sync_export
Validation : Export filtré, Backup, Restore
⚠️ UTILISE DATA TEST SÉPARÉE
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from .sync_export import SyncExport

# 🔐 CONFIGURATION TEST
TEST_DATA_DIR = Path("data_test")
REAL_DATA_DIR = Path("data")

def backup_real_data():
    """Sauvegarde données réelles avant tests"""
    print("🔐 Sauvegarde données réelles...")
    
    if REAL_DATA_DIR.exists():
        backup_dir = Path("data_backup_test")
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(REAL_DATA_DIR, backup_dir)
        print(f"✅ Backup créé : {backup_dir}")
    else:
        print("⚠️ Aucune donnée réelle à sauvegarder")

def restore_real_data():
    """Restaure données réelles après tests"""
    print("\n🔄 Restauration données réelles...")
    
    backup_dir = Path("data_backup_test")
    if backup_dir.exists():
        if REAL_DATA_DIR.exists():
            shutil.rmtree(REAL_DATA_DIR)
        shutil.copytree(backup_dir, REAL_DATA_DIR)
        shutil.rmtree(backup_dir)
        print("✅ Données réelles restaurées")
    else:
        print("⚠️ Aucun backup à restaurer")

def setup_test_environment():
    """Configure environnement test isolé"""
    print("🔧 Configuration environnement test...")
    
    # Nettoyage ancien test
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)
    
    # Création structure test
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    (TEST_DATA_DIR / "knowledge" / "general").mkdir(parents=True, exist_ok=True)
    (TEST_DATA_DIR / "knowledge" / "personal").mkdir(parents=True, exist_ok=True)
    (TEST_DATA_DIR / "backups").mkdir(exist_ok=True)
    
    print(f"✅ Environnement test : {TEST_DATA_DIR}")

def setup_test_data():
    """Création données test directement dans fichiers JSON"""
    print("\n📝 Création données test...")
    
    kb_dir = TEST_DATA_DIR / "knowledge"
    
    # Culture
    culture_file = kb_dir / "general" / "culture.json"
    culture_data = {
        "entries": [{
            "id": "test_culture_1",
            "question": "Qui a peint la Joconde ?",
            "answer": "Léonard de Vinci",
            "tags": ["art", "peinture"],
            "category": "general",
            "subcategory": "culture",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().strftime("%Y-%m-%d")
        }],
        "metadata": {
            "category": "general",
            "subcategory": "culture",
            "total_entries": 1,
            "last_updated": datetime.now().isoformat()
        }
    }
    with open(culture_file, 'w', encoding='utf-8') as f:
        json.dump(culture_data, f, ensure_ascii=False, indent=2)
    
    # Sciences
    sciences_file = kb_dir / "general" / "sciences.json"
    sciences_data = {
        "entries": [{
            "id": "test_sciences_1",
            "question": "Quelle est la vitesse de la lumière ?",
            "answer": "299 792 458 m/s",
            "tags": ["physique", "constante"],
            "category": "general",
            "subcategory": "sciences",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().strftime("%Y-%m-%d")
        }],
        "metadata": {
            "category": "general",
            "subcategory": "sciences",
            "total_entries": 1,
            "last_updated": datetime.now().isoformat()
        }
    }
    with open(sciences_file, 'w', encoding='utf-8') as f:
        json.dump(sciences_data, f, ensure_ascii=False, indent=2)
    
    # Cuisine
    cuisine_file = kb_dir / "personal" / "cuisine.json"
    cuisine_data = {
        "entries": [{
            "id": "test_cuisine_1",
            "question": "Temps cuisson pâtes ?",
            "answer": "8-12 minutes selon type",
            "tags": ["cuisine", "conseil"],
            "category": "personal",
            "subcategory": "cuisine",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().strftime("%Y-%m-%d")
        }],
        "metadata": {
            "category": "personal",
            "subcategory": "cuisine",
            "total_entries": 1,
            "last_updated": datetime.now().isoformat()
        }
    }
    with open(cuisine_file, 'w', encoding='utf-8') as f:
        json.dump(cuisine_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 3 entrées test créées")

def get_test_sync():
    """Instance SyncExport configurée pour tests"""
    sync = SyncExport()
    # Override chemins vers environnement test
    sync.data_dir = TEST_DATA_DIR / "knowledge"
    sync.backup_dir = TEST_DATA_DIR / "backups"
    sync.logs_file = TEST_DATA_DIR / "export_logs.json"
    return sync

def test_export_filters():
    """Test 1 : Export avec filtres"""
    print("\n🧪 TEST 1 : Export filtré")
    
    sync = get_test_sync()
    
    # Export sans filtre (tout)
    success, msg, data = sync.export_by_filters()
    assert success, f"Export complet échoué : {msg}"
    assert data is not None, "Pas de données retournées"
    assert data["metadata"]["total_entries"] >= 3, f"Pas assez d'entrées : {data['metadata']['total_entries']}"
    print(f"✅ Export complet : {data['metadata']['total_entries']} entrées")
    
    # Export catégorie "general"
    success, msg, data = sync.export_by_filters(category="general")
    assert success, f"Export catégorie échoué : {msg}"
    assert data["metadata"]["total_entries"] >= 2, "Filtre catégorie KO"
    print(f"✅ Export catégorie 'general' : {data['metadata']['total_entries']} entrées")
    
    # Export par tag
    success, msg, data = sync.export_by_filters(tags=["cuisine"])
    assert success, f"Export tags échoué : {msg}"
    assert data["metadata"]["total_entries"] >= 1, "Filtre tags KO"
    print(f"✅ Export tag 'cuisine' : {data['metadata']['total_entries']} entrée(s)")
    
    # Export date (aujourd'hui)
    today = datetime.now().strftime("%Y-%m-%d")
    success, msg, data = sync.export_by_filters(date_from=today)
    assert success, f"Export date échoué : {msg}"
    print(f"✅ Export date >= {today} : {data['metadata']['total_entries']} entrée(s)")

def test_backup_full():
    """Test 2 : Backup complet"""
    print("\n🧪 TEST 2 : Backup complet")
    
    sync = get_test_sync()
    
    success, msg, zip_path = sync.backup_full_knowledge()
    assert success, f"Backup échoué : {msg}"
    
    # Vérification fichier
    backup_file = Path(zip_path)
    assert backup_file.exists(), "ZIP backup absent"
    assert backup_file.stat().st_size > 0, "ZIP vide"
    
    # Vérification métadonnées
    meta_file = Path(f"{zip_path}.meta.json")
    assert meta_file.exists(), "Métadonnées absentes"
    
    with open(meta_file, 'r') as f:
        meta = json.load(f)
    assert "backup_date" in meta, "Date backup manquante"
    assert meta["files_count"] > 0, "Aucun fichier backupé"
    
    print(f"✅ Backup créé : {backup_file.name}")
    print(f"   📊 Taille : {round(backup_file.stat().st_size / 1024, 2)} KB")
    print(f"   📁 Fichiers : {meta['files_count']}")
    
    return zip_path

def test_restore_merge(backup_zip):
    """Test 3 : Restore mode merge"""
    print("\n🧪 TEST 3 : Restore (merge)")
    
    sync = get_test_sync()
    
    # Ajout entrée supplémentaire
    test_dir = TEST_DATA_DIR / "knowledge" / "test"
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / "test.json"
    
    test_data = {
        "entries": [{
            "id": "test_restore_1",
            "question": "Question test restore",
            "answer": "Réponse test",
            "tags": ["test"],
            "category": "test",
            "created": datetime.now().strftime("%Y-%m-%d")
        }],
        "metadata": {"category": "test", "total_entries": 1}
    }
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    # Restore merge
    success, msg, stats = sync.restore_from_backup(backup_zip, mode="merge")
    assert success, f"Restore échoué : {msg}"
    assert stats["files_restored"] > 0, "Aucun fichier restauré"
    
    print(f"✅ Restore merge : {stats['entries_added']} entrées ajoutées")
    print(f"   📁 Fichiers : {stats['files_restored']}")
    
    # Vérification entrée test toujours là
    assert test_file.exists(), "Entrée test disparue en mode merge"

def test_restore_replace(backup_zip):
    """Test 4 : Restore mode replace"""
    print("\n🧪 TEST 4 : Restore (replace)")
    
    sync = get_test_sync()
    
    # Ajout entrée temporaire
    temp_dir = TEST_DATA_DIR / "knowledge" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file = temp_dir / "temp.json"
    
    temp_data = {
        "entries": [{
            "id": "temp_1",
            "question": "Question temp",
            "answer": "Doit disparaître",
            "tags": ["temp"],
            "category": "temp"
        }],
        "metadata": {"category": "temp", "total_entries": 1}
    }
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(temp_data, f, ensure_ascii=False, indent=2)
    
    # Restore replace
    success, msg, stats = sync.restore_from_backup(backup_zip, mode="replace")
    assert success, f"Restore replace échoué : {msg}"
    
    print(f"✅ Restore replace : {stats['files_restored']} fichiers")
    
    # Vérification entrée temp disparue
    assert not temp_file.exists(), "Entrée temp toujours présente"

def test_backups_list():
    """Test 5 : Liste backups"""
    print("\n🧪 TEST 5 : Liste backups")
    
    sync = get_test_sync()
    backups = sync.get_backups_list()
    
    assert len(backups) > 0, "Aucun backup listé"
    
    print(f"✅ {len(backups)} backup(s) disponible(s)")
    for backup in backups[:3]:
        print(f"   📦 {backup['filename']} ({backup['size_mb']} MB)")

def test_logs():
    """Test 6 : Vérification logs"""
    print("\n🧪 TEST 6 : Logs opérations")
    
    sync = get_test_sync()
    logs_file = sync.logs_file
    
    if not logs_file.exists():
        print("⚠️ Fichier logs absent (normal si aucune opération)")
        return
    
    with open(logs_file, 'r') as f:
        logs = json.load(f)
    
    assert len(logs) > 0, "Logs vides"
    
    operations = set(log["operation"] for log in logs)
    print(f"✅ {len(logs)} opérations loggées")
    print(f"   🔧 Types : {', '.join(operations)}")

def cleanup_tests():
    """Nettoyage après tests"""
    print("\n🧹 Nettoyage environnement test...")
    
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)
    
    print("✅ Nettoyage terminé")

def run_all_tests():
    """Exécution suite complète"""
    print("=" * 60)
    print("🧪 TESTS SYNC_EXPORT - Suite complète")
    print("=" * 60)
    
    try:
        # 🔐 Backup données réelles
        backup_real_data()
        
        # Setup environnement test
        setup_test_environment()
        setup_test_data()
        
        # Tests
        test_export_filters()
        backup_zip = test_backup_full()
        test_restore_merge(backup_zip)
        test_restore_replace(backup_zip)
        test_backups_list()
        test_logs()
        
        # Cleanup
        cleanup_tests()
        
        # 🔄 Restauration données réelles
        restore_real_data()
        
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS PASSÉS !")
        print("=" * 60)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST ÉCHOUÉ : {e}")
        restore_real_data()
        return False
    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback
        traceback.print_exc()
        restore_real_data()
        return False

if __name__ == "__main__":
    run_all_tests()
