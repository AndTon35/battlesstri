import streamlit as st

# Définition des constantes
TAILLE_GRILLE = 10

# Définition des classes
class Bateau:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.cases = []

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.grille = [[0 for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]
        self.bateaux = []

    def placer_bateau(self, bateau):
        """
        Fonction pour placer un bateau sur la grille du joueur.
        """
        placement_valide = False
        while not placement_valide:
            x, y = st.selectbox("Choisissez la position du {} ({}) :".format(bateau.nom, bateau.taille),
                                 list(zip(range(TAILLE_GRILLE), range(TAILLE_GRILLE))), key=f"{bateau.nom}_position")
            direction = st.selectbox("Choisissez la direction (H pour Horizontal, V pour Vertical) :", ["H", "V"], key=f"{bateau.nom}_direction")

            if direction == "H":
                placement_valide = self.placer_bateau_horizontal(bateau, x, y)
            else:
                placement_valide = self.placer_bateau_vertical(bateau, x, y)

        self.bateaux.append(bateau)

    def placer_bateau_horizontal(self, bateau, x, y):
        """
        Place un bateau horizontalement sur la grille.
        """
        if y + bateau.taille <= TAILLE_GRILLE and all(self.grille[x][y+i] == 0 for i in range(bateau.taille)):
            for i in range(bateau.taille):
                self.grille[x][y+i] = bateau
                bateau.cases.append((x, y+i))
            return True
        return False

    def placer_bateau_vertical(self, bateau, x, y):
        """
        Place un bateau verticalement sur la grille.
        """
        if x + bateau.taille <= TAILLE_GRILLE and all(self.grille[x+i][y] == 0 for i in range(bateau.taille)):
            for i in range(bateau.taille):
                self.grille[x+i][y] = bateau
                bateau.cases.append((x+i, y))
            return True
        return False

    def tirer(self, x, y):
        """
        Fonction pour tirer sur une case de la grille d'un joueur.
        """
        if not 0 <= x < TAILLE_GRILLE or not 0 <= y < TAILLE_GRILLE:
            st.warning("Tir en dehors de la grille.")
            return False

        if self.grille[x][y] == -1:
            st.warning("Cette case a déjà été tirée.")
            return False

        self.grille[x][y] = -1
        bateau_touche = self.verifier_bateau_touche(x, y)

        if bateau_touche:
            st.success("Tir réussi !")
        else:
            st.warning("Tir manqué.")

        return bateau_touche

    def verifier_bateau_touche(self, x, y):
        """
        Vérifie si un tir a touché un bateau.
        """
        for bateau in self.bateaux:
            if (x, y) in bateau.cases:
                bateau.cases.remove((x, y))
                if len(bateau.cases) == 0:
                    st.success(f"Le {bateau.nom} a été coulé !")
                return True
        return False

# Fonction pour initialiser le jeu
def initialiser_jeu():
    joueurs = [Joueur("Joueur 1"), Joueur("Joueur 2")]
    bateaux = [Bateau("Porte-avions", 5), Bateau("Croiseur", 4), Bateau("Contre-torpilleur", 3), Bateau("Sous-marin", 3), Bateau("Torpilleur", 2)]
    for joueur in joueurs:
        for bateau in bateaux:
            joueur.placer_bateau(bateau)
    return joueurs, bateaux

# Fonction pour afficher la grille
def afficher_grille(joueur):
    """
    Fonction pour afficher la grille du joueur.
    """
    for ligne in joueur.grille:
        st.write(" ".join(str(case) for case in ligne))

# Fonction principale
def main():
    # Initialisation du jeu
    joueurs, bateaux = initialiser_jeu()

    # Interface utilisateur
    st.title("Bataille navale")

    # Affichage des grilles
    st.subheader("Grille de {}:".format(joueurs[0].nom))
    afficher_grille(joueurs[0])
    st.subheader("Grille de {}:".format(joueurs[1].nom))
    afficher_grille(joueurs[1])

    # Gestion du tour en cours
    tour_en_cours = 0
    while True:
        joueur_courant = joueurs[tour_en_cours]
        x, y = st.selectbox("Choisissez une case à tirer:",
                             list(zip(range(TAILLE_GRILLE), range(TAILLE_GRILLE))), key="tir_position")
        joueur_courant.tirer(x, y)

        # Changement de tour
        tour_en_cours = (tour_en_cours + 1) % 2

# Lancement de l'application
if __name__ == "__main__":
    main()
