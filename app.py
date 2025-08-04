import streamlit as st
import pandas as pd

# === Import des fonctions d'anomalies ===
from anomalies_logic.suivi_encours import detect_anomalies_suivi_encours
# from anomalies_logic.effectif_rh import detect_anomalies_effectif_rh
# from anomalies_logic.commandes import detect_anomalies_commandes

# === Titre ===
st.title("Détection d'anomalies dans les fichiers Excel")

# === Choix du type d'analyse ===
type_analyse = st.selectbox("Choisissez un type d’analyse :", ["Sélectionnez", "Suivi des encours", "Effectif RH", "Commandes"])

# === Upload de fichier ===
uploaded_file = st.file_uploader("Déposez votre fichier Excel ici", type=["xlsx", "xls"])

# === Traitement ===
if uploaded_file and type_analyse != "Sélectionnez":
    try:
        df = pd.read_excel(uploaded_file, header=1)

        # === Aperçu du fichier ===
        st.subheader("Aperçu du fichier importé")
        st.dataframe(df.head())

        # === Détection des anomalies selon le type choisi ===
        if type_analyse == "Suivi des encours":
            st.subheader("Anomalies détectées : Suivi des encours")
            detect_anomalies_suivi_encours(df)

        # elif type_analyse == "Effectif RH":
        #     st.subheader("Anomalies détectées : Effectif RH")
        #     detect_anomalies_effectif_rh(df)

        # elif type_analyse == "Commandes":
        #     st.subheader("Anomalies détectées : Commandes")
        #     detect_anomalies_commandes(df)

    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du fichier : {e}")

else:
    st.info("📎 Veuillez choisir un type d’analyse et importer un fichier Excel.")
