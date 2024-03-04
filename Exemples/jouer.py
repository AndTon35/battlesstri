# jouer.py
import streamlit as st

def afficher_jouer():
    st.title("Jouer")
    st.write("C'est votre tour de jouer.")
    # Ici, vous pouvez ajouter la logique pour tirer sur le plateau adverse
    if st.button("Terminer le tour"):
        st.session_state["page"] = "accueil"
