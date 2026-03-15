import streamlit as st
import streamlit.components.v1 as components
import base64

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="D&D Arena del Destino",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Rimuoviamo i margini superflui di Streamlit tramite CSS
st.markdown("""
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {
            padding: 0;
            margin: 0;
        }
        .stApp {
            background-color: #050505;
        }
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inseriamo qui il tuo codice HTML completo
# Ho aggiunto un piccolo controllo CSS iniziale per assicurarmi che il corpo sia visibile
game_html = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D&D Arena del Destino - Saga Mappat</title>
    <style>
        :root {
            --primary: #f1c40f;
            --secondary: #2c3e50;
            --danger: #e74c3c;
            --success: #2ecc71;
            --info: #3498db;
            --bg: #050505;
            --panel: rgba(20, 20, 20, 0.95);
        }

        body {
            background-color: var(--bg) !important;
            color: #eee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow: hidden;
            height: 100vh;
        }

        #setup-screen {
            position: fixed;
            inset: 0;
            background: #111; /* Fallback se l'immagine manca */
            background-image: url('https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?q=80&w=1920&auto=format&fit=crop'); 
            background-size: cover;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        /* ... resto del tuo CSS originale ... */
    </style>
    <!-- NOTA: Per brevità ho accorciato il CSS, ma nel tuo file incolla tutto il CSS e JS originale -->
</head>
<body onclick="playIntroOnce()">
    <!-- INCOLLA QUI TUTTO IL CORPO (BODY) DEL TUO HTML ORIGINALE -->
    <div id="setup-screen">
        <div class="card" style="background: rgba(0,0,0,0.8); border: 2px solid gold; padding: 2rem; border-radius: 15px; text-align: center;">
            <h1 style="color: gold;">Arena del Destino</h1>
            <p>Caricamento Saga Mappat...</p>
            <div style="margin: 20px 0; display: flex; flex-direction: column; gap: 10px; text-align: left;">
                <label>Nome Eroe</label>
                <input type="text" id="p-nome" style="padding: 10px; background: #222; color: white; border: 1px solid #444;" placeholder="Es. Bruenor...">
            </div>
            <button onclick="alert('Gioco in fase di inizializzazione...')" style="padding: 15px 30px; background: gold; border: none; font-weight: bold; cursor: pointer;">ENTRA NEL DUNGEON</button>
        </div>
    </div>
    
    <script>
        // Incolla qui tutto il tuo JavaScript originale
        console.log("Gioco caricato correttamente!");
    </script>
</body>
</html>
"""

# Funzione per codificare l'HTML e bypassare i blocchi del browser
def get_game_display(html_content):
    b64_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    return f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="1100px" style="border:none; overflow:hidden;" allow="autoplay"></iframe>'

# Visualizzazione del gioco tramite l'iframe codificato
st.components.v1.html(get_game_display(game_html), height=1100)
