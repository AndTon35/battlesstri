# accueil.py
import streamlit as st

def afficher_accueil():
    st.title("Bienvenue dans notre jeu de Bataille Navale")
    st.write("Pour commencer, veuillez placer vos bateaux sur le plateau de jeu.")
    if st.button("Commencer"):
        st.session_state["page"] = "placement"
