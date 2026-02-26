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