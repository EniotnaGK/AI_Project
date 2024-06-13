import os
import time
import requests

# Fonction pour télécharger les images en fonction des fichiers d'annotations YOLO
def recup_yolo_images():
    # Répertoire contenant le fichier d'annotations
    labels_directory = os.path.abspath("yolo/labels")

    # Répertoire où enregistrer les images       
    images_directory = "yolo/images"

    # URL de base pour télécharger les images
    base_url = "https://app.heartex.com/storage-data/uploaded/?filepath=upload/67163/"

    # Vérifie si le répertoire existe, sinon le crée
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)

    # Jeton d'authentification
    token = "f1b585c268f2fbe6fda53d28628884469cc8bc64"

    headers = {
        "Authorization": f"Token {token}"
    }

    print(f"Searching for label files in: {labels_directory}")

    # Parcours les fichiers d'annotations pour télécharger les images correspondantes
    for label_file in os.listdir(labels_directory):
        if label_file.endswith(".txt"):
            time.sleep(5)
            
            # Construit l'URL de l'image à partir du nom du fichier d'annotation
            label_file_name = os.path.splitext(label_file)[0]
            image_url = f"{base_url}{label_file_name}.jpg"

            response = requests.get(image_url, headers=headers)

            if response.status_code == 200:
                # Enregistre l'image dans le répertoire images
                image_path = os.path.join(images_directory, f"{label_file_name}.jpg")
                with open(image_path, 'wb') as image_file:
                    image_file.write(response.content)
                print(f"Image téléchargée : {label_file_name}.jpg")
            else:
                print(f"Erreur lors du téléchargement de l'image : {label_file_name}.jpg")

# Appelle la fonction pour télécharger les images
recup_yolo_images()
