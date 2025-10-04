import streamlit as st
import os
import json
from datetime import datetime
from .brain import AIBrain
from .learning import teach_ai
from .knowledge import KnowledgeBase

st.set_page_config(
    page_title="Claire-IA Conversationnelle",
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
            "content": "Salut ! Je suis Claire-IA. Comment puis-je t'aider ?"
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
                ai = AIBrain()
                response = ai.get_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

def knowledge_interface():
    """Onglet Connaissances - Visualisation et gestion"""
    st.header("📚 Base de Connaissances")
    
    kb = KnowledgeBase()
    categories = kb.list_categories()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🗂️ Catégories")
        
        # Sélection catégorie principale
        selected_cat = st.radio(
            "Catégorie principale:",
            categories,
            format_func=lambda x: f"📁 {x.title()}"
        )
        
        # Liste des sous-catégories disponibles
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

            try:
                # Lecture sécurisée avec validation de type
                result = kb.read_entries(selected_cat, selected_subcat)

                # Vérification du type de retour
                if isinstance(result, str):
                    st.error(f"❌ Erreur format : {result}")
                elif isinstance(result, list) and len(result) > 0:
                    for entry in result:
                        # Vérification que l'entrée est bien un dictionnaire
                        if isinstance(entry, dict):
                            with st.expander(f"🔹 {entry.get('question', 'Sans titre')}"):
                                st.write(f"**Réponse:** {entry.get('answer', 'N/A')}")
                                tags = entry.get('tags', [])
                                if tags:
                                    st.caption(f"🏷️ Tags: {', '.join(tags)}")
                                st.caption(f"📅 Créé: {entry.get('created', 'N/A')}")
                        else:
                            st.warning(f"⚠️ Entrée invalide : {type(entry)}")
                else:
                    st.info("📭 Aucune entrée dans cette sous-catégorie")
                    
            except Exception as e:
                st.error(f"❌ Erreur lecture : {str(e)}")
        else:
            st.info("👈 Sélectionnez une catégorie et une sous-catégorie")

def stats_interface():
    """Onglet Statistiques - Métriques et analyses"""
    st.header("📊 Statistiques")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        ai = AIBrain()
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
            # Compte toutes les entrées de toutes les sous-catégories
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

def admin_interface():
    """Onglet Gestion - Import/Export/Maintenance"""
    st.header("🔧 Gestion des Connaissances")
    
    tab1, tab2, tab3 = st.tabs(["📥 Import", "📤 Export", "🧹 Maintenance"])
    
    # TAB 1 : IMPORT JSON
    with tab1:
        st.subheader("📥 Importer des Connaissances")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Catégorie",
                ["general", "personal"],
                key="import_category"
            )
        
        with col2:
            if category == "general":
                subcategories = ["culture", "sciences", "technologies"]
            else:
                subcategories = ["cuisine", "admin", "sante", "budget"]
            
            subcategory = st.selectbox(
                "Sous-catégorie",
                subcategories,
                key="import_subcategory"
            )
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier JSON",
            type=["json"],
            help="Format attendu : {'entries': [{'question': '...', 'answer': '...'}]}"
        )
        
        if uploaded_file is not None:
            # Afficher aperçu
            file_content = uploaded_file.read().decode("utf-8")
            
            with st.expander("📄 Aperçu du fichier"):
                try:
                    preview_data = json.loads(file_content)
                    st.json(preview_data)
                except:
                    st.error("❌ Fichier JSON invalide")
            
            # Bouton d'import
            if st.button("🚀 Importer", type="primary"):
                from .import_handler import ImportHandler
                
                handler = ImportHandler()
                success, message, count = handler.import_from_json(
                    file_content, 
                    category, 
                    subcategory
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")
    
    # TAB 2 : EXPORT JSON
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
            kb = KnowledgeBase()
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
    
    # TAB 3 : MAINTENANCE
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
        
        # Section Apprentissage (conservée)
        st.subheader("🎓 Enseigner à l'IA")
        question = st.text_input("Question :", key="learn_question")
        answer = st.text_input("Réponse :", key="learn_answer")
        
        if st.button("🎓 Apprendre", type="primary"):
            if question and answer:
                try:
                    success = teach_ai(question, answer)
                    if success:
                        st.success(f"✅ Claire-IA a appris !\n**Q:** {question}\n**R:** {answer}")
                        st.balloons()
                    else:
                        st.error("❌ Erreur durant l'apprentissage")
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.error("⚠️ Veuillez remplir les deux champs")

def main():
    st.title("🤖 Claire-IA Conversationnelle")
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
