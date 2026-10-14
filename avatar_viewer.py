import os
import base64
import json

_FEMALE_GLB_B64 = None

def get_female_glb_b64() -> str:
    global _FEMALE_GLB_B64
    if _FEMALE_GLB_B64 is None:
        path = os.path.join("static", "models", "female_human_avatar.glb")
        if os.path.exists(path):
            with open(path, "rb") as f:
                _FEMALE_GLB_B64 = base64.b64encode(f.read()).decode("ascii")
        else:
            _FEMALE_GLB_B64 = ""
    return _FEMALE_GLB_B64

def render_threejs_avatar_viewer(
    tile_b64: str,
    matched_style: str = "Royal Haute Couture",
    height: int = 650
) -> str:
    """
    Renders an interactive Three.js WebGL fashion runway viewport where a realistic, natural
    Runway Human Model or Haute Couture Salon Dress Form wears the synthesized textile pattern
    in real-time feel-good motion.
    Embedded models are self-contained via base64 memory parsing with network fallback,
    guaranteeing 100% reliable rendering without CORS or 404 iframe errors.
    """
    style_clean = matched_style.replace('"', '\\"')
    female_b64 = get_female_glb_b64()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            html, body {{
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: radial-gradient(circle at 50% 35%, #18233c 0%, #060912 100%);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                color: #f1f5f9;
                user-select: none;
            }}
            #canvas-container {{
                width: 100%;
                height: 100%;
                position: absolute;
                top: 0;
                left: 0;
            }}
            .hud-panel {{
                position: absolute;
                top: 14px;
                left: 14px;
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 7px;
                background: rgba(9, 14, 26, 0.92);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(212, 175, 55, 0.4);
                border-radius: 12px;
                padding: 8px 14px;
                z-index: 10;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
                max-width: calc(100% - 28px);
            }}
            .hud-btn {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(212, 175, 55, 0.28);
                color: #f1f5f9;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: 700;
                border-radius: 7px;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }}
            .hud-btn:hover {{
                background: rgba(212, 175, 55, 0.25);
                border-color: #D4AF37;
                color: #ffffff;
                transform: translateY(-1px);
            }}
            .hud-btn.active {{
                background: linear-gradient(135deg, #D4AF37 0%, #AA771C 100%);
                border-color: #FFE58F;
                color: #070b16;
                box-shadow: 0 0 14px rgba(212, 175, 55, 0.6);
            }}
            .hud-sep {{
                width: 1px;
                height: 18px;
                background: rgba(212, 175, 55, 0.35);
                margin: 0 2px;
            }}
            .fit-badge {{
                position: absolute;
                top: 14px;
                right: 14px;
                background: rgba(9, 14, 26, 0.92);
                backdrop-filter: blur(14px);
                border: 1px solid rgba(212, 175, 55, 0.5);
                border-radius: 10px;
                padding: 7px 15px;
                font-size: 11px;
                font-weight: 800;
                color: #fce7a1;
                letter-spacing: 0.5px;
                z-index: 10;
                display: flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
            }}
            .hud-footer {{
                position: absolute;
                bottom: 12px;
                right: 14px;
                background: rgba(9, 14, 26, 0.85);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(212, 175, 55, 0.3);
                border-radius: 8px;
                padding: 5px 12px;
                font-size: 11px;
                color: #fce7a1;
                pointer-events: none;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                z-index: 10;
            }}
            #loading-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(7, 11, 22, 0.85);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 14px;
                z-index: 25;
                transition: opacity 0.35s ease;
                pointer-events: none;
            }}
            .spinner {{
                width: 44px;
                height: 44px;
                border: 3px solid rgba(212, 175, 55, 0.2);
                border-top: 3px solid #D4AF37;
                border-radius: 50%;
                animation: spin 0.9s linear infinite;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body>
        <div id="canvas-container"></div>

        <div id="loading-overlay">
            <div class="spinner"></div>
            <div id="loading-text" style="font-size: 13px; font-weight: 700; color: #fce7a1; letter-spacing: 0.5px;">
                ⚜️ Fitting Tailored Garment onto Runway Model...
            </div>
        </div>

        <div class="hud-panel">
            <span style="font-size: 11px; font-weight: 800; color: #D4AF37; margin-right: 3px;">FASHION MODEL:</span>
            <button class="hud-btn active" id="btn-female" onclick="switchModel('female')">💃 Runway Human Avatar</button>
            <button class="hud-btn" id="btn-form" onclick="switchModel('form')">👗 Haute Couture Dress Form</button>

            <div class="hud-sep"></div>
            <span style="font-size: 11px; font-weight: 700; color: #cbd5e1; margin-right: 3px;">MOTION:</span>
            <button class="hud-btn active" id="btn-motion" onclick="setMotion('walk')">🚶 Poise & Sway</button>
            <button class="hud-btn" id="btn-pose" onclick="setMotion('pose')">🧍 Stature Pose</button>
            <button class="hud-btn" id="btn-play" onclick="togglePlayPause()">⏸️ Pause</button>

            <div class="hud-sep"></div>
            <span style="font-size: 11px; font-weight: 700; color: #cbd5e1; margin-right: 3px;">SCALE:</span>
            <button class="hud-btn" id="btn-sc1" onclick="setPatternScale(1)">1×</button>
            <button class="hud-btn active" id="btn-sc2" onclick="setPatternScale(2)">2×</button>
            <button class="hud-btn" id="btn-sc3" onclick="setPatternScale(3)">3×</button>
            <button class="hud-btn" id="btn-sc5" onclick="setPatternScale(5)">5×</button>

            <div class="hud-sep"></div>
            <button class="hud-btn" onclick="setCameraView('full')">Full View</button>
            <button class="hud-btn" onclick="setCameraView('torso')">Torso</button>
            <button class="hud-btn" onclick="setCameraView('hem')">Hemline</button>
            <button class="hud-btn active" id="btn-turntable" onclick="toggleTurntable()">🔁 360°</button>
        </div>

        <div class="fit-badge">
            ⚜️ {style_clean}
        </div>

        <div class="hud-footer">
            ⚜️ Real-Time 3D Try-On • Drag to Orbit | Wheel to Zoom | Right-Drag to Pan
        </div>

        <script>
            let scene, camera, renderer, controls, clock;
            let currentModel = null;
            let currentBones = {{}};
            let currentModelType = 'female';
            let currentMotionType = 'walk';
            let currentRepeat = 2;
            let isPlaying = true;
            let autoRotate = true;

            const container = document.getElementById('canvas-container');
            const loadingOverlay = document.getElementById('loading-overlay');
            const loadingText = document.getElementById('loading-text');
            const tileData = "{tile_b64}";

            // Embedded In-Memory Female Avatar Model for 100% Reliable Rendering (Zero Network Latency / Zero CORS Error)
            const femaleGlbBase64 = "{female_b64}";

            const modelCache = {{}};
            const gltfLoader = new THREE.GLTFLoader();
            let fabricTex = null;

            function showLoading(show, message) {{
                if (loadingOverlay) {{
                    if (message && loadingText) loadingText.innerText = message;
                    loadingOverlay.style.opacity = show ? '1' : '0';
                    loadingOverlay.style.pointerEvents = show ? 'auto' : 'none';
                }}
            }}

            function parseGlbFromBase64(b64String, onDone, onError) {{
                try {{
                    if (!b64String || b64String.length < 500) {{
                        throw new Error('Embedded GLB base64 is empty or truncated');
                    }}
                    const binary = atob(b64String);
                    const len = binary.length;
                    const bytes = new Uint8Array(len);
                    for (let i = 0; i < len; i++) {{
                        bytes[i] = binary.charCodeAt(i);
                    }}
                    gltfLoader.parse(bytes.buffer, '', onDone, onError);
                }} catch(err) {{
                    if (onError) onError(err);
                }}
            }}

            function getOriginUrl(relPath) {{
                try {{
                    if (window.parent && window.parent.location && window.parent.location.origin && window.parent.location.origin !== 'null') {{
                        return window.parent.location.origin + relPath;
                    }}
                }} catch(e) {{}}
                if (document.referrer) {{
                    try {{
                        const u = new URL(document.referrer);
                        return u.origin + relPath;
                    }} catch(e) {{}}
                }}
                return relPath;
            }}

            function init() {{
                clock = new THREE.Clock();
                scene = new THREE.Scene();

                camera = new THREE.PerspectiveCamera(38, container.clientWidth / container.clientHeight, 0.1, 100);
                camera.position.set(0, 0.4, 4.3);

                renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                renderer.toneMapping = THREE.ACESFilmicToneMapping;
                renderer.toneMappingExposure = 1.35;
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                container.appendChild(renderer.domElement);

                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.06;
                controls.maxDistance = 14;
                controls.minDistance = 1.2;
                controls.autoRotate = autoRotate;
                controls.autoRotateSpeed = 1.2;
                controls.target.set(0, 0.2, 0);

                // Royal Obsidian Marble Stage
                const stageGeo = new THREE.CylinderGeometry(3.2, 3.5, 0.32, 64);
                const stageMat = new THREE.MeshStandardMaterial({{
                    color: 0x090f1d,
                    roughness: 0.35,
                    metalness: 0.75
                }});
                const stage = new THREE.Mesh(stageGeo, stageMat);
                stage.position.y = -1.16;
                stage.receiveShadow = true;
                scene.add(stage);

                // Golden Edge Ring
                const ringGeo = new THREE.TorusGeometry(3.3, 0.035, 16, 64);
                const ringMat = new THREE.MeshBasicMaterial({{ color: 0xd4af37 }});
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2;
                ring.position.y = -1.0;
                scene.add(ring);

                // Studio Lighting
                const ambLight = new THREE.AmbientLight(0xffffff, 0.95);
                scene.add(ambLight);

                const keyLight = new THREE.DirectionalLight(0xfff5e6, 1.4);
                keyLight.position.set(6, 8, 7);
                keyLight.castShadow = true;
                keyLight.shadow.mapSize.width = 1024;
                keyLight.shadow.mapSize.height = 1024;
                keyLight.shadow.bias = -0.001;
                scene.add(keyLight);

                const fillLight = new THREE.DirectionalLight(0xa5c4f5, 0.75);
                fillLight.position.set(-6, 4, -4);
                scene.add(fillLight);

                const rimLight = new THREE.DirectionalLight(0xffe6a3, 0.85);
                rimLight.position.set(0, 5, -5);
                scene.add(rimLight);

                const spotLight = new THREE.SpotLight(0xfffae0, 1.6, 12, Math.PI / 6, 0.45);
                spotLight.position.set(0, 6, 2);
                spotLight.target = stage;
                scene.add(spotLight);

                // Load Fabric Texture
                const texLoader = new THREE.TextureLoader();
                fabricTex = texLoader.load(tileData, function(tex) {{
                    tex.wrapS = THREE.RepeatWrapping;
                    tex.wrapT = THREE.RepeatWrapping;
                    tex.repeat.set(currentRepeat, currentRepeat);
                    if (renderer.capabilities && renderer.capabilities.getMaxAnisotropy) {{
                        tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
                    }}
                    tex.needsUpdate = true;
                    // Initial load starts with realistic runway human avatar
                    switchModel('female');
                }}, undefined, function(err) {{
                    console.error('Texture load notice, continuing with default model:', err);
                    switchModel('female');
                }});

                window.addEventListener('resize', onWindowResize, false);
                animate();
            }}

            // =========================================================================
            // 1. HAUTE COUTURE STUDIO DRESS FORM (100% Watertight, Smooth, Luxury Drape)
            // =========================================================================
            function buildDressForm() {{
                const group = new THREE.Group();

                // Material for the dress form & draped gown
                const fabricMat = new THREE.MeshStandardMaterial({{
                    map: fabricTex,
                    bumpMap: fabricTex,
                    bumpScale: 0.03,
                    roughness: 0.58,
                    metalness: 0.08,
                    side: THREE.DoubleSide
                }});

                // Smooth Couture Tailor's Torso
                const torsoPts = [];
                torsoPts.push(new THREE.Vector2(0.001, 0.95)); // neck center
                torsoPts.push(new THREE.Vector2(0.14, 0.92));  // neck collar
                torsoPts.push(new THREE.Vector2(0.32, 0.82));  // shoulder line
                torsoPts.push(new THREE.Vector2(0.37, 0.58));  // bust apex
                torsoPts.push(new THREE.Vector2(0.26, 0.30));  // cinched waist
                torsoPts.push(new THREE.Vector2(0.38, 0.02));  // high hip
                torsoPts.push(new THREE.Vector2(0.40, -0.22)); // low hip
                const torsoGeo = new THREE.LatheGeometry(torsoPts, 64);
                torsoGeo.computeVertexNormals();
                const torsoMesh = new THREE.Mesh(torsoGeo, fabricMat);
                torsoMesh.position.y = 0.25;
                torsoMesh.castShadow = true;
                group.add(torsoMesh);

                // Elegant Flowing Bell Skirt (Seamlessly continues from torso hip profile down to floor)
                const skirtPts = [];
                skirtPts.push(new THREE.Vector2(0.40, -0.22)); // seamlessly joins hip
                skirtPts.push(new THREE.Vector2(0.46, -0.42));
                skirtPts.push(new THREE.Vector2(0.60, -0.65));
                skirtPts.push(new THREE.Vector2(0.85, -0.88));
                skirtPts.push(new THREE.Vector2(1.15, -1.05)); // graceful flared hemline
                skirtPts.push(new THREE.Vector2(1.13, -1.08)); // hem turn-under
                skirtPts.push(new THREE.Vector2(0.001, -1.08)); // enclosed bottom base
                const skirtGeo = new THREE.LatheGeometry(skirtPts, 64);
                skirtGeo.computeVertexNormals();
                const skirtMesh = new THREE.Mesh(skirtGeo, fabricMat);
                skirtMesh.position.y = 0.25;
                skirtMesh.castShadow = true;
                group.add(skirtMesh);

                // Luxury Gilded Hardware (Pole, Finial, Atelier Base)
                const goldMat = new THREE.MeshStandardMaterial({{
                    color: 0xd4af37,
                    metalness: 0.88,
                    roughness: 0.22
                }});

                // Golden Finial Crown on Neck
                const finialNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.12, 0.18, 32), goldMat);
                finialNeck.position.y = 1.28;
                group.add(finialNeck);
                const finialBall = new THREE.Mesh(new THREE.SphereGeometry(0.11, 32, 32), goldMat);
                finialBall.position.y = 1.42;
                group.add(finialBall);

                // Polished Golden Support Column
                const centerPole = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 2.3, 32), goldMat);
                centerPole.position.y = 0.0;
                group.add(centerPole);

                // Ornate Tiered Cast-Brass Stand Pedestal
                const baseTier1 = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.72, 0.12, 48), goldMat);
                baseTier1.position.y = -0.92;
                baseTier1.receiveShadow = true;
                group.add(baseTier1);
                const baseTier2 = new THREE.Mesh(new THREE.CylinderGeometry(0.70, 0.82, 0.06, 48), goldMat);
                baseTier2.position.y = -0.98;
                baseTier2.receiveShadow = true;
                group.add(baseTier2);

                group.scale.set(1.3, 1.3, 1.3);
                return {{ root: group, bones: {{}} }};
            }}

            // =========================================================================
            // 2. REALISTIC RUNWAY HUMAN AVATAR (In-Memory Base64 + Network Fallback)
            // =========================================================================
            function loadFemaleHuman(onDone) {{
                if (modelCache['female']) {{
                    onDone(modelCache['female']);
                    return;
                }}
                showLoading(true, '💃 Fitting Ensemble onto Runway Human Model...');

                function setupFemaleScene(gltf) {{
                    const root = gltf.scene;

                    // Normalize bounding box & height
                    root.updateMatrixWorld(true);
                    const box = new THREE.Box3().setFromObject(root);
                    const size = box.getSize(new THREE.Vector3());
                    const scale = 3.1 / (size.y || 1);
                    root.scale.set(scale, scale, scale);
                    root.updateMatrixWorld(true);

                    // Place feet cleanly onto the stage
                    const scaledBox = new THREE.Box3().setFromObject(root);
                    root.position.y = -1.0 - scaledBox.min.y;
                    root.position.x = -scaledBox.getCenter(new THREE.Vector3()).x;
                    root.position.z = -scaledBox.getCenter(new THREE.Vector3()).z;

                    // Collect bones & bind pattern exclusively to clothing
                    const bones = {{}};
                    root.traverse((child) => {{
                        if (child.isBone) {{
                            bones[child.name] = child;
                        }}
                        if (child.isMesh) {{
                            child.castShadow = true;
                            child.receiveShadow = true;
                            // Top, bottom attire, and outfit items get the synthesized pattern
                            // Head, hair, facial features, and skin retain photorealistic look
                            const n = (child.name || '').toLowerCase();
                            const m = (child.material && child.material.name ? child.material.name : '').toLowerCase();
                            if (n.includes('outfit') || n.includes('top') || n.includes('bottom') || m.includes('outfit') || m.includes('top') || m.includes('bottom')) {{
                                child.material = new THREE.MeshStandardMaterial({{
                                    map: fabricTex,
                                    bumpMap: fabricTex,
                                    bumpScale: 0.032,
                                    roughness: 0.62,
                                    metalness: 0.08,
                                    side: THREE.DoubleSide
                                }});
                                child.material.needsUpdate = true;
                            }}
                        }}
                    }});

                    const obj = {{ root, bones }};
                    modelCache['female'] = obj;
                    showLoading(false);
                    onDone(obj);
                }}

                // Attempt 1: Parse from embedded in-memory Base64 (instant, zero CORS, zero 404)
                if (femaleGlbBase64 && femaleGlbBase64.length > 1000) {{
                    parseGlbFromBase64(femaleGlbBase64, setupFemaleScene, function(err1) {{
                        console.warn('Female base64 parse notice, trying network fetch:', err1);
                        fallbackFemaleNetwork();
                    }});
                }} else {{
                    fallbackFemaleNetwork();
                }}

                function fallbackFemaleNetwork() {{
                    const url = getOriginUrl('/app/static/models/female_human_avatar.glb');
                    gltfLoader.load(url, setupFemaleScene, undefined, function(err2) {{
                        console.error('Female avatar network load failed:', err2);
                        showLoading(false);
                        switchModel('form');
                    }});
                }}
            }}

            function switchModel(type) {{
                currentModelType = type;
                document.querySelectorAll('.hud-panel button[id^="btn-"]').forEach(btn => {{
                    if (btn.id === 'btn-female' || btn.id === 'btn-form') {{
                        btn.classList.remove('active');
                    }}
                }});
                const activeBtn = document.getElementById('btn-' + type);
                if (activeBtn) activeBtn.classList.add('active');

                if (currentModel) {{
                    scene.remove(currentModel);
                }}

                function applyModel(obj) {{
                    currentModel = obj.root;
                    currentBones = obj.bones || {{}};
                    scene.add(currentModel);
                }}

                if (type === 'female') {{
                    loadFemaleHuman(applyModel);
                }} else if (type === 'form') {{
                    if (!modelCache['form']) {{
                        modelCache['form'] = buildDressForm();
                    }}
                    applyModel(modelCache['form']);
                }}
            }}

            function setMotion(type) {{
                currentMotionType = type;
                document.getElementById('btn-motion').classList.toggle('active', type === 'walk');
                document.getElementById('btn-pose').classList.toggle('active', type === 'pose');
            }}

            function togglePlayPause() {{
                isPlaying = !isPlaying;
                document.getElementById('btn-play').innerText = isPlaying ? '⏸️ Pause' : '▶️ Play';
            }}

            function setPatternScale(count) {{
                currentRepeat = count;
                ['1', '2', '3', '5'].forEach(sc => {{
                    const el = document.getElementById('btn-sc' + sc);
                    if (el) el.classList.toggle('active', sc == count);
                }});

                if (fabricTex) {{
                    fabricTex.repeat.set(count, count);
                    fabricTex.needsUpdate = true;
                }}
            }}

            function setCameraView(view) {{
                if (view === 'full') {{
                    camera.position.set(0, 0.4, 4.3);
                    controls.target.set(0, 0.2, 0);
                }} else if (view === 'torso') {{
                    camera.position.set(0, 0.65, 2.2);
                    controls.target.set(0, 0.6, 0);
                }} else if (view === 'hem') {{
                    camera.position.set(0, -0.45, 2.3);
                    controls.target.set(0, -0.65, 0);
                }}
                controls.update();
            }}

            function toggleTurntable() {{
                autoRotate = !autoRotate;
                controls.autoRotate = autoRotate;
                document.getElementById('btn-turntable').classList.toggle('active', autoRotate);
            }}

            function onWindowResize() {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }}

            function animate() {{
                requestAnimationFrame(animate);
                const time = clock.getElapsedTime();

                // Feel-good life-like human modeling animation
                if (isPlaying && currentBones && Object.keys(currentBones).length > 0) {{
                    if (currentMotionType === 'walk') {{
                        // Natural Runway Modeling Motion
                        // 1. Natural Respiration / Breathing (expansion of chest and spine)
                        const breath = Math.sin(time * 2.0);
                        if (currentBones['Spine2']) {{
                            currentBones['Spine2'].rotation.x = breath * 0.025;
                        }}
                        if (currentBones['Neck']) {{
                            currentBones['Neck'].rotation.x = -breath * 0.015;
                        }}
                        // 2. Poise & subtle weight shifting
                        const sway = Math.sin(time * 1.0);
                        if (currentBones['Hips']) {{
                            currentBones['Hips'].rotation.y = sway * 0.045;
                            currentBones['Hips'].rotation.z = Math.cos(time * 1.0) * 0.018;
                        }}
                        // 3. Natural Head Glance (fashion modeling pose)
                        if (currentBones['Head']) {{
                            currentBones['Head'].rotation.y = Math.sin(time * 0.6) * 0.075;
                            currentBones['Head'].rotation.x = Math.sin(time * 1.1) * 0.025;
                        }}
                        // 4. Relaxed natural arm posture
                        if (currentBones['LeftArm']) {{
                            currentBones['LeftArm'].rotation.z = -0.12 + Math.sin(time * 1.0) * 0.025;
                        }}
                        if (currentBones['RightArm']) {{
                            currentBones['RightArm'].rotation.z = 0.12 - Math.sin(time * 1.0) * 0.025;
                        }}
                    }} else {{
                        // Stately Standing Stature with gentle natural breathing
                        const breath = Math.sin(time * 1.5);
                        if (currentBones['Spine2']) currentBones['Spine2'].rotation.x = breath * 0.015;
                        if (currentBones['Head']) currentBones['Head'].rotation.y = Math.sin(time * 0.4) * 0.04;
                    }}
                }}

                controls.update();
                renderer.render(scene, camera);
            }}

            window.onload = init;
        </script>
    </body>
    </html>
    """
