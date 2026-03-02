from datetime import date, timedelta, datetime
import os
import streamlit as st
from streamlit_calendar import calendar, state
import ast
import calendar as cal
from utilities import crea_csv_vuoto, leggi_csv, salva_csv
from config import *
from rotation import lunedi_settimana_corrente


def main():
    # ==========================
    # BOOTSTRAP DATI
    # ==========================
    if not os.path.exists(DATA_PATH):
        crea_csv_vuoto()
    try:
        df = leggi_csv()
    except FileNotFoundError:
        crea_csv_vuoto()
        df = leggi_csv()

    # ==========================
    # UI / GRAFICA STREAMLIT
    # ==========================

    tab1, tab2, tab3, tab4 = st.tabs([
        "Pianificazione Pulizie", 
        "Gestione Lavatrici", 
        "Acquisti per la casa", 
        "Splitwise"])

    with tab1:
        #st.header("📅 Pianificazione Pulizie")
        st.caption("DEPLOY MARK: 2026-02-24")
        st.set_page_config(page_title="Casa Lanfranchi", page_icon="🧹", layout="centered")
        st.title("🧹 Gestione Pulizie Casa Lanfranchi")

        oggi = date.today()
        lunedi_corrente = lunedi_settimana_corrente(oggi)
        domenica_corrente = lunedi_corrente + timedelta(days=6)

        st.subheader(
            f"Settimana corrente: {lunedi_corrente.isoformat()} → {domenica_corrente.isoformat()}"
        )

        # Filtra SOLO settimana corrente
        st.write("lunedi_corrente (type):", lunedi_corrente, type(lunedi_corrente))
        st.write("df['settimana'] dtype:", df["settimana"].dtype)
        st.write("Esempi valori settimana:", df["settimana"].head(10).tolist())
        df["settimana"] = df["settimana"].apply(ast.literal_eval)
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

        


        # Se vuoi vedere il modulo corrente nei log di Streamlit:
        # (meglio di print: lo vedi nell'app)
        #st.caption(f"__name__ = {__name__}")
    with tab2:
        st.header("📅 Gestione Lavatrici")
        st.caption("DEPLOY MARK: 2026-02-26")

        calendar_options = {
            "editable": True,
            "selectable": True,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
            "resources": [
                {"id": "a", "building": "Building A", "title": "Building A"},
                {"id": "b", "building": "Building A", "title": "Building B"},
                {"id": "c", "building": "Building B", "title": "Building C"},
                {"id": "d", "building": "Building B", "title": "Building D"},
                {"id": "e", "building": "Building C", "title": "Building E"},
                {"id": "f", "building": "Building C", "title": "Building F"},
            ],
        }
        calendar_events = [
            {
                "title": "Event 1",
                "start": "2023-07-31T08:30:00",
                "end": "2023-07-31T10:30:00",
                "resourceId": "a",
            },
            {
                "title": "Event 2",
                "start": "2023-07-31T07:30:00",
                "end": "2023-07-31T10:30:00",
                "resourceId": "b",
            },
            {
                "title": "Event 3",
                "start": "2023-07-31T10:40:00",
                "end": "2023-07-31T12:30:00",
                "resourceId": "a",
            }
        ]
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """

        calendar = calendar(
            events=calendar_events,
            options=calendar_options,
            custom_css=custom_css,
            key='calendar', # Assign a widget key to prevent state loss
            )
        st.write(calendar)




    with tab3:
        st.header("🧺 Acquisti per la casa")
        st.caption("DEPLOY MARK: 2026-02-26")




    with tab4:
        st.header("Splitwise")
        st.caption("DEPLOY MARK: 2026-02-26")

if __name__ == "__main__":
    main()