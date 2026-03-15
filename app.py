import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
GITHUB_BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/"

st.set_page_config(
    page_title="D&D Arena Mobile", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# CSS per eliminare ogni bordo di Streamlit e rendere l'app a tutto schermo
st.markdown("""
    <style>
        .block-container { padding: 0rem; max-width: 100%; }
        .stApp { background-color: #000; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        iframe { border: none; width: 100vw; height: 100vh; display: block; }
        #MainMenu {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Template HTML/JS/CSS Ottimizzato per Mobile (UX migliorata)
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>D&D Arena Mobile</title>
    <style>
        :root {
            --primary: #f1c40f; 
            --danger: #e74c3c;
            --success: #2ecc71; 
            --bg: #000;
            --ctrl-bg: rgba(255, 255, 255, 0.1);
        }
        * { 
            touch-action: none; 
            -webkit-tap-highlight-color: transparent; 
            user-select: none; 
            box-sizing: border-box; 
        }
        body { 
            background-color: var(--bg); 
            color: #eee; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0; 
            padding: 0;
            display: flex; 
            flex-direction: column; 
            height: 100vh; 
            width: 100vw;
            overflow: hidden;
        }
        
        /* Schermata Iniziale */
        #setup-screen { 
            position: fixed; inset: 0; 
            background: #111 url('__GITHUB_BASE__Maps/intro.jpg') center/cover; 
            z-index: 3000; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
        }
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.8); z-index: -1; }
        
        .card { 
            background: rgba(30, 30, 30, 0.95); 
            border: 1px solid var(--primary); 
            border-radius: 15px; 
            padding: 20px; 
            width: 90%; 
            max-width: 350px; 
            text-align: center; 
        }
        
        .input-group { margin: 15px 0; display: flex; flex-direction: column; gap: 8px; text-align: left; }
        label { font-size: 12px; color: var(--primary); font-weight: bold; text-transform: uppercase; }
        input, select { 
            background: #111; border: 1px solid #444; color: white; 
            padding: 12px; border-radius: 8px; font-size: 16px; width: 100%;
        }
        
        .start-btn { 
            background: var(--primary); color: black; border: none; 
            padding: 16px; border-radius: 10px; font-weight: bold; 
            width: 100%; font-size: 18px; margin-top: 10px;
        }

        /* UI Superiore */
        #ui-top { 
            height: 50px; width: 100%; background: #111; 
            display: flex; justify-content: space-around; align-items: center;
            border-bottom: 1px solid #333; z-index: 100; padding: 0 10px;
        }
        .stat-badge { font-size: 13px; font-weight: bold; display: flex; align-items: center; gap: 4px; }

        /* Contenitore Gioco */
        #game-viewport {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #050505;
            position: relative;
        }

        #game-container { 
            position: relative; 
            width: 98vw; 
            height: calc(98vw * (1.5)); /* Rapporto 1080/720 */
            max-height: 55vh;
            border: 1px solid #333;
            background: #000;
        }
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: cover; display: none; }

        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.03); }
        .cell.wall { background: transparent !important; } 

        .char { 
            position: absolute; width: 4.16%; height: 2.77%; 
            border-radius: 50%; border: 1px solid white; 
            z-index: 50; display: flex; align-items: center; justify-content: center; 
            transition: transform 0.15s linear; font-size: 12px; 
        }
        .hero { box-shadow: 0 0 10px var(--primary); border: 2px solid var(--primary); z-index: 60; }
        .enemy { background: #500; border-color: #f55; }
        .active-char { filter: brightness(1.5); outline: 2px solid #fff; }

        /* Controlli Mobile Estesi */
        #controls-layer {
            height: 180px;
            width: 100%;
            background: #111;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            border-top: 1px solid #333;
        }

        .d-pad {
            display: grid;
            grid-template-columns: repeat(3, 50px);
            grid-template-rows: repeat(3, 50px);
            gap: 5px;
        }
        .ctrl-btn {
            background: var(--ctrl-bg);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 20px;
            width: 50px; height: 50px;
        }
        .ctrl-btn:active { background: var(--primary); color: black; }

        .action-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .action-btn {
            padding: 15px 25px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 14px;
            border: none;
            min-width: 100px;
        }

        #action-panel { 
            position: absolute; top: 10px; left: 50%; transform: translateX(-50%); 
            background: var(--panel); border: 1px solid var(--primary); 
            padding: 10px; border-radius: 10px; display: none; 
            flex-direction: column; gap: 8px; z-index: 1000; width: 70%;
        }
        
        .log-container { 
            position: absolute; top: 60px; right: 10px; 
            width: 120px; height: 80px; 
            background: rgba(0,0,0,0.6); padding: 5px; 
            font-size: 9px; overflow-y: auto; border-radius: 5px; 
            color: #ccc; pointer-events: none; z-index: 80;
        }
        .loot-icon { position: absolute; z-index: 10; font-size: 16px; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music" loop></audio>

    <div id="setup-screen">
        <div class="card">
            <h1 style="color:var(--primary); margin:0;">ARENA D&D</h1>
            <p style="font-size:10px; color:#aaa; margin-bottom:15px;">SAGA MAPPAT - MOBILE V2</p>
            <div class="input-group">
                <label>Nome Personaggio</label>
                <input type="text" id="p-nome" placeholder="Eroe">
                <label>Razza</label>
                <select id="p-razza">
                    <option value="Umano">Umano</option><option value="Elfo">Elfo</option>
                    <option value="Nano">Nano</option><option value="Tiefling">Tiefling</option>
                </select>
                <label>Classe</label>
                <select id="p-classe">
                    <option value="Guerriero">Guerriero</option><option value="Mago">Mago</option>
                    <option value="Barbaro">Barbaro</option><option value="Ladro">Ladro</option>
                </select>
            </div>
            <button class="start-btn" onclick="iniziaAvventura()">ENTRA ⚔️</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">❤️ <span id="hp-display">0</span></div>
        <div class="stat-badge">💰 <span id="gold-display">0</span></div>
        <div class="stat-badge">🧪 <span id="potion-display">0</span></div>
        <div class="stat-badge">👣 <span id="moves-display">6</span></div>
        <div style="font-size:10px; color:var(--primary)">MAP <span id="map-name-display">1</span></div>
    </div>

    <div id="game-viewport">
        <div id="game-container">
            <div id="map-bg-container">
                <img id="map-img" class="map-asset">
            </div>
            <div id="grid"></div>
        </div>
        
        <div id="action-panel">
            <div style="font-size:10px; color:var(--primary); text-align:center; margin-bottom:5px;">COMBATTIMENTO</div>
            <div id="weapon-buttons" style="display:flex; flex-direction:column; gap:5px;"></div>
        </div>
        
        <div class="log-container" id="game-log"></div>
    </div>

    <div id="controls-layer">
        <div class="d-pad">
            <div></div><button class="ctrl-btn" onclick="muoviEroeBtn(0, -1)">▲</button><div></div>
            <button class="ctrl-btn" onclick="muoviEroeBtn(-1, 0)">◀</button>
            <button class="ctrl-btn" onclick="muoviEroeBtn(0, 1)">▼</button>
            <button class="ctrl-btn" onclick="muoviEroeBtn(1, 0)">▶</button>
        </div>
        
        <div class="action-group">
            <button class="action-btn" id="btn-potion" onclick="usaPozione()" style="background:var(--success); color:white;">BEVI 🧪</button>
            <button class="action-btn" onclick="prossimoTurno()" style="background:#444; color:white;">PASSA ⏭️</button>
        </div>
    </div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const audioPlayer = document.getElementById('bg-music');

        const RACE_ICONS = { "Umano": "🧔", "Elfo": "🧝", "Nano": "🎅", "Mezzorco": "👹", "Tiefling": "😈" };
        const HP_MAP = { "Barbaro": 12, "Guerriero": 10, "Mago": 6, "Ladro": 8 };
        const WEAPON_CONFIG = {
            "Guerriero": [{ name: "Spada", dice: 8, range: 1.5, icon: "⚔️" }],
            "Mago": [{ name: "Dardo", dice: 4, range: 12, icon: "🪄" }],
            "Barbaro": [{ name: "Ascia", dice: 12, range: 1.5, icon: "🪓" }],
            "Ladro": [{ name: "Pugnale", dice: 6, range: 1.5, icon: "🔪" }]
        };

        let currentMapNumber = 1, entities = [], currentIndex = 0, isCombat = false, activeEntity = null, loots = {};

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
            const razza = document.getElementById('p-razza').value;
            const classe = document.getElementById('p-classe').value;
            let hp = (HP_MAP[classe] || 10) + 20;
            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', razza, classe, 
                x: 12, y: 2, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: RACE_ICONS[razza],
                weapons: WEAPON_CONFIG[classe], inventory: { potions: 1, coins: 0 }
            }];
            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            document.getElementById('map-name-display').innerText = mapNumber;
            isCombat = false;
            document.getElementById('action-panel').style.display = 'none';
            const imgEl = document.getElementById('map-img');
            imgEl.src = BASE_URL + `Maps/${mapNumber}.jpg`;
            imgEl.onload = () => imgEl.style.display = 'block';
            audioPlayer.src = BASE_URL + `Music/${mapNumber}.mp3`;
            audioPlayer.play().catch(e => {});

            try {
                const response = await fetch(`${BASE_URL}Maps/${mapNumber}.json`);
                if (response.ok) applyLevelData(await response.json());
            } catch (e) {}

            const hero = entities.find(e => e.tipo === 'hero');
            hero.x = 12; hero.y = 2; hero.movesRemaining = 6;
            entities = [hero];
            for(let i=0; i < 2; i++) {
                entities.push({
                    nome: "Mob", hp: 10 + (mapNumber*5), tipo: 'enemy', 
                    x: 5 + (i*10), y: 25, dead: false, icon: "👹"
                });
            }
            disegnaEntita();
            aggiornaUI();
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            if (data.walls) data.walls.forEach(idx => { if (cells[idx]) cells[idx].classList.add('wall'); });
            loots = {};
            document.querySelectorAll('.loot-icon').forEach(l => l.remove());
            if (data.loot) data.loot.forEach(item => {
                const el = document.createElement('div');
                el.className = 'loot-icon';
                el.innerText = item.type === 'moneta' ? "💰" : "🧪";
                el.style.width = (100/COLS)+'%'; el.style.height = (100/ROWS)+'%';
                el.style.left = ((item.idx % COLS) * (100/COLS)) + '%';
                el.style.top = (Math.floor(item.idx / COLS) * (100/ROWS)) + '%';
                document.getElementById('game-container').appendChild(el);
                loots[item.idx] = { type: item.type, element: el };
            });
        }

        function disegnaEntita() {
            document.querySelectorAll('.char').forEach(c => c.remove());
            entities.forEach(ent => {
                const el = document.createElement('div');
                el.className = 'char ' + ent.tipo;
                el.innerText = ent.icon;
                if(ent.tipo === 'hero') el.classList.add('hero');
                document.getElementById('game-container').appendChild(el);
                ent.element = el;
                aggiornaPosizione(ent);
            });
        }

        function aggiornaPosizione(ent) {
            ent.element.style.left = (ent.x * (100/COLS)) + '%';
            ent.element.style.top = (ent.y * (100/ROWS)) + '%';
            if (ent.tipo === 'hero') {
                const idx = Math.floor(ent.y) * COLS + Math.floor(ent.x);
                if (loots[idx]) {
                    if (loots[idx].type === 'pozione') ent.inventory.potions++;
                    else ent.inventory.coins += 20;
                    loots[idx].element.remove(); delete loots[idx];
                    aggiornaUI();
                }
            }
        }

        function muoviEroeBtn(dx, dy) {
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero || (isCombat && activeEntity !== hero)) return;
            let nx = hero.x + dx, ny = hero.y + dy;
            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                const cell = document.querySelectorAll('.cell')[ny * COLS + nx];
                if (cell && !cell.classList.contains('wall')) {
                    hero.x = nx; hero.y = ny;
                    if(isCombat) hero.movesRemaining--;
                    aggiornaPosizione(hero);
                    if(!isCombat) {
                        entities.filter(en => en.tipo === 'enemy' && !en.dead).forEach(en => {
                            if(Math.sqrt(Math.pow(en.x-hero.x,2)+Math.pow(en.y-hero.y,2)) < 5) iniziaCombattimento();
                        });
                    }
                    if (hero.y >= ROWS - 1) caricaMappaCompleta(currentMapNumber + 1);
                }
            }
            aggiornaUI();
        }

        function usaPozione() {
            const hero = entities.find(e => e.tipo === 'hero');
            if (hero.inventory.potions > 0) {
                hero.inventory.potions--; hero.hp = Math.min(hero.maxHP, hero.hp + 15);
                addLog("Cura +15"); aggiornaUI();
            }
        }

        function aggiornaUI() {
            const hero = entities.find(e => e.tipo === 'hero');
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
            document.getElementById('gold-display').innerText = hero.inventory.coins;
            document.getElementById('potion-display').innerText = hero.inventory.potions;
            document.getElementById('btn-potion').disabled = hero.inventory.potions <= 0;
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true; addLog("LOTTA!");
            entities.forEach(ent => ent.ini = Math.floor(Math.random()*20)+1);
            entities.sort((a,b) => b.ini - a.ini);
            currentIndex = 0; selezionaTurno();
        }

        function selezionaTurno() {
            if (!isCombat) return;
            entities.forEach(e => e.element.classList.remove('active-char'));
            activeEntity = entities[currentIndex % entities.length];
            if(activeEntity.dead) return prossimoTurno();
            activeEntity.element.classList.add('active-char');
            if(activeEntity.tipo === 'enemy') {
                document.getElementById('action-panel').style.display = 'none';
                setTimeout(turnoIA, 600);
            } else {
                document.getElementById('action-panel').style.display = 'flex';
                renderAzioni();
            }
        }

        function renderAzioni() {
            const hero = entities.find(e => e.tipo === 'hero');
            const container = document.getElementById('weapon-buttons');
            container.innerHTML = '';
            hero.weapons.forEach(w => {
                const b = document.createElement('button');
                b.className = 'action-btn'; b.style.background = '#f1c40f'; b.style.color = 'black';
                b.innerHTML = `${w.icon} ATTACCA`;
                b.onclick = () => attacco(w);
                container.appendChild(b);
            });
        }

        function attacco(w) {
            const hero = entities.find(e => e.tipo === 'hero');
            const target = entities.find(e => e.tipo === 'enemy' && !e.dead);
            if(!target) return;
            if(Math.sqrt(Math.pow(hero.x-target.x,2)+Math.pow(hero.y-target.y,2)) <= w.range) {
                let d = Math.floor(Math.random()*w.dice)+5; target.hp -= d;
                addLog(`Danni: ${d}`);
                if(target.hp <= 0) { target.dead = true; target.element.style.opacity = '0.2'; }
                prossimoTurno();
            } else addLog("Lontano!");
        }

        function turnoIA() {
            if(!isCombat) return;
            const hero = entities.find(e => e.tipo === 'hero');
            if(activeEntity.x < hero.x) activeEntity.x++; else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++; else if(activeEntity.y > hero.y) activeEntity.y--;
            aggiornaPosizione(activeEntity);
            if(Math.sqrt(Math.pow(activeEntity.x-hero.x,2)+Math.pow(activeEntity.y-hero.y,2)) < 1.6) {
                hero.hp -= 5; addLog("Colpito! -5");
                if(hero.hp <= 0) { alert("SCONFITTA"); location.reload(); }
            }
            setTimeout(prossimoTurno, 500);
        }

        function prossimoTurno() { 
            if (entities.filter(e => e.tipo === 'enemy' && !e.dead).length === 0) {
                isCombat = false; document.getElementById('action-panel').style.display = 'none';
                addLog("VITTORIA"); return;
            }
            currentIndex++; selezionaTurno(); 
        }
    </script>
</body>
</html>
"""

# Rendering con altezza 100vh per coprire tutto lo schermo mobile
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" allow="autoplay"></iframe>', height=800)
