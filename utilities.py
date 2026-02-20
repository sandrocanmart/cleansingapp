import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta

DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"
COLONNE_ATTESE = ["settimana", "area", "responsabile", "stato"]

# --------------------------
# Utility: date settimana
# --------------------------
def lunedi_settimana_corrente(d: date) -> date:
    return d - timedelta(days=d.weekday())


# --------------------------
# CSV: create / read / save
# --------------------------
def crea_csv_vuoto():
    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLONNE_ATTESE)

def leggi_csv() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    if not set(COLONNE_ATTESE).issubset(df.columns):
        raise ValueError(
            f"CSV non valido. Colonne trovate: {list(df.columns)}. Attese: {COLONNE_ATTESE}"
        )

    df["area"] = df["area"].astype(str).str.strip()
    df["responsabile"] = df["responsabile"].astype(str).str.strip()
    df["stato"] = df["stato"].astype(str).str.strip()

    # settimana come date (non datetime)
    df["settimana"] = pd.to_datetime(df["settimana"], errors="coerce").dt.date

    return df

def salva_csv(df: pd.DataFrame):
    df_to_save = df.copy()
    df_to_save["settimana"] = df_to_save["settimana"].astype(str)
    df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")


# --------------------------
# Rotazione automatica
# --------------------------
def ruota_lista(responsabili: list[str]) -> list[str]:
    # stesso schema: primo va in fondo
    return responsabili[1:] + responsabili[:1]

def auto_ruota_e_scrivi_settimana_corrente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Se non esistono righe per la settimana corrente, crea la settimana corrente
    ruotando i responsabili rispetto all'ultima settimana presente e salva su CSV.
    NON cancella lo storico.
    """
    oggi = date.today()
    lun_corrente = lunedi_settimana_corrente(oggi)

    # Se già presente, non fare nulla
    if not df.empty and (df["settimana"] == lun_corrente).any():
        return df

    # Se df vuoto o senza settimane valide, non possiamo ruotare (manca template)
    if df.empty or df["settimana"].isna().all():
        return df

    # Prendiamo l'ultima settimana come template
    ultima_settimana = df["settimana"].max()
    df_last = df[df["settimana"] == ultima_settimana].copy()

    # Ruotiamo i responsabili mantenendo l'ordine delle righe (aree)
    responsabili_last = df_last["responsabile"].tolist()
    responsabili_new = ruota_lista(responsabili_last)

    df_new = df_last.copy()
    df_new["settimana"] = lun_corrente
    df_new["responsabile"] = responsabili_new
    df_new["stato"] = "Da fare"

    df_out = pd.concat([df, df_new], ignore_index=True)

    salva_csv(df_out)
    return df_out