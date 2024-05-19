# Utilise l'image de base Python 3.9
FROM python:3.

# Définit le répertoire de travail dans le conteneur
WORKDIR /app/Recup_images_labellisées

# Copie le fichier Python et les dépendances
COPY . /app/Recup_images_labellisées/

RUN pip install --no-cache-dir -r requirements.txt

# Exécute le script Python lorsque le conteneur démarre
CMD ["python", "Images_label_dl.py"]
