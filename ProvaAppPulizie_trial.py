import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta

# Percorso del file CSV
DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"

COLONNE_ATTESE = ["settimana", "area", "responsabile", "stato"]


# -------------------------------------------------------------------
# 1) Crea CSV SOLO se manca (header + zero righe) - niente dati fake
# -------------------------------------------------------------------
def crea_csv_vuoto():
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLONNE_ATTESE)


# -------------------------------------------------------------------
# 2) Leggi CSV in modo robusto + pulizia base
# -------------------------------------------------------------------
def leggi_csv():
    df = pd.read_csv(DATA_PATH)

    # Verifica colonne
    if not set(COLONNE_ATTESE).issubset(df.columns):
        raise ValueError(
            f"CSV non valido. Colonne trovate: {list(df.columns)}. "
            f"Attese: {COLONNE_ATTESE}"
        )

    # Pulizia base
    df["area"] = df["area"].astype(str).str.strip()
    df["responsabile"] = df["responsabile"].astype(str).str.strip()
    df["stato"] = df["stato"].astype(str).str.strip()

    # Parse settimana (string -> datetime), utile per max/filtri
    df["settimana"] = pd.to_datetime(df["settimana"], errors="coerce")

    return df


# -------------------------------------------------------------------
# 3) Bootstrap: se il file non esiste, crealo vuoto
# -------------------------------------------------------------------
if not os.path.exists(DATA_PATH):
    crea_csv_vuoto()

# Carica i dati con fallback (se CSV corrotto -> ricrea vuoto)
try:
    df = leggi_csv()
except Exception:
    crea_csv_vuoto()
    df = leggi_csv()


# -------------------------------------------------------------------
# 4) Configurazione pagina Streamlit
# -------------------------------------------------------------------
st.set_page_config(page_title="Pulizie Casa", page_icon="🧹", layout="centered")
st.title("🧹 Gestione Pulizie Casa")


# -------------------------------------------------------------------
# 5) Settimana corrente (gestisce anche csv vuoto)
# -------------------------------------------------------------------
if df.empty or df["settimana"].isna().all():
    st.subheader("Settimana di riferimento: (nessun dato)")
else:
    settimana_corrente = df["settimana"].max().date().isoformat()
    st.subheader(f"Settimana di riferimento: {settimana_corrente}")


# -------------------------------------------------------------------
# 6) Mostra tabella / task
#    - usa index per aggiornare senza ambiguità
#    - key univoca per checkbox (area potrebbe ripetersi)
# -------------------------------------------------------------------
if df.empty:
    st.info("Nessuna pulizia presente nel CSV. Aggiungi righe al file per vederle qui.")
else:
    for idx, row in df.iterrows():
        # Se settimana è NaT, la visualizzo come stringa vuota
        settimana_str = "" if pd.isna(row["settimana"]) else row["settimana"].date().isoformat()

        st.markdown(f"### 🏠 {row['area']}")
        st.write(f"👤 {row['responsabile']}")
        st.caption(f"📅 Settimana: {settimana_str}")

        checkbox_key = f"done_{idx}_{row['area']}_{row['responsabile']}"
        fatto = st.checkbox(
            "Segna come fatto",
            value=(row["stato"].lower() == "fatto"),
            key=checkbox_key
        )

        # Aggiorna lo stato in memoria
        if fatto:
            df.at[idx, "stato"] = "Fatto"
        else:
            # se vuoi che deselezionando torni "Da fare" (opzionale)
            if row["stato"].lower() == "fatto":
                df.at[idx, "stato"] = "Da fare"


# -------------------------------------------------------------------
# 7) Salva eventuali modifiche
#    - riconverte settimana a stringa iso per salvare pulito nel CSV
# -------------------------------------------------------------------
if st.button("💾 Salva modifiche"):
    df_to_save = df.copy()
    df_to_save["settimana"] = df_to_save["settimana"].dt.date.astype(str)
    df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")
    st.success("Stato aggiornato!")


# -------------------------------------------------------------------
# 8) Funzione per ruotare i turni (la tua, ma corretta sulla settimana)
# -------------------------------------------------------------------
def ruota_turni(df):
    responsabili = list(df["responsabile"])
    responsabili = responsabili[1:] + responsabili[:1]
    df["responsabile"] = responsabili

    # settimana prossima (oggi + 7 giorni) salvata come datetime coerente
    df["settimana"] = pd.to_datetime(date.today() + timedelta(days=7))

    df["stato"] = "Da fare"
    return df


# Pulsante di rotazione (se vuoi riattivarlo)
# if st.button("🔁 Ruota i turni"):
#     df = ruota_turni(df)
#     df_to_save = df.copy()
#     df_to_save["settimana"] = df_to_save["settimana"].dt.date.astype(str)
#     df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")
#     st.success("Turni ruotati con successo!")