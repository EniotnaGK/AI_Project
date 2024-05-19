# Objectifs du projet :

Grâce à des caméras installées dans le GrandLyon, nous avons visuellement accès à certains endroits de la ville, le but étant de récupérer leur flux vidéo à plusieurs moments de la journée et sous différentes météos afin de créer un dataset varier pour l'entraîner à détecter et à différencier des objets comme des voitures, des camions, des scooters ou même des personnes.

## Dépôt Git :

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
