import streamlit as st

from streamlit_server_state import server_state, server_state_lock



st.set_page_config(layout="wide")

with server_state_lock["rooms"]:
    if "rooms" not in server_state:
        server_state["rooms"] = []

with server_state_lock["nicknames"]:
    if "nicknames" not in server_state:
        server_state["nicknames"] = []

rooms = server_state["rooms"]
nicknames = server_state["nicknames"]

room = st.sidebar.radio("Select room", rooms)

with st.sidebar.form("New room"):

    def on_create():
        new_room_name = st.session_state.new_room_name
        with server_state_lock["rooms"]:
            server_state["rooms"] = server_state["rooms"] + [new_room_name]

    st.text_input("Room name", key="new_room_name")
    st.form_submit_button("Create a new room", on_click=on_create)

nicknames = st.sidebar.write("Personnes connectées :", nicknames)


if not room:
    st.stop()

room_key = f"room_{room}"
with server_state_lock[room_key]:
    if room_key not in server_state:
        server_state[room_key] = []

st.header('Salle de jeu : '+ room, divider='rainbow')

nickname = st.text_input("Votre pseudo", key=f"nickname_{room}")
if not nickname:
    st.warning("Entrez votre pseudo.")
    st.stop()


col1, col2 = st.columns([2,1])
with col1:
    st.header("Jeu")
    grille = st.columns(10)
    for i in range(10):
        with grille[i]:
            panel = st.container(border=True)
            st.header(str(i))
    
with col2:
    st.header("Chat")
    message_input_key = f"message_input_{room}"
    def on_message_input():
        new_message_text = st.session_state[message_input_key]
        if not new_message_text:
            return
    
        new_message_packet = {
            "nickname": nickname,
            "text": new_message_text,
        }
    
        with server_state_lock[room_key]:
            server_state[room_key] = server_state[room_key] + [new_message_packet]
    st.text_input("Message", key=message_input_key, on_change=on_message_input)
    st.subheader("Messages:")
    st.write(server_state[room_key])