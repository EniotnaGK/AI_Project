# AI_Project

Projet de Deep Learning sur de la classification d'images à partir d'images prises par les caméras de GrandLyon.


## Introduction

Nous avons eu accès à différentes caméra du GrandLyon et avons utilisés celle du pont Clémenceau. L'objectif est de faire de la computer vision entre différentes classes d'objets comme des voitures, des piétons, des bus...


## Architecture

Grâce à un script python je récupère les images de la caméra. Chaque image est actualisée environ chaque minute. Il faut donc faire un système de check de pixels des images pour qu'à chaque requête de notre code, il vérifie si la photo qu'il voit est la même que la précédente. Et il faut aussi mettre un timer de plusieurs secondes entre chaque requête afin de ne pas surcharger le site et lui éviter de crash.

J'ai décidé d'utiliser Docker afin de containeriser mon projet. L'installation de Docker sera la prochaine étape.


## Installation

Il faut d'abord télécharger Docker Desktop sur internet. Le lien ci-dessous téléchargera directement docker desktop sur votre pc.
(https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)

Installez le.

Une fois terminé, l'environnement est prêt à être utilisé.


Il faut ensuite cloner le dépôt Git.
Rendez-vous sur (https://github.com/EniotnaGK/AI_Project)


Ouvrez donc un terminal de commande en tapant ````windows + r````, tapez ````cmd```` et faites ````entrer````.


Ensuite placez




