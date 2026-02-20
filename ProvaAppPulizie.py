import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta

# Percorso del file CSV
DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"

COLONNE_ATTESE = ["settimana", "area", "responsabile", "stato"]

def lunedi_settimana_corrente(d: date) -> date:
    # weekday(): lun=0 ... dom=6
    return d - timedelta(days=d.weekday())

def crea_csv_vuoto():
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLONNE_ATTESE)

def leggi_csv():
    df = pd.read_csv(DATA_PATH)

    if not set(COLONNE_ATTESE).issubset(df.columns):
        raise ValueError(
            f"CSV non valido. Colonne trovate: {list(df.columns)}. "
            f"Attese: {COLONNE_ATTESE}"
        )

    # Pulizia base
    df["area"] = df["area"].astype(str).str.strip()
    df["responsabile"] = df["responsabile"].astype(str).str.strip()
    df["stato"] = df["stato"].astype(str).str.strip()

    # parse settimana (accetta tipo "2026-02-16")
    df["settimana"] = pd.to_datetime(df["settimana"], errors="coerce").dt.date

    return df

# Se il file non esiste, crealo (vuoto)
if not os.path.exists(DATA_PATH):
    crea_csv_vuoto()

# Carica dati
try:
    df = leggi_csv()
except Exception:
    crea_csv_vuoto()
    df = leggi_csv()

# Configurazione pagina Streamlit
st.set_page_config(page_title="Pulizie Casa", page_icon="🧹", layout="centered")
st.title("🧹 Gestione Pulizie Casa")

# --- FILTRO SETTIMANA CORRENTE (lun-dom) ---
oggi = date.today()
lunedi_corrente = lunedi_settimana_corrente(oggi)
domenica_corrente = lunedi_corrente + timedelta(days=6)

st.subheader(f"Settimana corrente: {lunedi_corrente.isoformat()} → {domenica_corrente.isoformat()}")

# Filtra solo la settimana corrente
df_settimana = df[df["settimana"] == lunedi_corrente].copy()

if df_settimana.empty:
    st.info("Nessuna pulizia pianificata per la settimana corrente nel CSV.")
else:
    # Mostra solo le pulizie della settimana corrente
    for idx, row in df_settimana.iterrows():
        st.markdown(f"### 🏠 {row['area']}")
        st.write(f"👤 {row['responsabile']}")

        checkbox_key = f"done_{idx}_{row['area']}_{row['responsabile']}"
        fatto = st.checkbox(
            "Segna come fatto",
            value=(str(row["stato"]).strip().lower() == "fatto"),
            key=checkbox_key
        )

        # Aggiorna DF originale (df) usando l'indice reale
        if fatto:
            df.at[idx, "stato"] = "Fatto"
        else:
            if str(df.at[idx, "stato"]).strip().lower() == "fatto":
                df.at[idx, "stato"] = "Da fare"

# Salva eventuali modifiche
if st.button("💾 Salva modifiche"):
    df_to_save = df.copy()
    df_to_save["settimana"] = df_to_save["settimana"].astype(str)  # date -> "YYYY-MM-DD"
    df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")
    st.success("Stato aggiornato!")

# Funzione per ruotare i turni (opzionale)
def ruota_turni(df):
    responsabili = list(df["responsabile"])
    responsabili = responsabili[1:] + responsabili[:1]
    df["responsabile"] = responsabili

    # setta la prossima settimana (lunedì della settimana prossima)
    prossima_settimana_lun = lunedi_settimana_corrente(date.today() + timedelta(days=7))
    df["settimana"] = prossima_settimana_lun

    df["stato"] = "Da fare"
    return df

# Pulsante di rotazione (se vuoi riattivarlo)
# if st.button("🔁 Ruota i turni"):
#     df = ruota_turni(df)
#     df_to_save = df.copy()
#     df_to_save["settimana"] = df_to_save["settimana"].astype(str)
#     df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")
#     st.success("Turni ruotati con successo!")