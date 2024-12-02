import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase con las credenciales
def init_firebase():
    try:
        cred = credentials.Certificate("ruta_al_archivo_credencial.json")  # Cambia a tu archivo
        firebase_admin.initialize_app(cred)
    except ValueError:
        st.warning("Firebase ya está inicializado")

# Conectar a Firestore
def get_firestore_client():
    if not firebase_admin._apps:
        init_firebase()
    return firestore.client()

# Guardar datos en Firebase
def guardar_en_firestore(data):
    db = get_firestore_client()
    doc_ref = db.collection("formulario").add(data)
    return doc_ref

# Interfaz del formulario
st.title("Formulario y Firebase")

# Crear el formulario
with st.form("mi_formulario"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
    mensaje = st.text_area("Mensaje")
    enviado = st.form_submit_button("Enviar")

# Procesar el formulario al enviar
if enviado:
    if nombre and correo and edad:
        datos = {
            "nombre": nombre,
            "correo": correo,
            "edad": edad,
            "mensaje": mensaje,
        }
        try:
            doc_ref = guardar_en_firestore(datos)
            st.success(f"¡Datos guardados con éxito! ID del documento: {doc_ref[1].id}")
        except Exception as e:
            st.error(f"Error al guardar los datos: {e}")
    else:
        st.error("Por favor, completa todos los campos obligatorios.")
