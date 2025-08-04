import streamlit as st
import pandas as pd

st.title("Détection d'anomalies dans les fichiers Excel")

uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Aperçu du fichier :", df.head())

    # Exemple de règle : détecter les lignes avec des champs vides
    anomalies = df[df.isnull().any(axis=1)]
    st.subheader("✅ Anomalies détectées")
    st.write(anomalies)
