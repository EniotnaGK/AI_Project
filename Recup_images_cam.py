import cv2
import requests
import numpy as np
from io import BytesIO
from PIL import Image
import os
import time
import pickle


def telecharger_image(url="https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG"):
    # Télécharger l'image à partir de l'URL
    response = requests.get("https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG")
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Ouvrir l'image à partir du contenu binaire
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Erreur lors de la requête pour télécharger l'image.")
        return None

def comparer_images(image1, image2):
    # Convertir les images en tableaux numpy
    np_image1 = np.array(image1)
    np_image2 = np.array(image2)

    # Comparer les tableaux numpy pour détecter les différences de pixels
    return not np.array_equal(np_image1, np_image2)

def enregistrer_image(image, chemin_enregistrement, liste_images):
    # Enregistrer l'image sur le disque
    image.save(chemin_enregistrement)
    print("Nouvelle image enregistrée.")
    # Ajouter l'image à la liste
    liste_images.append(image)

# URL de l'image à surveiller
url_image = "https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG"

# Chemin où enregistrer les images
dossier_enregistrement = "Images_Lyon"
if not os.path.exists(dossier_enregistrement):
    os.makedirs(dossier_enregistrement)

# Vérifier si une liste d'images existe déjà
chemin_liste_images = os.path.join(dossier_enregistrement, "liste_images.pkl")
if os.path.exists(chemin_liste_images):
    with open(chemin_liste_images, "rb") as fichier:
        liste_images = pickle.load(fichier)
else:
    liste_images = []

while True:
    # Télécharger la nouvelle image
    nouvelle_image = telecharger_image(url_image)
    
    # Charger la dernière image de la liste
    if liste_images:
        image_precedente = liste_images[-1]
    else:
        image_precedente = None
    
    # Comparer les images et enregistrer la nouvelle image si elles sont différentes
    if comparer_images(image_precedente, nouvelle_image):
        chemin_enregistrement = os.path.join(dossier_enregistrement, f"image_{len(liste_images)}.jpg")
        enregistrer_image(nouvelle_image, chemin_enregistrement, liste_images)
        # Sauvegarder la liste d'images
        with open(chemin_liste_images, "wb") as fichier:
            pickle.dump(liste_images, fichier)
    else:
        print("Aucun changement de pixels détecté.")
    
    # Pause de 5 secondes avant la prochaine requête
    time.sleep(20)
