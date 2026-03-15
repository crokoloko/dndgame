import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina per rimuovere spazi bianchi
st.set_page_config(
    page_title="D&D Arena del Destino",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Rimuoviamo il padding di Streamlit che potrebbe spostare il gioco
st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        iframe { display: block; margin: auto; }
        body { background-color: #050505; }
    </style>
""", unsafe_allow_html=True)

# Il tuo codice HTML (Inserito tra r''' ... ''')
# Usiamo r''' per evitare problemi con i caratteri speciali \ e gli apici
game_html = r'''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <style>
        /* Forza lo sfondo nero per evitare il flash bianco */
        html, body { background: #050505 !important; margin: 0; padding: 0; height: 100%; width: 100%; overflow: hidden; }
    </style>
''' + """
    <style>
        :root {
            --primary: #f1c40f;
            /* ... tutto il tuo CSS ... */
    </style>
    <body>
        <script>
            /* ... tutto il tuo JavaScript ... */
        </script>
    </body>
</html>
"""

# Visualizzazione con altezza fissa per accomodare il tuo canvas 1080px + UI
components.html(game_html, height=1200, scrolling=True)
