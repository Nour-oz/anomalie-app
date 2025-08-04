import streamlit as st
import pandas as pd
# from app.anomalies_logic.suivi_encours import detect_anomalies_suivi_encours
from anomalies_logic.suivi_encours import detect_anomalies_suivi_encours

st.title("Détection d'anomalies dans les fichiers Excel")

type_analyse = st.selectbox("Choisissez un type d’analyse :", ["Sélectionnez", "Suivi des encours"])
uploaded_file = st.file_uploader("Déposez votre fichier Excel ici", type=["xlsx", "xls"])

if uploaded_file and type_analyse == "Suivi des encours":
    try:
        df = pd.read_excel(uploaded_file, sheet_name="DATA BASE", header=1)

        st.subheader("Aperçu du fichier importé")
        st.write(df.head())

        anomalies = detect_anomalies_suivi_encours(df)

        st.subheader("📌 Anomalies détectées : Suivi des encours")
        if not anomalies.empty:
            st.write(f"Nombre total : {len(anomalies)}")
            st.dataframe(anomalies)
        else:
            st.success("✅ Aucune anomalie détectée.")

    except Exception as e:
        st.error(f"Erreur lors de la lecture ou de l'analyse : {e}")
else:
    st.info("Veuillez choisir un type et importer un fichier.")
