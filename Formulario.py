import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo si no está ya inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets["universe_domain"]
    })
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

try:
    doc_ref = db.collection("test").document("test_doc")
    doc_ref.set({"status": "connected"})
    st.success("Conexión exitosa a Firestore")
except Exception as e:
    st.error(f"Error al conectar con Firestore: {e}")
