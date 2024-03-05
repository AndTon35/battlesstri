import streamlit as st
from threading import RLock
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit import runtime
import json

# Initialisation de l'état côté client
if "nicknames" not in st.session_state:
    st.session_state["nicknames"] = {}
if "lock" not in st.session_state:
    st.session_state["lock"] = None

def add_pseudo_to_list(pseudo):
    # Chemin vers le fichier de stockage
    file_path = "pseudos.json"
    
    # Charger la liste des pseudos depuis le fichier
    try:
        with open(file_path, 'r') as file:
            pseudos = json.load(file)
    except FileNotFoundError:
        pseudos = []
    
    # Ajouter le nouveau pseudo à la liste
    pseudos.append(pseudo)
    
    # Sauvegarder la liste mise à jour dans le fichier
    with open(file_path, 'w') as file:
        json.dump(pseudos, file)

def get_pseudos_list():
    # Chemin vers le fichier de stockage
    file_path = "pseudos.json"
    
    # Charger la liste des pseudos depuis le fichier
    try:
        with open(file_path, 'r') as file:
            pseudos = json.load(file)
    except FileNotFoundError:
        pseudos = []
    
    return pseudos


def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

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
        st.session_state["nicknames"]["pseudo"] = nickname
        st.session_state["nicknames"]["address"] = get_remote_ip()
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


st.markdown(f"The remote ip is {get_remote_ip()}")