import streamlit as st
import requests
import datetime
import base64

# Ajouter du CSS pour l'image de fond

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('background.jpg')

# Titre de l'application
st.title('Prix de votre course (en vrai ça sera plus cher)')

# Entrées de l'utilisateur
pickup_date = st.date_input('Date de prise en charge')
pickup_time = st.time_input('Heure de prise en charge')
pickup_address = st.text_input('Adresse de prise en charge')
dropoff_address = st.text_input('Adresse de dépose')
passenger_count = st.number_input('Nombre de passagers', min_value=1, step=1)

# Convertir les adresses en coordonnées géographiques (latitude et longitude)
def geocode_address(address):
    # Utilisez une API de géocodage pour convertir l'adresse en coordonnées géographiques
    # Ici, nous supposons que vous utilisez Google Maps Geocoding API
    # Remplacez 'YOUR_API_KEY' par votre propre clé API
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=YOUR_API_KEY'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        return None

# Fonction pour appeler l'API de prédiction de prix de course
def predict_fare(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude, passenger_count):
    url = 'https://taxifare.lewagon.ai/predict'
    params = {
        'pickup_latitude': pickup_latitude,
        'pickup_longitude': pickup_longitude,
        'dropoff_latitude': dropoff_latitude,
        'dropoff_longitude': dropoff_longitude,
        'passenger_count': passenger_count
    }
    response = requests.get(url, params=params)
    return response.json()

# Ajouter un bouton de soumission
if st.button('Prix'):
    # Convertir les adresses en coordonnées géographiques
    pickup_latlng = geocode_address(pickup_address)
    dropoff_latlng = geocode_address(dropoff_address)

    # Vérifier si les coordonnées ont été obtenues avec succès
    if pickup_latlng and dropoff_latlng:
        pickup_latitude, pickup_longitude = pickup_latlng
        dropoff_latitude, dropoff_longitude = dropoff_latlng

        # Appeler l'API de prédiction de prix de course
        result = predict_fare(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude, passenger_count)

        # Afficher le résultat
        if 'fare' in result:
            st.write(f'Le prix estimé de la course est : ${result["fare"]:.2f}')
        else:
            st.write('Erreur dans la prédiction du prix de la course')
    else:
        st.write('Adresse invalide. Veuillez vérifier et réessayer.')
