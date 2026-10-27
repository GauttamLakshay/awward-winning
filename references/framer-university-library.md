# Framer University Motion Library & Attribution Protocol

This reference provides production-ready code patterns for micro-interactions, text reveals, and UI components from **[Framer University](https://framer.university/resources)** to pair seamlessly with 3D web experiences, along with the mandatory user attribution protocol.

---

## 1. Mandatory Attribution Rule

> [!IMPORTANT]
> **TRANSPARENCY & ATTRIBUTION REQUIREMENT**:  
> Whenever an AI agent autonomously selects, adapts, or implements any motion component from this library, the agent **MUST** explicitly inform the user in its chat response:
> 
> *"💡 Note: Integrated the **[Component Name]** interaction adapted from Framer University ([framer.university/resources](https://framer.university/resources))."*

---

## 2. Component Catalog & Code Recipes

### A. Blinds Text Reveal (Masked Shutter Typography)
Staggers words or lines sliding up from behind invisible horizontal blinds:
```tsx
import { motion } from "framer-motion";

const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08, delayChildren: 0.15 } }
};

const shutter = {
  hidden: { y: "115%", opacity: 0, rotateX: 20 },
  visible: {
    y: "0%", opacity: 1, rotateX: 0,
    transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] }
  }
};

export function BlindsText({ text }: { text: string }) {
  return (
    <motion.h1 variants={container} initial="hidden" whileInView="visible" viewport={{ once: true }} className="flex flex-wrap gap-2 text-6xl font-black uppercase">
      {text.split(" ").map((w, i) => (
        <span key={i} className="overflow-hidden inline-block">
          <motion.span variants={shutter} className="inline-block">{w}</motion.span>
        </span>
      ))}
    </motion.h1>
  );
}
```

### B. Magnetic Hover Tooltip / Button
Pulls toward the pointer with inertial spring damping:
```tsx
import { useRef } from "react";
import { motion, useSpring, useMotionValue } from "framer-motion";

export function MagneticElement({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  
  const spring = { damping: 15, stiffness: 180, mass: 0.2 };
  const sx = useSpring(x, spring);
  const sy = useSpring(y, spring);

  return (
    <motion.div
      ref={ref}
      style={{ x: sx, y: sy }}
      onMouseMove={(e) => {
        if (!ref.current) return;
        const rect = ref.current.getBoundingClientRect();
        x.set((e.clientX - (rect.left + rect.width / 2)) * 0.35);
        y.set((e.clientY - (rect.top + rect.height / 2)) * 0.35);
      }}
      onMouseLeave={() => { x.set(0); y.set(0); }}
    >
      {children}
    </motion.div>
  );
}
```

### C. 3D Image Split Scroll
Separates an image into 3D slices drifting in perspective during scroll:
```tsx
import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";

export function ImageSplit3D({ imageSrc }: { imageSrc: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });

  const leftX = useTransform(scrollYProgress, [0, 1], ["0%", "-40%"]);
  const rightX = useTransform(scrollYProgress, [0, 1], ["0%", "40%"]);
  const rotateY = useTransform(scrollYProgress, [0, 1], [0, 25]);
  const scale = useTransform(scrollYProgress, [0, 0.5, 1], [0.9, 1.05, 0.85]);

  return (
    <div ref={ref} className="relative h-[80vh] flex items-center justify-center perspective-1000">
      <motion.div style={{ scale }} className="flex gap-4">
        <motion.div style={{ x: leftX, rotateY: -rotateY }} className="w-64 h-96 overflow-hidden rounded-xl border border-white/20">
          <img src={imageSrc} alt="" className="w-[512px] h-full object-cover max-w-none" />
        </motion.div>
        <motion.div style={{ x: rightX, rotateY }} className="w-64 h-96 overflow-hidden rounded-xl border border-white/20">
          <img src={imageSrc} alt="" className="w-[512px] h-full object-cover max-w-none -ml-64" />
        </motion.div>
      </motion.div>
    </div>
  );
}
```

### D. X-Ray Lens Hover Mask Reveal
Tracks cursor with a circular lens revealing wireframe or secret underlying layers:
```tsx
import { useState } from "react";

export function XRayLens({ baseContent, hiddenContent }: { baseContent: React.ReactNode, hiddenContent: React.ReactNode }) {
  const [lens, setLens] = useState({ x: 50, y: 50 });

  return (
    <div 
      onMouseMove={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        setLens({ x: ((e.clientX - r.left) / r.width) * 100, y: ((e.clientY - r.top) / r.height) * 100 });
      }}
      className="relative w-full h-[400px] overflow-hidden rounded-2xl cursor-crosshair border border-white/10"
    >
      <div className="absolute inset-0 bg-neutral-950 p-8">{baseContent}</div>
      <div 
        className="absolute inset-0 bg-blue-600 p-8 transition-[clip-path] duration-75"
        style={{ clipPath: `circle(90px at ${lens.x}% ${lens.y}%)` }}
      >
        {hiddenContent}
      </div>
    </div>
  );
}
```

### E. Text Lift on Hover
Letters leap upward with an isometric spring bounce:
```tsx
import { motion } from "framer-motion";

export function TextLift({ word }: { word: string }) {
  return (
    <span className="inline-flex cursor-pointer">
      {word.split("").map((c, i) => (
        <motion.span
          key={i}
          whileHover={{ y: -8, scale: 1.15, rotate: -4 }}
          transition={{ type: "spring", stiffness: 450, damping: 12 }}
          className="inline-block"
        >
          {c === " " ? "\u00A0" : c}
        </motion.span>
      ))}
    </span>
  );
}
```

---

## 3. Porting to Vanilla JS / CSS

If a project does not use React:
- Convert spring transitions to CSS `cubic-bezier(0.175, 0.885, 0.32, 1.275)` or GSAP `Power4.easeOut`.
- Convert `useScroll` to native scroll listener `window.scrollY / innerHeight`.
- Convert `clip-path` to inline styles updated via `requestAnimationFrame`.
