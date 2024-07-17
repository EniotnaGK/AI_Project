import streamlit as st
import pandas as pd
import os

# Titre de l'application Streamlit
st.title('Dashboard de détection IA à Lyon')

# Chargement des données depuis un fichier CSV
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Emplacement du fichier CSV (à adapter selon votre propre chemin)
file_path = 'detected_classes.csv'

# Chargement des données
data = load_data(file_path)

# Affichage des données en tant que tableau
st.subheader('Données de détection :')

# Widget de filtre par classe
selected_class = st.sidebar.selectbox('Sélectionner une classe', ['Toutes'] + list(data['class_name'].unique()))

if selected_class != 'Toutes':
    data = data[data['class_name'] == selected_class]

# Widget de recherche par ID d'image
search_query = st.sidebar.text_input('Rechercher par ID d\'image')

# Widget pour afficher ou cacher l'image
show_image = st.sidebar.checkbox('Afficher l\'image', value=True)

if search_query:
    data = data[data['id'].str.contains(search_query, case=False, na=False)]

st.write(data)

# Vérifier si l'image existe et l'afficher si la case est cochée
if search_query and show_image:
    image_path = f'predict_images/{search_query}'  # Adapter l'extension selon vos images
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Image pour ID : {search_query}")
    else:
        st.write("Image non trouvée pour cet ID.")

# Statistiques simples
st.subheader('Statistiques :')
st.write(f"Nombre total d'entrées : {len(data)}")
st.write(f"Classes uniques : {data['class_name'].nunique()}")

# Graphique de comptage par classe
st.subheader('Graphique de comptage par classe :')
count_chart = data['class_name'].value_counts().plot(kind='bar')
st.pyplot(count_chart.figure)
