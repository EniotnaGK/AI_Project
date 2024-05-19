# Objectifs du projet

Grâce à des caméras installées dans le GrandLyon, nous avons visuellement accès à certains endroits de la ville, le but étant de récupérer leur flux vidéo à plusieurs moments de la journée et sous différentes météos afin de créer un dataset varier pour l'entraîner à détecter et à différencier des objets comme des voitures, des camions, des scooters ou même des personnes.

# Dépôt Git

- Un dossier ````Recup_images```` qui contient :
  - L'image ````Dockerfile````
    
  - Le script ````Recup_images_cam.py```` pour récupérer le flux de la caméra et enregistrer les images
    
  - Le fichier ````requirements.txt```` pour installer les dépendances
    
 
- Un dossier ````Recup_images_labellisées```` qui contient :
  
  - L'image ````Dockerfile````
    
  - Le script ````Images_label_dl.py```` pour télécharger les fichiers Yolo exportés du site ````Label Studio````
    
  - Le fichier ````requirements.txt```` pour installer les dépedances
 
- Un ````README.md```` pour expliquer comment installer le projet

- Un ````CONTRIBUTING.md```` pour expliquer comment reprendre le projet ainsi que les aspects techniques.



# Labellisation

Nous avons labellisés des images sur Label Studio. Nous avons d'abord capturés ces images via nos codes respectifs, puis nous les avons importés puis labéllisées et enfin nous les avons exportés via différents formats (JSON, coco, Yolo...) pour ma part j'ai choisi Yolo.

Vous pouvez accéder à notre projet via [ le site ](https://app.heartex.com/projects/67163) .


# Détails code

#### Nous allons commencer par le dossier ````Recup_images```` :

## Le Dockerfile :

``` Dockerfile
# Utilise l'image de base Python 3.9
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
WORKDIR /app/Recup_images

# Copie le fichier Python et les dépendances
COPY . /app/Recup_images/

# Installe les dépendances Python spécifiées dans le fichier requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exécute le script Python lorsque le conteneur démarre
CMD ["python", "Recup_images_cam.py"]
```


## Recup_images_cam.py

### Les imports des packages python :
``` python
import requests
import numpy as np
from io import BytesIO
from PIL import Image
import os
import time
import datetime
import imagehash
```

### La fonction pour télécharger l'image depuis l'URL de la caméra
``` python
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
```

### La fonction pour comparer les images par hash
``` python
def comparer_images_par_hash(image1, image2):
    if image1 is None or image2 is None:
        return True
    # Calculer le hachage d'image pour chaque image
    hash_image1 = imagehash.average_hash(image1)
    hash_image2 = imagehash.average_hash(image2)

    return hash_image1 - hash_image2 > 2
```

### La fonction pour enregistrer l'image
``` python
def enregistrer_image(image, chemin_enregistrement):
    # Obtenir la date et l'heure actuelles
    filename = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg' 
    
    # Concaténer le nom du fichier avec la date et l'heure actuelles et l'extension
    chemin_enregistrement_date = os.path.join(chemin_enregistrement, filename)
    
    # Enregistrer l'image sur le disque avec le nom incluant la date et l'heure actuelles
    image.save(chemin_enregistrement_date)
    print("Nouvelle image enregistrée avec la date et l'heure d'aujourd'hui.")
    return filename
```

### La dernière partie du code est là où l'on va par exemple renseigner l'URL où l'on va télécharger la nouvelle image ainsi que là où l'on va créer le répertoire où enregistrer les images s'il n'est pas déjà crée, appeler la fonction pour comparer les images ou encore régler le temps entre chaque requête.
``` python
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
```


## Requirements.txt
``` txt
numpy==1.26.4
opencv-contrib-python==4.9.0.80
requests==2.27.1
pillow==10.3.0
TIME-python==0.0.17
imagehash==4.3.1
```


#### Nous allons continuer avec le 2e dossier ````Recup_images_labellisées```` :

## Le Dockerfile :
``` Dockerfile
# Utilise l'image de base Python 3.9
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
WORKDIR /app/Recup_images_labellisées

# Copie le fichier Python et les dépendances
COPY . /app/Recup_images_labellisées/

RUN pip install --no-cache-dir -r requirements.txt

# Exécute le script Python lorsque le conteneur démarre
CMD ["python", "Images_label_dl.py"]
```


## Images_label_dl.py :

### Les imports des packages python :
```python
import os
import time
import requests
```


### La fonction pour télécharger les images exportées depuis Label Studio
```python
# Fonction pour télécharger les images en fonction des fichiers d'annotations YOLO
def recup_yolo_images():
    # Répertoire contenant le fichier d'annotations
    labels_directory = os.path.abspath("labels")

    # Répertoire où enregistrer les images       
    images_directory = "Images"

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
```


## Requirements.txt
``` txt
requests==2.27.1
```


