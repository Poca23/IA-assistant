# app/interface.py
import streamlit as st
import os
import json
import time
from datetime import datetime
from pathlib import Path
from .brain import AIBrain
from .learning import teach_ai
from .knowledge import KnowledgeBase
from .sync_import import SyncImport
from .sync_export import SyncExport

st.set_page_config(
    page_title="BB-IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def init_ai():
    return AIBrain()

@st.cache_resource
def init_kb():
    return KnowledgeBase()

@st.cache_resource
def init_sync_import():
    return SyncImport()

@st.cache_resource
def init_sync_export():
    return SyncExport()

def chat_interface():
    """Onglet Chat - Interface conversationnelle"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Salut ! Je suis BB-IA. Comment puis-je t'aider ?"
        })

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Écris ton message..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Je réfléchis..."):
                ai = init_ai()
                response = ai.get_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def knowledge_interface():
    """Onglet Connaissances - Visualisation et gestion"""
    st.header("📚 Base de Connaissances")
    st.caption("🗂️ Documentation organisée avec catégoires, tags et recherche avancée")

    kb = init_kb()
    categories = kb.list_categories()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("🗂️ Catégories")

        selected_cat = st.radio(
            "Catégorie principale:",
            categories,
            format_func=lambda x: f"📁 {x.title()}"
        )

        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge', selected_cat)

        if os.path.exists(data_path):
            subcategories = [
                f.replace('.json', '') 
                for f in os.listdir(data_path) 
                if f.endswith('.json')
            ]

            if subcategories:
                st.divider()
                selected_subcat = st.radio(
                    "Sous-catégorie:",
                    subcategories,
                    format_func=lambda x: f"📄 {x.title()}"
                )
            else:
                selected_subcat = None
                st.info("Aucune sous-catégorie")
        else:
            selected_subcat = None

    with col2:
        if selected_cat and selected_subcat:
            st.subheader(f"📖 {selected_cat.title()} / {selected_subcat.title()}")

            with st.expander("➕ Créer une nouvelle entrée", expanded=False):
                with st.form(key=f"create_form_{selected_cat}_{selected_subcat}"):
                    new_question = st.text_input("Question :")
                    new_answer = st.text_area("Réponse :")
                    new_tags = st.text_input("Tags (séparés par virgules) :")

                    submitted = st.form_submit_button("➕ Ajouter", type="primary")

                    if submitted and new_question and new_answer:
                        tags_list = [t.strip() for t in new_tags.split(",")] if new_tags else []

                        success = kb.create_entry(
                            selected_cat, 
                            selected_subcat,
                            new_question,
                            new_answer,
                            tags_list
                        )

                        if success:
                            st.success("✅ Entrée créée avec succès !")
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la création")

            st.divider()

            try:
                result = kb.read_entries(selected_cat, selected_subcat)

                if isinstance(result, str):
                    st.error(f"❌ Erreur format : {result}")
                elif isinstance(result, list) and len(result) > 0:
                    for idx, entry in enumerate(result):
                        if isinstance(entry, dict):
                            entry_id = entry.get('id', f'unknown_{idx}')
                            entry_title = str(entry.get('question', 'Sans titre'))

                            col_content, col_actions = st.columns([5, 1])

                            with col_content:
                                with st.expander(f"🔹 {entry_title}"):
                                    if f"edit_{entry_id}" not in st.session_state:
                                        st.write(f"**Réponse:** {entry.get('answer', 'N/A')}")
                                        tags = entry.get('tags', [])
                                        if tags:
                                            st.caption(f"🏷️ Tags: {', '.join(map(str, tags))}")
                                        st.caption(f"📅 Créé: {entry.get('created', 'N/A')}")
                                    else:
                                        edit_question = st.text_input(
                                            "Question :", 
                                            value=entry.get('question', ''),
                                            key=f"edit_q_{entry_id}"
                                        )
                                        edit_answer = st.text_area(
                                            "Réponse :", 
                                            value=entry.get('answer', ''),
                                            key=f"edit_a_{entry_id}",
                                            height=150
                                        )
                                        edit_tags = st.text_input(
                                            "Tags :", 
                                            value=', '.join(map(str, entry.get('tags', []))),
                                            key=f"edit_t_{entry_id}"
                                        )

                                        col_save, col_cancel = st.columns(2)

                                        with col_save:
                                            if st.button("💾 Sauvegarder", key=f"save_{entry_id}", type="primary"):
                                                tags_list = [t.strip() for t in edit_tags.split(",")] if edit_tags else []

                                                success = kb.update_entry(
                                                    selected_cat,
                                                    selected_subcat,
                                                    entry_id,
                                                    question=edit_question,
                                                    answer=edit_answer,
                                                    tags=tags_list
                                                )

                                                if success:
                                                    del st.session_state[f"edit_{entry_id}"]
                                                    st.success("✅ Modifications sauvegardées !")
                                                    st.rerun()
                                                else:
                                                    st.error("❌ Erreur sauvegarde")

                                        with col_cancel:
                                            if st.button("❌ Annuler", key=f"cancel_{entry_id}"):
                                                del st.session_state[f"edit_{entry_id}"]
                                                st.rerun()

                            with col_actions:
                                if f"edit_{entry_id}" not in st.session_state:
                                    if st.button("✏️", key=f"btn_edit_{entry_id}", help="Modifier"):
                                        st.session_state[f"edit_{entry_id}"] = True
                                        st.rerun()

                                if f"confirm_del_{entry_id}" not in st.session_state:
                                    if st.button("🗑️", key=f"btn_del_{entry_id}", help="Supprimer"):
                                        st.session_state[f"confirm_del_{entry_id}"] = True
                                        st.rerun()

                                if st.session_state.get(f"confirm_del_{entry_id}", False):
                                    col_yes, col_no = st.columns(2)

                                    with col_yes:
                                        if st.button("✓", key=f"yes_{entry_id}", help="Confirmer", type="primary"):
                                            success = kb.delete_entry(
                                                selected_cat,
                                                selected_subcat,
                                                entry_id
                                            )

                                            if success:
                                                del st.session_state[f"confirm_del_{entry_id}"]
                                                st.success("✅ Entrée supprimée !")
                                                st.rerun()
                                            else:
                                                st.error("❌ Erreur suppression")

                                    with col_no:
                                        if st.button("✗", key=f"no_{entry_id}", help="Annuler"):
                                            del st.session_state[f"confirm_del_{entry_id}"]
                                            st.rerun()
                        else:
                            st.warning(f"⚠️ Entrée invalide : {type(entry)}")
                else:
                    st.info("📭 Aucune entrée dans cette sous-catégorie")

            except Exception as e:
                st.error(f"❌ Erreur lecture : {str(e)}")
        else:
            st.info("👈 Sélectionnez une catégorie et une sous-catégorie")

def stats_interface():
    """Onglet Statistiques - Métriques"""
    st.header("📊 Statistiques")

    col1, col2, col3 = st.columns(3)

    try:
        ai = init_ai()
        kb = init_kb()
        conversations = ai.memory.load_conversations()

        with col1:
            st.metric(
                "💬 Conversations",
                len(conversations.get('conversations', []))
            )

        with col2:
            st.metric(
                "🎓 Réponses apprises",
                len(conversations.get('learned_responses', {}))
            )

        with col3:
            total_entries = 0
            for cat in kb.list_categories():
                cat_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge', cat)
                if os.path.exists(cat_path):
                    for subcat_file in os.listdir(cat_path):
                        if subcat_file.endswith('.json'):
                            subcat = subcat_file.replace('.json', '')
                            entries = kb.read_entries(cat, subcat)
                            if isinstance(entries, list):
                                total_entries += len(entries)

            st.metric("📚 Entrées Knowledge", total_entries)

        st.subheader("📈 Évolution")
        st.info("Graphiques en développement - Phase 5")

    except Exception as e:
        st.error(f"❌ Erreur chargement stats : {str(e)}")

def import_advanced_interface():
    """Import avancé avec preview"""
    st.subheader("📥 Import Avancé")

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Catégorie", ["general", "personal"], key="import_cat")
    with col2:
        subcategory = st.text_input("Sous-catégorie", 
                                     placeholder="ex: technologies",
                                     key="import_subcat")

    uploaded = st.file_uploader("Sélectionner JSON", type=["json"], key="import_file")

    if uploaded and subcategory:
        content = uploaded.read().decode("utf-8")
        sync = init_sync_import()

        with st.spinner("Analyse du fichier..."):
            preview = sync.preview_import(content, category, subcategory)

        if not preview["valid"]:
            st.error(preview["message"])
            return

        st.success(preview["message"])

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total", preview["total"])
        col2.metric("✅ Nouvelles", preview["new"])
        col3.metric("⚠️ Doublons", preview["duplicates"])

        if preview["preview"]:
            with st.expander("👁️ Aperçu des 5 premières entrées"):
                for entry in preview["preview"]:
                    st.markdown(f"**Q:** {entry['question']}")
                    st.markdown(f"**R:** {entry['answer'][:100]}...")
                    st.divider()

        if preview["new"] > 0:
            if st.button("✅ Importer les nouvelles entrées", 
                        type="primary",
                        key="import_btn"):
                result = sync.merge_import(
                    category, subcategory,
                    preview["entries_to_import"]
                )

                if result["success"]:
                    st.success(f"🎉 {result['imported']} entrées importées !")
                    st.rerun()
                else:
                    st.error(f"❌ Erreur: {result['error']}")
        else:
            st.info("ℹ️ Aucune nouvelle entrée à importer")

def export_interface():
    """Tab Export & Backup"""
    st.subheader("📤 Export & Backup")

    sync_export = init_sync_export()

    # Section 1 : Export Filtré
    with st.expander("🔍 Export Filtré", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            export_category = st.selectbox(
                "Catégorie",
                ["Toutes", "general", "personal"],
                key="export_filter_cat"
            )
            export_tags = st.text_input(
                "Tags (séparés par virgules)",
                key="export_tags",
                placeholder="ex: python, ia"
            )

        with col2:
            export_subcategory = st.text_input(
                "Sous-catégorie (optionnel)",
                key="export_subcat",
                placeholder="ex: technologies"
            )
            export_date_from = st.date_input(
                "Date début (optionnel)",
                value=None,
                key="export_date_from"
            )

        if st.button("📥 Générer Export", type="primary", key="export_btn"):
            with st.spinner("Génération export..."):
                cat_filter = None if export_category == "Toutes" else export_category
                subcat_filter = export_subcategory if export_subcategory else None
                tags_filter = [t.strip() for t in export_tags.split(",")] if export_tags else None
                date_filter = export_date_from.strftime("%Y-%m-%d") if export_date_from else None

                success, message, data = sync_export.export_by_filters(
                    category=cat_filter,
                    subcategory=subcat_filter,
                    tags=tags_filter,
                    date_from=date_filter
                )

                if success and data:
                    st.success(message)

                    with st.expander("👁️ Aperçu Export"):
                        st.json({
                            "total_entries": data["metadata"]["total_entries"],
                            "filtres_appliqués": data["metadata"]["filters"],
                            "premiere_entree": data["entries"][0] if data["entries"] else None
                        })

                    json_str = json.dumps(data, indent=2, ensure_ascii=False)

                    st.download_button(
                        "💾 Télécharger Export JSON",
                        data=json_str,
                        file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key="download_export"
                    )
                else:
                    st.error(message)

    st.divider()

    # Section 2 : Backup Complet
    with st.expander("💾 Backup Complet"):
        st.info("📦 Créer un backup complet de la Knowledge Base (ZIP)")

        if st.button("🔄 Créer Backup", type="primary", key="backup_btn"):
            with st.spinner("Création backup..."):
                success, message, backup_path = sync_export.backup_full_knowledge()

                if success and backup_path:
                    st.success(message)

                    backup_file = Path(backup_path)
                    size_mb = round(backup_file.stat().st_size / (1024*1024), 2)

                    col1, col2 = st.columns(2)
                    col1.metric("📦 Taille", f"{size_mb} MB")
                    col2.metric("📅 Créé", datetime.now().strftime("%H:%M:%S"))

                    with open(backup_path, "rb") as f:
                        st.download_button(
                            "📥 Télécharger Backup ZIP",
                            data=f,
                            file_name=backup_file.name,
                            mime="application/zip",
                            key="download_backup"
                        )
                else:
                    st.error(message)

    st.divider()

    # Section 3 : Restauration (✅ CORRECTION BALLOONS)
    with st.expander("📦 Restauration Backup"):
        backups_list = sync_export.get_backups_list()

        if backups_list:
            st.info(f"💾 {len(backups_list)} backup(s) disponible(s)")

            backup_options = [
                f"{b['filename']} - {b['size_mb']} MB - {b['created']}"
                for b in backups_list
            ]

            selected_idx = st.selectbox(
                "Sélectionner un backup",
                range(len(backup_options)),
                format_func=lambda x: backup_options[x],
                key="restore_select"
            )

            selected_backup = backups_list[selected_idx]

            restore_mode = st.radio(
                "Mode de restauration",
                ["merge", "replace"],
                format_func=lambda x: "🔀 Fusion (merge)" if x == "merge" else "🔄 Remplacement (replace)",
                key="restore_mode"
            )

            if restore_mode == "merge":
                st.info("ℹ️ Les doublons seront ignorés, nouvelles entrées ajoutées")
            else:
                st.warning("⚠️ ATTENTION : Toutes les données actuelles seront supprimées !")

            if st.button("🔄 Restaurer", type="primary", key="restore_btn"):
                with st.spinner(f"Restauration {restore_mode}..."):
                    success, message, stats = sync_export.restore_from_backup(
                        selected_backup["path"],
                        mode=restore_mode
                    )

                if success:
                    st.success(message)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("📁 Fichiers", stats.get('files_restored', 0))
                    col2.metric("📊 Entrées", stats.get('entries_restored', 0))
                    col3.metric("⏱️ Durée", f"{stats.get('duration', 0):.2f}s")

                    # ✅ CORRECTION : Balloons AVANT rerun
                    st.balloons()
                    time.sleep(1.5)  # Pause pour voir animation
                    
                    st.cache_resource.clear()
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("📭 Aucun backup disponible")

    st.divider()

    # Section 4 : Historique
    with st.expander("📊 Historique Opérations"):
        logs_file = sync_export.logs_file

        if logs_file.exists():
            with open(logs_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

            if logs:
                st.info(f"📝 {len(logs)} opération(s)")

                for log in reversed(logs[-10:]):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    col1.markdown(f"**{log['operation']}**")
                    col2.markdown(f"📊 {log['count']}")
                    col3.markdown(f"🕒 {log['timestamp'][:19]}")

                    if log.get('details'):
                        with st.expander("Détails"):
                            st.json(log['details'])
                    st.divider()
            else:
                st.info("📭 Aucune opération")
        else:
            st.info("📭 Fichier logs introuvable")

def maintenance_interface():
    """Tab Maintenance - Simplifié"""
    st.subheader("🧹 Maintenance")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🆕 Nouvelle Conversation", key="new_conv"):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Nouvelle conversation ! Comment puis-je t'aider ?"
            })
            st.success("✅ Conversation réinitialisée")
            st.rerun()

    with col2:
        if st.button("📊 Statistiques Cache", key="cache_stats"):
            st.info("Cache Streamlit actif")

    with col3:
        if st.button("🔄 Recharger Données", key="reload_data"):
            st.cache_resource.clear()
            st.success("✅ Cache vidé")
            st.rerun()

    st.divider()

    # ✅ MESSAGE REDIRECTION
    st.info("""
    💡 **Pour enseigner à l'IA :**
    
    Utilisez l'onglet **📚 Connaissances** :
    - Catégorie **Personal**
    - Sous-catégorie **Quick**
    
    Vos apprentissages seront consultables et éditables !
    """)

def admin_interface():
    """Onglet Gestion"""
    st.header("⚙️ Gestion")

    tab1, tab2, tab3 = st.tabs([
        "📥 Import Avancé", 
        "📤 Export & Backup", 
        "🧹 Maintenance"
    ])

    with tab1:
        import_advanced_interface()

    with tab2:
        export_interface()

    with tab3:
        maintenance_interface()

def main():
    st.title("🤖 BB-IA")
    st.markdown("*Votre première IA qui apprend !*")

    st.markdown("""
    <style>
    .stApp { max-width: 100%; }
    .stChatMessage { padding: 0.5rem; margin: 0.25rem 0; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    </style>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["💬 Chat", "📚 Connaissances", "📊 Statistiques", "⚙️ Gestion"])

    with tabs[0]:
        chat_interface()

    with tabs[1]:
        knowledge_interface()

    with tabs[2]:
        stats_interface()

    with tabs[3]:
        admin_interface()

if __name__ == "__main__":
    main()
