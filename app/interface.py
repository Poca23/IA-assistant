# app/interface.py
import streamlit as st
import os
import json
from datetime import datetime
from .brain import AIBrain
from .learning import teach_ai
from .knowledge import KnowledgeBase

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
    from .sync_import import SyncImport
    
    st.subheader("📥 Import Avancé")
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Catégorie", ["general", "personal"])
    with col2:
        subcategory = st.text_input("Sous-catégorie", 
                                     placeholder="ex: technologies")
    
    uploaded = st.file_uploader("Sélectionner JSON", type=["json"])
    
    if uploaded and subcategory:
        content = uploaded.read().decode("utf-8")
        sync = SyncImport()
        
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
                        type="primary"):
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

def admin_interface():
    """Onglet Gestion - Outils maintenance"""
    st.header("⚙️ Gestion")
    
    tab1, tab2, tab3 = st.tabs(["📥 Import Avancé", "📤 Export", "🧹 Maintenance"])
    
    with tab1:
        import_advanced_interface()
    
    with tab2:
        st.subheader("📤 Exporter des Connaissances")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_category = st.selectbox(
                "Catégorie",
                ["general", "personal"],
                key="export_category"
            )
        
        with col2:
            if export_category == "general":
                export_subcategories = ["culture", "sciences", "technologies"]
            else:
                export_subcategories = ["cuisine", "admin", "sante", "budget"]
            
            export_subcategory = st.selectbox(
                "Sous-catégorie",
                export_subcategories,
                key="export_subcategory"
            )
        
        if st.button("📥 Télécharger JSON"):
            kb = init_kb()
            entries = kb.read_entries(export_category, export_subcategory)
            
            if entries and isinstance(entries, list):
                export_data = {
                    "entries": entries,
                    "metadata": {
                        "category": export_category,
                        "subcategory": export_subcategory,
                        "total_entries": len(entries),
                        "exported": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                
                json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="💾 Télécharger",
                    data=json_str,
                    file_name=f"{export_category}_{export_subcategory}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                st.success(f"✅ Prêt à télécharger ({len(entries)} entrées)")
            else:
                st.warning("⚠️ Aucune entrée à exporter")
    
    with tab3:
        st.subheader("🧹 Maintenance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🆕 Nouvelle Conversation"):
                st.session_state.messages = []
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": "Nouvelle conversation ! Comment puis-je t'aider ?"
                })
                st.success("✅ Conversation réinitialisée")
                st.rerun()
        
        with col2:
            if st.button("📊 Statistiques Cache"):
                st.info("Cache Streamlit actif")
        
        with col3:
            if st.button("🔄 Recharger Données"):
                st.cache_resource.clear()
                st.success("✅ Cache vidé")
                st.rerun()
        
        st.divider()
        
        st.subheader("🎓 Enseigner à l'IA")
        question = st.text_input("Question :", key="learn_question")
        answer = st.text_input("Réponse :", key="learn_answer")
        
        if st.button("🎓 Apprendre", type="primary"):
            if question and answer:
                try:
                    success = teach_ai(question, answer)
                    if success:
                        st.success(f"✅ BB-IA a appris !\n**Q:** {question}\n**R:** {answer}")
                        st.balloons()
                    else:
                        st.error("❌ Erreur durant l'apprentissage")
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.error("⚠️ Veuillez remplir les deux champs")

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
