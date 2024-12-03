import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.write(st.secrets["firebase"])
