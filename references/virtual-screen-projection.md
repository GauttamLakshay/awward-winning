# Virtual Screen & 3D-to-HTML Projection Architecture

This guide details how to implement the dual-layer screen architecture found in `helloworlddsgn.com`, where a live, interactive HTML operating system is pinned onto a 3D monitor mesh rendered in Three.js.

---

## 1. The Core Architecture

In WebGL, rendering interactive HTML inside a 3D scene normally relies on `CSS3DRenderer`. However, `CSS3DRenderer` has major drawbacks:
- It suffers from z-fighting and lighting disconnection.
- HTML elements do not receive WebGL post-processing (bloom, ambient occlusion, depth of field).
- Scaling and pixel density can become blurry on retina displays.

The **Dual-Layer Hybrid Projection System** solves this:
1. The **3D Monitor Mesh** is rendered inside WebGL with physical materials, specular reflections, and ambient occlusion.
2. The **Interactive Operating System** is authored as standard HTML/CSS in a dedicated container (`<div id="screen" class="os">`).
3. Every animation frame, the 3D bounding box corners of the monitor screen mesh are projected through the camera matrix into 2D viewport pixel coordinates.
4. The HTML element is transformed via CSS `translate3d(x, y, 0) scale(sx, sy)` to match the 3D screen perfectly.

---

## 2. Mathematical Coordinate Projection Formula

```javascript
import * as THREE from 'three';

export class ScreenProjectionController {
  constructor(screenMesh, htmlElement, virtualWidth = 1600, virtualHeight = 900) {
    this.mesh = screenMesh;
    this.el = htmlElement;
    this.vW = virtualWidth;
    this.vH = virtualHeight;

    this.box = new THREE.Box3();
    this.topLeft3D = new THREE.Vector3();
    this.bottomRight3D = new THREE.Vector3();
    this.lastTransform = '';
  }

  update(camera, canvas) {
    if (!this.mesh || !this.el) return;

    // 1. Calculate 3D bounding box of the screen mesh
    this.box.setFromObject(this.mesh);
    this.topLeft3D.set(this.box.min.x, this.box.max.y, this.box.max.z);
    this.bottomRight3D.set(this.box.max.x, this.box.min.y, this.box.max.z);

    // 2. Project 3D vectors to normalized device coordinates [-1, 1]
    const p1 = this.topLeft3D.clone().project(camera);
    const p2 = this.bottomRight3D.clone().project(camera);

    // 3. Convert NDC to canvas pixel coordinates
    const W = canvas.clientWidth;
    const H = canvas.clientHeight;
    const x1 = (p1.x * 0.5 + 0.5) * W;
    const y1 = (-p1.y * 0.5 + 0.5) * H;
    const x2 = (p2.x * 0.5 + 0.5) * W;
    const y2 = (-p2.y * 0.5 + 0.5) * H;

    // 4. Calculate scale relative to the virtual HTML canvas size
    const sx = (x2 - x1) / this.vW;
    const sy = (y2 - y1) / this.vH;

    // 5. Apply 60fps hardware-accelerated transform
    const transform = `translate3d(${x1.toFixed(1)}px, ${y1.toFixed(1)}px, 0) scale(${sx.toFixed(4)}, ${sy.toFixed(4)})`;
    if (transform !== this.lastTransform) {
      this.el.style.transform = transform;
      this.lastTransform = transform;
    }
  }
}
```

---

## 3. HTML/CSS OS Container Setup

Ensure the projected element uses top-left transform origin and fixed virtual dimensions:

```css
#screen.os {
  position: fixed;
  top: 0;
  left: 0;
  width: 1600px;
  height: 900px;
  transform-origin: 0 0;
  pointer-events: auto;
  z-index: 50;
  overflow: hidden;
  user-select: none;
  background: #051727;
}

/* Tension Physics: when holding an interactive update button */
#screen.tension {
  animation: screenTremble 0.05s infinite alternate ease-in-out;
}

@keyframes screenTremble {
  0% { filter: brightness(1.05) contrast(1.02); }
  100% { filter: brightness(1.15) contrast(1.08); }
}
```
