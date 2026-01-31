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
            --accent-color: #f59e0b; /* Gold/Orange for CNY */
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

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        header {{
            padding: 0.5rem 2rem;
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
            gap: 2rem;
        }}

        h1 {{
            font-size: 1.25rem;
            color: var(--accent-color);
            text-shadow: 0 0 10px var(--accent-glow);
            margin-right: 1rem;
        }}
        
        .tabs {{
            display: flex;
            background: #0f172a;
            padding: 4px;
            border-radius: 8px;
            border: 1px solid #334155;
        }}
        
        .tab-btn {{
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }}
        
        .tab-btn.active {{
            background: var(--card-bg);
            color: var(--text-primary);
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        
        .tab-btn:hover:not(.active) {{
            color: var(--text-primary);
        }}

        #controls {{
            display: flex;
            gap: 1rem;
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
            font-size: 0.9rem;
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

        /* --- STAGE AREA --- */
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
            /* COLLAPSED STATE (Hidden) */
            width: 0;
            margin: 0;
            opacity: 0;
            transform: scale(0.8);
            
            height: 120px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
            position: relative;
            
            /* Staggered entry */
            transition: 
                width 0.5s ease-in-out,
                margin 0.5s ease-in-out,
                opacity 0.5s ease-in-out,
                transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
            
            overflow: hidden;
        }}
        
        /* Apply dynamic delay based on index for natural entrance */
        .avatar.visible {{
            transition-delay: calc(var(--i) * 0.1s);
        }}
        
        /* Slow stagger for one-by-one visualization */
        .avatar.visible.slow-entry {{
            transition-delay: calc(var(--i) * 0.5s);
        }}

        .avatar-inner {{
            width: 80px; 
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        /* Side Exit transforms */
        .avatar.side-left {{
            transform: translateX(-150px) scale(0.8);
        }}

        .avatar.side-right {{
           transform: translateX(150px) scale(0.8);
        }}
        
        .avatar.visible {{
            /* VISIBLE STATE */
            width: 80px;
            margin: 0 1rem;
            opacity: 1;
            transform: translateX(0) scale(1);
        }}

        .avatar.speaking {{
            transform: translateY(-15px) scale(1.15);
            z-index: 10;
        }}
        
        .avatar.speaking .avatar-body {{
            box-shadow: 0 0 20px var(--glow-color);
            border: 2px solid #fff;
        }}

        .avatar-body {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.5rem;
            color: rgba(255,255,255,0.9);
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            border: 2px solid transparent;
            transition: all 0.3s ease;
            margin-bottom: 0.5rem;
            position: relative;
        }}
        
        .avatar-body::after {{
            content: '';
            position: absolute;
            bottom: -30px;
            width: 40px;
            height: 30px;
            background: var(--color);
            opacity: 0.5;
            border-radius: 10px 10px 0 0;
            z-index: -1;
        }}

        .avatar-name {{
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            background: rgba(0,0,0,0.3);
            padding: 2px 6px;
            border-radius: 4px;
            white-space: nowrap;
        }}
        
        /* Speaker Colors Implementation */
        .avatar[data-name="Jasmine"] {{ --color: var(--speaker-jasmine); --glow-color: var(--speaker-jasmine); }}
        .avatar[data-name="Esther"] {{ --color: var(--speaker-esther); --glow-color: var(--speaker-esther); }}
        .avatar[data-name="Amy"] {{ --color: var(--speaker-amy); --glow-color: var(--speaker-amy); }}
        .avatar[data-name="Chris"] {{ --color: var(--speaker-chris); --glow-color: var(--speaker-chris); }}
        .avatar[data-name="Jason"] {{ --color: var(--speaker-jason); --glow-color: var(--speaker-jason); }}
        .avatar[data-name="Evan"] {{ --color: var(--speaker-evan); --glow-color: var(--speaker-evan); }}
        .avatar[data-name="多多"] {{ --color: var(--speaker-duoduo); --glow-color: var(--speaker-duoduo); }}
        .avatar[data-name="Emeline"] {{ --color: var(--speaker-emeline); --glow-color: var(--speaker-emeline); }}


        main {{
            flex: 1;
            overflow-y: auto;
            padding: 2rem;
            scroll-behavior: smooth;
        }}

        #script-container {{
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            padding-bottom: 50vh;
        }}

        .line-item {{
            opacity: 0.4;
            transition: all 0.3s ease;
            border-left: 4px solid #334155;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            background: transparent;
        }}

        .line-item.active {{
            opacity: 1;
            background: var(--card-bg);
            border-left-color: var(--accent-color);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}

        .header-item {{
            margin-top: 3rem;
            margin-bottom: 1rem;
            text-align: center;
            color: var(--accent-color);
            font-size: 1.5rem;
            font-weight: bold;
            border-bottom: 1px solid #334155;
            padding-bottom: 0.5rem;
        }}
        
        .speaker-label {{
             font-weight: bold;
             margin-bottom: 0.25rem;
             display: block;
        }}
        
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

        /* Responsive / Mobile Styles */
        @media (max-width: 768px) {{
            header {{
                flex-direction: column;
                height: auto;
                padding: 1rem;
                gap: 1rem;
            }}
            
            .header-left {{
                flex-direction: column;
                gap: 0.5rem;
                width: 100%;
            }}

            h1 {{
                font-size: 1.2rem;
                margin-right: 0;
                text-align: center;
            }}
            
            #controls {{
                width: 100%;
                justify-content: center;
            }}
            
            .tabs {{
                width: 100%;
                justify-content: center;
            }}
            
            .tab-btn {{
                flex: 1;
                text-align: center;
            }}

            /* Adjust Stage */
            #stage-container {{
                height: 30vh;
                padding-bottom: 3rem; 
            }}

            .avatar {{
                /* Tighter margins and scaling for mobile */
            }}
            
            .avatar.visible {{
                width: 50px; /* Reduced visual width space */
                margin: 0 0.15rem; /* Very tight margins */
            }}
            
            .avatar-inner {{
                 transform: scale(0.65); 
            }}
            
            /* Adjust Script View */
            main {{
                padding: 1rem;
            }}
            
            #script-container {{
                 gap: 1rem;
            }}
            
            .content-cn {{
                font-size: 1.1rem;
            }}
            
            .content-en {{
                font-size: 0.9rem;
            }}
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
            <button id="prev-btn">Previous (←)</button>
            <button id="next-btn" class="primary">Next (Space/→)</button>
            <button id="autoplay-btn">Auto-Play</button>
        </div>
    </header>

    <div id="stage-container">
        <!-- Avatars will be injected here -->
    </div>

    <main>
        <div id="script-container"></div>
    </main>

    <script>
        // Holds "Morning" and "Afternoon" arrays
        const allData = {json.dumps(all_data, ensure_ascii=False)};
        // Updated Host Order
        const hosts = ["Amy", "多多", "Emeline", "Jason", "Jasmine", "Chris", "Esther", "Evan"];
        
        let currentSession = 'Morning';
        let scriptData = []; // Will hold current session data
        let currentIndex = -1;
        let autoPlayInterval = null;
        
        // --- Init Session Data ---
        function initSession(sessionName) {{
            currentSession = sessionName;
            scriptData = allData[sessionName] || [];
            
            // Re-index
            scriptData.forEach((item, idx) => {{
                item.index = idx;
            }});
            
            // Clean up UI
            currentIndex = 0;
            render();
            // Reset active tab UI
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                if(btn.textContent === sessionName) btn.classList.add('active');
                else btn.classList.remove('active');
            }});
            
            setIndex(0);
        }}

        function switchTab(sessionName) {{
            if (autoPlayInterval) {{
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
                document.getElementById('autoplay-btn').textContent = 'Auto-Play';
                document.getElementById('autoplay-btn').classList.remove('primary');
            }}
            initSession(sessionName);
        }}

        function getSegmentSpeakers(idx) {{
            let start = idx;
            let end = idx;
            
            if (scriptData.length === 0) return [];
            
            // Safely limit while loops
            while(start > 0 && scriptData[start] && scriptData[start].type !== 'header') {{
                start--;
            }}
            while(end < scriptData.length - 1 && scriptData[end+1] && scriptData[end+1].type !== 'header') {{
                end++;
            }}
            
            if (!scriptData[idx] || scriptData[idx].type === 'header') {{
                 return [];
            }}

            const speakers = new Set();
            for (let i = start; i <= end; i++) {{
                const s = scriptData[i].speaker;
                if (s) {{
                    const sLower = s.toLowerCase();
                    if (sLower === 'all' || sLower.includes('one by one')) {{
                        return hosts; 
                    }}
                    const clean = s.replace(/[^a-zA-Z\u4e00-\u9fa5]/g, ''); 
                    if (hosts.includes(clean)) speakers.add(clean);
                }}
            }}
            return Array.from(speakers);
        }}

        // --- Init Stage ---
        const stage = document.getElementById('stage-container');
        const avatarEls = {{}};
        
        // Create avatars
        hosts.forEach((name, index) => {{
            const el = document.createElement('div');
            const sideClass = index < 4 ? 'side-left' : 'side-right';
            
            el.className = `avatar ${{sideClass}}`;
            el.dataset.name = name;
            el.style.setProperty('--i', index); 
            
            el.innerHTML = `
                <div class="avatar-inner">
                    <div class="avatar-body">${{name[0]}}</div>
                    <div class="avatar-name">${{name}}</div>
                </div>
            `;
            stage.appendChild(el);
            avatarEls[name] = el;
        }});


        // --- Render Script ---
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
                    el.innerHTML = `
                        <div class="speaker-label speaker-${{cleanSpeaker}}">${{item.speaker}}</div>
                        <div class="content-cn">${{item.text_cn}}</div>
                        <div class="content-en">${{item.text_en}}</div>
                    `;
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
            
            // Update visibility
            hosts.forEach(name => {{
                const el = avatarEls[name];
                
                // Toggle slow entry class
                if (isOneByOne) {{
                    el.classList.add('slow-entry');
                }} else {{
                    el.classList.remove('slow-entry');
                }}
                
                // Are they on stage?
                if (activeSpeakers.includes(name)) {{
                    el.classList.add('visible');
                }} else {{
                    el.classList.remove('visible');
                    el.classList.remove('speaking');
                }}
                
                // Are they speaking right now?
                if (name === currentSpeaker || (isAll && activeSpeakers.includes(name))) {{
                    el.classList.add('speaking');
                }} else {{
                    el.classList.remove('speaking');
                }}
            }});
        }}

        // --- Controls ---
        function next() {{ setIndex(currentIndex + 1); }}
        function prev() {{ setIndex(currentIndex - 1); }}
        
        function toggleAutoPlay() {{
            const btn = document.getElementById('autoplay-btn');
            if (autoPlayInterval) {{
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
                btn.textContent = 'Auto-Play';
                btn.classList.remove('primary');
            }} else {{
                btn.textContent = 'Stop';
                btn.classList.add('primary');
                next();
                autoPlayInterval = setInterval(next, 3000);
            }}
        }}

        document.getElementById('next-btn').addEventListener('click', next);
        document.getElementById('prev-btn').addEventListener('click', prev);
        document.getElementById('autoplay-btn').addEventListener('click', toggleAutoPlay);
        
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space' || e.code === 'ArrowRight') {{
                e.preventDefault();
                next();
            }}
            if (e.code === 'ArrowLeft') {{
                e.preventDefault();
                prev();
            }}
        }});

        // Init with Morning
        initSession('Morning');

    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
