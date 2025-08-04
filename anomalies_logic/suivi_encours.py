import pandas as pd
import streamlit as st

def detect_anomalies_suivi_encours(df):
    anomalies = []

    # === Convertir les colonnes de dates ===
    date_cols = [
        "date_envoi_po",
        "date_reception_po",
        "date_swift",
        "date_demande_deposit",
        "dernière_date_validation_échantillon",
        "dernière_date_réception_échantillon",
        "dernière_date_envoi_d_échantillon",
        "dernière_etd",
        "dernière_eta",
        "date_première_validation_cq",
        "dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)",
        "date_balance",
        "date_facture",
        "date_de_livraison"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # === Règles de détection ===
    if "date_envoi_po" in df.columns and "date_reception_po" in df.columns:
        anomalies_po = df[df["date_envoi_po"] > df["date_reception_po"]].copy()
        anomalies_po["type_anomalie"] = "❌ Date envoi PO après réception PO"
        anomalies.append(anomalies_po)

    if "date_swift" in df.columns and "date_demande_deposit" in df.columns:
        anomalies_swift = df[df["date_swift"] < df["date_demande_deposit"]].copy()
        anomalies_swift["type_anomalie"] = "❌ SWIFT avant demande de dépôt"
        anomalies.append(anomalies_swift)

    if "dernière_date_validation_échantillon" in df.columns and "dernière_date_réception_échantillon" in df.columns:
        anomalies_valid_ech = df[
            df["dernière_date_validation_échantillon"] < df["dernière_date_réception_échantillon"]
        ].copy()
        anomalies_valid_ech["type_anomalie"] = "❌ Validation échantillon avant réception"
        anomalies.append(anomalies_valid_ech)

    if "dernière_date_envoi_d_échantillon" in df.columns and "dernière_date_réception_échantillon" in df.columns:
        anomalies_envoi = df[
            df["dernière_date_envoi_d_échantillon"] > df["dernière_date_réception_échantillon"]
        ].copy()
        anomalies_envoi["type_anomalie"] = "❌ Envoi échantillon après réception"
        anomalies.append(anomalies_envoi)

    if "dernière_etd" in df.columns and "dernière_eta" in df.columns:
        anomalies_etd_eta = df[df["dernière_etd"] > df["dernière_eta"]].copy()
        anomalies_etd_eta["type_anomalie"] = "❌ ETD après ETA"
        anomalies.append(anomalies_etd_eta)

    if "date_première_validation_cq" in df.columns and "dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)" in df.columns:
        anomalies_val_cq = df[
            df["date_première_validation_cq"] < df["dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)"]
        ].copy()
