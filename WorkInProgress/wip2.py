import streamlit as st
import json
from streamlit_server_state import server_state, server_state_lock
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import pandas as pd

st.set_page_config(layout="wide")
pseudos = {}

with server_state_lock["rooms"]:
    if "rooms" not in server_state:
        server_state["rooms"] = []

with server_state_lock["nicknames"]:
    if "nicknames" not in server_state:
        server_state["nicknames"] = []

rooms = server_state["rooms"]
nicknames = server_state["nicknames"]

room = st.sidebar.radio("Select room", rooms)


# Recupere l'ip du client
def get_remote_ip() -> str:
    """Retourne l'adresse IP à distance du client."""

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


def add_pseudo_to_list(pseudo, ip_address):
    """Ajoute un pseudo et son adresse IP à la liste des pseudos enregistrés."""

    file_path = "pseudos.json"

    try:
        with open(file_path, "r") as file:
            try:
                pseudos = json.load(file)
            except json.JSONDecodeError:
                pseudos = []
    except FileNotFoundError:
        pseudos = []

    # Créé un dictionnaire pour associer le pseudo à l'adresse IP
    pseudo_data = {"pseudo": pseudo, "ip_address": ip_address}
    pseudos.append(pseudo_data)

    with open(file_path, "w") as file:
        json.dump(pseudos, file)


def get_pseudo_from_ip(ip_address):
    file_path = "pseudos.json"

    try:
        with open(file_path, "r") as file:
            try:
                pseudos = json.load(file)
            except json.JSONDecodeError:
                pseudos = {}
    except FileNotFoundError:
        pseudos = {}
    if not isinstance(pseudos, dict):
        pseudos = {}

    return pseudos.get(ip_address)


def get_pseudos_list():
    """Récupère la liste des pseudos enregistrés."""

    file_path = "pseudos.json"

    try:
        with open(file_path, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Retourne une liste vide en cas d'erreur
    except FileNotFoundError:
        return []  # Retourne une liste vide si le fichier n'existe pas


def check_ip_uniqueness(ip_address, pseudos):
    """
    Vérifie si l'adresse IP est déjà associée à un pseudo dans la liste.

    Args:
      ip_address (str): L'adresse IP à vérifier.
      pseudos (list): La liste des pseudos et adresses IP.

    Returns:
      bool: True si l'adresse IP est déjà associée à un pseudo, False sinon.
    """

    for pseudo_data in pseudos:
        if pseudo_data["ip_address"] == ip_address:
            return True
    return False


def main():
    with st.sidebar:
        with st.form("New room"):

            def on_create():
                new_room_name = st.session_state.new_room_name
                if new_room_name in rooms:
                    st.error("Salle déjà existante")
                else:
                    with server_state_lock["rooms"]:
                        server_state["rooms"] = server_state["rooms"] + [new_room_name]

            st.text_input("Room name", key="new_room_name")
            st.form_submit_button("Create a new room", on_click=on_create)

        with st.container():
            st.sidebar.write("# Liste des personnes connectées")
            pseudo = st.sidebar.text_input("Entrez votre pseudo:")
            if st.sidebar.button("Ajouter"):
                ip_address = get_remote_ip()
                pseudos = get_pseudos_list()
                is_ip_unique = check_ip_uniqueness(ip_address, pseudos)
                if is_ip_unique:
                    # Afficher un message d'erreur indiquant que l'adresse IP est déjà utilisée
                    st.sidebar.error(
                        "L'adresse IP est déjà associée à un autre pseudo."
                    )
                else:
                    add_pseudo_to_list(pseudo, ip_address)
                    st.sidebar.success(f"Pseudo {pseudo} ajouté avec succès.")
                    # for ip, pseudo in pseudos:
                    # pseudos_placeholder.write(f"{pseudo} (IP: {ip})")

            st.sidebar.button("Mettre à jour la liste")

            pseudos_placeholder = st.sidebar.empty()
            pseudos = get_pseudos_list()
            pseudos_placeholder.write("#### Liste des joueurs connectés:")

            if not isinstance(pseudos, list):  # Vérifie si la variable est une liste
                st.sidebar.error(
                    "Une erreur est survenue lors de la récupération des pseudos."
                )
                return

            for pseudo_data in pseudos:
                # Accède aux valeurs en utilisant les clés du dictionnaire
                pseudo = pseudo_data.get(
                    "pseudo", ""
                )  # Valeur par défaut si la clé n'existe pas
                ip_address = pseudo_data.get("ip_address", "")

                st.sidebar.write(f"{pseudo} (IP: {ip_address})")

                # my_pseudo = pseudos.get(ip_address, None)
                # if pseudo:
                #    st.sidebar.write(f"Le pseudo est {my_pseudo}")
                # else:
                #    st.sidebar.write("Aucun pseudo n'a été entré")

    # with st.sidebar.form("Pseudo"):
    #
    #    def on_name():
    #        new_pseudo = st.session_state.new_pseudo
    #        if new_pseudo in nicknames:
    #            st.error("Pseudo déjà utilisé")
    #        else:
    #            with server_state_lock["nicknames"]:
    #                server_state["nickames"] = server_state["nicknames"] + [new_pseudo]
    #
    #    st.text_input("Pseudo", key='new_pseudo')
    #    st.form_submit_button("Entrez votre pseudo", on_click=on_name)
    #    #nickname = st.text_input("Votre pseudo", key=f"nickname_{room}")
    #    #if not nickname:
    #    #    st.warning("Entrez votre pseudo.")
    #    #    st.stop()
    # st.sidebar.write("Personnes connectées :", nicknames)
    # print(nicknames)

    if not room:
        st.stop()

    room_key = f"room_{room}"
    with server_state_lock[room_key]:
        if room_key not in server_state:
            server_state[room_key] = []

    st.header("Salle de jeu : " + room, divider="rainbow")

    col1, col2 = st.columns([2, 1])
    with col1:
        data = {}
        for i in range(10):
            col = f'col{i}'
            data[col]= range(10)
        df = pd.DataFrame(data)

        columns = st.multiselect("Columns:",df.columns, key='column_selector__columns')
        filter = st.radio("Choose by:", ("exclusion","inclusion"), key='column_selector__filter')

        if filter == "exclusion":
            columns = [col for col in df.columns if col not in columns]

        df[columns]
    
    #with col1:
    #    options = ['Eau', 'Bateau1', 'Bateau2']
    #    num_row = 10
    #    st.header("Jeu")
    #    grille = st.columns(10)
    #    for i in range(10):
    #        with grille[i]:
    #            #panel = st.container(border=True)
    #            st.header(str(i))
    #            for i in range(num_row):
    #                st.text_input('col'+str(grille[i]), key = f'input')

    with col2:
        st.header("Chat")
        message_input_key = f"message_input_{room}"

        def on_message_input():
            new_message_text = st.session_state[message_input_key]
            if not new_message_text:
                return

            current_ip = get_remote_ip()
            current_pseudo = get_pseudo_from_ip(current_ip)
            st.sidebar.write(current_ip)
            current_nick = pseudos
            st.sidebar.write(pseudo)
            if current_pseudo != pseudo:
                st.error("Le pseudo ne correspond pas à la session.")
                return

            new_message_packet = {
                "nickname": pseudo,
                "text": new_message_text,
            }

            with server_state_lock[room_key]:
                server_state[room_key] = server_state[room_key] + [new_message_packet]

        st.text_input("Message", key=message_input_key, on_change=on_message_input)
        st.subheader("Messages:")
        st.write(server_state[room_key])


if __name__ == "__main__":
    main()
