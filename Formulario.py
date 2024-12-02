import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("formulario-211c0-firebase-adminsdk-3tiuf-1b8c819c76.json")
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
