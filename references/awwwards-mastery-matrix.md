# Awwwards Site of the Year Master Decision Matrix

This reference serves as the master decision tree for AI agents to determine **when to use what technology, physics model, and interaction pattern** to create award-winning, extraordinary web experiences.

---

## 1. The Pacing & Emotional Arc (The 4-Act Play)

Awwwards winning websites are never flat scrolls; they follow a cinematic four-act narrative structure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE 4-ACT CINEMATIC ARC                           │
├─────────────────┬──────────────────┬───────────────────┬────────────────────┤
│ ACT 1: HOOK     │ ACT 2: DISCOVERY │ ACT 3: CLIMAX     │ ACT 4: RESOLUTION  │
│ (0 - 150 vh)    │ (150 - 400 vh)   │ (400 - 700 vh)    │ (700+ vh)          │
├─────────────────┼──────────────────┼───────────────────┼────────────────────┤
│ • Macro shot    │ • Camera pullback│ • Spatial morph   │ • Return to wide   │
│ • First physical│ • Atmospheric    │ • Direct device   │ • Portfolio tunnel │
│   interaction   │   lighting shifts│   interaction     │   or works vortex  │
│ • Sound unlock  │ • Hybrid HTML    │ • Interactive gate│ • Tactile contact  │
│ • Zero lag load │   typography     │   tension physics │   & footer slate   │
└─────────────────┴──────────────────┴───────────────────┴────────────────────┘
```

---

## 2. Technology Selection Matrix: When to Use What

| Goal | Primary Tech | Why / Performance Rule | Fallback / Alternative |
| :--- | :--- | :--- | :--- |
| **Interactive In-Scene Device** (Computer, phone, TV) | **3D-to-HTML Matrix Projection** (`vector.project(camera)`) | Renders real clickable HTML DOM inside WebGL with zero blur | Spline 3D Scene Viewer |
| **Micro-Interactions & Text Reveals** | **Framer Motion** (`framer-motion` variants) | Physics springs, GPU accelerated, declarative | Vanilla CSS `cubic-bezier(0.16, 1, 0.3, 1)` |
| **Hero Atmosphere & Vignette** | **GLSL Custom Post-Pass** (Film grain, radial blur, chromatic aberration) | Single unified pass to avoid multi-render target penalties | CSS SVG filter noise (low-end tier) |
| **Custom 3D Scene Props** | **Spline 3D** or **DALL-E 3 + Tripo3D** | Rapid iteration without Blender bottlenecks | Three.js procedural primitives (`RoundedBoxGeometry`) |
| **Narrative Momentum & Stoppage** | **Interactive Scroll Gates** (`wheel` interception) | Forces user to engage with interactive devices before proceeding | Passive scroll indicator |

---

## 3. Sensory Design Checklist (Sound + Sight + Touch)

An extraordinary website stimulates multiple senses simultaneously:

1. **Spatial & Haptic Sound Design**:
   - Subtle mechanical click on button press (synthesized via Web Audio API or 20ms audio buffer).
   - Ambient low-frequency room drone or projector motor hum (muffled when out of focus, clear when focused).
   - Audio must never play unprompted: tied to the first user gesture (e.g. cable connect or sound toggle).
2. **Kinetic Inertia & Tension**:
   - Buttons and draggable elements have mass (`damping: 15, stiffness: 180`).
   - Holding down buttons tightens camera FOV and introduces micro-tremor jitter.
3. **Lighting Temperature Choreography**:
   - Light temperature shifts with time/scroll (e.g., 2700K warm amber $\rightarrow$ 6500K cool daylight).
   - Moving spotlight coordinates tied to camera spline.

---

## 4. The 1:1 Reference Cloning Checklist

When given a reference screenshot by the user:
- [ ] **Palette DNA**: Extract 3 dominant hex colors + ambient light color.
- [ ] **Material Breakdown**: Identify roughness (matte vs gloss), metalness, and transparency.
- [ ] **Decal Segmentation**: Separate background environment, screen interface, and foreground stickers.
- [ ] **Generation & Critic Loop**: Pass prompts to DALL-E 3, evaluate output against reference crop, and apply corrective delta instructions until style fidelity $\ge 95\%$.
- [ ] **Attribution**: Disclose any Framer University interaction patterns utilized.
