import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
GITHUB_BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/"

st.set_page_config(
    page_title="D&D Arena Tablet Vertical", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# CSS per forzare Streamlit a sparire e lasciare spazio al gioco verticale
st.markdown("""
    <style>
        .block-container { padding: 0rem; max-width: 100%; }
        .stApp { background-color: #000; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        iframe { border: none; width: 100vw; height: 100dvh; display: block; }
        [data-testid="stHeader"] {display: none;}
        #MainMenu {visibility: hidden;}
        div[data-testid="stVerticalBlock"] > div:has(iframe) { padding: 0; }
    </style>
""", unsafe_allow_html=True)

# Template HTML/JS/CSS Ottimizzato per Tablet Verticale (Rapporto 24:36)
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>D&D Arena Tablet Vertical</title>
    <style>
        :root {
            --primary: #f1c40f; 
            --bg: #000;
            --panel: rgba(25, 25, 25, 0.98);
            --ctrl-bg: #1a1a1a;
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
            font-family: 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 0;
            display: flex; flex-direction: column; 
            height: 100dvh; width: 100vw;
            overflow: hidden;
        }
        
        /* Setup Screen */
        #setup-screen { 
            position: fixed; inset: 0; 
            background: #111 url('__GITHUB_BASE__Maps/intro.jpg') center/cover; 
            z-index: 5000; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
        }
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.8); z-index: -1; }
        .card { 
            background: var(--panel); border: 2px solid var(--primary); 
            border-radius: 15px; padding: 30px; width: 80%; max-width: 450px; text-align: center; 
        }
        .input-group { margin: 15px 0; display: flex; flex-direction: column; gap: 10px; text-align: left; }
        input, select { 
            background: #111; border: 1px solid #444; color: white; 
            padding: 15px; border-radius: 10px; font-size: 18px; width: 100%;
        }
        .start-btn { 
            background: var(--primary); color: black; border: none; 
            padding: 20px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 22px; cursor: pointer;
        }

        /* Top Bar */
        #ui-top { 
            height: 60px; width: 100%; background: #111; 
            display: flex; justify-content: space-around; align-items: center;
            border-bottom: 2px solid #333; z-index: 1000; flex-shrink: 0;
        }
        .stat-badge { font-weight: bold; font-size: 18px; display: flex; align-items: center; gap: 5px; }

        /* Area Gioco (Verticale) */
        #game-viewport {
            flex: 1;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: #050505;
            overflow: hidden;
        }
        #game-container { 
            position: relative; 
            height: 100%;
            aspect-ratio: 24 / 36; /* Forza il verticale 2:3 */
            background: #000;
            box-shadow: 0 0 30px rgba(0,0,0,1);
            border: 1px solid #333;
        }
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: fill; display: none; }
        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.02); }
        .cell.wall { background: transparent !important; }

        /* Personaggi */
        .char { 
            position: absolute; width: 4.16%; height: 2.77%; 
            border-radius: 50%; border: 1px solid white; 
            z-index: 50; display: flex; align-items: center; justify-content: center; 
            transition: transform 0.1s linear; font-size: 14px; 
        }
        .hero { box-shadow: 0 0 15px var(--primary); border: 2px solid var(--primary); z-index: 100; }
        .enemy { background: #800; border-color: #f88; }
        .active-char { border-color: #fff; box-shadow: 0 0 20px #fff; z-index: 110; }

        /* Controlli Tablet Inferiori */
        #controls-area {
            height: 240px; width: 100%;
            background: #111;
            display: flex; justify-content: space-around; align-items: center;
            padding: 15px; border-top: 2px solid #333; flex-shrink: 0;
        }
        .d-pad {
            display: grid; grid-template-columns: repeat(3, 70px); grid-template-rows: repeat(3, 70px);
            gap: 10px;
        }
        .ctrl-btn {
            background: var(--ctrl-bg); border: 2px solid #444; border-radius: 15px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 30px; width: 70px; height: 70px;
        }
        .ctrl-btn:active { background: var(--primary); color: black; transform: scale(0.95); }

        .actions-group { display: flex; flex-direction: column; gap: 15px; }
        .action-btn {
            width: 150px; height: 85px; border-radius: 15px; border: none;
            font-weight: bold; font-size: 16px; color: white; cursor: pointer;
            box-shadow: 0 5px 0 #000;
        }
        .action-btn:active { transform: translateY(3px); box-shadow: none; }

        /* Pannello Combattimento */
        #action-panel { 
            position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); 
            background: var(--panel); border: 3px solid var(--primary); 
            padding: 15px; border-radius: 15px; display: none; 
            flex-direction: column; gap: 10px; z-index: 2000; width: 320px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        }
        
        .log-box { 
            position: absolute; top: 10px; right: 10px; width: 200px; height: 110px; 
            background: rgba(0,0,0,0.8); padding: 10px; font-size: 11px; 
            overflow-y: hidden; border-radius: 10px; color: #ccc; pointer-events: none; 
            z-index: 1000; border: 1px solid #333;
        }
        .loot-icon { position: absolute; z-index: 10; font-size: 24px; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music" loop></audio>

    <div id="setup-screen">
        <div class="card">
            <h1 style="color:var(--primary); margin:0; font-size: 36px;">D&D ARENA</h1>
            <p style="color:#aaa; margin-top:5px;">SAGA MAPPAT - TABLET VERTICAL</p>
            <div class="input-group">
                <label>Nome Eroe</label>
                <input type="text" id="p-nome" placeholder="Inserisci nome...">
                <label>Classe</label>
                <select id="p-classe">
                    <option value="Guerriero">Guerriero ⚔️</option>
                    <option value="Mago">Mago 🪄</option>
                    <option value="Barbaro">Barbaro 🪓</option>
                    <option value="Ladro">Ladro 🔪</option>
                </select>
            </div>
            <button class="start-btn" onclick="iniziaAvventura()">ENTRA NEL DUNGEON ⚔️</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">❤️ <span id="hp-display">0</span></div>
        <div class="stat-badge">💰 <span id="gold-display">0</span></div>
        <div class="stat-badge">🧪 <span id="potion-display">0</span></div>
        <div class="stat-badge">👣 <span id="moves-display">6</span></div>
    </div>

    <div id="game-viewport">
        <div id="game-container">
            <div id="map-bg-container">
                <img id="map-img" class="map-asset">
            </div>
            <div id="grid"></div>
        </div>
        
        <div id="action-panel">
            <div style="font-size:14px; color:var(--primary); text-align:center; font-weight:bold; margin-bottom:5px;">Tuo Turno</div>
            <div id="weapon-buttons" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>
        
        <div class="log-box" id="game-log"></div>
    </div>

    <div id="controls-area">
        <div class="d-pad">
            <div></div><button class="ctrl-btn" onclick="muoviEroeBtn(0, -1)">▲</button><div></div>
            <button class="ctrl-btn" onclick="muoviEroeBtn(-1, 0)">◀</button>
            <button class="ctrl-btn" onclick="muoviEroeBtn(0, 1)">▼</button>
            <button class="ctrl-btn" onclick="muoviEroeBtn(1, 0)">▶</button>
        </div>
        
        <div class="actions-group">
            <button class="action-btn" id="btn-potion" onclick="usaPozione()" style="background:#2ecc71;">CURA 🧪</button>
            <button class="action-btn" onclick="prossimoTurno()" style="background:#444;">PASSA ⏭️</button>
        </div>
    </div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const audioPlayer = document.getElementById('bg-music');

        const HP_MAP = { "Barbaro": 12, "Guerriero": 10, "Mago": 6, "Ladro": 8 };
        const WEAPON_CONFIG = {
            "Guerriero": [{ name: "Spada Lunga", dice: 8, range: 1.5, icon: "⚔️" }],
            "Mago": [{ name: "Dardo Incantato", dice: 4, range: 12, icon: "🪄" }],
            "Barbaro": [{ name: "Ascia Bipenne", dice: 12, range: 1.5, icon: "🪓" }],
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
            log.innerHTML = `<div>> ${msg}</div>` + log.innerHTML;
        }

        function iniziaAvventura() {
            document.getElementById('setup-screen').style.display = 'none';
            const grid = document.getElementById("grid");
            grid.innerHTML = "";
            for (let i = 0; i < COLS * ROWS; i++) {
                const c = document.createElement("div"); c.className = "cell"; grid.appendChild(c);
            }
            const nome = document.getElementById('p-nome').value || "Eroe";
            const classe = document.getElementById('p-classe').value;
            let hp = (HP_MAP[classe] || 10) + 20;
            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', classe, 
                x: 12, y: 3, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: "👤",
                weapons: WEAPON_CONFIG[classe], inventory: { potions: 1, coins: 0 }
            }];
            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
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
                else applyLevelData({});
            } catch (e) { applyLevelData({}); }

            const hero = entities.find(e => e.tipo === 'hero');
            hero.x = 12; hero.y = 3; hero.movesRemaining = 6;
            entities = [hero];
            for(let i=0; i < 2; i++) {
                entities.push({
                    nome: "Mostro", hp: 10 + (mapNumber*6), tipo: 'enemy', 
                    x: 6 + (i*10), y: 24, dead: false, icon: "👹"
                });
            }
            disegnaEntita();
            aggiornaUI();
            addLog("Area " + mapNumber + " caricata.");
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
                    else ent.inventory.coins += 25;
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
                hero.inventory.potions--; 
                hero.hp = Math.min(hero.maxHP, hero.hp + 15);
                addLog("Cura effettuata (+15 HP)"); 
                aggiornaUI();
            }
        }

        function aggiornaUI() {
            const hero = entities.find(e => e.tipo === 'hero');
            if(!hero) return;
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
            document.getElementById('gold-display').innerText = hero.inventory.coins;
            document.getElementById('potion-display').innerText = hero.inventory.potions;
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true; 
            addLog("COMBATTIMENTO ATTIVATO!");
            entities.forEach(ent => ent.ini = Math.floor(Math.random()*20)+1);
            entities.sort((a,b) => b.ini - a.ini);
            currentIndex = 0; selezionaTurno();
        }

        function selezionaTurno() {
            if (!isCombat) return;
            entities.forEach(e => { if(e.element) e.element.classList.remove('active-char'); });
            activeEntity = entities[currentIndex % entities.length];
            if(!activeEntity || activeEntity.dead) return prossimoTurno();
            activeEntity.element.classList.add('active-char');
            
            const panel = document.getElementById('action-panel');
            if(activeEntity.tipo === 'enemy') {
                panel.style.display = 'none';
                setTimeout(turnoIA, 700);
            } else {
                panel.style.display = 'flex';
                renderAzioni();
            }
        }

        function renderAzioni() {
            const hero = entities.find(e => e.tipo === 'hero');
            const container = document.getElementById('weapon-buttons');
            container.innerHTML = '';
            hero.weapons.forEach(w => {
                const b = document.createElement('button');
                b.style.padding = '15px'; b.style.borderRadius = '10px'; b.style.border = 'none';
                b.style.background = '#f1c40f'; b.style.fontWeight = 'bold'; b.style.fontSize = '16px';
                b.innerHTML = `${w.icon} ATTACCA (${w.name})`;
                b.onclick = () => attacco(w);
                container.appendChild(b);
            });
        }

        function attacco(w) {
            const hero = entities.find(e => e.tipo === 'hero');
            const target = entities.find(e => e.tipo === 'enemy' && !e.dead);
            if(!target) return;
            if(Math.sqrt(Math.pow(hero.x-target.x,2)+Math.pow(hero.y-target.y,2)) <= w.range) {
                let d = Math.floor(Math.random()*w.dice)+6; 
                target.hp -= d;
                addLog(`Danni inflitti: ${d}`);
                if(target.hp <= 0) { 
                    target.dead = true; 
                    target.element.style.opacity = '0.2';
                    addLog("Nemico abbattuto!");
                }
                prossimoTurno();
            } else addLog("Fuori portata!");
        }

        function turnoIA() {
            if(!isCombat || !activeEntity || activeEntity.dead) return prossimoTurno();
            const hero = entities.find(e => e.tipo === 'hero');
            if(activeEntity.x < hero.x) activeEntity.x++; else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++; else if(activeEntity.y > hero.y) activeEntity.y--;
            aggiornaPosizione(activeEntity);
            if(Math.sqrt(Math.pow(activeEntity.x-hero.x,2)+Math.pow(activeEntity.y-hero.y,2)) < 1.6) {
                let d = Math.floor(Math.random()*5)+3;
                hero.hp -= d; addLog(`Colpito dal mostro: -${d} HP`);
                if(hero.hp <= 0) { alert("SCONFITTA! L'eroe è caduto."); location.reload(); }
            }
            setTimeout(prossimoTurno, 600);
        }

        function prossimoTurno() { 
            if (entities.filter(e => e.tipo === 'enemy' && !e.dead).length === 0) {
                isCombat = false; 
                document.getElementById('action-panel').style.display = 'none';
                entities.forEach(e => { if(e.element) e.element.classList.remove('active-char'); });
                addLog("VITTORIA!"); return;
            }
            currentIndex++; selezionaTurno(); 
        }
    </script>
</body>
</html>
"""

# Rendering finale con altezza corretta per iframe Streamlit su Tablet
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" allow="autoplay"></iframe>', height=1080)
