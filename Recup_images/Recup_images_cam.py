import requests
import numpy as np
from io import BytesIO
from PIL import Image
import os
import time
import datetime
import imagehash

def telecharger_image(url="https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG"):
    # Télécharger l'image à partir de l'URL
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Ouvrir l'image à partir du contenu binaire
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Erreur lors de la requête pour télécharger l'image.")
        return None

def comparer_images_par_hash(image1, image2):
    if image1 is None or image2 is None:
        return True
    # Calculer le hachage d'image pour chaque image
    hash_image1 = imagehash.average_hash(image1)
    hash_image2 = imagehash.average_hash(image2)

    return hash_image1 - hash_image2 > 2

def enregistrer_image(image, chemin_enregistrement):
    # Obtenir la date et l'heure actuelles
    filename = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg' 
    
    # Concaténer le nom du fichier avec la date et l'heure actuelles et l'extension
    chemin_enregistrement_date = os.path.join(chemin_enregistrement, filename)
    
    # Enregistrer l'image sur le disque avec le nom incluant la date et l'heure actuelles
    image.save(chemin_enregistrement_date)
    print("Nouvelle image enregistrée avec la date et l'heure d'aujourd'hui.")
    return filename

# URL de l'image à surveiller
url_image = "https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/CWL9018.JPG"

# Chemin où enregistrer les images
dossier_enregistrement = "Images_Lyon"
if not os.path.exists(dossier_enregistrement):
    os.makedirs(dossier_enregistrement)

# Vérifier si une liste d'images existe déjà
liste_images = os.listdir(dossier_enregistrement)


while True:
    # Télécharger la nouvelle image
    nouvelle_image = telecharger_image(url_image)
    
    # Charger la dernière image de la liste
    if liste_images:
        image_precedente = Image.open(os.path.join(dossier_enregistrement, liste_images[-1]))
    else:
        image_precedente = None
    
    # Comparer les images et enregistrer la nouvelle image si elles sont différentes
    if comparer_images_par_hash(image_precedente, nouvelle_image):
        filename = enregistrer_image(nouvelle_image, dossier_enregistrement)
        # Sauvegarder la liste d'images
        liste_images.append(filename)
    else:
        print("Aucun changement de pixels détecté.")
    
    # Pause de 20 secondes avant la prochaine requête
    time.sleep(20)
