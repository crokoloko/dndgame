import streamlit as st
import streamlit.components.v1 as components
import base64

# --- CONFIGURAZIONE REPOSITORY ---
USER = "crokoloko"
REPO = "dndgame"
BRANCH = "main"
GITHUB_BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/"

st.set_page_config(
    page_title="D&D Arena PC Edition", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# CSS per pulire l'interfaccia Streamlit e ottimizzare lo spazio per PC
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        .stApp { background-color: #050505; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
        #MainMenu {visibility: hidden;}
        iframe { 
            width: 100% !important; 
            height: 98vh !important; 
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Template HTML/JS/CSS - NOTA: NON è una f-string per evitare conflitti con le graffe {}
html_template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D&D Arena PC Edition</title>
    <style>
        :root {
            --primary: #f1c40f; 
            --danger: #e74c3c;
            --success: #2ecc71; 
            --bg: #050505;
            --panel: rgba(20, 20, 20, 0.95);
        }
        body, html { 
            background-color: var(--bg); 
            color: #eee; 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 0; padding: 0;
            height: 100%; width: 100%;
            overflow: hidden;
        }
        
        body { display: flex; flex-direction: column; }
        
        #setup-screen { 
            position: absolute; top: 0; left: 0; 
            width: 100%; height: 100%;
            background: #111 url('__GITHUB_BASE__Maps/intro.jpg') center/cover; 
            z-index: 5000; 
            display: flex; flex-direction: column; align-items: center; justify-content: center; 
        }
        #setup-screen::before { content: ""; position: absolute; inset: 0; background: rgba(0, 0, 0, 0.75); z-index: -1; }
        
        .card { 
            background: var(--panel); border: 2px solid var(--primary); 
            border-radius: 15px; padding: 30px; width: 95%; max-width: 600px; 
            text-align: center; box-shadow: 0 0 50px rgba(0,0,0,0.8); z-index: 5001;
        }
        
        .setup-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
        .input-group { display: flex; flex-direction: column; gap: 8px; text-align: left; }
        label { font-size: 13px; color: var(--primary); font-weight: bold; text-transform: uppercase; }
        input, select { 
            background: #111; border: 1px solid #444; color: white; 
            padding: 10px; border-radius: 8px; font-size: 15px; width: 100%;
        }
        
        .start-btn { 
            background: var(--primary); color: black; border: none; 
            padding: 18px; border-radius: 10px; font-weight: bold; width: 100%; font-size: 20px; cursor: pointer;
            transition: 0.3s; margin-top: 10px;
        }
        .start-btn:hover { background: #fff; transform: translateY(-2px); }

        #ui-top { 
            height: 70px; width: 100%; background: #111; 
            display: flex; justify-content: center; align-items: center;
            border-bottom: 2px solid #333; z-index: 1000; gap: 20px; flex-shrink: 0;
        }
        .stat-badge { font-weight: bold; font-size: 17px; display: flex; align-items: center; gap: 8px; padding: 5px 12px; background: #222; border-radius: 10px; border: 1px solid #444; }

        #main-layout { display: flex; flex: 1; width: 100%; height: calc(100% - 70px); overflow: hidden; }

        #game-viewport { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; background: #000; padding: 15px; }
        #game-container { 
            position: relative; height: 100%; aspect-ratio: 24 / 36;
            background: #111; box-shadow: 0 0 40px rgba(0,0,0,1); border: 2px solid #333;
        }
        
        #map-bg-container { position: absolute; inset: 0; z-index: 1; }
        .map-asset { width: 100%; height: 100%; object-fit: fill; display: none; }
        #grid { position: absolute; inset: 0; display: grid; grid-template-columns: repeat(24, 1fr); grid-template-rows: repeat(36, 1fr); z-index: 5; pointer-events: none; }
        .cell { border: 1px solid rgba(255,255,255,0.02); }

        .char { 
            position: absolute; width: 4.16%; height: 2.77%; 
            border-radius: 50%; border: 1px solid white; 
            z-index: 50; display: flex; align-items: center; justify-content: center; 
            transition: transform 0.1s linear; font-size: 16px; 
        }
        .hero { box-shadow: 0 0 15px var(--primary); border: 2px solid var(--primary); z-index: 100; background: rgba(241, 196, 15, 0.2); }
        .enemy { background: #800; border-color: #f88; }
        .active-char { border-color: #fff; box-shadow: 0 0 25px #fff; z-index: 110; outline: 2px solid #fff; }

        #side-panel { width: 340px; background: #111; border-left: 2px solid #333; display: flex; flex-direction: column; padding: 20px; gap: 15px; flex-shrink: 0; }
        .action-card { background: #222; border: 1px solid var(--primary); border-radius: 12px; padding: 15px; text-align: center; }
        #log-box { flex: 1; background: #000; border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: 12px; overflow-y: auto; color: #aaa; font-family: 'Courier New', monospace; }
        .log-entry { margin-bottom: 4px; border-bottom: 1px solid #1a1a1a; padding-bottom: 2px; }

        .pc-btn { background: var(--primary); color: black; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-bottom: 8px; font-size: 15px; }
        .pc-btn:hover { background: #fff; }
        .pc-btn:disabled { background: #444; color: #888; cursor: not-allowed; }

        .loot-icon { position: absolute; z-index: 10; font-size: 22px; display: flex; align-items: center; justify-content: center; pointer-events: none; animation: float 2s infinite ease-in-out; }
        @keyframes float { 0% { transform: translateY(0); } 50% { transform: translateY(-5px); } 100% { transform: translateY(0); } }
        
        kbd { background: #444; border-radius: 4px; border: 1px solid #666; color: #fff; padding: 2px 6px; font-size: 11px; margin: 0 2px; }
    </style>
</head>
<body onclick="playIntroOnce()">
    <audio id="bg-music" loop></audio>

    <div id="setup-screen">
        <div class="card">
            <h1 style="color:var(--primary); margin:0; font-size: 40px;">D&D ARENA</h1>
            <p style="color:#aaa; font-weight:bold; letter-spacing: 2px;">SAGA MAPPAT - PC DEFINITIVA</p>
            
            <div class="setup-grid">
                <div class="input-group">
                    <label>Nome Eroe</label>
                    <input type="text" id="p-nome" placeholder="Eroe">
                </div>
                <div class="input-group">
                    <label>Razza</label>
                    <select id="p-razza">
                        <option value="Umano">Umano</option><option value="Elfo">Elfo</option>
                        <option value="Nano">Nano</option><option value="Halfling">Halfling</option>
                        <option value="Dragonide">Dragonide</option><option value="Gnomo">Gnomo</option>
                        <option value="Mezzelfo">Mezzelfo</option><option value="Mezzorco">Mezzorco</option>
                        <option value="Tiefling">Tiefling</option>
                    </select>
                </div>
                <div class="input-group" style="grid-column: span 2;">
                    <label>Classe</label>
                    <select id="p-classe">
                        <option value="Barbaro">Barbaro (🪓 Ascia)</option>
                        <option value="Guerriero">Guerriero (⚔️ Spada)</option>
                        <option value="Paladino">Paladino (🔨 Martello)</option>
                        <option value="Ranger">Ranger (🏹 Arco)</option>
                        <option value="Chierico">Chierico (🏏 Mazza)</option>
                        <option value="Ladro">Ladro (🔪 Pugnale)</option>
                        <option value="Bardo">Bardo (🤺 Stocco)</option>
                        <option value="Druido">Druido (🦯 Bastone)</option>
                        <option value="Monaco">Monaco (👊 Pugni)</option>
                        <option value="Warlock">Warlock (💜 Deflagrazione)</option>
                        <option value="Mago">Mago (🪄 Dardo Incantato)</option>
                        <option value="Stregone">Stregone (☄️ Dardo di Fuoco)</option>
                    </select>
                </div>
            </div>
            <button class="start-btn" onclick="iniziaAvventura()">COMINCIA LA SAGA ⚔️</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">❤️ <span id="hp-display">0</span> HP</div>
        <div class="stat-badge">💰 <span id="gold-display">0</span> ORO</div>
        <div class="stat-badge">🧪 <span id="potion-display">0</span> POZIONI</div>
        <div class="stat-badge">👣 <span id="moves-display">6</span> PASSI</div>
        <div style="font-size: 13px; color: var(--primary);">AREA: <span id="map-name-display">1</span></div>
    </div>

    <div id="main-layout">
        <div id="game-viewport">
            <div id="game-container">
                <div id="map-bg-container">
                    <img id="map-img" class="map-asset">
                </div>
                <div id="grid"></div>
            </div>
        </div>

        <div id="side-panel">
            <div class="action-card">
                <h3 style="color:var(--primary); margin-top:0; font-size: 16px;">AZIONI</h3>
                <div id="weapon-buttons" style="display:flex; flex-direction:column; gap:8px;"></div>
                <hr style="border:0; border-top:1px solid #444; margin:12px 0;">
                <button class="pc-btn" id="btn-potion" onclick="usaPozione()">USA POZIONE (P)</button>
                <button class="pc-btn" onclick="prossimoTurno()" style="background:#444; color:white;">PASSA TURNO (SPAZIO)</button>
            </div>

            <div id="log-box"></div>

            <div style="font-size:10px; color:#555; text-align:center;">
                Comandi: <kbd>WASD</kbd> muovi | <kbd>P</kbd> cura | <kbd>Space</kbd> passa
            </div>
        </div>
    </div>

    <script>
        const BASE_URL = "__GITHUB_BASE__";
        const COLS = 24, ROWS = 36;
        const audioPlayer = document.getElementById('bg-music');

        const RACE_ICONS = { "Umano": "🧔", "Elfo": "🧝", "Nano": "🎅", "Halfling": "👦", "Dragonide": "🐲", "Gnomo": "🧙‍♂️", "Mezzelfo": "🧝‍♂️", "Mezzorco": "👹", "Tiefling": "😈" };
        const HP_MAP = { "Barbaro": 14, "Guerriero": 12, "Paladino": 12, "Ranger": 10, "Chierico": 10, "Ladro": 10, "Bardo": 8, "Druido": 8, "Monaco": 8, "Warlock": 8, "Mago": 6, "Stregone": 6 };
        
        const WEAPON_CONFIG = {
            "Barbaro": [{ name: "Ascia Bipenne", dice: 12, range: 1.5, icon: "🪓" }],
            "Guerriero": [{ name: "Spada Lunga", dice: 8, range: 1.5, icon: "⚔️" }],
            "Paladino": [{ name: "Martello Guerra", dice: 10, range: 1.5, icon: "🔨" }],
            "Ranger": [{ name: "Arco Lungo", dice: 8, range: 12, icon: "🏹" }],
            "Chierico": [{ name: "Mazza Pesante", dice: 6, range: 1.5, icon: "🏏" }],
            "Ladro": [{ name: "Pugnale", dice: 6, range: 1.5, icon: "🔪" }],
            "Bardo": [{ name: "Stocco", dice: 8, range: 1.5, icon: "🤺" }],
            "Druido": [{ name: "Bastone", dice: 6, range: 1.5, icon: "🦯" }],
            "Monaco": [{ name: "Pugni", dice: 6, range: 1.5, icon: "👊" }],
            "Warlock": [{ name: "Deflagrazione", dice: 10, range: 10, icon: "💜" }],
            "Mago": [{ name: "Dardo Incantato", dice: 4, range: 12, icon: "🪄" }],
            "Stregone": [{ name: "Dardo di Fuoco", dice: 10, range: 10, icon: "☄️" }]
        };

        let currentMapNumber = 1, entities = [], currentIndex = 0, isCombat = false, activeEntity = null, loots = {};

        function playIntroOnce() {
            if (audioPlayer.paused) {
                audioPlayer.src = BASE_URL + "Music/intro.mp3";
                audioPlayer.play().catch(e => {});
            }
        }

        function addLog(msg) {
            const log = document.getElementById('log-box');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerText = `> ${msg}`;
            log.prepend(entry);
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
            const razza = document.getElementById('p-razza').value;
            
            let hp = (HP_MAP[classe] || 10) + 20;
            if(razza === "Nano") hp += 5;
            
            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', classe, razza,
                x: 12, y: 3, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: RACE_ICONS[razza] || "🧔",
                weapons: WEAPON_CONFIG[classe], inventory: { potions: 1, coins: 0 }
            }];
            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            document.getElementById('map-name-display').innerText = mapNumber;
            isCombat = false;
            
            const imgEl = document.getElementById('map-img');
            imgEl.style.display = 'none';
            // Tentativo caricamento immagine con estensione jpg
            imgEl.src = BASE_URL + "Maps/" + mapNumber + ".jpg";
            imgEl.onload = () => imgEl.style.display = 'block';
            imgEl.onerror = () => {
                // Se fallisce, prova png
                if(!imgEl.src.endsWith(".png")) imgEl.src = BASE_URL + "Maps/" + mapNumber + ".png";
            };

            audioPlayer.src = BASE_URL + "Music/" + mapNumber + ".mp3";
            audioPlayer.play().catch(e => {});

            try {
                const response = await fetch(BASE_URL + "Maps/" + mapNumber + ".json");
                if (response.ok) applyLevelData(await response.json());
                else applyLevelData({});
            } catch (e) { applyLevelData({}); }

            const hero = entities.find(e => e.tipo === 'hero');
            hero.x = 12; hero.y = 3; hero.movesRemaining = 6;
            entities = [hero];
            
            let enemyNum = 2 + Math.floor(mapNumber / 2);
            for(let i=0; i < enemyNum; i++) {
                entities.push({
                    nome: "Mostro", hp: 10 + (mapNumber*8), tipo: 'enemy', 
                    x: 4 + Math.floor(Math.random()*16), y: 15 + Math.floor(Math.random()*15), 
                    dead: false, icon: "👹"
                });
            }
            disegnaEntita();
            aggiornaUI();
            addLog("Ingresso nell'area " + mapNumber);
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            if (data.walls) data.walls.forEach(idx => { if (cells[idx]) cells[idx].classList.add('wall'); });
            
            loots = {};
            document.querySelectorAll('.loot-icon').forEach(l => l.remove());
            if (data.loot) data.loot.forEach(item => spawnLoot(item.idx, item.type));
        }

        function spawnLoot(idx, type) {
            const el = document.createElement('div');
            el.className = 'loot-icon';
            el.innerText = type === 'moneta' ? "💰" : "🧪";
            el.style.width = (100/COLS)+'%'; el.style.height = (100/ROWS)+'%';
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
            ent.element.style.left = (ent.x * (100/COLS)) + '%';
            ent.element.style.top = (ent.y * (100/ROWS)) + '%';
            if (ent.tipo === 'hero') {
                const idx = Math.floor(ent.y) * COLS + Math.floor(ent.x);
                if (loots[idx]) {
                    if (loots[idx].type === 'pozione') {
                        ent.inventory.potions++;
                        addLog("Hai raccolto una pozione!");
                    } else {
                        ent.inventory.coins += 25;
                        addLog("Hai trovato dell'oro!");
                    }
                    loots[idx].element.remove(); delete loots[idx];
                    aggiornaUI();
                }
            }
        }

        function muoviEroe(dx, dy) {
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
            document.getElementById('btn-potion').disabled = hero.inventory.potions <= 0;
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true; 
            addLog("LOTTA INIZIATA!");
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
            if(activeEntity.tipo === 'enemy') setTimeout(turnoIA, 600);
            else renderAzioni();
            aggiornaUI();
        }

        function renderAzioni() {
            const hero = entities.find(e => e.tipo === 'hero');
            const container = document.getElementById('weapon-buttons');
            container.innerHTML = '';
            hero.weapons.forEach(w => {
                const b = document.createElement('button');
                b.className = 'pc-btn';
                b.innerHTML = w.icon + " ATTACCA (" + w.name + ")";
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
                addLog("Colpisci per " + d + " danni!");
                if(target.hp <= 0) { 
                    target.dead = true; target.element.style.opacity = '0.2';
                    addLog("Nemico ucciso!");
                    // DROP LOOT
                    const idx = Math.floor(target.y) * COLS + Math.floor(target.x);
                    const rand = Math.random();
                    if(rand < 0.2) spawnLoot(idx, 'pozione');
                    else if(rand < 0.8) spawnLoot(idx, 'moneta');
                }
                prossimoTurno();
            } else addLog("Nemico troppo lontano!");
        }

        function turnoIA() {
            if(!isCombat || !activeEntity || activeEntity.dead) return prossimoTurno();
            const hero = entities.find(e => e.tipo === 'hero');
            if(activeEntity.x < hero.x) activeEntity.x++; else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++; else if(activeEntity.y > hero.y) activeEntity.y--;
            aggiornaPosizione(activeEntity);
            if(Math.sqrt(Math.pow(activeEntity.x-hero.x,2)+Math.pow(activeEntity.y-hero.y,2)) < 1.6) {
                let d = Math.floor(Math.random()*6)+4;
                hero.hp -= d; addLog("Il mostro ti morde: -" + d + " HP");
                if(hero.hp <= 0) { alert("SEI MORTO."); location.reload(); }
            }
            setTimeout(prossimoTurno, 600);
        }

        function prossimoTurno() { 
            if (entities.filter(e => e.tipo === 'enemy' && !e.dead).length === 0) {
                isCombat = false; 
                entities.forEach(e => { if(e.element) e.element.classList.remove('active-char'); });
                addLog("Vittoria! Area ripulita."); 
                aggiornaUI();
                return;
            }
            currentIndex++; selezionaTurno(); 
        }

        window.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            if (['w', 'arrowup'].includes(key)) muoviEroe(0, -1);
            if (['s', 'arrowdown'].includes(key)) muoviEroe(0, 1);
            if (['a', 'arrowleft'].includes(key)) muoviEroe(-1, 0);
            if (['d', 'arrowright'].includes(key)) muoviEroe(1, 0);
            if (key === 'p') usaPozione();
            if (key === ' ' || key === 'enter') prossimoTurno();
        });
    </script>
</body>
</html>
"""

# Rendering finale
game_html = html_template.replace("__GITHUB_BASE__", GITHUB_BASE)
components.html(game_html, height=1000, scrolling=False)
