# AI_Project

Projet de Deep Learning sur de la classification d'images à partir d'images prises par les caméras de GrandLyon.


## Introduction

Nous avons eu accès à différentes caméra du GrandLyon et avons utilisés celle du pont Clémenceau. L'objectif est de faire de la computer vision entre différentes classes d'objets comme des voitures, des piétons, des bus...


## Architecture

Grâce à un script python je récupère les images de la caméra. Chaque image est actualisée environ chaque minute. Il faut donc faire un système de check de pixels des images pour qu'à chaque requête de notre code, il vérifie si la photo qu'il voit est la même que la précédente. Et il faut aussi mettre un timer de plusieurs secondes entre chaque requête afin de ne pas surcharger le site et lui éviter de crash.

J'ai décidé d'utiliser Docker afin de containeriser mon projet. L'installation de Docker sera la prochaine étape.


# Partie Développement

## Installation

Il faut d'abord télécharger Docker Desktop sur internet. Le lien ci-dessous téléchargera directement docker desktop sur votre pc.
(https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)

Une fois installé, il faut ensuite cloner le dépôt Git.

Copiez ````git clone https://github.com/EniotnaGK/AI_Project.git````

Ouvrez ensuite un terminal de commande en tapant ````windows + r````, tapez ````cmd```` et faites ````Entrer````.

Ensuite placez-vous à la racine de votre projet en utilisant ````cd to/your/path````. Collez ````git clone https://github.com/EniotnaGK/AI_Project.git```` et faites un ````cd AI_Project````.

Une fois le dépôt installé dans votre répertoire, tapez ````code .```` pour lancer visual studio, si vous ne l'avez pas voici un lien pour le télécharger : https://code.visualstudio.com/download .


## Utilisation

### Récupération d'images depuis la caméra


Ouvrez un terminal dans visual studio et faites ````cd Recup_images ````.

Ensuite entrez: 
```python
docker build -t recup_images_cam .
```

Cela va créer notre image Docker afin de récupérer les images de la caméra et va en même temps installer les dépendances du fichier "requirements.txt" pour éxécuter ce code.

Il faut ensuite lancer le container en faisant :
```dockerfile 
docker run -v data:/app/Recup_images/Images_Lyon -it recup_images_cam
```
Ce qui va lancer le ````recup_images_cam.py```` et cela va donc récupérer les photos de la caméra sur votre docker et les enregistrer en local à l'emplacement que vous choisirez, les requêtes sont envoyées toutes les 20 secondes.

### Exportation des fichiers au format Yolo :


Il faut se rendre sur Label studio [depuis ce lien](https://app.heartex.com/projects/67163/data?tab=88181), cliquer sur "Exporter" et puis choisir de télécharger le snapshot le plus récent et choisir le format yolo.

Une fois téléchargé, vous déziperez le dossier et le renommerez "yolo".

Vous le placerez dans votre dossier "Récup_images_labellisées".


### Récupération des images labellisées 


Il faut maintenant changer de répertoire et se mettre dans celui de la récupération d'images labellisées plutôt que celui de la récup des images de la cam.

Allez dans votre terminal et faites donc d'abord ````cd ..```` puis ````cd Recup_images_labellisées````.

Nous allons créer la 2e image avec : 
```dockerfile
docker build -t images_label_dl .
```
Et puis lancer le container avec : 
```dockerfile 
docker run -it images_label_dl
```

Il téléchargera les images labellisées en format JPEG sur votre docker.

Comme pour la 1ère fois, afin d'enregistrer les images sur votre ordinateur il vous faudra taper la commande :
```dockerfile
docker run data:/app/Recup_images_labellisées/yolo/images
```
Après cela, les images contenues dans votre docker seront copiées puis collées dans le répertoire de votre choix.


# Partie Production


## Récupération d'images

Comme effectué ci dessus nous allons lancer notre script python pour récupérer les images depuis l'API. Ce script va tourner et actualiser les requêtes toutes les 20 secondes et va ensuite enregistrer les images en local au fur et à mesure.

Pour ce faire nous allons lancer la commande :
```dockerfile
docker build -t recup_images_cam .
``` 
Puis :
```dockerfile
docker run -v data:/app/Recup_images/Images_Lyon -it recup_images_cam
```
Pour créer puis lancer le container respectivement.

## Object Detector

Nous avons ensuite le script python ````main.py```` qui lui va lire les images du dossier, effectuer un mask de prétraitement afin de cacher la partie au fond de l'image pour ne pas fausser nos résultats.

Il va ensuite charger le modèle préentrainé choisi (Yolov8m dans notre cas) ainsi que les poids de notre entrainement. Il va faire une prédiction de nos images, il va estimer nos différents objets grâce à des bounding box et va nous afficher le pourcentage de prédiction.

Il va ensuite enregistrer les images en local ainsi que sur un csv qui nous servira à alimenter notre dashboard.

Pour ce faire nous devons créer et exécuter le dockerfile :

```dockerfile
docker build -t main -f Dockerfile_main .
```

```dockerfile
docker run -v C:\Users\antoi\Documents\AI_Project\Docker:/app/detected_classes -it main
```

## Dashboard Analysis

A l'aide de la librairie streamlit nous allons créer des graphiques pour afficher nos données.

Lancer la commande :
```dockerfile
docker build -t dashboard -f Dockerfile_dashboard .
```
Puis :
```dockerfile
docker run -it dashboard
```
Afin de créer et lancer le docker contenant notre dashboard.

Vous pouvez naviguer et tester les différents filtres et analyser les données des images.
