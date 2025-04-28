import streamlit as st

def inverser_chaine(chaine):
    return chaine[::-1]

st.title("Inversion de chaîne")

texte = st.text_input("Entrez une chaîne de caractères")

if st.button("Inverser"):
    resultat = inverser_chaine(texte)
    st.write("Résultat :", resultat)

