import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
# Questo URL permette al browser di leggere i tuoi file direttamente da GitHub
GITHUB_BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/"

st.set_page_config(page_title="D&D Arena del Destino", layout="wide")

# CSS per pulire l'interfaccia Streamlit
st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        .stApp { background-color: #050505; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

# Tutto il codice HTML, CSS e JS originale integrato con i tuoi link
game_html = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D&D Arena del Destino</title>
    <style>
        :root {{
            --primary: #f1c40f; --secondary: #2c3e50; --danger: #e74c3c;
            --success: #2ecc71; --info: #3498db; --bg: #050505;
            --panel: rgba(20, 20, 20, 0.95);
        }}
        body {{ background-color: var(--bg); color: #eee; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; overflow: hidden; height: 100vh; }}
        #setup-screen {{ position: fixed; inset: 0; background: #111 url('{GITHUB_BASE}Maps/intro.jpg') center/cover; z-index: 2000; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        #setup-screen::before {{ content: ""; position: absolute; inset: 0; background: rgba(0,0,0,0.6); z-index: -1; }}
        .card {{ background: rgba(26,26,26,0.9); border: 2px solid var(--primary); border-radius: 12px; padding: 30px; width: 450px; text-align: center; box-shadow: 0 0 30px rgba(0,0,0,0.5); }}
        .input-group {{ margin: 15px 0; display: flex; flex-direction: column; gap: 10px; text-align: left; }}
        input, select {{ background: #333; border: 1px solid #555; color: white; padding: 10px; border-radius: 6px; }}
        button {{ background: var(--primary); color: black; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }}
        button:hover {{ transform: scale(1.05); background: #d4ac0d; }}
        #ui-top {{ width: 100%; background: #111; padding: 12px; display: flex; justify-content: space-around; border-bottom: 2px solid #333; z-index: 100; }}
        .stat-badge {{ background: #222; padding: 5px 15px; border-radius: 20px; border: 1px solid #444; font-size: 14px; display: flex; align-items: center; gap: 8px; }}
        #game-container {{ position: relative; width: 720px; height: 1080px; margin-top: 10px; border: 3px solid #333; overflow: hidden; background: #000; }}
        #map-bg-container {{ position: absolute; inset: 0; z-index: 1; }}
        .map-asset {{ width: 100%; height: 100%; object-fit: cover; display: none; opacity: 0.85; }}
        #grid {{ position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }}
        .cell {{ border: 1px solid rgba(255,255,255,0.03); }}
        .char {{ position: absolute; width: 28px; height: 28px; border-radius: 50%; border: 2px solid white; z-index: 50; display: flex; align-items: center; justify-content: center; transition: transform 0.2s; font-size: 18px; }}
        .hero {{ box-shadow: 0 0 10px var(--primary); }}
        .enemy {{ background: #5a0000; border-color: #ff4444; }}
        .active-char {{ outline: 3px solid var(--primary); box-shadow: 0 0 20px var(--primary); z-index: 60; }}
        #action-panel {{ position: fixed; bottom: 210px; background: var(--panel); border: 2px solid var(--primary); padding: 15px; border-radius: 12px; display: none; flex-direction: column; gap: 10px; z-index: 500; }}
        .log-container {{ position: fixed; bottom: 20px; right: 20px; width: 320px; height: 180px; background: var(--panel); border: 1px solid #444; padding: 15px; font-size: 12px; overflow-y: auto; border-radius: 8px; color: #ccc; }}
        .log-entry {{ border-left: 3px solid var(--primary); padding-left: 10px; margin-bottom: 5px; }}
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music"></audio>

    <div id="setup-screen">
        <div class="card">
            <h1>Arena del Destino</h1>
            <div class="input-group">
                <label>Nome Eroe</label>
                <input type="text" id="p-nome" placeholder="Es. Bruenor...">
                <label>Classe</label>
                <select id="p-classe">
                    <option value="Barbaro">Barbaro</option><option value="Guerriero">Guerriero</option><option value="Mago">Mago</option><option value="Paladino">Paladino</option>
                </select>
            </div>
            <button onclick="iniziaAvventura()">ENTRA NEL DUNGEON</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">Mappa: <span id="map-name-display">1</span></div>
        <div class="stat-badge">❤️ HP: <span id="hp-display" style="color:var(--danger)">0</span></div>
        <div class="stat-badge">👣 Passi: <span id="moves-display">6</span>/6</div>
        <button onclick="alert('Zaino Vuoto')">🎒 Zaino</button>
    </div>

    <div id="game-container">
        <div id="map-bg-container">
            <img id="map-img" class="map-asset">
        </div>
        <div id="grid"></div>
    </div>

    <div id="action-panel">
        <div id="weapon-buttons" style="display:flex; gap:10px;"></div>
        <button onclick="prossimoTurno()" style="background:#442222; color:white; margin-top:10px;">Passa Turno</button>
    </div>

    <div class="log-container" id="game-log"></div>

    <script>
        const BASE_URL = "{GITHUB_BASE}";
        const COLS = 24, ROWS = 36;
        const CELL_W = 720 / COLS, CELL_H = 1080 / ROWS;
        const audioPlayer = document.getElementById('bg-music');
        
        let entities = [], currentIndex = 0, isCombat = false, activeEntity = null;

        function playIntroOnce() {{
            if (audioPlayer.paused) {{
                audioPlayer.src = BASE_URL + "Music/intro.mp3";
                audioPlayer.loop = true;
                audioPlayer.play().catch(e => {{}});
            }}
        }}

        function addLog(msg) {{
            const log = document.getElementById('game-log');
            log.innerHTML += `<div class="log-entry">> ${{msg}}</div>`;
            log.scrollTop = log.scrollHeight;
        }}

        function iniziaAvventura() {{
            document.getElementById('setup-screen').style.display = 'none';
            const grid = document.getElementById("grid");
            for (let i = 0; i < COLS * ROWS; i++) {{
                const c = document.createElement("div"); c.className = "cell"; grid.appendChild(c);
            }}
            
            const nome = document.getElementById('p-nome').value || "Eroe";
            const classe = document.getElementById('p-classe').value;
            
            entities = [{{ nome, hp: 20, maxHP: 20, tipo: 'hero', x: 12, y: 5, movesRemaining: 6, element: null }}];
            caricaLivello(1);
        }}

        function caricaLivello(num) {{
            document.getElementById('map-name-display').innerText = num;
            const imgEl = document.getElementById('map-img');
            imgEl.src = BASE_URL + "Maps/" + num + ".jpg";
            imgEl.style.display = 'block';
            
            audioPlayer.src = BASE_URL + "Music/" + num + ".mp3";
            audioPlayer.play().catch(e => {{}});

            // Spawn nemico di prova
            entities.push({{ nome: "Mostro", hp: 10, tipo: 'enemy', x: 12, y: 25, movesRemaining: 6, element: null }});
            
            creaGrafica();
            aggiornaUI();
            addLog("Livello " + num + " iniziato.");
        }}

        function creaGrafica() {{
            entities.forEach(ent => {{
                if (ent.element) ent.element.remove();
                const el = document.createElement('div');
                el.className = 'char ' + ent.tipo;
                el.innerText = ent.tipo === 'hero' ? "👤" : "👹";
                if(ent.tipo === 'hero') el.style.backgroundColor = "#3498db";
                document.getElementById('game-container').appendChild(el);
                ent.element = el;
                posiziona(ent);
            }});
        }}

        function posiziona(ent) {{
            ent.element.style.transform = `translate(${{ent.x * CELL_W}}px, ${{ent.y * CELL_H}}px)`;
        }}

        function aggiornaUI() {{
            const hero = entities.find(e => e.tipo === 'hero');
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
        }}

        window.addEventListener('keydown', (e) => {{
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero) return;
            let dx = 0, dy = 0;
            if (e.key === 'w' || e.key === 'ArrowUp') dy = -1;
            if (e.key === 's' || e.key === 'ArrowDown') dy = 1;
            if (e.key === 'a' || e.key === 'ArrowLeft') dx = -1;
            if (e.key === 'd' || e.key === 'ArrowRight') dx = 1;
            
            if (dx !== 0 || dy !== 0) {{
                hero.x += dx; hero.y += dy;
                posiziona(hero);
                // Controllo prossimità nemici
                entities.filter(en => en.tipo === 'enemy').forEach(en => {{
                    let d = Math.sqrt(Math.pow(en.x-hero.x, 2) + Math.pow(en.y-hero.y, 2));
                    if (d < 3) {{ 
                        document.getElementById('action-panel').style.display = 'flex';
                        if(!isCombat) addLog("Combattimento iniziato!");
                        isCombat = true; 
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
"""

# Codifica Base64 per la massima compatibilità
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="1150px" allow="autoplay"></iframe>', height=1150)
