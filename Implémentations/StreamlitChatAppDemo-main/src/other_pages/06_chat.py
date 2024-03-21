# This page is for chat
import streamlit as st
from st_pages import add_page_title
import const
import datetime
import os
from PIL import Image
#import openai
from streamlit_autorefresh import st_autorefresh
from modules import common
from modules.authenticator import common_auth
from modules.database import database
import pandas as pd
from streamlit_server_state import server_state, server_state_lock
import string

st.set_page_config(layout="wide")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

rooms = server_state["rooms"]
with st.sidebar:  
    room = st.radio("Select room", rooms)
    with st.form("Nouvelle salle de jeu"):
        def on_create():
            new_room_name = st.session_state.new_room_name
            new_room_password = st.session_state.new_room_password
            if new_room_name in rooms:
                st.error("Salle de jeu déjà existante")
            elif new_room_name == "" or new_room_name == " ":
                st.error("Nom de la salle invalide")
            else:
                with server_state_lock["rooms"]:
                    server_state["rooms"] = server_state["rooms"] + [new_room_name]
        st.text_input("Nom de la salle de jeu", key = "new_room_name")
        st.text_input("Mot de passe", type="password", key="new_room_password")
        st.form_submit_button("Créer une nouvelle salle de jeu", on_click=on_create)

if not room:
    st.stop()

#add_page_title()
room_key = f"room_{room}"
with server_state_lock[room_key]:
    if room_key not in server_state:
        server_state[room_key] = []

       
#if room:
#    entered_password = st.text_input("Entrez le mot de passe de la salle de jeu", type="password", key="entered_password")
#    room_password = None
#    for r in server_state['rooms']:
#        room_password = r[1]
#        break
#    if room_password and entered_password == room_password:
#        st.success("Accès à la salle autorisé")
#    else:
#        st.error("Accès à la salle refusé, mot de passe incorrect")

st.header("Salle de jeu : " + room, divider="rainbow")
col1, col2 = st.columns([2, 1])

CHAT_ID = room

cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


with col1:
    subcol1, subcol2 = st.columns([2, 1])
    #data = {}
    #for i in range(10):
    #    col = cols[i]
    #    data[col]= range(10)
    #df = pd.DataFrame(data)
#
    #columns = st.multiselect("Columns:",df.columns, key='column_selector__columns')
    ##filter = st.radio("Choose by:", ("exclusion","inclusion"), key='column_selector__filter')
#
    ##if filter == "exclusion":
    #columns = [col for col in df.columns if col not in columns]
#
    #df[columns]

    container1 = st.container()
    container2 = st.container()
    #container1.write("TEST")
    with container1:
        subcol11, subcol12 = st.columns([2, 1])
        with subcol11:
            st.write("Grille de votre adversaire: ")
            data1 = {
                "A": [0,0,0,0,0,0,0,0,0,0],
                "B": [0,0,0,0,0,0,0,0,0,0],
                "C": [0,0,0,0,0,0,0,0,0,0],
                "D": [0,0,0,0,0,0,0,0,0,0],
                "E": [0,0,0,0,0,0,0,0,0,0],
                "F": [0,0,0,0,0,0,0,0,0,0],
                "G": [0,0,0,0,0,0,0,0,0,0],
                "H": [0,0,0,0,0,0,0,0,0,0],
                "I": [0,0,0,0,0,0,0,0,0,0],
                "J": [0,0,0,0,0,0,0,0,0,0]
                }

            df1 = pd.DataFrame(data1)
            st.write(df1)
        with subcol12:
            st.write("Bateaux restant de votre adversaire :")
            st.image('../resource/images/maillebreze.png')
            st.image('../resource/images/amiralwilliams.png')
            st.image('../resource/images/kusnetsov.png')
            st.image('../resource/images/submarine.png')
            
            
            
    with container2:
        subcol21, subcol22 = st.columns([2, 1])
        with subcol21:
            st.write("Votre grille: ")
            data2 = {
                "A": [0,0,0,0,0,0,0,0,0,0],
                "B": [0,0,0,0,0,0,0,0,0,0],
                "C": [0,0,0,0,0,0,0,0,0,0],
                "D": [0,0,0,0,0,0,0,0,0,0],
                "E": [0,0,0,0,0,0,0,0,0,0],
                "F": [0,0,0,0,0,0,0,0,0,0],
                "G": [0,0,0,0,0,0,0,0,0,0],
                "H": [0,0,0,0,0,0,0,0,0,0],
                "I": [0,0,0,0,0,0,0,0,0,0],
                "J": [0,0,0,0,0,0,0,0,0,0]
            }
            df2 = pd.DataFrame(data2)
            st.write(df2)
        with subcol22:
            st.write("Bateaux restant :")
            st.image('../resource/images/maillebreze.png')
            st.image('../resource/images/amiralwilliams.png')
            st.image('../resource/images/kusnetsov.png')
            st.image('../resource/images/submarine.png')
            
            
    
    #my_expander = st.expander(label='Expand me')
    #my_expander.write('TEST')
    #clicked = my_expander.button('CLIC')
    
