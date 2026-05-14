import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import io

# Mode étiré pour mieux voir
st.set_page_config(layout="wide") 

# Accueil !
st.title(":rainbow[🌈 Générateur de mèmes :100:]", text_alignment="center")
st.write("Charger une image pour commencer !")

# Charger mon image depuis mon pc
image_charge = st.file_uploader("Choisis une image !", type=["jpg","jpeg","png"])


if image_charge is not None :

    # Ouvrir l'image et afficher un message de succès !
    image = Image.open(image_charge)
    largeur, hauteur = image.size
    st.success("Image chargé avec succès !")

    # Ajouter du texte n°1 sur mon image 
    st.subheader("Texte du haut")
    texte_haut = st.text_input("Texte du haut", "MON TEXTE DU HAUT")
    col1, col2 = st.columns(2)
    with col1:
        x_haut = st.slider("Position X (haut)", 0, largeur, largeur // 2)
    with col2:
        y_haut = st.slider("Position Y (haut)", 0, hauteur, hauteur // 10)

    # Ajouter du texte n°2 sur mon image
    st.subheader("Texte du bas")
    texte_bas = st.text_input("Texte du bas", "MON TEXTE DU BAS")
    col1, col2 = st.columns(2)
    with col1 :
        x_bas = st.slider("Position x (bas)", 0, largeur, largeur // 2)
    with col2 :
        y_bas = st.slider("Position y (bas)", 0, hauteur, hauteur - hauteur // 10)

    # Modifier le texte à afficher sur l'image
    st.subheader("Modifier les options du texte")
    taille_texte = st.slider("Faites glisser le curseur pour agrandir ou diminuer le texte", min_value=10, max_value=500, value=50)
    couleur_texte = st.color_picker("Choisir la couleur du texte", value="#E8E0E0")
    fonte = ImageFont.load_default(size=taille_texte)


    # Affichage du texte sur une copie de l'image
    image_modifiee = image.copy()
    texte_image = ImageDraw.Draw(image_modifiee)

    # Afficher le texte sur la copie et centrer les coordonnées du texte sur x, y
    try:
        texte_image.text((x_haut, y_haut), texte_haut, fill=couleur_texte, font=fonte, anchor="mm")
        texte_image.text((x_bas, y_bas), texte_bas, fill=couleur_texte, font=fonte, anchor="mm")
    except KeyError:
        texte_image.text((x_haut, y_haut), texte_haut, fill=couleur_texte, font=fonte)
        texte_image.text((x_bas, y_bas), texte_bas, fill=couleur_texte, font=fonte)


    # Afficher le résultat
    fonte = ImageFont.load_default(size=taille_texte)
    st.image(image_modifiee, caption="Ton mème",width="content")

    # Créer un fichier en mémoire pour accueillir notre mème
    fichier_memoire = io.BytesIO()
    image.save(fichier_memoire, format="png")
    fichier_memoire.seek(0)

    # Bouton de téléchargement
    st.download_button("Télécharger mon mème", data=fichier_memoire, file_name="Mon_mème.png", mime="image/png")

    # Création de la galerie
    if st.button("Sauvegarder dans la galerie") :
        os.makedirs("galerie", exist_ok=True)
        nombre_meme = len(os.listdir("galerie"))
        image_modifiee.save(f"galerie/Mème_{nombre_meme+1}.png")
        st.success("Mème sauvegardé avec succès")


# Affichage ou création de la galerie
st.title("galerie")
os.makedirs("galerie", exist_ok=True)
memes = os.listdir("galerie")

if len(memes) == 0:
    st.write("Aucun mème dans la galerie pour l'instant.")
else:
    colonnes = st.columns(3)
    for i, fichier in enumerate(memes):
        with colonnes[i % 3]:
            st.image(f"galerie/{fichier}", caption=fichier)

# Partager sur les réseaux sociaux
st.title("Envie de partager tes mèmes avec tes amis ?")
st.subheader("Alors vas y !")
texte_partage = "Regarde le mème que j'ai créé !"


if len(os.listdir("galerie")) != 0 :
    # Lien x
    lien_x = f"https://twitter.com/intent/tweet?text={texte_partage}"
    st.link_button("Partager sur x", lien_x)

    # Lien facebook
    lien_facebook = f"https://www.facebook.com/sharer/sharer.php?quote={texte_partage}"
    st.link_button("Partager sur Facebook", lien_facebook)
else :
    st.write("Aucun mème à partager :(")

    
