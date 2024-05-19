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
