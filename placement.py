# placement.py
import streamlit as st

def afficher_placement():
    st.title("Placement des bateaux")
    st.write("Placez vos bateaux sur le plateau de jeu.")
    # Ici, vous pouvez ajouter des boutons ou des champs de saisie pour placer les bateaux
    if st.button("Valider le placement des bateaux"):
        st.session_state["page"] = "jouer"
