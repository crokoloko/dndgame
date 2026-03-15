import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
GITHUB_BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/"

st.set_page_config(page_title="D&D Arena Mobile", layout="wide", initial_sidebar_state="collapsed")

# CSS per pulire l'interfaccia Streamlit e adattarla al mobile
st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        .stApp { background-color: #050505; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        iframe { border: none; width: 100%; height: 100vh; }
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Template HTML/JS/CSS ottimizzato per Mobile
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>D&D Arena Mobile</title>
    <style>
        :root {
            --primary: #f1c40f; --secondary: #2c3e50; --danger: #e74c3c;
            --success: #2ecc71; --info: #3498db; --bg: #050505;
            --panel: rgba(20, 20, 20, 0.98);
        }
        * { touch-action: manipulation; }
        body { 
            background-color: var(--bg); color: #eee; 
            font-family: 'Segoe UI', sans-serif; margin: 0; 
            display: flex; flex-direction: column; align-items: center; 
            overflow: hidden; height: 100vh; width: 100vw;
        }
        
        #setup-screen { position: fixed; inset: 0; background: #111 url('__GITHUB_BASE__Maps/intro.jpg') center/cover; z-index: 2000; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.75); z-index: -1; }
        
        .card { background: rgba(26, 26, 26, 0.95); border: 2px solid var(--primary); border-radius: 12px; padding: 20px; width: 85%; max-width: 400px; text-align: center; }
        
        .input-group { margin: 10px 0; display: flex; flex-direction: column; gap: 5px; text-align: left; }
        label { font-size: 12px; color: var(--primary); font-weight: bold; }
        input, select { background: #222; border: 1px solid #444; color: white; padding: 12px; border-radius: 6px; font-size: 16px; width: 100%; box-sizing: border-box; }
        
        button { background: var(--primary); color: black; border: none; padding: 14px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; }
        
        #ui-top { width: 100%; background: #111; padding: 5px; display: flex; justify-content: center; flex-wrap: wrap; border-bottom: 1px solid #333; z-index: 100; gap: 5px; }
        .stat-badge { background: #222; padding: 4px 8px; border-radius: 15px; border: 1px solid #444; font-size: 11px; display: flex; align-items: center; gap: 4px; }

        #game-container { 
            position: relative; 
            width: 95vw; 
            height: calc(95vw * (1080 / 720)); 
            max-height: 65vh;
            margin-top: 5px; border: 2px solid #333; overflow: hidden; background: #000; 
        }
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: cover; display: none; }

        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.01); }
        .cell.wall { background: transparent !important; } 

        .char { position: absolute; width: 4%; height: 2.7%; border-radius: 50%; border: 1px solid white; z-index: 50; display: flex; align-items: center; justify-content: center; transition: transform 0.2s; font-size: 12px; }
        .hero { box-shadow: 0 0 10px var(--primary); border-width: 2px; }
        .enemy { background: #5a0000; border-color: #ff4444; }
        
        /* D-PAD MOBILE */
        #mobile-controls {
            position: fixed; bottom: 20px; left: 20px;
            display: grid; grid-template-columns: repeat(3, 60px); grid-template-rows: repeat(2, 60px);
            gap: 10px; z-index: 1000;
        }
        .joy-btn {
            background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-size: 24px; color: white; width: 60px; height: 60px;
        }
        .joy-btn:active { background: var(--primary); color: black; }

        #action-panel { position: fixed; top: 100px; left: 50%; transform: translateX(-50%); background: var(--panel); border: 2px solid var(--primary); padding: 10px; border-radius: 12px; display: none; flex-direction: column; gap: 8px; z-index: 1500; width: 80%; max-width: 300px; box-shadow: 0 5px 20px rgba(0,0,0,0.8); }
        
        .log-container { position: fixed; bottom: 10px; right: 10px; width: 140px; height: 100px; background: rgba(0,0,0,0.7); padding: 8px; font-size: 10px; overflow-y: auto; border-radius: 8px; color: #ccc; pointer-events: none; }
        .loot-icon { position: absolute; z-index: 10; font-size: 18px; display: flex; align-items: center; justify-content: center; }
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music" loop></audio>

    <div id="setup-screen">
        <div class="card">
            <h1 style="color:var(--primary); margin:0; font-size: 24px;">Arena del Destino</h1>
            <p style="font-size:12px; color:#aaa;">Edizione Mobile</p>
            <div class="input-group">
                <label>Nome Eroe</label>
                <input type="text" id="p-nome" placeholder="Nome...">
                <label>Razza</label>
                <select id="p-razza">
                    <option value="Umano">Umano</option><option value="Elfo">Elfo</option><option value="Nano">Nano</option>
                    <option value="Mezzorco">Mezzorco</option><option value="Tiefling">Tiefling</option>
                </select>
                <label>Classe</label>
                <select id="p-classe">
                    <option value="Guerriero">Guerriero</option><option value="Mago">Mago</option><option value="Ladro">Ladro</option><option value="Barbaro">Barbaro</option>
                </select>
            </div>
            <button onclick="iniziaAvventura()">GIOCA ORA ⚔️</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">❤️ <span id="hp-display">0</span></div>
        <div class="stat-badge">💰 <span id="gold-display">0</span></div>
        <div class="stat-badge">🧪 <span id="potion-display">0</span></div>
        <button id="btn-use-potion" onclick="usaPozione()" style="padding: 4px 8px; font-size: 10px;">BEVI</button>
        <div class="stat-badge">👣 <span id="moves-display">6</span></div>
    </div>

    <div id="game-container">
        <div id="map-bg-container">
            <img id="map-img" class="map-asset">
        </div>
        <div id="grid"></div>
    </div>

    <!-- CONTROLLI MOBILE -->
    <div id="mobile-controls">
        <div></div><button class="joy-btn" onclick="muoviEroeBtn(0, -1)">▲</button><div></div>
        <button class="joy-btn" onclick="muoviEroeBtn(-1, 0)">◀</button>
        <button class="joy-btn" onclick="muoviEroeBtn(0, 1)">▼</button>
        <button class="joy-btn" onclick="muoviEroeBtn(1, 0)">▶</button>
    </div>

    <div id="action-panel">
        <div style="font-size:11px; color:var(--primary); font-weight:bold; text-align:center;">AZIONI</div>
        <div id="weapon-buttons" style="display:flex; flex-direction:column; gap:5px;"></div>
        <button onclick="prossimoTurno()" style="background:#422; color:white; margin-top:5px; font-size:12px; padding:8px;">Passa</button>
    </div>

    <div class="log-container" id="game-log"></div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const audioPlayer = document.getElementById('bg-music');

        const RACE_ICONS = { "Umano": "🧔", "Elfo": "🧝", "Nano": "🎅", "Halfling": "👦", "Dragonide": "🐲", "Gnomo": "🧙‍♂️", "Mezzelfo": "🧝‍♂️", "Mezzorco": "👹", "Tiefling": "😈" };
        const HP_MAP = { "Barbaro": 12, "Guerriero": 10, "Paladino": 10, "Ranger": 10, "Chierico": 8, "Ladro": 8, "Bardo": 8, "Druido": 8, "Monaco": 8, "Warlock": 8, "Mago": 6, "Stregone": 6 };
        
        const WEAPON_CONFIG = {
            "Barbaro": [{ name: "Ascia", dice: 12, range: 1.5, icon: "🪓" }],
            "Guerriero": [{ name: "Spada", dice: 8, range: 1.5, icon: "⚔️" }],
            "Mago": [{ name: "Dardo", dice: 4, range: 12, icon: "🪄" }],
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
            let hp = (HP_MAP[classe] || 10) + 15;
            if(razza === "Nano") hp += 5;

            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', razza, classe, 
                x: 12, y: 2, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: RACE_ICONS[razza],
                weapons: WEAPON_CONFIG[classe] || WEAPON_CONFIG["Guerriero"],
                inventory: { potions: 1, coins: 0 }
            }];

            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            isCombat = false;
            document.getElementById('action-panel').style.display = 'none';

            const imgEl = document.getElementById('map-img');
            imgEl.style.display = 'none';
            const extensions = ['jpg', 'png', 'jpeg'];
            let loaded = false;
            for (let ext of extensions) {
                if (loaded) break;
                const testUrl = `${BASE_URL}Maps/${mapNumber}.${ext}`;
                try {
                    const check = await fetch(testUrl, { method: 'HEAD' });
                    if (check.ok) { imgEl.src = testUrl; imgEl.style.display = 'block'; loaded = true; }
                } catch(e) {}
            }

            audioPlayer.src = BASE_URL + "Music/" + mapNumber + ".mp3";
            audioPlayer.play().catch(e => {});

            try {
                const response = await fetch(`${BASE_URL}Maps/${mapNumber}.json`);
                if (response.ok) applyLevelData(await response.json());
                else applyLevelData({});
            } catch (e) { applyLevelData({}); }

            const hero = entities.find(e => e.tipo === 'hero');
            hero.x = 12; hero.y = 2; hero.movesRemaining = 6;
            
            entities = [hero];
            let enemyCount = 1 + Math.floor(mapNumber / 2);
            for(let i=0; i<enemyCount; i++) {
                entities.push({
                    nome: "Nemico", hp: 8 + (mapNumber*5), 
                    tipo: 'enemy', x: Math.floor(Math.random()*18)+3, 
                    y: Math.floor(Math.random()*15)+18, 
                    movesRemaining: 4, dead: false, element: null,
                    icon: "👹"
                });
            }
            disegnaEntita();
            aggiornaUI();
            addLog("Mappa " + mapNumber);
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            if (data.walls) data.walls.forEach(idx => { if (cells[idx]) cells[idx].classList.add('wall'); });

            loots = {};
            document.querySelectorAll('.loot-icon').forEach(l => l.remove());
            if (data.loot) data.loot.forEach(item => spawnLoot(parseInt(item.idx), item.type));
        }

        function spawnLoot(idx, type) {
            const el = document.createElement('div');
            el.className = 'loot-icon';
            el.innerText = type === 'moneta' ? "💰" : "🧪";
            el.style.width = (100/COLS) + '%'; el.style.height = (100/ROWS) + '%';
            el.style.left = ((idx % COLS) * (100/COLS)) + '%';
            el.style.top = (Math.floor(idx / COLS) * (100/ROWS)) + '%';
            document.getElementById('game-container').appendChild(el);
            loots[idx] = { type, element: el };
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
            if(!ent.element) return;
            ent.element.style.left = (ent.x * (100/COLS)) + '%';
            ent.element.style.top = (ent.y * (100/ROWS)) + '%';
            
            if (ent.tipo === 'hero') {
                const idx = Math.floor(ent.y) * COLS + Math.floor(ent.x);
                if (loots[idx]) {
                    if (loots[idx].type === 'pozione') ent.inventory.potions++;
                    else ent.inventory.coins += 15;
                    loots[idx].element.remove();
                    delete loots[idx];
                    aggiornaUI();
                }
            }
        }

        function muoviEroeBtn(dx, dy) {
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero || hero.dead || (isCombat && activeEntity !== hero)) return;
            
            let nx = hero.x + dx, ny = hero.y + dy;
            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                const cell = document.querySelectorAll('.cell')[ny * COLS + nx];
                if (cell && !cell.classList.contains('wall')) {
                    hero.x = nx; hero.y = ny;
                    if(isCombat) hero.movesRemaining--;
                    aggiornaPosizione(hero);
                    if(!isCombat) {
                        entities.filter(en => en.tipo === 'enemy' && !en.dead).forEach(en => {
                            if(Math.sqrt(Math.pow(en.x-hero.x, 2) + Math.pow(en.y-hero.y, 2)) < 5) iniziaCombattimento();
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
                addLog("Cura +15 HP");
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
            document.getElementById('btn-use-potion').disabled = hero.inventory.potions <= 0;
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true;
            addLog("LOTTA!");
            entities.forEach(ent => ent.ini = Math.floor(Math.random()*20)+1);
            entities.sort((a,b) => b.ini - a.ini);
            currentIndex = 0;
            selezionaTurno();
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
                setTimeout(turnoIA, 600);
            } else {
                panel.style.display = 'flex';
                renderAzioni();
            }
            aggiornaUI();
        }

        function renderAzioni() {
            const hero = entities.find(e => e.tipo === 'hero');
            const btnContainer = document.getElementById('weapon-buttons');
            btnContainer.innerHTML = '';
            hero.weapons.forEach(weapon => {
                const btn = document.createElement('button');
                btn.innerHTML = `${weapon.icon} ${weapon.name}`;
                btn.onclick = () => attaccaConArma(weapon);
                btnContainer.appendChild(btn);
            });
        }

        function attaccaConArma(weapon) {
            const hero = entities.find(e => e.tipo === 'hero');
            const target = entities.find(e => e.tipo === 'enemy' && !e.dead);
            if(!target) return;
            let dist = Math.sqrt(Math.pow(hero.x - target.x, 2) + Math.pow(hero.y - target.y, 2));
            if(dist <= weapon.range) {
                let dmg = Math.floor(Math.random() * weapon.dice) + 5;
                target.hp -= dmg;
                addLog(`Danni: ${dmg}`);
                if(target.hp <= 0) {
                    target.dead = true; target.element.style.opacity = "0.2";
                    spawnLoot(Math.floor(target.y)*COLS+Math.floor(target.x), 'moneta');
                    controllaFineCombattimento();
                }
                document.getElementById('action-panel').style.display = 'none';
                prossimoTurno();
            } else addLog("Lontano!");
        }

        function controllaFineCombattimento() {
            if (entities.filter(e => e.tipo === 'enemy' && !e.dead).length === 0) {
                isCombat = false;
                document.getElementById('action-panel').style.display = 'none';
                addLog("Vittoria!");
                aggiornaUI();
            }
        }

        function turnoIA() {
            if(!isCombat || !activeEntity || activeEntity.dead) return prossimoTurno();
            const hero = entities.find(e => e.tipo === 'hero');
            if(activeEntity.x < hero.x) activeEntity.x++; else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++; else if(activeEntity.y > hero.y) activeEntity.y--;
            aggiornaPosizione(activeEntity);
            if(Math.sqrt(Math.pow(activeEntity.x - hero.x, 2) + Math.pow(activeEntity.y - hero.y, 2)) < 1.6) {
                let dmg = Math.floor(Math.random()*6)+2;
                hero.hp -= dmg; addLog(`Subisci ${dmg}`);
                if(hero.hp <= 0) { alert("Sconfitta!"); location.reload(); }
            }
            setTimeout(prossimoTurno, 500);
        }

        function prossimoTurno() { if(isCombat) { currentIndex++; selezionaTurno(); } }
    </script>
</body>
</html>
"""

# Rendering
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)
b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
components.html(f'<iframe src="data:text/html;base64,{b64_html}" allow="autoplay"></iframe>', height=800)
