import streamlit as st
import numpy as np

GRID_SIZE = 10
grille = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def afficher_accueil():
    st.title("Bienvenue dans notre jeu de Bataille Navale")
    st.write("Pour commencer, veuillez placer vos bateaux sur le plateau de jeu.")
    if st.button("Commencer"):
        st.session_state["page"] = "placement"
        
def afficher_grille(grille):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Utiliser st.selectbox pour chaque cellule de la grille
            # Ici, on suppose que l'utilisateur peut choisir entre des valeurs comme '.' (point d'eau), 'S' (bateau)
            grille[i][j] = st.selectbox(label=f"Cellule ({i},{j})", options=['.', 'S'], index=1 if grille[i][j] == 'S' else 0)
        #st.write("") # Pour passer à la ligne
        
def afficher_placement():
    st.title("Placement des bateaux")
    st.write("Placez vos bateaux sur le plateau de jeu.")
    
    afficher_grille(grille)
        
    if st.button("Valider le placement des bateaux"):
        st.session_state["page"] = "jouer"

def afficher_jouer():
    st.title("Jouer")
    st.write("C'est votre tour de jouer.")


    if st.button("Terminer le tour"):
        st.session_state["page"] = "accueil"



def main():
    st.set_page_config(page_title="Jeu de Bataille Navale", layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choisissez une page", ["Accueil", "Placement des bateaux", "Jouer"])
    if page == "Accueil":
        afficher_accueil()
    elif page == "Placement des bateaux":
        afficher_placement()
    elif page == "Jouer":
        afficher_jouer()

if __name__ == "__main__":
    main()
