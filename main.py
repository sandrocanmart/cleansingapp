import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta
from utilities import *


# Percorso del file CSV
DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"
COLONNE_ATTESE = ["settimana", "area", "responsabile", "stato"]





# ==========================
# BOOTSTRAP DATI
# ==========================
if not os.path.exists(DATA_PATH):
    crea_csv_vuoto()

try:
    df = leggi_csv()
except Exception:
    crea_csv_vuoto()
    df = leggi_csv()

# Auto-rotazione: se manca la settimana corrente, la crea e salva
df = auto_ruota_e_scrivi_settimana_corrente(df)


# ==========================
# UI / GRAFICA STREAMLIT
# ==========================
st.caption("DEPLOY MARK: 2026-02-24")
st.set_page_config(page_title="Casa Lanfranchi", page_icon="🧹", layout="centered")
st.title("🧹 Gestione Pulizie Casa Lanfranchi")

oggi = date.today()
lunedi_corrente = lunedi_settimana_corrente(oggi)
domenica_corrente = lunedi_corrente + timedelta(days=6)

st.subheader(f"Settimana corrente: {lunedi_corrente.isoformat()} → {domenica_corrente.isoformat()}")

# Filtra SOLO settimana corrente
df_settimana = df[df["settimana"] == lunedi_corrente].copy()

if df_settimana.empty:
    st.info("Nessuna pulizia pianificata per la settimana corrente nel CSV.")
else:
    for idx, row in df_settimana.iterrows():
        st.markdown(f"### 🏠 {row['area']}")
        st.write(f"👤 {row['responsabile']}")

        checkbox_key = f"done_{idx}_{row['area']}_{row['responsabile']}"

        fatto = st.checkbox(
            "Segna come fatto",
            value=(str(row["stato"]).strip().lower() == "fatto"),
            key=checkbox_key
        )

        # Aggiorna il DF principale usando l'indice originale
        if fatto:
            df.at[idx, "stato"] = "Fatto"
        else:
            if str(df.at[idx, "stato"]).strip().lower() == "fatto":
                df.at[idx, "stato"] = "Da fare"

# Salva eventuali modifiche
if st.button("💾 Salva modifiche"):
    salva_csv(df)
    st.success("Stato aggiornato!")



# st.write("DATA_PATH:", DATA_PATH)
# st.write("Exists:", os.path.exists(DATA_PATH))

# st.write("Oggi:", date.today())
# lun_corr = lunedi_settimana_corrente(date.today())
# st.write("Lunedì corrente:", lun_corr)

# st.write("DF shape:", df.shape)
# st.write("DF head:", df.head())

# st.write("Settimane uniche (prime 30):", sorted(df["settimana"].dropna().unique())[:30])
# st.write("Match lunedì corrente?:", (df["settimana"] == lun_corr).any())
# st.write("NaN settimane:", df["settimana"].isna().sum())
