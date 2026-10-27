# Master Shaders & Post-Processing Library

Drop-in GLSL shaders for next-generation cinematic 3D web experiences, optimized for Three.js.

---

## 1. Convex CRT Curved Tube Shader

Curves a flat 2D canvas texture into a retro convex CRT tube with scanlines and soft vignetting:

```javascript
import * as THREE from 'three';

export function createCrtTubeMaterial(canvasTexture) {
  return new THREE.ShaderMaterial({
    uniforms: {
      map: { value: canvasTexture },
      power: { value: 1.0 },
      time: { value: 0.0 }
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D map;
      uniform float power, time;
      varying vec2 vUv;

      void main() {
        vec2 c = vUv - 0.5;
        // Convex tube bulge
        vec2 uv = 0.5 + c * (1.0 + 0.09 * dot(c, c) * 4.0) * 0.94;

        if (uv.x < 0.0 || uv.y < 0.0 || uv.x > 1.0 || uv.y > 1.0) {
          gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
          return;
        }

        vec3 col = texture2D(map, uv).rgb;

        // Anti-aliased dynamic scanlines
        float lines = fwidth(uv.y) * 1080.0;
        col *= 1.0 - 0.1 * (0.5 - 0.5 * cos(uv.y * 1080.0 * 3.14159)) * (1.0 - smoothstep(0.5, 1.0, lines));

        // Soft CRT dark corner vignette
        col *= mix(0.55, 1.0, smoothstep(0.75, 0.3, length(c * vec2(1.0, 1.15))));

        gl_FragColor = vec4(col * power, 1.0);
      }
    `,
    toneMapped: false,
    fog: false
  });
}
```

---

## 2. Live WebGL Mesh Gradient Shader

A 5-point orbital mesh gradient with domain warping and noise dithering (rendered at 1/3 resolution to maximize performance):

```glsl
// Fragment Shader
precision mediump float;
varying vec2 uv;
uniform float t, aspect;
uniform vec3 c[5];

vec2 orbit(float i) {
  return vec2(
    0.5 + 0.42 * sin(t * (0.11 + i * 0.023) + i * 1.7),
    0.5 + 0.42 * cos(t * (0.09 + i * 0.019) + i * 2.3)
  );
}

void main() {
  vec2 q = uv;
  // Soft domain warp: colors flow smoothly
  q += 0.06 * vec2(sin(q.y * 5.0 + t * 0.3), cos(q.x * 4.0 - t * 0.25));

  vec3 col = vec3(0.0);
  float w = 0.0;
  for (int i = 0; i < 5; i++) {
    vec2 d = (q - orbit(float(i))) * vec2(aspect, 1.0);
    float k = exp(-dot(d, d) * 3.2);
    col += c[i] * k;
    w += k;
  }
  col /= max(w, 1e-3);

  // Noise dither to eliminate banding
  col += (fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) / 255.0;

  gl_FragColor = vec4(col, 1.0);
}
```

---

## 3. Radial Velocity Zoom Blur Shader

```glsl
uniform sampler2D tex;
uniform float uBlur, uAspect;
varying vec2 vUv;

void main() {
  vec2 d = vUv - 0.5;
  vec4 s;

  if (uBlur < 0.01) {
    s = texture2D(tex, vUv);
  } else {
    float totalWeight = 0.0;
    s = vec4(0.0);
    for (int i = 0; i < 10; i++) {
      float k = float(i) / 9.0;
      float w = 1.0 - k * 0.6;
      s += texture2D(tex, 0.5 + d * (1.0 - uBlur * k * 0.07)) * w;
      totalWeight += w;
    }
    s /= totalWeight;
  }

  // Vignette: stronger when in flight
  float r = length(d * vec2(uAspect, 1.0));
  s.rgb *= mix(1.0, smoothstep(1.2, 0.5, r), 0.25 + uBlur * 0.45);

  gl_FragColor = s;
}
```
