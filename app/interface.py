# app/interface.py - Interface web Streamlit SANS boucle infinie
import streamlit as st
import time
from app.brain import AIBrain
from app.learning import teach_ai

# Configuration page
st.set_page_config(
    page_title="Claire-IA Conversationnelle",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation IA
@st.cache_resource
def init_ai():
    return AIBrain()

def main():
    # Header
    st.title("🤖 Claire-IA Conversationnelle")
    st.markdown("*Votre première IA qui apprend !*")
    
    # CSS pour éviter erreurs console
    st.markdown("""
    <style>
    .stApp { max-width: 100%; }
    .stChatMessage { padding: 0.5rem; margin: 0.25rem 0; }
    .stSidebar { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialiser l'historique de session
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Salut ! Je suis Claire-IA. Comment puis-je t'aider ?"
        })
    
    # Afficher l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input utilisateur
    if prompt := st.chat_input("Écris ton message..."):
        # Afficher le message utilisateur
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Générer et afficher la réponse IA
        with st.chat_message("assistant"):
            with st.spinner("Je réfléchis..."):
                ai = AIBrain()  # Nouvelle instance à chaque fois
                response = ai.get_response(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar - Fonctionnalités
    with st.sidebar:
        st.header("🧠 Contrôles IA")
        
        # Section apprentissage
        st.subheader("📚 Enseigner à l'IA")
        question = st.text_input("Question :", key="learn_question")
        answer = st.text_input("Réponse :", key="learn_answer")
        
        # Bouton Apprendre SANS st.rerun()
        if st.button("🎓 Apprendre"):
            if question and answer:
                try:
                    success = teach_ai(question, answer)
                    if success:
                        st.success(f"✅ Claire-IA a appris !\n**Q:** {question}\n**R:** {answer}")
                        # PLUS DE st.rerun() ici !
                        st.balloons()  # Animation de succès
                    else:
                        st.error("❌ Erreur durant l'apprentissage")
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
            else:
                st.error("⚠️ Veuillez remplir les deux champs")
        
        # Stats rechargées automatiquement
        st.subheader("📊 Statistiques")
        try:
            ai_stats = AIBrain()
            conversations = ai_stats.memory.load_conversations()
            st.metric("Conversations", len(conversations.get('conversations', [])))
            st.metric("Réponses apprises", len(conversations.get('learned_responses', {})))
        except Exception as e:
            st.error(f"❌ Erreur stats : {str(e)}")
        
        # Clear conversation SANS st.rerun()
        if st.button("🗑️ Nouvelle conversation"):
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Nouvelle conversation ! Comment puis-je t'aider ?"
            })
            st.success("🆕 Conversation effacée !")

if __name__ == "__main__":
    main()
