import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
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

# Definiamo l'HTML come stringa normale per evitare errori con le parentesi graffe {}
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
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.7); z-index: -1; }
        
        .card { background: rgba(26, 26, 26, 0.95); border: 2px solid var(--primary); border-radius: 12px; padding: 25px; width: 450px; text-align: center; box-shadow: 0 0 30px rgba(0,0,0,0.8); }
        
        .input-group { margin: 12px 0; display: flex; flex-direction: column; gap: 5px; text-align: left; }
        label { font-size: 13px; color: var(--primary); font-weight: bold; }
        input, select { background: #222; border: 1px solid #444; color: white; padding: 10px; border-radius: 6px; font-size: 14px; }
        
        button { background: var(--primary); color: black; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { transform: scale(1.05); background: #d4ac0d; }

        #ui-top { width: 100%; background: #111; padding: 10px; display: flex; justify-content: space-around; border-bottom: 2px solid #333; z-index: 100; }
        .stat-badge { background: #222; padding: 5px 12px; border-radius: 20px; border: 1px solid #444; font-size: 13px; display: flex; align-items: center; gap: 8px; }

        #game-container { position: relative; width: 720px; height: 1080px; margin-top: 5px; border: 2px solid #333; overflow: hidden; background: #000; }
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: cover; display: none; }

        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.02); box-sizing: border-box; }
        
        /* MURI TRASPARENTI COME RICHIESTO */
        .cell.wall { background: transparent; border: none; } 

        .char { position: absolute; width: 28px; height: 28px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.8); z-index: 50; display: flex; align-items: center; justify-content: center; transition: transform 0.2s; font-size: 18px; user-select: none; }
        .hero { box-shadow: 0 0 15px var(--primary); }
        .enemy { background: #5a0000; border-color: #ff4444; }
        .active-char { outline: 3px solid white; z-index: 60; animation: pulse 1s infinite; }
        
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }

        #action-panel { position: fixed; bottom: 210px; background: var(--panel); border: 2px solid var(--primary); padding: 15px; border-radius: 12px; display: none; flex-direction: column; gap: 8px; z-index: 500; min-width: 220px; }
        .log-container { position: fixed; bottom: 20px; right: 20px; width: 300px; height: 160px; background: var(--panel); border: 1px solid #444; padding: 12px; font-size: 12px; overflow-y: auto; border-radius: 8px; color: #ccc; }
        .log-entry { border-left: 3px solid var(--primary); padding-left: 8px; margin-bottom: 4px; }
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music" loop></audio>

    <div id="setup-screen">
        <div class="card">
            <h1 style="color:var(--primary); margin-top:0;">Arena del Destino</h1>
            <div class="input-group">
                <label>Nome Eroe</label>
                <input type="text" id="p-nome" placeholder="Inserisci nome...">
                
                <label>Razza</label>
                <select id="p-razza">
                    <option value="Umano">Umano</option><option value="Elfo">Elfo</option>
                    <option value="Nano">Nano</option><option value="Halfling">Halfling</option>
                    <option value="Dragonide">Dragonide</option><option value="Gnomo">Gnomo</option>
                    <option value="Mezzelfo">Mezzelfo</option><option value="Mezzorco">Mezzorco</option>
                    <option value="Tiefling">Tiefling</option>
                </select>

                <label>Classe</label>
                <select id="p-classe">
                    <option value="Barbaro">Barbaro</option><option value="Guerriero">Guerriero</option>
                    <option value="Paladino">Paladino</option><option value="Ranger">Ranger</option>
                    <option value="Chierico">Chierico</option><option value="Ladro">Ladro</option>
                    <option value="Bardo">Bardo</option><option value="Druido">Druido</option>
                    <option value="Monaco">Monaco</option><option value="Warlock">Warlock</option>
                    <option value="Mago">Mago</option><option value="Stregone">Stregone</option>
                </select>
            </div>
            <button onclick="iniziaAvventura()">INIZIA SAGA MAPPAT</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">Mappa: <span id="map-name-display">1</span></div>
        <div class="stat-badge">❤️ HP: <span id="hp-display" style="color:var(--danger)">0</span></div>
        <div class="stat-badge">👣 Passi: <span id="moves-display">6</span>/6</div>
        <div class="stat-badge">⚔️ Iniziativa: <span id="ini-display">-</span></div>
    </div>

    <div id="game-container">
        <div id="map-bg-container">
            <img id="map-img" class="map-asset">
        </div>
        <div id="grid"></div>
    </div>

    <div id="action-panel">
        <div style="font-size:12px; color:var(--primary); font-weight:bold; margin-bottom:5px;">AZIONI COMBATTIMENTO</div>
        <div id="weapon-buttons" style="display:flex; flex-direction:column; gap:5px;"></div>
        <button onclick="prossimoTurno()" style="background:#442222; color:white; margin-top:5px; font-size:12px;">Passa Turno</button>
    </div>

    <div class="log-container" id="game-log"></div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const CELL_W = 720 / COLS, CELL_H = 1080 / ROWS;
        const audioPlayer = document.getElementById('bg-music');

        const RACE_ICONS = { "Umano": "🧔", "Elfo": "🧝", "Nano": "🎅", "Halfling": "👦", "Dragonide": "🐲", "Gnomo": "🧙‍♂️", "Mezzelfo": "🧝‍♂️", "Mezzorco": "👹", "Tiefling": "😈" };
        const HP_MAP = { "Barbaro": 12, "Guerriero": 10, "Paladino": 10, "Ranger": 10, "Chierico": 8, "Ladro": 8, "Bardo": 8, "Druido": 8, "Monaco": 8, "Warlock": 8, "Mago": 6, "Stregone": 6 };
        const ENEMY_ICONS = ["👹", "🧟", "💀", "🐺", "🦎", "👻"];

        let currentMapNumber = 1, entities = [], currentIndex = 0, isCombat = false, activeEntity = null, loots = {};

        function playIntroOnce() {
            if (audioPlayer.paused) {
                audioPlayer.src = BASE_URL + "Music/intro.mp3";
                audioPlayer.play().catch(e => {});
            }
        }

        function addLog(msg) {
            const log = document.getElementById('game-log');
            log.innerHTML += `<div class="log-entry">> ${msg}</div>`;
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
            const razza = document.getElementById('p-razza').value;
            const classe = document.getElementById('p-classe').value;
            
            let hp = HP_MAP[classe] + 10; // Base HP + Classe
            if(razza === "Nano") hp += 2;

            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', razza, classe, 
                x: 12, y: 3, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: RACE_ICONS[razza] 
            }];

            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            document.getElementById('map-name-display').innerText = mapNumber;
            isCombat = false;
            document.getElementById('action-panel').style.display = 'none';

            // Sfondo e Musica
            const imgEl = document.getElementById('map-img');
            imgEl.src = BASE_URL + "Maps/" + mapNumber + ".jpg";
            imgEl.onload = () => imgEl.style.display = 'block';
            audioPlayer.src = BASE_URL + "Music/" + mapNumber + ".mp3";
            audioPlayer.play().catch(e => {});

            // Carica JSON Muri
            try {
                const response = await fetch(`${BASE_URL}Maps/${mapNumber}.json`);
                if (response.ok) {
                    const data = await response.json();
                    applyLevelData(data);
                }
            } catch (e) { console.log("JSON non trovato"); }

            // Reset Eroe e Spawn Nemici
            const hero = entities[0];
            hero.x = 12; hero.y = 3; hero.movesRemaining = 6;
            
            // Rimuovi vecchi nemici
            entities = [hero];
            let enemyCount = 1 + Math.floor(mapNumber / 2);
            for(let i=0; i<enemyCount; i++) {
                entities.push({
                    nome: "Nemico " + (i+1), hp: 5 + (mapNumber*3), 
                    tipo: 'enemy', x: Math.floor(Math.random()*20)+2, 
                    y: Math.floor(Math.random()*10)+20, 
                    movesRemaining: 4, dead: false, element: null,
                    icon: ENEMY_ICONS[Math.floor(Math.random()*ENEMY_ICONS.length)]
                });
            }

            disegnaEntita();
            aggiornaUI();
            addLog("Sei entrato nel Livello " + mapNumber);
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            if (data.walls) {
                data.walls.forEach(idx => { if (cells[idx]) cells[idx].classList.add('wall'); });
            }
        }

        function disegnaEntita() {
            const container = document.getElementById('game-container');
            // Pulizia
            document.querySelectorAll('.char').forEach(c => c.remove());
            
            entities.forEach(ent => {
                const el = document.createElement('div');
                el.className = 'char ' + ent.tipo;
                el.innerText = ent.icon;
                if(ent.tipo === 'hero') el.classList.add('hero');
                container.appendChild(el);
                ent.element = el;
                aggiornaPosizione(ent);
            });
        }

        function aggiornaPosizione(ent) {
            if(!ent.element) return;
            ent.element.style.transform = `translate(${ent.x * CELL_W}px, ${ent.y * CELL_H}px)`;
        }

        function aggiornaUI() {
            const hero = entities[0];
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
            document.getElementById('ini-display').innerText = isCombat ? hero.ini : "-";
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true;
            addLog("NEMICI AVVISTATI! Inizia il combattimento.");
            document.getElementById('action-panel').style.display = 'flex';
            
            entities.forEach(ent => ent.ini = Math.floor(Math.random()*20)+1);
            entities.sort((a,b) => b.ini - a.ini);
            
            currentIndex = 0;
            selezionaTurno();
        }

        function selezionaTurno() {
            entities.forEach(e => e.element.classList.remove('active-char'));
            activeEntity = entities[currentIndex % entities.length];
            
            if(activeEntity.dead) return prossimoTurno();
            
            activeEntity.element.classList.add('active-char');
            activeEntity.movesRemaining = (activeEntity.tipo === 'hero') ? 6 : 4;
            
            if(activeEntity.tipo === 'enemy') {
                setTimeout(turnoIA, 600);
            } else {
                renderAzioni();
            }
            aggiornaUI();
        }

        function renderAzioni() {
            const btnContainer = document.getElementById('weapon-buttons');
            btnContainer.innerHTML = '<button onclick="attaccoBase()">⚔️ Attacco Base</button>';
        }

        function attaccoBase() {
            const hero = entities.find(e => e.tipo === 'hero');
            const target = entities.find(e => e.tipo === 'enemy' && !e.dead);
            if(!target) return;

            let dist = Math.sqrt(Math.pow(hero.x - target.x, 2) + Math.pow(hero.y - target.y, 2));
            if(dist < 3) {
                let dmg = Math.floor(Math.random()*8)+2;
                target.hp -= dmg;
                addLog("Colpisci il nemico per " + dmg + " danni!");
                if(target.hp <= 0) {
                    target.dead = true;
                    target.element.style.opacity = "0.3";
                    addLog("Nemico sconfitto!");
                }
                prossimoTurno();
            } else {
                addLog("Il nemico è troppo lontano!");
            }
        }

        function turnoIA() {
            const hero = entities.find(e => e.tipo === 'hero');
            // Semplice IA: si muove verso l'eroe
            if(activeEntity.x < hero.x) activeEntity.x++;
            else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++;
            else if(activeEntity.y > hero.y) activeEntity.y--;
            
            aggiornaPosizione(activeEntity);
            
            let dist = Math.sqrt(Math.pow(activeEntity.x - hero.x, 2) + Math.pow(activeEntity.y - hero.y, 2));
            if(dist < 1.5) {
                let dmg = Math.floor(Math.random()*4)+1;
                hero.hp -= dmg;
                addLog("Il nemico ti colpisce! -" + dmg + " HP");
            }
            setTimeout(prossimoTurno, 500);
        }

        function prossimoTurno() {
            currentIndex++;
            selezionaTurno();
        }

        window.addEventListener('keydown', (e) => {
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero || hero.dead || (isCombat && activeEntity !== hero)) return;

            let nx = hero.x, ny = hero.y;
            if (e.key === 'w' || e.key === 'ArrowUp') ny--;
            if (e.key === 's' || e.key === 'ArrowDown') ny++;
            if (e.key === 'a' || e.key === 'ArrowLeft') nx--;
            if (e.key === 'd' || e.key === 'ArrowRight') nx++;

            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                const cell = document.querySelectorAll('.cell')[ny * COLS + nx];
                if (cell && !cell.classList.contains('wall')) {
                    hero.x = nx; hero.y = ny;
                    if(isCombat) hero.movesRemaining--;
                    aggiornaPosizione(hero);
                    
                    if(!isCombat) {
                        entities.filter(en => en.tipo === 'enemy' && !en.dead).forEach(en => {
                            let d = Math.sqrt(Math.pow(en.x-hero.x, 2) + Math.pow(en.y-hero.y, 2));
                            if(d < 6) iniziaCombattimento();
                        });
                    }
                    
                    if (hero.y >= ROWS - 1) caricaMappaCompleta(currentMapNumber + 1);
                }
            }
            aggiornaUI();
        });
    </script>
</body>
</html>
"""

# Sostituzione finale e renderizzazione
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" width="100%" height="1150px" allow="autoplay"></iframe>', height=1150)
