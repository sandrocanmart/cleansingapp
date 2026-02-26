from datetime import date, timedelta
import os
import csv
import pandas as pd
from config import *
from utilities import *

def lunedi_settimana_corrente(d: date) -> date:
    """Data del lunedì della settimana di una data d."""

    return d - timedelta(days=d.weekday())

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