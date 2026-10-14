import json

def render_threejs_avatar_viewer(
    tile_b64: str,
    matched_style: str = "Royal Haute Couture",
    height: int = 650
) -> str:
    """
    Renders an interactive Three.js WebGL fashion runway viewport where realistic, natural
    human models (Woman in runway outfit, Man in tailored suit/kurta, or Haute Couture Dress Form)
    wear the synthesized textile pattern in real-time feel-good motion.
    """
    style_clean = matched_style.replace('"', '\\"')

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
                background: rgba(9, 14, 26, 0.88);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(212, 175, 55, 0.35);
                border-radius: 12px;
                padding: 8px 14px;
                z-index: 10;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65);
                max-width: calc(100% - 28px);
            }}
            .hud-btn {{
                background: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(212, 175, 55, 0.25);
                color: #f1f5f9;
                padding: 6px 12px;
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
                box-shadow: 0 0 12px rgba(212, 175, 55, 0.5);
            }}
            .hud-sep {{
                width: 1px;
                height: 18px;
                background: rgba(212, 175, 55, 0.3);
                margin: 0 2px;
            }}
            .fit-badge {{
                position: absolute;
                top: 14px;
                right: 14px;
                background: rgba(9, 14, 26, 0.88);
                backdrop-filter: blur(14px);
                border: 1px solid rgba(212, 175, 55, 0.45);
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
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
            }}
            .hud-footer {{
                position: absolute;
                bottom: 12px;
                right: 14px;
                background: rgba(9, 14, 26, 0.82);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(212, 175, 55, 0.25);
                border-radius: 8px;
                padding: 5px 12px;
                font-size: 11px;
                color: #fce7a1;
                pointer-events: none;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
                z-index: 10;
            }}
            #loading-overlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(7, 11, 22, 0.88);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 14px;
                z-index: 25;
                transition: opacity 0.4s ease;
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
            <div style="font-size: 13px; font-weight: 700; color: #fce7a1; letter-spacing: 0.5px;">
                ⚜️ Fitting Tailored Garment onto Runway Model...
            </div>
        </div>

        <div class="hud-panel">
            <span style="font-size: 11px; font-weight: 800; color: #D4AF37; margin-right: 3px;">FASHION MODEL:</span>
            <button class="hud-btn active" id="btn-female" onclick="switchModel('female')">💃 Woman (Runway Ensemble)</button>
            <button class="hud-btn" id="btn-male" onclick="switchModel('male')">🕺 Man (Tailored Suit)</button>
            <button class="hud-btn" id="btn-form" onclick="switchModel('form')">👗 Studio Dress Form</button>

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
            const tileData = "{tile_b64}";

            const modelCache = {{}};
            const gltfLoader = new THREE.GLTFLoader();
            let fabricTex = null;

            function showLoading(show) {{
                if (loadingOverlay) {{
                    loadingOverlay.style.opacity = show ? '1' : '0';
                    loadingOverlay.style.pointerEvents = show ? 'auto' : 'none';
                }}
            }}

            function init() {{
                clock = new THREE.Clock();
                scene = new THREE.Scene();

                camera = new THREE.PerspectiveCamera(38, container.clientWidth / container.clientHeight, 0.1, 100);
                camera.position.set(0, 0.35, 4.2);

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
                controls.target.set(0, 0.15, 0);

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
                const ambLight = new THREE.AmbientLight(0xffffff, 0.85);
                scene.add(ambLight);

                const keyLight = new THREE.DirectionalLight(0xfff0d8, 1.45);
                keyLight.position.set(6, 8, 7);
                keyLight.castShadow = true;
                keyLight.shadow.mapSize.width = 1024;
                keyLight.shadow.mapSize.height = 1024;
                keyLight.shadow.bias = -0.001;
                scene.add(keyLight);

                const fillLight = new THREE.DirectionalLight(0x90b4ee, 0.75);
                fillLight.position.set(-6, 4, -4);
                scene.add(fillLight);

                const rimLight = new THREE.DirectionalLight(0xffe6a3, 0.8);
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
                    // Load initial model after texture is ready
                    switchModel('female');
                }});

                window.addEventListener('resize', onWindowResize, false);
                animate();
            }}

            function buildDressForm() {{
                const group = new THREE.Group();

                // Couture Torso form
                const pts = [];
                pts.push(new THREE.Vector2(0.001, 1.05));
                pts.push(new THREE.Vector2(0.18, 1.0));
                pts.push(new THREE.Vector2(0.38, 0.85));
                pts.push(new THREE.Vector2(0.42, 0.60));
                pts.push(new THREE.Vector2(0.30, 0.35));
                pts.push(new THREE.Vector2(0.44, 0.0));
                pts.push(new THREE.Vector2(0.42, -0.25));
                pts.push(new THREE.Vector2(0.001, -0.25));
                const torsoGeo = new THREE.LatheGeometry(pts, 48);
                const torsoMat = new THREE.MeshStandardMaterial({{
                    map: fabricTex,
                    bumpMap: fabricTex,
                    bumpScale: 0.03,
                    roughness: 0.65,
                    metalness: 0.12
                }});
                const torsoMesh = new THREE.Mesh(torsoGeo, torsoMat);
                torsoMesh.position.y = 0.25;
                torsoMesh.castShadow = true;
                group.add(torsoMesh);

                // Pleated Flared Gown Skirt
                const skirtGeo = new THREE.CylinderGeometry(0.32, 1.45, 1.35, 72, 32, true);
                const sPos = skirtGeo.attributes.position;
                for (let i = 0; i < sPos.count; i++) {{
                    const y = sPos.getY(i);
                    const ratio = (-y + 0.675) / 1.35;
                    const angle = Math.atan2(sPos.getZ(i), sPos.getX(i));
                    const pleat = Math.sin(angle * 14) * 0.09 * ratio;
                    sPos.setX(i, sPos.getX(i) * (1 + pleat));
                    sPos.setZ(i, sPos.getZ(i) * (1 + pleat));
                }}
                skirtGeo.computeVertexNormals();
                const skirtMesh = new THREE.Mesh(skirtGeo, torsoMat);
                skirtMesh.position.y = -0.35;
                skirtMesh.castShadow = true;
                group.add(skirtMesh);

                // Golden Stand & Pole
                const poleGeo = new THREE.CylinderGeometry(0.045, 0.045, 2.2, 24);
                const goldMat = new THREE.MeshStandardMaterial({{
                    color: 0xd4af37,
                    metalness: 0.85,
                    roughness: 0.25
                }});
                const pole = new THREE.Mesh(poleGeo, goldMat);
                pole.position.y = -0.1;
                group.add(pole);

                // Golden Finial Crown
                const finialGeo = new THREE.SphereGeometry(0.12, 24, 24);
                const finial = new THREE.Mesh(finialGeo, goldMat);
                finial.position.y = 1.35;
                group.add(finial);

                // Tripod Base
                const baseGeo = new THREE.CylinderGeometry(0.55, 0.7, 0.12, 32);
                const base = new THREE.Mesh(baseGeo, goldMat);
                base.position.y = -0.94;
                base.receiveShadow = true;
                group.add(base);

                group.scale.set(1.35, 1.35, 1.35);
                return {{ root: group, bones: {{}} }};
            }}

            function loadFemaleHuman(onDone) {{
                if (modelCache['female']) {{
                    onDone(modelCache['female']);
                    return;
                }}
                showLoading(true);
                const url = '/app/static/models/female_human_avatar.glb';

                gltfLoader.load(url, function(gltf) {{
                    const root = gltf.scene;

                    // Normalize bounding box & height
                    const box = new THREE.Box3().setFromObject(root);
                    const size = box.getSize(new THREE.Vector3());
                    const scale = 3.1 / (size.y || 1);
                    root.scale.set(scale, scale, scale);

                    // Place feet on stage top
                    const scaledBox = new THREE.Box3().setFromObject(root);
                    root.position.y = -1.0 - scaledBox.min.y;
                    root.position.x = -scaledBox.getCenter(new THREE.Vector3()).x;
                    root.position.z = -scaledBox.getCenter(new THREE.Vector3()).z;

                    // Collect bones & map fabric to outfit
                    const bones = {{}};
                    root.traverse((child) => {{
                        if (child.isBone) {{
                            bones[child.name] = child;
                        }}
                        if (child.isMesh) {{
                            child.castShadow = true;
                            child.receiveShadow = true;
                            // Only apply pattern to top and bottom clothes!
                            // Head, Hair, Eyes, and Body skin retain photorealistic look
                            if (child.name === 'Wolf3D_Outfit_Top' || child.name === 'Wolf3D_Outfit_Bottom.002' || (child.material && child.material.name.includes('Outfit'))) {{
                                child.material = new THREE.MeshStandardMaterial({{
                                    map: fabricTex,
                                    bumpMap: fabricTex,
                                    bumpScale: 0.035,
                                    roughness: 0.65,
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
                }}, undefined, function(err) {{
                    console.error('Female avatar load failed:', err);
                    showLoading(false);
                    switchModel('form');
                }});
            }}

            function loadMaleHuman(onDone) {{
                if (modelCache['male']) {{
                    onDone(modelCache['male']);
                    return;
                }}
                showLoading(true);
                const url = '/app/static/models/male_human_avatar.glb';

                gltfLoader.load(url, function(gltf) {{
                    const root = gltf.scene;

                    // Normalize bounding box & height
                    const box = new THREE.Box3().setFromObject(root);
                    const size = box.getSize(new THREE.Vector3());
                    const scale = 3.1 / (size.y || 1);
                    root.scale.set(scale, scale, scale);

                    // Place feet on stage top
                    const scaledBox = new THREE.Box3().setFromObject(root);
                    root.position.y = -1.0 - scaledBox.min.y;
                    root.position.x = -scaledBox.getCenter(new THREE.Vector3()).x;
                    root.position.z = -scaledBox.getCenter(new THREE.Vector3()).z;

                    const bones = {{}};
                    root.traverse((child) => {{
                        if (child.isBone) {{
                            bones[child.name] = child;
                        }}
                        if (child.isMesh) {{
                            child.castShadow = true;
                            child.receiveShadow = true;
                            // Apply fabric to tailored jacket/suit and pants (avaturn_look_0)
                            // Head_Mesh, Hair, and Eyes retain photorealistic look
                            if (child.name === 'avaturn_look_0' || (child.material && child.material.name.includes('look'))) {{
                                child.material = new THREE.MeshStandardMaterial({{
                                    map: fabricTex,
                                    bumpMap: fabricTex,
                                    bumpScale: 0.035,
                                    roughness: 0.65,
                                    metalness: 0.08,
                                    side: THREE.DoubleSide
                                }});
                                child.material.needsUpdate = true;
                            }}
                        }}
                    }});

                    const obj = {{ root, bones }};
                    modelCache['male'] = obj;
                    showLoading(false);
                    onDone(obj);
                }}, undefined, function(err) {{
                    console.error('Male avatar load failed:', err);
                    showLoading(false);
                    switchModel('form');
                }});
            }}

            function switchModel(type) {{
                currentModelType = type;
                document.querySelectorAll('.hud-panel button[id^="btn-"]').forEach(btn => {{
                    if (btn.id === 'btn-female' || btn.id === 'btn-male' || btn.id === 'btn-form') {{
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
                    currentBones = obj.bones;
                    scene.add(currentModel);
                }}

                if (type === 'female') {{
                    loadFemaleHuman(applyModel);
                }} else if (type === 'male') {{
                    loadMaleHuman(applyModel);
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
                    camera.position.set(0, 0.35, 4.2);
                    controls.target.set(0, 0.15, 0);
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
                if (isPlaying && currentBones) {{
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
