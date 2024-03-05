import json
import streamlit as st

def add_pseudo_to_list(pseudo):
    file_path = "pseudos.json"
    
    try:
        with open(file_path, 'r') as file:
            try:
                pseudos = json.load(file)
            except json.JSONDecodeError:
                pseudos = []
    except FileNotFoundError:
        pseudos = []
    
    pseudos.append(pseudo)
    
    with open(file_path, 'w') as file:
        json.dump(pseudos, file)

def get_pseudos_list():
    file_path = "pseudos.json"
    
    try:
        with open(file_path, 'r') as file:
            try:
                pseudos = json.load(file)
            except json.JSONDecodeError:
                pseudos = []
    except FileNotFoundError:
        pseudos = []
    
    return pseudos

def main():
    st.title("Liste des pseudos des personnes connectées")
    
    pseudo = st.text_input("Entrez votre pseudo:")
    if st.button("Ajouter"):
        add_pseudo_to_list(pseudo)
        st.success(f"Pseudo {pseudo} ajouté avec succès.")
    
    pseudos = get_pseudos_list()
    st.write("Liste des pseudos:")
    for pseudo in pseudos:
        st.write(pseudo)

if __name__ == "__main__":
    main()