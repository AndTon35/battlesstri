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

def on_name(nouveau_pseudo):
    """Gère la soumission du formulaire pour ajouter un pseudo."""
    if nouveau_pseudo:
        acquire_lock()
        try:
            add_nickname(nouveau_pseudo)
            st.success("Pseudo enregistré !")
        finally:
            release_lock()
    else:
        st.warning("Veuillez entrer un pseudo valide.")

# Utilisation de la barre latérale pour la saisie de pseudo
with st.sidebar.form("Pseudo"):
    nouveau_pseudo = st.text_input("Entrez votre pseudo", key='new_pseudo').strip()
    if st.form_submit_button("Valider"):
        on_name(nouveau_pseudo)

# Affichage de la liste des pseudos connectés
st.sidebar.write("Personnes connectées :", get_nicknames())
