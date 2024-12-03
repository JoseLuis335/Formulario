import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo si no está ya inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\n", " "),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
    })
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Probar la conexión
try:
    doc_ref = db.collection("id").document("Tienda")
    doc_ref.set({"status": "connected"})
    print("Conexión exitosa a Firestore")
except Exception as e:
    print(f"Error al conectar con Firestore: {e}")
