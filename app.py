import streamlit as st
import streamlit.components.v1 as components

# Configurazione pagina Streamlit
st.set_page_config(page_title="D&D Arena del Destino", layout="wide")

# Nascondi i margini predefiniti di Streamlit per dare spazio al gioco
st.markdown("""
    <style>
    .main {
        padding: 0rem;
    }
    .stApp {
        background-color: #050505;
    }
    </style>
    """, unsafe_allow_html=True)

# Inserisci qui il tuo codice HTML completo
game_html = """
<!DOCTYPE html>
<html lang="it">
... (INCOLLA QUI TUTTO IL TUO CODICE HTML COMPLETO) ...
</html>
"""

# Visualizzazione del gioco
# Nota: width=740 e height=1200 per adattarsi al tuo canvas 720x1080 + UI
components.html(game_html, height=1200, scrolling=True)
