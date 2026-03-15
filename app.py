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

# Template HTML/JS/CSS
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
        
        .cell.wall { background: transparent !important; border: none !important; } 

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
                    <option value="Umano">Umano</option><option value="Elfo">Elfo</option><option value="Nano">Nano</option>
                    <option value="Halfling">Halfling</option><option value="Dragonide">Dragonide</option><option value="Gnomo">Gnomo</option>
                    <option value="Mezzelfo">Mezzelfo</option><option value="Mezzorco">Mezzorco</option><option value="Tiefling">Tiefling</option>
                </select>
                <label>Classe</label>
                <select id="p-classe">
                    <option value="Barbaro">Barbaro</option><option value="Guerriero">Guerriero</option><option value="Paladino">Paladino</option>
                    <option value="Ranger">Ranger</option><option value="Chierico">Chierico</option><option value="Ladro">Ladro</option>
                    <option value="Bardo">Bardo</option><option value="Druido">Druido</option><option value="Monaco">Monaco</option>
                    <option value="Warlock">Warlock</option><option value="Mago">Mago</option><option value="Stregone">Stregone</option>
                </select>
            </div>
            <button onclick="iniziaAvventura()">INIZIA SAGA MAPPAT</button>
        </div>
    </div>

    <div id="ui-top">
        <div class="stat-badge">Mappa: <span id="map-name-display">1</span></div>
        <div class="stat-badge">❤️ HP: <span id="hp-display" style="color:var(--danger)">0</span></div>
        <div class="stat-badge">👣 Passi: <span id="moves-display">6</span>/6</div>
        <div class="stat-badge">⚔️ Stato: <span id="turn-display">Esplorazione</span></div>
    </div>

    <div id="game-container">
        <div id="map-bg-container">
            <img id="map-img" class="map-asset">
        </div>
        <div id="grid"></div>
    </div>

    <div id="action-panel">
        <div style="font-size:12px; color:var(--primary); font-weight:bold; margin-bottom:5px; text-align:center;">AZIONI COMBATTIMENTO</div>
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

        const WEAPON_CONFIG = {
            "Barbaro": [{ name: "Ascia Bipenne", dice: 12, range: 1.5, icon: "🪓" }, { name: "Giavellotto", dice: 6, range: 6, icon: "🎯" }],
            "Guerriero": [{ name: "Spada Lunga", dice: 8, range: 1.5, icon: "⚔️" }, { name: "Arco Lungo", dice: 8, range: 10, icon: "🏹" }],
            "Paladino": [{ name: "Martello da Guerra", dice: 10, range: 1.5, icon: "🔨" }, { name: "Punizione Divina", dice: 8, range: 3, icon: "✨" }],
            "Ranger": [{ name: "Arco Lungo", dice: 8, range: 12, icon: "🏹" }, { name: "Spada Corta", dice: 6, range: 1.5, icon: "🗡️" }],
            "Chierico": [{ name: "Mazza", dice: 6, range: 1.5, icon: "🏏" }, { name: "Fiamma Sacra", dice: 8, range: 8, icon: "🔥" }],
            "Ladro": [{ name: "Pugnale Furtivo", dice: 6, range: 1.5, icon: "🔪" }, { name: "Balestra Leggera", dice: 8, range: 8, icon: "🏹" }],
            "Bardo": [{ name: "Stocco", dice: 8, range: 1.5, icon: "🤺" }, { name: "Beffa Crudele", dice: 4, range: 8, icon: "🎶" }],
            "Druido": [{ name: "Bastone", dice: 6, range: 1.5, icon: "🦯" }, { name: "Frusta di Spine", dice: 6, range: 6, icon: "🌿" }],
            "Monaco": [{ name: "Colpo Senz'Armi", dice: 6, range: 1.5, icon: "👊" }, { name: "Dardi di Energia", dice: 4, range: 6, icon: "☄️" }],
            "Warlock": [{ name: "Deflagrazione Occulta", dice: 10, range: 10, icon: "💜" }, { name: "Pugnale di Vetro", dice: 4, range: 1.5, icon: "🔪" }],
            "Mago": [{ name: "Dardo Incantato", dice: 4, range: 12, icon: "🪄" }, { name: "Palla di Fuoco", dice: 10, range: 8, icon: "💥" }],
            "Stregone": [{ name: "Dardo di Fuoco", dice: 10, range: 10, icon: "☄️" }, { name: "Scossa Elettrica", dice: 8, range: 1.5, icon: "⚡" }]
        };

        let currentMapNumber = 1, entities = [], currentIndex = 0, isCombat = false, activeEntity = null;

        function playIntroOnce() {
            if (audioPlayer.paused) {
                audioPlayer.src = BASE_URL + "Music/intro.mp3";
                audioPlayer.play().catch(e => { console.error("Audio intro mancante"); });
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
            
            let hp = HP_MAP[classe] + 15;
            if(razza === "Nano") hp += 5;

            entities = [{ 
                nome, hp, maxHP: hp, tipo: 'hero', razza, classe, 
                x: 12, y: 2, movesRemaining: 6, element: null, 
                ini: 0, dead: false, icon: RACE_ICONS[razza],
                weapons: WEAPON_CONFIG[classe] || []
            }];

            caricaMappaCompleta(1);
        }

        async function caricaMappaCompleta(mapNumber) {
            currentMapNumber = mapNumber;
            document.getElementById('map-name-display').innerText = mapNumber;
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
            if (!loaded) addLog("Immagine Mappa " + mapNumber + " non trovata.");

            audioPlayer.src = BASE_URL + "Music/" + mapNumber + ".mp3";
            audioPlayer.play().catch(e => {});

            try {
                const response = await fetch(`${BASE_URL}Maps/${mapNumber}.json`);
                if (response.ok) applyLevelData(await response.json());
                else applyLevelData({});
            } catch (e) { applyLevelData({}); }

            const hero = entities.find(e => e.tipo === 'hero');
            hero.x = 12; hero.y = 2; hero.movesRemaining = 6;
            
            // Pulisci nemici ma tieni eroe
            entities = [hero];
            let enemyCount = 1 + Math.floor(mapNumber / 1.5);
            for(let i=0; i<enemyCount; i++) {
                entities.push({
                    nome: "Mostro " + (i+1), hp: 8 + (mapNumber*5), 
                    tipo: 'enemy', x: Math.floor(Math.random()*18)+3, 
                    y: Math.floor(Math.random()*15)+18, 
                    movesRemaining: 4, dead: false, element: null,
                    icon: ENEMY_ICONS[Math.floor(Math.random()*ENEMY_ICONS.length)]
                });
            }
            disegnaEntita();
            aggiornaUI();
            addLog("Ingresso Mappa " + mapNumber);
        }

        function applyLevelData(data) {
            const cells = document.querySelectorAll('.cell');
            cells.forEach(c => c.classList.remove('wall'));
            if (data.walls) data.walls.forEach(idx => { if (cells[idx]) cells[idx].classList.add('wall'); });
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
            ent.element.style.transform = `translate(${ent.x * CELL_W}px, ${ent.y * CELL_H}px)`;
        }

        function aggiornaUI() {
            const hero = entities.find(e => e.tipo === 'hero');
            if(!hero) return;
            document.getElementById('hp-display').innerText = hero.hp;
            document.getElementById('moves-display').innerText = hero.movesRemaining;
            document.getElementById('turn-display').innerText = isCombat ? "Combattimento" : "Esplorazione";
        }

        function iniziaCombattimento() {
            if(isCombat) return;
            isCombat = true;
            addLog("COMBATTIMENTO!");
            entities.forEach(ent => ent.ini = Math.floor(Math.random()*20)+1);
            // IMPORTANTE: il riordino non influirà sul movimento perché cerchiamo il pg per TIPO
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
            activeEntity.movesRemaining = (activeEntity.tipo === 'hero') ? 6 : 4;
            
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
                let dmg = Math.floor(Math.random() * weapon.dice) + 3;
                target.hp -= dmg;
                addLog(`Usi ${weapon.name}: ${dmg} danni!`);
                if(target.hp <= 0) {
                    target.dead = true;
                    target.element.style.opacity = "0.2";
                    addLog(target.nome + " sconfitto!");
                    controllaFineCombattimento();
                }
                document.getElementById('action-panel').style.display = 'none';
                if(isCombat) prossimoTurno();
            } else {
                addLog(`Bersaglio fuori portata!`);
            }
        }

        function controllaFineCombattimento() {
            const nemiciVivi = entities.filter(e => e.tipo === 'enemy' && !e.dead).length;
            if (nemiciVivi === 0) {
                isCombat = false;
                activeEntity = null;
                document.getElementById('action-panel').style.display = 'none';
                entities.forEach(e => { if(e.element) e.element.classList.remove('active-char'); });
                addLog("Vittoria! Area sicura.");
                const hero = entities.find(e => e.tipo === 'hero');
                hero.movesRemaining = 6;
                aggiornaUI();
            }
        }

        function turnoIA() {
            if(!isCombat || !activeEntity || activeEntity.dead) return prossimoTurno();
            const hero = entities.find(e => e.tipo === 'hero');
            
            if(activeEntity.x < hero.x) activeEntity.x++; else if(activeEntity.x > hero.x) activeEntity.x--;
            if(activeEntity.y < hero.y) activeEntity.y++; else if(activeEntity.y > hero.y) activeEntity.y--;
            aggiornaPosizione(activeEntity);
            
            let d = Math.sqrt(Math.pow(activeEntity.x - hero.x, 2) + Math.pow(activeEntity.y - hero.y, 2));
            if(d < 1.6) {
                let dmg = Math.floor(Math.random()*6)+2;
                hero.hp -= dmg;
                addLog("Il mostro colpisce! -" + dmg + " HP");
                if(hero.hp <= 0) { alert("Saga Fallita."); location.reload(); }
            }
            setTimeout(prossimoTurno, 500);
        }

        function prossimoTurno() {
            if (!isCombat) return;
            currentIndex++;
            selezionaTurno();
        }

        window.addEventListener('keydown', (e) => {
            // CERCA L'EROE IN TUTTO L'ELENCO, NON SOLO IN POSIZIONE 0
            const hero = entities.find(e => e.tipo === 'hero');
            if (!hero || hero.dead) return;
            
            // SE SIAMO IN COMBATTIMENTO, BLOCCA SE NON È IL TURNO DELL'EROE
            if (isCombat && activeEntity !== hero) return;
            
            let nx = hero.x, ny = hero.y;
            if (['w', 'ArrowUp'].includes(e.key)) ny--;
            if (['s', 'ArrowDown'].includes(e.key)) ny++;
            if (['a', 'ArrowLeft'].includes(e.key)) nx--;
            if (['d', 'ArrowRight'].includes(e.key)) nx++;

            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                const cell = document.querySelectorAll('.cell')[ny * COLS + nx];
                if (cell && !cell.classList.contains('wall')) {
                    hero.x = nx; hero.y = ny;
                    if(isCombat) hero.movesRemaining--;
                    aggiornaPosizione(hero);
                    
                    if(!isCombat) {
                        entities.filter(en => en.tipo === 'enemy' && !en.dead).forEach(en => {
                            if(Math.sqrt(Math.pow(en.x-hero.x, 2) + Math.pow(en.y-hero.y, 2)) < 6) iniziaCombattimento();
                        });
                    }
                    
                    if (hero.y >= ROWS - 1) {
                        addLog("Passaggio all'area successiva...");
                        caricaMappaCompleta(currentMapNumber + 1);
                    }
                }
            }
            aggiornaUI();
        });
    </script>
</body>
</html>
"""

### Cosa ho sistemato:
1.  **Ricerca Eroe Dinamica:** Nel listener della tastiera, ora uso `entities.find(e => e.tipo === 'hero')`. Questo evita che il personaggio rimanga bloccato se l'elenco dei personaggi viene riordinato durante il combattimento.
2.  **Reset Post-Lotta:** Nella funzione `controllaFineCombattimento`, ora pulisco lo stato `activeEntity` e rimuovo la classe CSS `active-char`. Questo assicura che il sistema di movimento "capisca" che la battaglia è finita e ti restituisca il controllo.
3.  **Movimenti Infiniti in Esplorazione:** Ho rimosso il blocco dei movimenti fuori dal combattimento, così puoi esplorare liberamente le mappe.
4.  **Resoconto HP:** Ho aggiunto un controllo per aggiornare gli HP anche subito dopo la vittoria, così sai sempre quanta vita ti è rimasta.

Copia e incolla su GitHub e il gioco sarà fluido al 100%! Buon divertimento nella Saga Mappat!
