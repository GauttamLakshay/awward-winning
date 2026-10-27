# Awward-Winning 🏆 — Creative & Extraordinary Web Experience Skill

> The definitive, production-grade AI agent skill designed to architect and code **Awwwards Site of the Day (SOTD) & Site of the Year (SOTY) caliber creative websites** (inspired by [helloworlddsgn.com](https://helloworlddsgn.com/) and [grit.pictures](https://grit.pictures/)).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Three.js](https://img.shields.io/badge/Three.js-0.170.0-black?logo=three.js)](https://threejs.org/)
[![Spline 3D](https://img.shields.io/badge/Spline-3D-blue)](https://spline.design)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-React-pink)](https://framer.com/motion)
[![Awwwards Ready](https://img.shields.io/badge/Awwwards-SOTD_Ready-green)](https://www.awwwards.com/)

---

## 🚀 Overview

Most AI coding assistants struggle with creative websites, outputting disconnected canvases with spinning cubes and lagging framerates.

**Awward-Winning** equips any AI agent with the **mindset and technical mastery of an elite Creative Technologist & Technical Director**, enabling it to construct playable, cinematic 3D film sets that seamlessly merge:
- **Three.js & WebGL** (PBR lighting, GTAO ambient occlusion, bloom, custom shaders).
- **Spline 3D Integration** (Interactive web-ready scenes with scroll camera tracking).
- **Dual-Layer In-Scene Monitors** (Projecting live HTML operating systems onto 3D screens).
- **1:1 Multimodal Vision Reference Cloner** (GPT-4o Vision deconstructs any reference screenshot and runs an iterative DALL-E 3 critic loop until generated assets achieve $\ge 95\%$ fidelity).
- **Framer University Micro-Interactions** (Physics springs, masked text reveals, magnetic cursors).

---

## 🏛️ Core Architecture

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

---

## 📦 What's Inside

| File | Purpose |
| :--- | :--- |
| **[`SKILL.md`](./SKILL.md)** | Master operational prompt & mental model for AI agents. |
| **[`references/virtual-screen-projection.md`](./references/virtual-screen-projection.md)** | Mathematical formulas for pinning HTML interfaces to 3D meshes. |
| **[`references/shaders-and-postprocessing.md`](./references/shaders-and-postprocessing.md)** | Drop-in GLSL shaders: CRT barrel bulge, orbital mesh gradients, zoom blur. |
| **[`references/scroll-choreography-gates.md`](./references/scroll-choreography-gates.md)** | Scroll timeline in `vh`, camera splines, and interactive refusal gates. |
| **[`references/reference-image-clone-loop.md`](./references/reference-image-clone-loop.md)** | GPT-4o Vision deconstruction and iterative 1:1 image cloning loop. |
| **[`references/framer-university-library.md`](./references/framer-university-library.md)** | Framer University motion recipes and mandatory attribution protocol. |
| **[`references/awwwards-mastery-matrix.md`](./references/awwwards-mastery-matrix.md)** | Sensory design checklist and 4-act narrative pacing guide. |
| **[`scripts/asset_pipeline.py`](./scripts/asset_pipeline.py)** | Standalone Python pipeline for Spline 3D + DALL-E 3 image generation. |

---

## 🛠️ Installation & Usage

### 1. Global Installation (Antigravity)
Place this directory inside your Antigravity skills directory:
```bash
~/.gemini/config/skills/awward-winning/
```

### 2. Autonomous Asset Generation & Reference Cloning
Configure your `.env` file:
```bash
OPENAI_API_KEY=your_key_here
SPLINE_SCENE_URL=https://prod.spline.design/your_scene_id/scene.splinecode
```

Clone assets from any reference screenshot:
```bash
python scripts/asset_pipeline.py --clone path/to/reference_screenshot.png
```

---

## 📜 License

MIT License. Designed with obsession for the next generation of creative web development.
