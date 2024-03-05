import json
import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

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
        with open(file_path, 'r') as file:
            try:
                pseudos = json.load(file)
            except json.JSONDecodeError:
                pseudos = []
    except FileNotFoundError:
        pseudos = []

    # Créé un dictionnaire pour associer le pseudo à l'adresse IP
    pseudo_data = {"pseudo": pseudo, "ip_address": ip_address}
    pseudos.append(pseudo_data)

    with open(file_path, 'w') as file:
        json.dump(pseudos, file)

def get_pseudos_list():
    """Récupère la liste des pseudos enregistrés."""

    file_path = "pseudos.json"

    try:
        with open(file_path, 'r') as file:
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
    st.title("Liste des pseudos des personnes connectées")

    pseudo = st.text_input("Entrez votre pseudo:")

    if st.button("Ajouter"):
        ip_address = get_remote_ip()
        pseudos = get_pseudos_list()

        is_ip_unique = check_ip_uniqueness(ip_address, pseudos)
        if is_ip_unique:
            # Afficher un message d'erreur indiquant que l'adresse IP est déjà utilisée
            st.error("L'adresse IP est déjà associée à un autre pseudo.")
        else:
            add_pseudo_to_list(pseudo, ip_address)
            st.success(f"Pseudo {pseudo} ajouté avec succès.")
            pseudos_placeholder = st.empty()
            pseudos = get_pseudos_list()
            pseudos_placeholder.write("Liste des pseudos avec leurs adresses IP:")
            #for ip, pseudo in pseudos:
                #pseudos_placeholder.write(f"{pseudo} (IP: {ip})")
    st.button("Mettre à jour la liste")

    pseudos = get_pseudos_list()

    if not isinstance(pseudos, list):  # Vérifie si la variable est une liste
        st.error("Une erreur est survenue lors de la récupération des pseudos.")
        return

    st.write("Liste des pseudos avec leurs adresses IP:")

    for pseudo_data in pseudos:
        # Accède aux valeurs en utilisant les clés du dictionnaire
        pseudo = pseudo_data.get('pseudo', '')  # Valeur par défaut si la clé n'existe pas
        ip_address = pseudo_data.get('ip_address', '')

        st.write(f"{pseudo} - {ip_address}")

if __name__ == "__main__":
    main()