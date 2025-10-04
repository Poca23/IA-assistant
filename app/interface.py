import streamlit as st
import os
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
    
    kb = init_kb()
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
    """Onglet Gestion - Administration et apprentissage"""
    st.header("⚙️ Gestion IA")
    
    tab1, tab2 = st.tabs(["🎓 Apprentissage", "🔧 Maintenance"])
    
    with tab1:
        st.subheader("📚 Enseigner à l'IA")
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
    
    with tab2:
        st.subheader("🗑️ Actions")
        
        if st.button("🆕 Nouvelle conversation"):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Nouvelle conversation ! Comment puis-je t'aider ?"
            })
            st.success("✅ Conversation effacée !")
        
        st.divider()
        st.info("🚧 Import/Export JSON - À venir en Étape 23B")

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
