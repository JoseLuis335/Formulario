import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore

import firebase_admin
from firebase_admin import credentials, firestore

# Obtener las credenciales desde los secretos de Streamlit
firebase_config = st.secrets["firebase"]

# Convertir la clave privada (en formato de string multilínea) a un formato compatible
private_key = firebase_config["private_key"].replace("\n", "\\n")

# Crear el objeto de credenciales a partir del diccionario
cred = credentials.Certificate({
    "type": firebase_config["type"],
    "project_id": firebase_config["project_id"],
    "private_key_id": firebase_config["private_key_id"],
    "private_key": private_key,
    "client_email": firebase_config["client_email"],
    "client_id": firebase_config["client_id"],
    "auth_uri": firebase_config["auth_uri"],
    "token_uri": firebase_config["token_uri"],
    "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_config["client_x509_cert_url"],
    "universe_domain": firebase_config["universe_domain"]
})

# Inicializar Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Intentar acceder a una colección
try:
    docs = db.collection("id").stream()  # Cambia "test" por el nombre de una colección existente
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
    print("¡Conexión exitosa a Firestore!")
except Exception as e:
    print(f"Error al conectar a Firestore: {e}")
