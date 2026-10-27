---
name: awward-winning
description: >-
  The definitive AI agent skill for generating Awwwards Site of the Day (SOTD) and Site of the Year (SOTY)
  caliber creative websites. Masterfully unifies cinematic 3D film sets, dual-layer in-scene monitor projections
  with live HTML OSs, Spline 3D + DALL-E 3 asset pipelines, 1:1 multimodal vision reference cloning, custom GLSL
  shaders (CRT barrel bulge, velocity zoom blur, orbital mesh warp), and Framer University micro-interactions.
---

# Awward-Winning Web Design & Engineering Skill

An elite, industry-defining skill and operational manual for AI agents to conceive, architect, and code **Awwwards / FWA / Webby Site of the Day & Site of the Year tier creative web experiences** (pioneered by legendary productions like [helloworlddsgn.com](https://helloworlddsgn.com/) and [grit.pictures](https://grit.pictures/)).

---

## 1. The Core Mental Model: The "Playable Film Set"

When tasked with creating an award-winning creative website, **never think in terms of a flat 2D webpage with a 3D model embedded in a canvas**. 

Instead, think as a **Director, Cinematographer, and Technical Architect on a Playable Film Set**:
- **The World is a Physical Stage**: The website is a living 3D environment (a room, a landscape, a futuristic laboratory, a cyber-vortex) populated with physically modeled props, lighting, and atmosphere.
- **The User is the Camera Operator**: The user's scroll position does not merely slide HTML elements up and down; it drives a virtual 35mm cinema camera along mathematically calculated spatial splines, pulling back from macro close-ups into wide cinematic vistas.
- **Screens Within the Screen**: Interactive devices inside the 3D world (monitors, phones, slates, holographic displays) are **dual-layered entities**:
  1. *Subservient 3D mesh* inside WebGL receiving scene lighting, ambient occlusion, and reflections.
  2. *Living HTML DOM interface* dynamically projected and pinned onto the 3D mesh surface using camera matrix transformations, allowing native drag-and-drop, real text selection, forms, and interactive buttons.
- **Narrative Progression via Era Morphing**: Scrolling does not just reveal new sections; it physically transforms the entire 3D world (lighting temperature shifts, geometry morphs, haze clears, objects evolve).

---

## 2. The Interactive Monitor Mechanism (Virtual OS on 3D Mesh)

The defining hallmark of high-end sites like *Hello World* is a 3D monitor in the scene that transitions and responds to user interaction.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DUAL-LAYER SCREEN ARCHITECTURE                        │
├──────────────────────────────────────┬──────────────────────────────────────┤
│          3D WEBGL MESH LAYER         │          2D HTML OS OVERLAY          │
│ • GLTF 3D Room Environment           │ • Pure HTML/CSS Desktop UI           │
│ • PBR Case & Frame Reflections       │ • Real Clickable Buttons & Forms     │
│ • CRT Barrel Distortion Shader       │ • OS 95 -> OS 7 -> OS 11 Morphs      │
│ • Curved Tube Bulge & Scanlines      │ • Tension Physics (Tilt & Tremble)   │
└──────────────────────────────────────┴──────────────────────────────────────┘
                                  ▲
                                  │ project(camera)
                                  │ translate3d(x, y, 0) scale(sx, sy)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PIXEL-PERFECT SYNC: HTML element follows 3D screen corners every frame      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### A. The 3D-to-2D Matrix Projection Formula
To pin a live HTML DOM interface (such as a simulated operating system) onto a 3D monitor mesh:

```javascript
// Pinning a 1600x900 HTML container onto a 3D mesh bounding box
const vTopLeft = new THREE.Vector3();
const vBottomRight = new THREE.Vector3();

function projectToPixel(vector, camera, canvas) {
  const v = vector.clone().project(camera);
  return {
    x: (v.x * 0.5 + 0.5) * canvas.clientWidth,
    y: (-v.y * 0.5 + 0.5) * canvas.clientHeight
  };
}

function updateVirtualScreen(htmlScreenElement, screenMesh3D, camera, canvas) {
  if (!screenMesh3D || !htmlScreenElement) return;

  const bbox = new THREE.Box3().setFromObject(screenMesh3D);
  vTopLeft.set(bbox.min.x, bbox.max.y, bbox.max.z);
  vBottomRight.set(bbox.max.x, bbox.min.y, bbox.max.z);

  const p1 = projectToPixel(vTopLeft, camera, canvas);
  const p2 = projectToPixel(vBottomRight, camera, canvas);

  const scaleX = (p2.x - p1.x) / 1600; // Native HTML canvas width
  const scaleY = (p2.y - p1.y) / 900;  // Native HTML canvas height

  htmlScreenElement.style.transform = 
    `translate3d(${p1.x.toFixed(1)}px, ${p1.y.toFixed(1)}px, 0) scale(${scaleX.toFixed(4)}, ${scaleY.toFixed(4)})`;
}
```

### B. The CRT Curved Tube Shader (Bulge, Scanlines, Aperture Grille)
For retro monitors, map an offscreen procedural canvas onto a curved tube shader:
```glsl
// Custom CRT Fragment Shader
uniform sampler2D map;
uniform float time, power;
varying vec2 vUv;

void main() {
  vec2 c = vUv - 0.5;
  // Convex barrel tube distortion: picture bulges towards viewer
  vec2 uv = 0.5 + c * (1.0 + 0.09 * dot(c, c) * 4.0) * 0.94;
  
  if (uv.x < 0.0 || uv.y < 0.0 || uv.x > 1.0 || uv.y > 1.0) {
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    return;
  }
  
  vec3 col = texture2D(map, uv).rgb;
  
  // Anti-aliased dynamic scanlines (scales with screen size to prevent moire)
  float lines = fwidth(uv.y) * 1080.0;
  col *= 1.0 - 0.1 * (0.5 - 0.5 * cos(uv.y * 1080.0 * 3.14159)) * (1.0 - smoothstep(0.5, 1.0, lines));
  
  // Soft CRT vignette corners
  col *= mix(0.55, 1.0, smoothstep(0.75, 0.3, length(c * vec2(1.0, 1.15))));
  gl_FragColor = vec4(col * power, 1.0);
}
```

---

## 3. Scroll Choreography & The Interactive "Gates" Engine

### A. The Camera Spline Timeline
Measure the story progression in viewport heights (`vh`) rather than arbitrary pixel offsets:
- `pv = (scrollY / innerHeight) * 100` (Scroll percentage in `vh`).
- Interpolate camera position and target across defined stages using cubic hermite easing:

```javascript
function updateCameraFlight(pv) {
  // Stage 1: Macro close-up on monitor (0vh to 200vh)
  const t1 = easeInOutCubic(clamp((pv - 0) / 200, 0, 1));
  camera.position.lerpVectors(CLOSE_SHOT.pos, WIDE_SHOT.pos, t1);
  camera.lookAt(targetVector.lerpVectors(CLOSE_SHOT.target, WIDE_SHOT.target, t1));
  
  // Camera lens tension & mouse parallax
  camera.position.x += mouseSmooth.x * 0.22 * (1 - 0.9 * t1);
  camera.position.y -= mouseSmooth.y * 0.10 * (1 - 0.9 * t1);
  camera.rotateZ(-mouseSmooth.x * 0.008); // Subtle handheld camera roll
}
```

### B. Interactive Scroll Gates (Refusal & Spring Bounce)
When an on-screen interaction is required (e.g. dragging a cable plug, holding an update button, confirming a dialog), **scrolling down must be intercepted and rejected with a physical spring bounce**:

```javascript
const GATES = [
  { id: "connect", triggerVh: 0, completed: false },
  { id: "os_upgrade", triggerVh: 380, completed: false }
];

window.addEventListener("wheel", (e) => {
  const activeGate = GATES.find(g => !g.completed && currentVh >= g.triggerVh);
  if (activeGate && e.deltaY > 0) {
    e.preventDefault();
    // Trigger physical bounce animation on page
    document.body.classList.add("scroll-bounce-shake");
    setTimeout(() => document.body.classList.remove("scroll-bounce-shake"), 250);
  }
}, { passive: false });
```

---

## 4. Environment & Era Morphing System

In award-winning 3D sites, scrolling down transforms the environment dynamically:
1. **Light Temperature & Position Transition**:
   - Transitioning from 90s tungsten amber (`#f3aa56`, 3.4 intensity) to modern daylight LED (`#e4effa`, 2.2 intensity).
   - Moving spotlight coordinates and angles smoothly as the user advances through history.
2. **Atmospheric Fog & Haze**:
   - Starting with dense amber haze around the CRT screen (`#5a4436`), clearing into deep midnight blue (`#0b0c18`).
3. **Cardboard / Mesh Vertex Morph Wave**:
   - Passing a horizontal spatial wave coordinate (`uWaveA`, `uWaveB`) to a custom vertex shader that peels or unfolds retro geometry into modern geometry.

---

## 5. 3D-to-2D Hybrid DOM Anchoring (`html-text`)

Instead of rendering 3D text into WebGL (which creates blurry textures, breaks browser translation, and destroys SEO/accessibility):
1. Create real HTML headings (`<h2>`, `<p>`).
2. Attach them to an invisible 3D world anchor coordinate (`new THREE.Vector3(0, 1.9, -1.2)`).
3. Every frame, project the coordinate:
   $$\text{scale} = \frac{\text{pxPerMetre}(\text{camera}, \text{anchor})}{\text{baseScale}}$$
   $$\text{position} = \text{project}(\text{anchor})$$
4. Apply auto-avoidance logic: calculate distance to the 3D monitor and automatically nudge the HTML text upward or downward so it never obscures interactive 3D props.

---

## 6. Custom Cinematic Shaders Library

### A. Live WebGL Mesh Gradient Shader (`mesh.js`)
A super-lightweight 5-point orbital mesh gradient with domain warping and noise dithering:
- **Optimization Trick**: Render to an off-screen canvas at **1/3 resolution** (`scale = 0.33`) because soft gradients do not require high pixel density. This saves 90% GPU fillrate!

### B. Radial Velocity Zoom Blur Shader (`works.js`)
When traveling between chapters in a 3D camera fly-through tunnel, calculate travel velocity and apply a 10-tap weighted radial blur along vector $(uv - 0.5)$:
```glsl
uniform sampler2D tex;
uniform float uBlur;
varying vec2 vUv;

void main() {
  vec2 d = vUv - 0.5;
  if (uBlur < 0.01) {
    gl_FragColor = texture2D(tex, vUv);
    return;
  }
  vec4 acc = vec4(0.0);
  float totalWeight = 0.0;
  for (int i = 0; i < 10; i++) {
    float k = float(i) / 9.0;
    float w = 1.0 - k * 0.6;
    acc += texture2D(tex, 0.5 + d * (1.0 - uBlur * k * 0.07)) * w;
    totalWeight += w;
  }
  gl_FragColor = acc / totalWeight;
}
```

### C. Master Film Postprocessing Pass
Combine edge chromatic aberration, 9-tap disc lens blur, S-curve tone grading, procedural animated film grain, and vignette in a single unified post-pass to minimize draw calls.

---

## 7. Performance & 60fps Mobile Survival Budget

Next-gen 3D sites will crash mobile devices (iOS WebGL memory limit reload) if not strictly budgeted:
1. **Quality Tiering (Tiers 0, 1, 2)**:
   - **Tier 0 (Low-end / Mobile)**: Disable GTAO (Ambient Occlusion) and UnrealBloom. Render at `DPR = 1.0`.
   - **Tier 1 (Mid-range)**: Enable UnrealBloom, disable GTAO. Render at `DPR = 1.25`.
   - **Tier 2 (High-performance Desktop)**: Full GTAO + Bloom + 8x Anisotropy. Render at `min(window.devicePixelRatio, 1.75)`.
2. **Context Creation on Proximity**:
   - Secondary 3D canvases (like the 3D phone or portfolio tunnel) should only initialize their WebGL context when their container is within `IntersectionObserver(rootMargin: "150% 0px")`. Dispose geometries and textures when scrolled far away.
3. **Texture & Model Optimization**:
   - Compress all 3D geometries with **Draco** or **Meshopt**.
   - Use **KTX2 / Basis Universal** or WebP textures to prevent texture memory bloat.

---

## 8. AI Agent Decision Matrix

When asked to build an award-winning site:
1. **Define the Physical Metaphor**: What is the 3D space? (e.g., retro room, futuristic command deck, architectural pavilion, kinetic art gallery).
2. **Define the Camera Spline**: What are the 3-5 camera waypoints as the user scrolls?
3. **Choose the Screen Inside the Screen**: What interactive device anchors the experience?
4. **Setup the Hybrid Projection**: Establish `vector.project(camera)` for real HTML interactions.
5. **Implement Scroll Gates**: Which narrative milestones require user interaction before releasing scroll?
6. **Apply the Unified Post-Pass**: Add cinematic color grade, subtle grain, and chromatic aberration.

---

## 9. Framer University Autonomous Motion & Mandatory Attribution Rule

Agents may autonomously select and integrate micro-interactions, text reveals, and UI component patterns from **[Framer University](https://framer.university/resources)** (e.g. Blinds Text Reveal, Magnetic Cursor, 3D Image Split Scroll, X-Ray Hover Lens, Shader Buttons, Text Lift). Full recipes are documented in [`references/framer-university-library.md`](./references/framer-university-library.md).

> [!IMPORTANT]
> **MANDATORY ATTRIBUTION PROTOCOL**:  
> Whenever the AI agent autonomously leverages or adapts an interaction pattern from Framer University, the agent **MUST** explicitly notify the user in its response:
> 
> *"💡 Note: Integrated the **[Component Name]** interaction adapted from Framer University ([framer.university/resources](https://framer.university/resources))."*
