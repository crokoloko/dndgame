import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
# Utilizziamo un segnaposto per la base URL
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

# Definiamo l'HTML come una stringa normale (senza f-string) per evitare errori di sintassi con le graffe {}
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D&D Arena del Destino</title>
    <style>
        :root {
            --primary: #f1c40f; --secondary: #2c3e50; --danger: #e74c3c;
            --success: #2ecc71; --info: #3498db; --bg: #050505;
            --panel: rgba(20, 20, 20, 0.95);
        }
        body { background-color: var(--bg); color: #eee; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; overflow: hidden; height: 100vh; }
        #setup-screen { position: fixed; inset: 0; background: #111 url('__GITHUB_BASE__Maps/intro.jpg') center/cover; z-index: 2000; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.6); z-index: -1; }
        .card { background: rgba(26, 26, 26, 0.9); border: 2px solid var(--primary); border-radius: 12px; padding: 30px; width: 450px; text-align: center; }
        .input-group { margin: 15px 0; display: flex; flex-direction: column; gap: 10px; text-align: left; }
        input, select { background: #333; border: 1px solid #555; color: white; padding: 10px; border-radius: 6px; }
        button { background: var(--primary); color: black; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        #ui-top { width: 100%; background: #111; padding: 12px; display: flex; justify-content: space-around; border-bottom: 2px solid #333; z-index: 100; }
        .stat-badge { background: #222; padding: 5px 15px; border-radius: 20px; border: 1px solid #444; font-size: 14px; display: flex; align-items: center; gap: 8px; }
        #game-container { position: relative; width: 720px; height: 1080px; margin-top: 10px; border: 3px solid #333; overflow: hidden; background: #000; }
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: cover; display: none; opacity: 0.85; }
        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.01); box-sizing: border-box; }
        .cell.wall { background: rgba(255,0,0,0.1); border: 1px solid rgba(255,255,255,0.05); } 
        .char { position: absolute; width: 28px; height: 28px; border-radius: 50%; border: 2px solid white; z-index: 50; display: flex; align-items: center; justify-content: center; transition: transform 0.2s; font-size: 18px; }
        .hero { box-shadow: 0 0 10px var(--primary); }
        .enemy { background: #5a0000; border-color: #ff4444; }
        .loot-icon { position: absolute; z-index: 10; font-size: 20px; display: flex; align-items: center; justify-content: center; }
        .log-container { position: fixed; bottom: 20px; right: 20px; width: 320px; height: 180px; background: var(--panel); border: 1px solid #444; padding: 15px; font-size: 12px; overflow-y: auto; border-radius: 8px; color: #ccc; }
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
                    <option value="Guerriero">Guerriero</option><option value="Mago">Mago</option>
                </select>
            </div>
            <button onclick="iniziaAvventura()">ENTRA NEL DUNGEON</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">Mappa: <span id="map-name-display">1</span></div>
        <div class="stat-badge">❤️ HP: <span id="hp-display">0</span></div>
        <div class="stat-badge">👣 Passi: <span id="moves-display">6</span>/6</div>
    </div>

    <div id="game-container">
        <div id="map-bg-container">
            <img id="map-img" class="map-asset">
        </div>
        <div id="grid"></div>
    </div>
    <div class="log-container" id="game-log"></div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const CELL_W = 720 / COLS, CELL_H = 1080 / ROWS;
        const audioPlayer = document.getElementById('bg-music');
        
        let currentMapNumber = 1, entities = [], loots = {};

        function playIntroOnce() {
            if (audioPlayer.paused) {
                audioPlayer.src = BASE_URL + "Music/intro.mp3";
                audioPlayer.play().catch(e => {});
            }
        }

        function addLog(msg) {
            const log = document.getElementById('game-log');
            log.innerHTML += `<div>> ${msg}</div>`;
            log.scrollTop = log.scrollHeight;
        }

        function iniziaAvventura() {
            document.getElementById('setup-screen').style.display = 'none';
            const grid = document.getElementById("grid");
            grid.innerHTML = "";
            for (let i = 0; i < COLS * ROWS; i++) {
                const c = document.createElement("div"); c.className = "cell"; grid.appendChild(c);
            }
            const nome = document.getElementById('p-nome').value || "Eroe";
            entities = [{ nome, hp: 20, tipo: 'hero', x: 12, y: 2, movesRemaining: 6, element: null, inventory: { potions: 0, coins: 0 } }];
            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            document.getElementById('map-name-display').innerText = mapNumber;

            const imgEl = document.getElementById('map-img');
            imgEl.src = BASE_URL + "Maps/" + mapNumber + ".jpg";
            imgEl.style.display = 'block';
            audioPlayer.src = BASE_URL + "Music/" + mapNumber + ".mp3";
            audioPlayer.play().catch(e => {});

            try {
                const response = await fetch(`${BASE_URL}Maps/${mapNumber}.json`);
                if (response.ok) {
                    const data = await response.json();
                    applyLevelData(data);
                    addLog("Mappa " + mapNumber + " caricata con successo.");
                }
            } catch (e) {
                addLog("Errore nel caricamento dei muri JSON.");
            }

            creaGrafica();
            aggiornaUI();
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            
            if (data.walls) {
                data.walls.forEach(idx => {
                    if (cells[idx]) cells[idx].classList.add('wall');
                });
            }

            loots = {};
            document.querySelectorAll('.loot-icon').forEach(l => l.remove());
            if (data.loot) {
                data.loot.forEach(item => {
                    const idx = parseInt(item.idx);
                    const el = document.createElement('div');
                    el.className = 'loot-icon';
                    el.innerText = item.type === 'moneta' ? "💰" : "🧪";
                    el.style.width = CELL_W + 'px'; el.style.height = CELL_H + 'px';
                    el.style.left = (idx % COLS) * CELL_W + 'px';
                    el.style.top = Math.floor(idx / COLS) * CELL_H + 'px';
                    document.getElementById('game-container').appendChild(el);
                    loots[idx] = { type: item.type, element: el };
                });
            }
        }

        function creaGrafica() {
            entities.forEach(ent => {
                if (ent.element) ent.element.remove();
                const el = document.createElement('div');
                el.className = 'char ' + ent.tipo;
                el.innerText = ent.tipo === 'hero' ? "👤" : "👹";
                document.getElementById('game-container').appendChild(el);
                ent.element = el;
                aggiornaPosizione(ent);
            });
        }

        function aggiornaPosizione(ent) {
            ent.element.style.transform = `translate(${ent.x * CELL_W}px, ${ent.y * CELL_H}px)`;
            
            if (ent.tipo === 'hero') {
                const idx = Math.floor(ent.y) * COLS + Math.floor(ent.x);
                if (loots[idx]) {
                    addLog("Hai raccolto: " + loots[idx].type);
                    loots[idx].element.remove();
                    delete loots[idx];
                }
            }
        }

        function aggiornaUI() {
            const hero = entities.find(e => e.tipo === 'hero');
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
        }

        window.addEventListener('keydown', (e) => {
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero) return;
            let nx = hero.x, ny = hero.y;

            if (e.key === 'w' || e.key === 'ArrowUp') ny--;
            if (e.key === 's' || e.key === 'ArrowDown') ny++;
            if (e.key === 'a' || e.key === 'ArrowLeft') nx--;
            if (e.key === 'd' || e.key === 'ArrowRight') nx++;

            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                const targetIdx = ny * COLS + nx;
                const cell = document.querySelectorAll('.cell')[targetIdx];
                
                if (cell && !cell.classList.contains('wall')) {
                    hero.x = nx; hero.y = ny;
                    aggiornaPosizione(hero);
                    if (hero.y >= ROWS - 1) caricaMappaCompleta(currentMapNumber + 1);
                } else {
                    addLog("C'è un muro!");
                }
            }
        });
    </script>
</body>
</html>
"""

# Sostituiamo il segnaposto con la variabile Python reale
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)

# Codifica Base64 per la sicurezza di Streamlit
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="1150px" allow="autoplay"></iframe>', height=1150)
