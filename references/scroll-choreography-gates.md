# Scroll Choreography, Splines & Interactive Gates

This document covers the scroll timeline architecture, camera spline interpolation, and interactive gate refusal with physical spring bounce.

---

## 1. Measuring Story Progression in `vh`

Never bind 3D animations directly to raw window pixel scroll `window.scrollY`. Instead, normalize the scroll distance relative to viewport height (`vh`):

```javascript
let targetVh = 0;
let currentVh = 0;

function readScroll() {
  targetVh = (window.scrollY / window.innerHeight) * 100;
}

window.addEventListener('scroll', readScroll, { passive: true });

function tick(delta) {
  // Smooth inertial lerp
  currentVh += (targetVh - currentVh) * 0.12;
  updateScene(currentVh);
}
```

---

## 2. Interactive Gates Engine (Scroll Interception & Bounce)

When the story reaches an interactive checkpoint (e.g. at 600vh), the page must refuse scrolling down until the interaction is satisfied:

```javascript
export class ScrollGatesEngine {
  constructor(gatesList) {
    this.gates = gatesList; // Array of { id, triggerVh, completed }
  }

  isBlocked(currentVh) {
    return this.gates.find(g => !g.completed && currentVh >= g.triggerVh);
  }

  completeGate(id) {
    const gate = this.gates.find(g => g.id === id);
    if (gate) gate.completed = true;
  }

  attachListeners() {
    window.addEventListener('wheel', (e) => {
      const currentVh = (window.scrollY / window.innerHeight) * 100;
      const blockedGate = this.isBlocked(currentVh);

      if (blockedGate && e.deltaY > 0) {
        e.preventDefault();
        // Shake feedback indicating scroll is blocked
        const maxScroll = (blockedGate.triggerVh / 100) * window.innerHeight;
        window.scrollTo(0, maxScroll);
        document.body.classList.add('scroll-refused-bounce');
        setTimeout(() => document.body.classList.remove('scroll-refused-bounce'), 200);
      }
    }, { passive: false });
  }
}
```

### CSS Refusal Bounce Keyframes:
```css
body.scroll-refused-bounce {
  animation: scrollSpring 0.22s cubic-bezier(0.2, 0.9, 0.3, 1.2);
}

@keyframes scrollSpring {
  0% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0); }
}
```
