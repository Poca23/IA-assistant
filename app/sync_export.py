# app/sync_export.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import zipfile

class SyncExport:
    """Gestionnaire export/backup Knowledge Base"""
    
    def __init__(self):
        self.data_dir = Path("data/knowledge")
        self.backup_dir = Path("data/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.logs_file = Path("data/export_logs.json")
    
    def export_by_filters(
        self, 
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Export filtré des entrées
        
        Returns:
            (success, message, exported_data)
        """
        try:
            # Récupération toutes les entrées via lecture directe
            all_entries = []
            
            if not self.data_dir.exists():
                return True, "✅ Export : 0 entrées (répertoire vide)", {
                    "entries": [],
                    "metadata": {
                        "export_date": datetime.now().isoformat(),
                        "total_entries": 0,
                        "filters": {}
                    }
                }
            
            for cat_dir in self.data_dir.iterdir():
                if not cat_dir.is_dir():
                    continue
                
                for json_file in cat_dir.glob("*.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        entries = data.get("entries", [])
                        metadata = data.get("metadata", {})
                        
                        # Ajout infos catégorie/subcategory
                        for entry in entries:
                            if "category" not in entry:
                                entry["category"] = metadata.get("category", cat_dir.name)
                            if "subcategory" not in entry:
                                entry["subcategory"] = metadata.get("subcategory", json_file.stem)
                        
                        all_entries.extend(entries)
                        
                    except Exception as e:
                        print(f"⚠️ Erreur lecture {json_file} : {e}")
                        continue
            
            # Application des filtres
            filtered = all_entries
            
            if category:
                filtered = [e for e in filtered if e.get("category") == category]
            
            if subcategory:
                filtered = [e for e in filtered if e.get("subcategory") == subcategory]
            
            if tags:
                filtered = [
                    e for e in filtered 
                    if any(tag in e.get("tags", []) for tag in tags)
                ]
            
            if date_from:
                filtered = [
                    e for e in filtered 
                    if e.get("created", "") >= date_from
                ]
            
            if date_to:
                filtered = [
                    e for e in filtered 
                    if e.get("created", "") <= date_to
                ]
            
            # Construction export
            export_data = {
                "entries": filtered,
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "total_entries": len(filtered),
                    "filters": {
                        "category": category,
                        "subcategory": subcategory,
                        "tags": tags,
                        "date_from": date_from,
                        "date_to": date_to
                    }
                }
            }
            
            # Log opération
            self._log_operation("export_filtered", len(filtered), {
                "category": category,
                "subcategory": subcategory,
                "tags": tags
            })
            
            return True, f"✅ Export : {len(filtered)} entrées", export_data
            
        except Exception as e:
            return False, f"❌ Erreur export : {str(e)}", None
    
    def backup_full_knowledge(self) -> Tuple[bool, str, Optional[str]]:
        """
        Backup complet Knowledge Base en ZIP
        
        Returns:
            (success, message, zip_path)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"backup_kb_{timestamp}.zip"
            zip_path = self.backup_dir / zip_filename
            
            files_count = 0
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for json_file in self.data_dir.rglob("*.json"):
                    arcname = json_file.relative_to(self.data_dir)
                    zipf.write(json_file, arcname)
                    files_count += 1
            
            # Métadonnées backup
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "files_count": files_count,
                "size_bytes": zip_path.stat().st_size
            }
            
            meta_path = Path(f"{zip_path}.meta.json")
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            self._log_operation("backup_full", files_count, {"zip": zip_filename})
            
            return True, f"✅ Backup créé : {zip_filename}", str(zip_path)
            
        except Exception as e:
            return False, f"❌ Erreur backup : {str(e)}", None
    
    def restore_from_backup(
        self, 
        zip_path: str, 
        mode: str = "merge"
    ) -> Tuple[bool, str, Dict]:
        """
        Restaure depuis backup
        
        Args:
            zip_path: Chemin fichier ZIP
            mode: "merge" (fusion) ou "replace" (remplacement)
        
        Returns:
            (success, message, stats)
        """
        try:
            zip_file = Path(zip_path)
            if not zip_file.exists():
                return False, "❌ Fichier backup introuvable", {}
            
            stats = {
                "files_restored": 0,
                "entries_added": 0
            }
            
            # Replace : nettoyage complet
            if mode == "replace":
                if self.data_dir.exists():
                    import shutil
                    shutil.rmtree(self.data_dir)
                self.data_dir.mkdir(parents=True, exist_ok=True)
            
            # Extraction ZIP
            with zipfile.ZipFile(zip_file, 'r') as zipf:
                zipf.extractall(self.data_dir)
                stats["files_restored"] = len(zipf.namelist())
            
            # Comptage entrées (merge uniquement)
            if mode == "merge":
                for json_file in self.data_dir.rglob("*.json"):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        stats["entries_added"] += len(data.get("entries", []))
                    except:
                        continue
            
            self._log_operation("restore", stats["files_restored"], 
                              {"mode": mode, "source": zip_file.name})
            
            msg = f"✅ Restauration {mode} : {stats['files_restored']} fichiers"
            return True, msg, stats
            
        except Exception as e:
            return False, f"❌ Erreur restore : {str(e)}", {}
    
    def get_backups_list(self) -> List[Dict]:
        """
        Liste des backups disponibles
        
        Returns:
            Liste dictionnaires avec infos backups
        """
        backups = []
        
        for zip_file in self.backup_dir.glob("backup_kb_*.zip"):
            meta_file = Path(f"{zip_file}.meta.json")
            
            backup_info = {
                "filename": zip_file.name,
                "path": str(zip_file),
                "size_mb": round(zip_file.stat().st_size / (1024*1024), 2),
                "created": datetime.fromtimestamp(zip_file.stat().st_ctime).isoformat()
            }
            
            if meta_file.exists():
                try:
                    with open(meta_file, 'r') as f:
                        backup_info["metadata"] = json.load(f)
                except:
                    pass
            
            backups.append(backup_info)
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    
    def _log_operation(self, operation: str, count: int, details: Dict):
        """
        Enregistrement logs opérations
        
        Args:
            operation: Type opération (export_filtered, backup_full, restore)
            count: Nombre éléments traités
            details: Détails opération
        """
        try:
            logs = []
            if self.logs_file.exists():
                with open(self.logs_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "operation": operation,
                "count": count,
                "details": details
            })
            
            # Garde 100 derniers logs
            logs = logs[-100:]
            
            with open(self.logs_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            print(f"⚠️ Log erreur : {e}")
