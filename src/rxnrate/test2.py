import streamlit as st

# Initialiser la "page" dans la session si elle n'existe pas
if "page" not in st.session_state:
    st.session_state.page = "accueil"

# Fonction pour changer de page
def aller_a_la_page_suivante():
    st.session_state.page = "analyse"

# Affichage selon la "page"
if st.session_state.page == "accueil":
    st.title("Page d'accueil")
    st.write("Bienvenue ! Cliquez pour continuer.")
    if st.button("Aller à la page suivante"):
        aller_a_la_page_suivante()

elif st.session_state.page == "analyse":
    st.title("Page d'analyse")
    st.write("Voici la deuxième page !")
    