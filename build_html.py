import json

# Read the data
with open('data.json', 'r', encoding='utf-8') as f:
    # Now this is a dictionary { "Morning": [...], "Afternoon": [...] }
    all_data = json.load(f)

# HTML Template
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Year of the Horse - OCA-CVC Host Simulator</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-color: #f59e0b;
            --accent-glow: rgba(245, 158, 11, 0.4);
            
            /* Speaker Identities */
            --speaker-jasmine: #ec4899;
            --speaker-esther: #8b5cf6;
            --speaker-amy: #06b6d4;
            --speaker-chris: #3b82f6;
            --speaker-jason: #10b981;
            --speaker-evan: #f43f5e;
            --speaker-duoduo: #eab308;
            --speaker-emeline: #d946ef;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        /* --- HEADER & CONTROLS --- */
        header {{
            padding: 0.5rem 1rem;
            background: rgba(15, 23, 42, 0.95);
            border-bottom: 1px solid #334155;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
            height: 70px;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        h1 {{
            font-size: 1.2rem;
            color: var(--accent-color);
            text-shadow: 0 0 10px var(--accent-glow);
            margin-right: 0.5rem;
            white-space: nowrap;
        }}
        
        .tabs {{
            display: flex;
            background: #0f172a;
            padding: 2px;
            border-radius: 8px;
            border: 1px solid #334155;
        }}
        
        .tab-btn {{
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
            font-size: 0.85rem;
        }}
        
        .tab-btn.active {{
            background: var(--card-bg);
            color: var(--text-primary);
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}

        #controls {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}

        button {{
            background: var(--card-bg);
            color: var(--text-primary);
            border: 1px solid #334155;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
            font-size: 0.85rem;
        }}

        button:hover {{
            border-color: var(--accent-color);
            background: #334155;
        }}

        button.primary {{
            background: var(--accent-color);
            color: #000;
            border: none;
        }}

        /* --- EDITOR MODAL --- */
        #editor-modal {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }}
        
        #editor-content {{
            background: var(--bg-color);
            width: 90%;
            max-width: 1000px;
            height: 80vh;
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            border: 1px solid #334155;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .editor-header {{
            padding: 1rem;
            border-bottom: 1px solid #334155;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .editor-body {{
            flex: 1;
            display: flex;
            overflow: hidden;
        }}
        
        .editor-column {{
            flex: 1;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #334155;
            overflow-y: auto;
        }}
        
        .editor-column:last-child {{ border-right: none; }}
        
        .editor-column h3 {{
            margin-bottom: 1rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Drag & Drop List */
        #sortable-list {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .sortable-item {{
            background: var(--card-bg);
            padding: 0.75rem;
            border-radius: 6px;
            cursor: grab;
            border: 1px solid #334155;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: background 0.2s;
        }}
        
        .sortable-item:hover {{
            background: #334155;
        }}
        
        .sortable-item:active {{
            cursor: grabbing;
        }}
        
        .sortable-item .handle {{
            color: var(--text-secondary);
            font-size: 1.2rem;
            line-height: 1;
        }}
        
        /* CSV Text Area */
        #csv-input {{
            flex: 1;
            background: #020617;
            color: #ccc;
            border: 1px solid #334155;
            padding: 1rem;
            font-family: monospace;
            resize: none;
            border-radius: 6px;
        }}
        
        .editor-footer {{
            padding: 1rem;
            border-top: 1px solid #334155;
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
        }}

        /* --- STAGE --- */
        #stage-container {{
            height: 35vh;
            background: linear-gradient(to bottom, #020617, #0f172a);
            position: relative;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            overflow: hidden;
            border-bottom: 1px solid #334155;
        }}

        .avatar {{
            width: 0; margin: 0; opacity: 0;
            transform: scale(0.8);
            height: 140px; 
            display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
            position: relative;
            transition: 
                width 0.5s ease-in-out,
                margin 0.5s ease-in-out,
                opacity 0.5s ease-in-out,
                transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
            overflow: hidden;
        }}
        
        .avatar.side-left {{ transform: translateX(-150px) scale(0.8); }}
        .avatar.side-right {{ transform: translateX(150px) scale(0.8); }}
        .avatar.visible {{
            width: 80px; 
            margin: 0 10px; /* Fixed consistent margin */
            opacity: 1;
            transform: translateX(0) scale(1);
            transition-delay: calc(var(--i) * 0.1s);
            flex-shrink: 0; /* Important: Do not shrink avatars if space is tight */
        }}
        .avatar.visible.slow-entry {{
            transition-delay: calc(var(--i) * 0.5s);
        }}
        .avatar.speaking {{ transform: translateY(-15px) scale(1.15); z-index: 10; }}
        
        .avatar-inner {{ width: 80px; display: flex; flex-direction: column; align-items: center; position: relative; }}

        /* Humanoid Figure */
        .avatar-body {{
            width: 50px; height: 50px; border-radius: 50%;
            background: var(--color);
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; font-size: 1.2rem;
            color: rgba(255,255,255,0.9);
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative; z-index: 2;
        }}
        .avatar.speaking .avatar-body {{
            box-shadow: 0 0 20px var(--glow-color); border: 2px solid #fff;
        }}
        .avatar-body::after {{
            content: ''; position: absolute; top: 45px; left: 50%; transform: translateX(-50%);
            width: 60px; height: 40px; background: var(--color); opacity: 0.8;
            border-radius: 20px 20px 0 0; z-index: -1;
        }}
        .avatar-body::before {{
             content: ''; position: absolute; bottom: -5px; width: 20px; height: 10px;
             background: var(--color); z-index: -1;
        }}
        .avatar-name {{
            font-size: 0.8rem; font-weight: 600; color: var(--text-secondary);
            background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 4px;
            white-space: nowrap; margin-top: 45px; z-index: 3;
        }}
        
        /* Speaker Colors */
        .avatar[data-name="Jasmine"] {{ --color: var(--speaker-jasmine); --glow-color: var(--speaker-jasmine); }}
        .avatar[data-name="Esther"] {{ --color: var(--speaker-esther); --glow-color: var(--speaker-esther); }}
        .avatar[data-name="Amy"] {{ --color: var(--speaker-amy); --glow-color: var(--speaker-amy); }}
        .avatar[data-name="Chris"] {{ --color: var(--speaker-chris); --glow-color: var(--speaker-chris); }}
        .avatar[data-name="Jason"] {{ --color: var(--speaker-jason); --glow-color: var(--speaker-jason); }}
        .avatar[data-name="Evan"] {{ --color: var(--speaker-evan); --glow-color: var(--speaker-evan); }}
        .avatar[data-name="多多"] {{ --color: var(--speaker-duoduo); --glow-color: var(--speaker-duoduo); }}
        .avatar[data-name="Emeline"] {{ --color: var(--speaker-emeline); --glow-color: var(--speaker-emeline); }}

        main {{ flex: 1; overflow-y: auto; padding: 2rem; scroll-behavior: smooth; }}
        #script-container {{ max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; gap: 1.5rem; padding-bottom: 50vh; }}
        
        .line-item {{
            opacity: 0.4; transition: all 0.3s ease; border-left: 4px solid #334155; padding: 1rem;
            border-radius: 0 8px 8px 0; background: transparent;
        }}
        .line-item.active {{
            opacity: 1; background: var(--card-bg); border-left-color: var(--accent-color);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}
        .header-item {{
            margin-top: 3rem; margin-bottom: 1rem; text-align: center;
            color: var(--accent-color); font-size: 1.5rem; font-weight: bold;
            border-bottom: 1px solid #334155; padding-bottom: 0.5rem;
        }}
        .speaker-label {{ font-weight: bold; margin-bottom: 0.25rem; display: block; }}
        .speaker-Jasmine {{ color: var(--speaker-jasmine); }}
        .speaker-Esther {{ color: var(--speaker-esther); }}
        .speaker-Amy {{ color: var(--speaker-amy); }}
        .speaker-Chris {{ color: var(--speaker-chris); }}
        .speaker-Jason {{ color: var(--speaker-jason); }}
        .speaker-Evan {{ color: var(--speaker-evan); }}
        .speaker-多多 {{ color: var(--speaker-duoduo); }}
        .speaker-Emeline {{ color: var(--speaker-emeline); }}

        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-color); }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}

        @media (max-width: 768px) {{
            header {{ flex-direction: column; height: auto; padding: 1rem; gap: 1rem; }}
            .header-left {{ flex-direction: column; gap: 0.5rem; width: 100%; }}
            #controls {{ width: 100%; justify-content: center; flex-wrap: wrap; }}
            .avatar.visible {{ width: 50px; margin: 0 0.15rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-left">
            <h1>Host Simulator</h1>
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('Morning')">Morning</button>
                <button class="tab-btn" onclick="switchTab('Afternoon')">Afternoon</button>
            </div>
        </div>
        <div id="controls">
            <button class="secondary" onclick="openEditor()">Edit / Paste CSV</button>
            <button id="prev-btn">Previous</button>
            <button id="next-btn" class="primary">Next</button>
            <button id="autoplay-btn">Auto-Play</button>
        </div>
    </header>

    <div id="stage-container">
        <!-- Avatars injected here -->
    </div>

    <main>
        <div id="script-container"></div>
    </main>

    <!-- EDITOR MODAL -->
    <div id="editor-modal">
        <div id="editor-content">
            <div class="editor-header">
                <h2>Manage Program Order</h2>
                <button onclick="closeEditor()" style="background:#ef4444; border:none; color:white;">Cancel</button>
            </div>
            <div class="editor-body">
                <div class="editor-column">
                    <h3>Drag to Reorder Programs</h3>
                    <div id="sortable-list">
                        <!-- Draggable items will be here -->
                    </div>
                </div>
                <div class="editor-column">
                    <h3>Paste CSV Data</h3>
                    <p style="font-size:0.8rem; color:#888; margin-bottom:0.5rem;">Paste full CSV content here to override current session.</p>
                    <textarea id="csv-input" placeholder="Speaker, Chinese, English..."></textarea>
                    <button class="secondary" style="margin-top:1rem;" onclick="processPastedCSV()">Load from Text Box</button>
                </div>
            </div>
            <div class="editor-footer">
                <button class="primary" onclick="applyEditorChanges()">Apply Changes</button>
            </div>
        </div>
    </div>

    <script>
        const allData = {json.dumps(all_data, ensure_ascii=False)};
        const hosts = ["Amy", "多多", "Emeline", "Jason", "Jasmine", "Chris", "Esther", "Evan"];
        
        let currentSession = 'Morning';
        let scriptData = []; // Flat array for rendering
        let structuredSegments = []; // List of segments for editing
        
        let currentIndex = -1;
        let autoPlayInterval = null;
        
        // --- DATA STRUCTURE MANAGEMENT ---
        
        // Flatten structured segments back to simple component list
        function flattenSegments(segs) {{
            const flat = [];
            segs.forEach(seg => {{
                if (seg.header) flat.push(seg.header);
                seg.lines.forEach(line => flat.push(line));
            }});
            return flat;
        }}
        
        // Group flat data into segments based on Headers
        function groupToSegments(flatData) {{
            if (!flatData || flatData.length === 0) return [];
            const segs = [];
            let currentSeg = {{ header: null, lines: [] }};
            
            flatData.forEach(item => {{
                if (item.type === 'header') {{
                    // If we have accumulated lines or a previous header, push it
                    if (currentSeg.header || currentSeg.lines.length > 0) {{
                        segs.push(currentSeg);
                    }}
                    currentSeg = {{ header: item, lines: [] }};
                }} else {{
                    currentSeg.lines.push(item);
                }}
            }});
            
            // Push final segment
            if (currentSeg.header || currentSeg.lines.length > 0) {{
                segs.push(currentSeg);
            }}
            
            return segs;
        }}

        function initSession(sessionName) {{
            currentSession = sessionName;
            scriptData = allData[sessionName] || [];
            
            // Re-index
            scriptData.forEach((item, idx) => {{ item.index = idx; }});
            
            currentIndex = 0;
            render();
            
            // UI Update
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                if(btn.textContent === sessionName) btn.classList.add('active');
                else btn.classList.remove('active');
            }});
            setIndex(0);
        }}

        function switchTab(sessionName) {{
            stopAutoPlay();
            initSession(sessionName);
        }}

        // --- EDITOR LOGIC ---
        let dragSrcEl = null;

        function openEditor() {{
            document.getElementById('editor-modal').style.display = 'flex';
            
            // 1. Convert current session data to segments
            const segs = groupToSegments(scriptData);
            
            // 2. Render Drag List
            const listEl = document.getElementById('sortable-list');
            listEl.innerHTML = '';
            
            segs.forEach((seg, idx) => {{
                const item = document.createElement('div');
                item.className = 'sortable-item';
                item.draggable = true;
                item.dataset.index = idx;
                
                const title = seg.header ? seg.header.text : `(Segment ${{idx+1}} - No Header)`;
                item.innerHTML = `<span class="handle">☰</span> <span>${{title}}</span>`;
                
                // Events
                item.addEventListener('dragstart', handleDragStart);
                item.addEventListener('dragover', handleDragOver);
                item.addEventListener('drop', handleDrop);
                item.addEventListener('dragenter', handleDragEnter);
                item.addEventListener('dragleave', handleDragLeave);
                item.addEventListener('dragend', handleDragEnd);
                
                listEl.appendChild(item);
            }});
            
            // 3. Clear CSV box
            document.getElementById('csv-input').value = '';
        }}
        
        function closeEditor() {{
            document.getElementById('editor-modal').style.display = 'none';
        }}
        
        function applyEditorChanges() {{
            // Reconstruct order from DOM
            const listEl = document.getElementById('sortable-list');
            const newOrderIndices = Array.from(listEl.children).map(child => parseInt(child.dataset.index));
            
            const oldSegs = groupToSegments(scriptData);
            const newSegs = newOrderIndices.map(i => oldSegs[i]);
            
            // Flatten back to scriptData
            const newFlat = flattenSegments(newSegs);
            
            // Save to master data
            allData[currentSession] = newFlat;
            initSession(currentSession);
            
            closeEditor();
        }}
        
        function processPastedCSV() {{
            const text = document.getElementById('csv-input').value;
            if(!text.trim()) return;
            
            const newData = parseCSV(text);
            if (newData.length > 0) {{
                // Update master data immediately
                allData[currentSession] = newData;
                // Refresh Editor List so they can reorder if they want
                // Note: we need to update scriptData temporary var to reflect paste for groupToSegments to work
                scriptData = newData;
                
                // Re-render the sortable list
                const segs = groupToSegments(scriptData);
                const listEl = document.getElementById('sortable-list');
                listEl.innerHTML = '';
                 segs.forEach((seg, idx) => {{
                    const item = document.createElement('div');
                    item.className = 'sortable-item';
                    item.draggable = true;
                    item.dataset.index = idx;
                    const title = seg.header ? seg.header.text : `(Segment ${{idx+1}} - No Header)`;
                    item.innerHTML = `<span class="handle">☰</span> <span>${{title}}</span>`;
                    item.addEventListener('dragstart', handleDragStart);
                    item.addEventListener('dragover', handleDragOver);
                    item.addEventListener('drop', handleDrop);
                    item.addEventListener('dragenter', handleDragEnter);
                    item.addEventListener('dragleave', handleDragLeave);
                    item.addEventListener('dragend', handleDragEnd);
                    listEl.appendChild(item);
                }});
                
                alert(`Parsed ${{newData.length}} lines. You can now reorder them or Click Apply.`);
            }} else {{
                alert('Could not parse CSV.');
            }}
        }}

        // --- Drag & Drop Handlers ---
        function handleDragStart(e) {{
            dragSrcEl = this;
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', this.innerHTML);
            this.style.opacity = '0.4';
        }}
        
        function handleDragOver(e) {{
            if (e.preventDefault) e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            return false;
        }}
        
        function handleDragEnter(e) {{ this.classList.add('over'); }}
        function handleDragLeave(e) {{ this.classList.remove('over'); }}
        
        function handleDrop(e) {{
            if (e.stopPropagation) e.stopPropagation();
            if (dragSrcEl !== this) {{
                // Swap DOM elements
                const list = this.parentNode;
                const items = Array.from(list.children);
                const srcIdx = items.indexOf(dragSrcEl);
                const targetIdx = items.indexOf(this);
                
                if (srcIdx < targetIdx) {{
                    list.insertBefore(dragSrcEl, this.nextSibling);
                }} else {{
                    list.insertBefore(dragSrcEl, this);
                }}
            }}
            return false;
        }}
        
        function handleDragEnd(e) {{
            this.style.opacity = '1';
            document.querySelectorAll('.sortable-item').forEach(item => item.classList.remove('over'));
        }}

        // --- CSV PARSING (Same as before) ---
        function parseCSV(text) {{
            const lines = text.split(/\\r?\\n/);
            const data = [];
            let currentSpeaker = null;
            
            for (let line of lines) {{
                const row = [];
                let inQuote = false;
                let currentVal = '';
                for (let i = 0; i < line.length; i++) {{
                    const char = line[i];
                    if (char === '"') inQuote = !inQuote;
                    else if (char === ',' && !inQuote) {{ row.push(currentVal.trim()); currentVal = ''; }}
                    else currentVal += char;
                }}
                row.push(currentVal.trim());
                while (row.length < 3) row.push('');
                
                let speaker = row[0].replace(/^"|"$/g, '').trim(); 
                const text_cn = row[1].replace(/^"|"$/g, '').trim();
                const text_en = row[2].replace(/^"|"$/g, '').trim();

                if (!speaker && !text_cn && !text_en) continue;
                if (speaker.toLowerCase() === 'ending') {{
                     data.push({{ type: 'header', text: 'Ending' }});
                     currentSpeaker = null; continue;
                }}
                
                const combined = (text_cn + text_en).toLowerCase();
                if (combined.includes('minutes') || speaker.includes('minutes')) continue;

                if (speaker === '节目' || text_cn.startsWith('#') || (!speaker && text_cn.startsWith('#'))) {{
                    data.push({{ type: 'header', text: text_cn + ' ' + text_en }});
                    currentSpeaker = null; continue;
                }}

                if (speaker) currentSpeaker = speaker;
                const effectiveSpeaker = speaker || currentSpeaker;
                
                 if (effectiveSpeaker && (effectiveSpeaker.includes('开场') || text_cn.includes('开场')) && !text_en) {{
                     if (text_cn.length < 10) {{
                        data.push({{ type: 'header', text: effectiveSpeaker.includes('开场') ? effectiveSpeaker : text_cn}});
                        currentSpeaker = null; continue;
                     }}
                }}
                
                if (effectiveSpeaker) {{
                    data.push({{ type: 'dialogue', speaker: effectiveSpeaker, text_cn: text_cn, text_en: text_en }});
                }}
            }}
            return data;
        }}

        // --- SIMULATOR LOGIC (Standard) ---
        function getSegmentSpeakers(idx) {{
            if (scriptData.length === 0) return [];
            let start = idx, end = idx;
            while(start > 0 && scriptData[start] && scriptData[start].type !== 'header') start--;
            while(end < scriptData.length - 1 && scriptData[end+1] && scriptData[end+1].type !== 'header') end++;
            
            if (!scriptData[idx] || scriptData[idx].type === 'header') return [];

            const speakers = new Set();
            for (let i = start; i <= end; i++) {{
                const s = scriptData[i].speaker;
                if (s) {{
                    const sLower = s.toLowerCase();
                    if (sLower === 'all' || sLower.includes('one by one')) return hosts; 
                    const clean = s.replace(/[^a-zA-Z\u4e00-\u9fa5]/g, ''); 
                    if (hosts.includes(clean)) speakers.add(clean);
                }}
            }}
            return Array.from(speakers);
        }}

        const stage = document.getElementById('stage-container');
        const avatarEls = {{}};
        hosts.forEach((name, index) => {{
            const el = document.createElement('div');
            const sideClass = index < 4 ? 'side-left' : 'side-right';
            el.className = `avatar ${{sideClass}}`;
            el.dataset.name = name;
            el.style.setProperty('--i', index); 
            el.innerHTML = `<div class="avatar-inner"><div class="avatar-body">${{name[0]}}</div><div class="avatar-name">${{name}}</div></div>`;
            stage.appendChild(el);
            avatarEls[name] = el;
        }});

        const container = document.getElementById('script-container');
        function render() {{
            container.innerHTML = '';
            scriptData.forEach((item, index) => {{
                const el = document.createElement('div');
                el.id = 'line-' + index;
                if (item.type === 'header') {{
                    el.className = 'header-item';
                    el.textContent = item.text;
                }} else {{
                    el.className = 'line-item';
                    const s = item.speaker || '';
                    const cleanSpeaker = s.replace(/[^a-zA-Z\u4e00-\u9fa5]/g, '');
                    el.innerHTML = `<div class="speaker-label speaker-${{cleanSpeaker}}">${{item.speaker}}</div><div class="content-cn">${{item.text_cn}}</div><div class="content-en">${{item.text_en}}</div>`;
                }}
                el.addEventListener('click', () => setIndex(index));
                container.appendChild(el);
            }});
        }}

        function setIndex(index) {{
            if (scriptData.length === 0) return;
            if (index < 0) index = 0;
            if (index >= scriptData.length) index = scriptData.length - 1;
            
            if (currentIndex !== -1) {{
                const prev = document.getElementById('line-' + currentIndex);
                if (prev) prev.classList.remove('active');
            }}
            currentIndex = index;
            const nextEl = document.getElementById('line-' + currentIndex);
            if (nextEl) {{
                nextEl.classList.add('active');
                nextEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
            updateStage(index);
        }}
        
        function updateStage(index) {{
            const activeSpeakers = getSegmentSpeakers(index);
            const currentItem = scriptData[index];
            if (!currentItem) return;
            const currentSpeakerRaw = currentItem.speaker || '';
            const speakersLower = currentSpeakerRaw.toLowerCase();
            const isAll = speakersLower === 'all' || speakersLower.includes('one by one');
            const isOneByOne = speakersLower.includes('one by one');
            const currentSpeaker = currentSpeakerRaw.replace(/[^a-zA-Z\u4e00-\u9fa5]/g, '');
            
            hosts.forEach(name => {{
                const el = avatarEls[name];
                if (isOneByOne) el.classList.add('slow-entry'); else el.classList.remove('slow-entry');
                
                if (activeSpeakers.includes(name)) el.classList.add('visible');
                else {{ el.classList.remove('visible'); el.classList.remove('speaking'); }}
                
                if (name === currentSpeaker || (isAll && activeSpeakers.includes(name))) el.classList.add('speaking');
                else el.classList.remove('speaking');
            }});
        }}

        function next() {{ setIndex(currentIndex + 1); }}
        function prev() {{ setIndex(currentIndex - 1); }}
        function stopAutoPlay() {{
            if (autoPlayInterval) {{
                clearInterval(autoPlayInterval); autoPlayInterval = null;
                const btn = document.getElementById('autoplay-btn');
                btn.textContent = 'Auto-Play'; btn.classList.remove('primary');
            }}
        }} 
        function toggleAutoPlay() {{
            if (autoPlayInterval) stopAutoPlay();
            else {{
                const btn = document.getElementById('autoplay-btn');
                btn.textContent = 'Stop'; btn.classList.add('primary');
                next();
                autoPlayInterval = setInterval(next, 3000);
            }}
        }}

        document.getElementById('next-btn').addEventListener('click', next);
        document.getElementById('prev-btn').addEventListener('click', prev);
        document.getElementById('autoplay-btn').addEventListener('click', toggleAutoPlay);
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space' || e.code === 'ArrowRight') {{ e.preventDefault(); next(); }}
            if (e.code === 'ArrowLeft') {{ e.preventDefault(); prev(); }}
        }});

        initSession('Morning');
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
