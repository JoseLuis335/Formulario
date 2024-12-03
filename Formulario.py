import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Inicializar Firebase solo si no está ya inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
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

# Leer las opciones desde el archivo DOMICILIOS.xlsx
try:
    domicilios_df = pd.read_excel("DOMICILIOS.xlsx")
    tiendas = domicilios_df["Tienda"].unique().tolist()
    domicilio = domicilios_df["Domicilio"].unique().tolist()
    municipios = domicilios_df["Municipio"].unique().tolist()
    estados = domicilios_df["Estado"].unique().tolist()
except Exception as e:
    st.error(f"Error al leer el archivo DOMICILIOS.xlsx: {e}")
    tiendas,domicilio , municipios, estados = [], [], [], []

# Título de la app
st.title("Registro de Domicilios")

# Formulario para registrar un domicilio
with st.form("registro_domicilio"):
    st.subheader("Registrar un nuevo domicilio")

    tienda = st.selectbox("Selecciona la tienda", tiendas)
    domicilio = st.text_input("Ingresa el domicilio", domicilio)
    municipio = st.selectbox("Selecciona el municipio", municipios)
    estado = st.selectbox("Selecciona el estado", estados)
    status = st.selectbox("Selecciona el estado de la tienda", ["Abierto", "Cerrado"])

    # Botón para enviar el formulario
    submitted = st.form_submit_button("Registrar")

    if submitted:
        if tienda and domicilio and municipio and estado and status:
            try:
                # Crear un nuevo documento en Firestore
                doc_ref = db.collection("DOMICILIOS").document()
                doc_ref.set({
                    "Tienda": tienda,
                    "Domicilio": domicilio,
                    "Municipio": municipio,
                    "Estado": estado,
                    "STATUS": status,
                })
                st.success("Domicilio registrado exitosamente")
            except Exception as e:
                st.error(f"Error al registrar el domicilio: {e}")
        else:
            st.warning("Por favor, completa todos los campos antes de enviar.")

# Mostrar los domicilios registrados
st.subheader("Domicilios registrados")
try:
    domicilios_ref = db.collection("DOMICILIOS")
    docs = domicilios_ref.stream()

    data = []
    for doc in docs:
        data.append(doc.to_dict())

    if data:
        domicilios_registrados_df = pd.DataFrame(data)
        st.dataframe(domicilios_registrados_df)
    else:
        st.info("No hay domicilios registrados aún.")
except Exception as e:
    st.error(f"Error al obtener los domicilios registrados: {e}")
