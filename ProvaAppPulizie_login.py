import streamlit as st
import pandas as pd
import os
import csv
from datetime import date, timedelta

# Percorso del file CSV
DATA_PATH = r"C:\DevOps\CleansingAPP\AppPulizie\pulizie2.csv"


import streamlit as st
import hashlib

# ------------------------
# Funzione hash password
# ------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------------
# Utenti (per ora hardcoded)
# ------------------------
users = {
    "sandro": hash_password("1234"),
    "coinquilina1": hash_password("abcd")
}


# ------------------------
# Inizializza sessione
# ------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ------------------------
# Login form
# ------------------------
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == hash_password(password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login effettuato!")
            st.rerun()
        else:
            st.error("Credenziali errate")


# ------------------------
# Logout
# ------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()


# ------------------------
# APP PROTETTA
# ------------------------
if not st.session_state.authenticated:s
    login()
else:
    st.sidebar.write(f"Ciao {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()

    st.title("App Pulizie")
    st.write("Benvenuto nell'app!")


