import streamlit as st
import pandas as pd

# === Choix du type d'analyse
st.title("Détection d'anomalies dans les fichiers Excel")
type_analyse = st.selectbox("Choisissez un type d’analyse :", ["Sélectionnez", "Suivi des encours", "Effectif RH", "Commandes", "Autre"])

# === Upload de fichier
uploaded_file = st.file_uploader("Déposez votre fichier Excel ici", type=["xlsx", "xls"])

if uploaded_file and type_analyse != "Sélectionnez":
    try:
        df = pd.read_excel(uploaded_file)

        # Affichage de l'en-tête pour vérification
        st.subheader("Aperçu du fichier")
        st.write(df.head())

        # Logique différente selon le type choisi
        if type_analyse == "Suivi des encours":
            st.subheader("Anomalies - Suivi des encours")
            # === EXEMPLE 1 : date_reception < date_envoi
            if "date_envoi_po" in df.columns and "date_reception_po" in df.columns:
                mask = df["date_reception_po"] < df["date_envoi_po"]
                anomalies = df[mask]
                st.write(f"📌 {len(anomalies)} anomalies trouvées (Réception avant envoi) :")
                st.dataframe(anomalies)
            else:
                st.warning("❗ Les colonnes 'date_envoi_po' et 'date_reception_po' sont absentes du fichier.")

        elif type_analyse == "Effectif RH":
            st.subheader("Anomalies - Effectif RH")
            # Ajoute ici ta logique RH

        elif type_analyse == "Commandes":
            st.subheader("Anomalies - Commandes")
            # Ajoute ici ta logique Commandes

        else:
            st.info("Aucune règle définie pour ce type d’analyse.")
    
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

else:
    st.info("Veuillez choisir un type d’analyse et importer un fichier Excel.")
