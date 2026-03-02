from datetime import date, timedelta
import os
import csv
import pandas as pd
import streamlit as st
from config import *



def crea_csv_vuoto() -> None:
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
    df_to_save["settimana"] = pd.to_datetime(df["settimana"], errors="coerce").dt.date
    df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8")


