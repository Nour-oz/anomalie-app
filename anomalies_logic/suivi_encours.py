import pandas as pd

def detect_anomalies_suivi_encours(df):
    anomalies = []

    # Nettoyer les noms de colonnes
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("’", "_")
        .str.replace("'", "_")
    )

    # Convertir les colonnes de dates
    date_cols = [
        "date_envoi_po", "date_reception_po", "date_swift", "date_demande_deposit",
        "dernière_date_validation_échantillon", "dernière_date_réception_échantillon",
        "dernière_date_envoi_d_échantillon", "dernière_etd", "dernière_eta",
        "date_première_validation_cq", "dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)",
        "date_balance", "date_facture", "date_de_livraison"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Règles d'anomalies
    if "date_envoi_po" in df.columns and "date_reception_po" in df.columns:
        mask = df["date_envoi_po"] > df["date_reception_po"]
        temp = df[mask].copy()
        temp["type_anomalie"] = "❌ Date envoi PO après réception"
        anomalies.append(temp)

    if "date_swift" in df.columns and "date_demande_deposit" in df.columns:
        mask = df["date_swift"] < df["date_demande_deposit"]
        temp = df[mask].copy()
        temp["type_anomalie"] = "❌ SWIFT avant demande de dépôt"
        anomalies.append(temp)

    # 4. Validation échantillon avant réception
    if "dernière_date_validation_échantillon" in df.columns and "dernière_date_réception_échantillon" in df.columns:
        anomalies_valid_ech = df[
            (df["dernière_date_validation_échantillon"] < df["dernière_date_réception_échantillon"])
        ].copy()
        anomalies_valid_ech["type_anomalie"] = "❌ Validation échantillon avant réception"
        anomalies.append(anomalies_valid_ech)

    # 5. Envoi échantillon après réception
    if "dernière_date_envoi_d_échantillon" in df.columns and "dernière_date_réception_échantillon" in df.columns:
        anomalies_envoi_ech = df[
            (df["dernière_date_envoi_d_échantillon"] > df["dernière_date_réception_échantillon"])
        ].copy()
        anomalies_envoi_ech["type_anomalie"] = "❌ Envoi échantillon après réception"
        anomalies.append(anomalies_envoi_ech)

    # 6. ETD après ETA
    if "dernière_etd" in df.columns and "dernière_eta" in df.columns:
        anomalies_etd_eta = df[
            (df["dernière_etd"] > df["dernière_eta"])
        ].copy()
        anomalies_etd_eta["type_anomalie"] = "❌ ETD après ETA"
        anomalies.append(anomalies_etd_eta)

    # 7. Validation CQ avant Demande Inspecteur
    if "date_première_validation_cq" in df.columns and "dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)" in df.columns:
        anomalies_val_cq = df[
            (df["date_première_validation_cq"] < df["dernière_date_prévue_cq_(_dernier__date_inspection__réelle__)"])
        ].copy()
        anomalies_val_cq["type_anomalie"] = "❌ Validation CQ avant dernière_date_prévue_cq_(_dernier__date_inspection__réelle)"
        anomalies.append(anomalies_val_cq)

    # 8. Balance avant Facture
    if "date_balance" in df.columns and "date_facture" in df.columns:
        anomalies_balance_facture = df[
            (df["date_balance"] < df["date_facture"])
        ].copy()
        anomalies_balance_facture["type_anomalie"] = "❌ Balance avant Facture"
        anomalies.append(anomalies_balance_facture)

    # 9. Livraison avant ETA
    if "date_de_livraison" in df.columns and "dernière_eta" in df.columns:
        anomalies_liv_eta = df[
            (df["date_de_livraison"] < df["dernière_eta"])
        ].copy()
        anomalies_liv_eta["type_anomalie"] = "❌ Livraison avant ETA"
        anomalies.append(anomalies_liv_eta)

    if anomalies:
        return pd.concat(anomalies, ignore_index=True)
    else:
        return pd.DataFrame()
