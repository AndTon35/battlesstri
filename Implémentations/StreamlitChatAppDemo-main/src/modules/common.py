import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages
import const
from modules import common
from modules.database import database
from streamlit_server_state import server_state, server_state_lock

db = database.Database()

with server_state_lock["rooms"]:
    if "rooms" not in server_state:
        server_state["rooms"] = []





def set_pages():
    """Set the pages to be shown in the sidebar.
    """
    default_pages = [
        Page("01_login.py", "Login/Logout", "🏠"),
        Page("other_pages/02_register_user.py", "Enregistrement de votre profil", "📝"),
    ]
    after_login_pages = [
        Page("other_pages/03_reset_password.py", "Changez votre mot de passe", "🔑"),
        Page("other_pages/04_change_icon.py", "Changez votre avatar", "👤"),
        Page("other_pages/06_chat.py", "Salle de jeu", "💬"),
        Page("other_pages/07_settings.py", "Paramètres", "⚙️"),
    ]
    pages = default_pages
    
    # Check if user is logged in
    if (
        common.check_if_exists_in_session(const.SESSION_INFO_AUTH_STATUS)
        and st.session_state[const.SESSION_INFO_AUTH_STATUS]
    ):
        pages += after_login_pages
    show_pages(pages)


def check_if_exists_in_session(key: str) -> bool:
    """Check if key exists in session state

    Args:
        key (str): key to check.

    Returns:
        bool : True if key exists in session state, False otherwise.
    """
    if key in st.session_state:
        return True
    else:
        return False