with col2:
    st.header("Chat")
    authenticator = common_auth.get_authenticator()
    db = database.Database()
    if (
        common.check_if_exists_in_session(const.SESSION_INFO_AUTH_STATUS)
        and st.session_state[const.SESSION_INFO_AUTH_STATUS]
    ):
        messages = []

        user_infos = {}
        username = st.session_state[const.SESSION_INFO_USERNAME]
        name = st.session_state[const.SESSION_INFO_NAME]
        user_msg = st.chat_input("Entrez votre message")

        # Show old chat messages
        chat_log = db.get_chat_log(chat_id=CHAT_ID, limit=const.MAX_CHAT_LOGS)
        if chat_log is not None:
            for msg_info in chat_log:
                log_chat_id, log_username, log_name, log_message, log_sent_time = msg_info
                # Get user info
                if log_username not in user_infos:
                    tmp_user_info = db.get_user_info(log_username)
                    if tmp_user_info is None:
                        st.error(const.ERR_MSG_GET_USER_INFO)
                    else:
                        user_infos[log_username] = {
                            "username": log_username,
                            "name": tmp_user_info[2],
                            "image_path": tmp_user_info[4],
                            "image": None,
                        }
                # Show chat message
                if log_username in user_infos:
                    if (
                        user_infos[log_username]["image"] is None
                        and user_infos[log_username]["image_path"] is not None
                        and os.path.isfile(user_infos[log_username]["image_path"])
                    ):
                        # Load user image
                        user_infos[log_username]["image"] = Image.open(
                            user_infos[log_username]["image_path"]
                        )
                    with st.chat_message(
                        log_name, avatar=user_infos[log_username]["image"]
                    ):
                        st.write(log_name + "> " + log_message)

        else:
            st.error(const.ERR_MSG_GET_CHAT_LOGS)

        # Show user message
        if user_msg:
            # Show new chat message
            db.insert_chat_log(
                chat_id=CHAT_ID,
                username=username,
                name=name,
                message=user_msg,
                sent_time=datetime.datetime.now(),
            )
            if username not in user_infos:
                # Get user info
                tmp_user_info = db.get_user_info(username)
                if tmp_user_info is None:
                    st.error(const.ERR_MSG_GET_USER_INFO)
                else:
                    user_infos[username] = {
                        "username": username,
                        "name": tmp_user_info[2],
                        "image_path": tmp_user_info[4],
                        "image": None,
                    }
            if (
                username in user_infos
                and user_infos[username]["image"] is None
                and user_infos[username]["image_path"] is not None
                and os.path.isfile(user_infos[username]["image_path"])
            ):
                user_infos[username]["image"] = Image.open(
                    user_infos[username]["image_path"]
                )
            with st.chat_message(name, avatar=user_infos[username]["image"]):
                st.write(name + "> " + user_msg)

        count = st_autorefresh(
            interval=const.REFRESH_INTERVAL, limit=None, key="fizzbuzzcounter"
        )
    else:
        st.error("You are not logged in. Please go to the login page.")
