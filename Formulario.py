import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase solo si no está ya inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate("formulario-211c0-firebase-adminsdk-3tiuf-1b8c819c76.json")
    firebase_admin.initialize_app(cred)

# Conectar a Firestore
db = firestore.client()

# Probar la conexión
try:
    doc_ref = db.collection("test").document("test_doc")
    doc_ref.set({"status": "connected"})
    st.success("Conexión exitosa a Firestore")
except Exception as e:
    st.error(f"Error al conectar con Firestore: {e}")
