import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase con las credenciales
def init_firebase():
    try:
        cred = credentials.Certificate("formulario-211c0-firebase-adminsdk-3tiuf-1b8c819c76.json")  # Cambia a tu archivo
        firebase_admin.initialize_app(cred)
    except ValueError:
        st.warning("Firebase ya está inicializado")

# Conectar a Firestore
def get_firestore_client():
    if not firebase_admin._apps:
        init_firebase()
    return firestore.client()

# Verificar conexión con Firebase
def verificar_conexion():
    try:
        db = get_firestore_client()
        # Intentar listar colecciones como prueba
        colecciones = db.collections()
        nombres_colecciones = [col.id for col in colecciones]
        return True, nombres_colecciones
    except Exception as e:
        return False, str(e)

# Verificar conexión antes de mostrar el formulario
st.title("Formulario y Firebase")

st.subheader("Verificación de conexión con Firebase")
conexion_exitosa, resultado = verificar_conexion()

if conexion_exitosa:
    st.success("¡Conexión exitosa con Firebase!")
    st.write("Colecciones disponibles:", resultado)
else:
    st.error("Error al conectar con Firebase")
    st.write("Detalles del error:", resultado)
    st.stop()  # Detener la ejecución si no hay conexión

# Crear el formulario solo si la conexión es exitosa
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
            doc_ref = get_firestore_client().collection("formulario").add(datos)
            st.success(f"¡Datos guardados con éxito! ID del documento: {doc_ref[1].id}")
        except Exception as e:
            st.error(f"Error al guardar los datos: {e}")
    else:
        st.error("Por favor, completa todos los campos obligatorios.")
