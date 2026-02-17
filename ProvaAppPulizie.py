import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta

# Percorso del file CSV
DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"

    

# 🔹 Funzione per creare un CSV valido
def crea_csv_iniziale():
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["settimana", "area", "responsabile", "stato"])
        writer.writerows([
            ["2026-02-21", "Bagno picc. + polvere", "Carlottina", "Da fare"],
            ["2026-02-21", "Cucina", "Sandro", "Fatto"],
            ["2026-02-21", "Pavimenti", "Marta", "Fatto"],
            ["2026-02-21", "Bagno grande", "Daria", "Da fare"]
        ])
    #st.info("📄 File 'pulizie.csv' creato o ripristinato con dati iniziali.")

# 🔹 Se il file non esiste, crealo
if not os.path.exists(DATA_PATH):
    crea_csv_iniziale()

# 🔹 Carica i dati
try:
    df = pd.read_csv(DATA_PATH)
    # Se le colonne non sono corrette, rigenera il file
    colonne_attese = {"settimana", "area", "responsabile", "stato"}
    if not colonne_attese.issubset(df.columns):
        crea_csv_iniziale()
        df = pd.read_csv(DATA_PATH)
except Exception:
    crea_csv_iniziale()
    df = pd.read_csv(DATA_PATH)

# Configurazione pagina Streamlit
st.set_page_config(page_title="Pulizie Casa", page_icon="🧹", layout="centered")
st.title("🧹 Gestione Pulizie Casa")

# Mostra settimana corrente
settimana_corrente = df["settimana"].max()
st.subheader(f"Settimana di riferimento: {settimana_corrente}")

# Mostra tabella
for _, row in df.iterrows():
    st.markdown(f"### 🏠 {row['area']}")
    st.write(f"👤 {row['responsabile']}")
    stato = st.checkbox(
        "Segna come fatto", value=row["stato"] == "Fatto", key=row["area"]
    )
    if stato and row["stato"] != "Fatto":
        df.loc[df["area"] == row["area"], "stato"] = "Fatto"

# Salva eventuali modifiche
if st.button("💾 Salva modifiche"):
    df.to_csv(DATA_PATH, index=False)
    st.success("Stato aggiornato!")

# Funzione per ruotare i turni
def ruota_turni(df):
    responsabili = list(df["responsabile"])
    responsabili = responsabili[1:] + responsabili[:1]
    df["responsabile"] = responsabili
    df["settimana"] = (date.today() + timedelta(days=7)).isoformat()
    df["stato"] = "Da fare"
    return df

# Pulsante di rotazione
if st.button("🔁 Ruota i turni"):
    df = ruota_turni(df)
    df.to_csv(DATA_PATH, index=False)
    st.success("Turni ruotati con successo!")
