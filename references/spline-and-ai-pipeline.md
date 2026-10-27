# Spline 3D & AI Asset Generation Pipeline

This reference defines the automated pipeline for connecting Spline 3D scenes with ChatGPT / DALL-E 3 image asset generation.

---

## 1. Connection Protocol

The AI agent verifies the presence of credentials and Spline scene URLs:
- **`OPENAI_API_KEY`**: For autonomous DALL-E 3 image asset generation.
- **`SPLINE_SCENE_URL`**: The exported `.splinecode` URL from Spline (e.g. `https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode`).

If missing, the agent guides the user:
```bash
# In .env file:
OPENAI_API_KEY=your_key_here
SPLINE_SCENE_URL=https://prod.spline.design/your_scene_id/scene.splinecode
```

---

## 2. The 3-Step Asset Discovery Interview

The AI agent conducts an efficient 3-step asset interview with the user:
1. **Scene Concept & Aesthetic**: What is the theme? (e.g. Cyberpunk workstation, luxury watch podium, retro 90s bedroom, spaceship cockpit).
2. **2D Texture & Decal Requirements**: What should appear on screens, posters, stickers, or polaroids?
   - *Example*: "Retro Windows 95 wallpaper with floating neon icons" or "Grainy 35mm polaroid film photo of city skyline".
3. **Spline 3D Scene Choice**:
   - Option A: User provides their custom Spline export URL.
   - Option B: Agent suggests high-quality community Spline scenes (interactive desk, 3D room, keyboard, floating sphere).

---

## 3. Autonomous Image Asset Generation (DALL-E 3)

The agent calls OpenAI's image generation endpoint to create high-resolution textures, wallpapers, and stickers directly into `./assets/generated/`:

```python
import urllib.request
import json

def generate_asset(prompt, filename, api_key):
    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": "dall-e-3",
        "prompt": f"{prompt}, high resolution, ultra-clean web asset, crisp edges",
        "n": 1,
        "size": "1024x1024"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        img_url = data["data"][0]["url"]
        # Download and save
        with urllib.request.urlopen(img_url) as r, open(filename, "wb") as f:
            f.write(r.read())
```

---

## 4. Embedding Spline 3D with Scroll Camera Synchronization

```html
<!-- Spline Web Component -->
<script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.72/build/spline-viewer.js"></script>

<div class="spline-scene-wrap">
  <spline-viewer url="https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode"></spline-viewer>
</div>

<script>
  // Camera & Scroll Interactivity
  const viewer = document.querySelector('spline-viewer');
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = Math.min(Math.max(scrollY / maxScroll, 0), 1);

    // Manipulate Spline canvas or emit events
    if (viewer && viewer.shadowRoot) {
      const canvas = viewer.shadowRoot.querySelector('canvas');
      if (canvas) {
        canvas.style.transform = `scale(${1 + progress * 0.08})`;
      }
    }
  });
</script>
```
