import streamlit as st
from threading import RLock

# Initialisation de l'état côté client
if "nicknames" not in st.session_state:
    st.session_state["nicknames"] = []
if "lock" not in st.session_state:
    st.session_state["lock"] = None

def acquire_lock():
    """Acquiert un verrou sur l'état côté client."""
    if st.session_state["lock"] is None:
        st.session_state["lock"] = RLock()
    st.session_state["lock"].acquire()

def release_lock():
    """Libère le verrou sur l'état côté client."""
    if st.session_state["lock"] is not None:
        st.session_state["lock"].release()

def get_nicknames():
    """Récupère la liste des pseudos depuis l'état côté client."""
    return st.session_state["nicknames"]

def add_nickname(nickname):
    """Ajoute un nouveau pseudo à la liste dans l'état côté client."""
    acquire_lock()
    try:
        st.session_state["nicknames"].append(nickname)
    finally:
        release_lock()

def remove_nickname(nickname):
    """Retire un pseudo de la liste des pseudos."""
    acquire_lock()
    try:
        if nickname in st.session_state["nicknames"]:
            st.session_state["nicknames"].remove(nickname)
    finally:
        release_lock()

# Utilisation de la barre latérale pour la saisie de pseudo
with st.sidebar.form("Pseudo"):
    pseudo_saisie = st.text_input("Entrez votre pseudo", key='new_pseudo')
    if st.form_submit_button("Valider"):
        add_nickname(pseudo_saisie)
        st.success("Pseudo enregistré !")

# Bouton de déconnexion
if st.sidebar.button("Déconnexion"):
    remove_nickname(pseudo_saisie)
    st.success("Déconnexion réussie !")

# Affichage de la liste des pseudos connectés
st.sidebar.write("Personnes connectées :", get_nicknames())
