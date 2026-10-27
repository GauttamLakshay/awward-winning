# Reference Image Deconstruction & Iterative Cloning Loop

This protocol teaches AI agents how to accept any reference image/screenshot of a website or 3D scene, reverse-engineer every visual asset, and iteratively generate matching assets via GPT/DALL-E 3 until the generated assets achieve 1:1 aesthetic fidelity.

---

## 1. The 5-Stage Cloning Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE ITERATIVE VISUAL CLONING LOOP                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. MULTIMODAL DECONSTRUCTION (Vision Analysis)                              │
│    • Extract color palette (Primary, Secondary, Ambient light color)        │
│    • Detect lighting model (Key light direction, soft vs harsh shadows)     │
│    • Catalog individual sub-assets (Wallpapers, Stickers, Polaroids, UI)    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. ASSET SEGMENTATION MANIFEST                                              │
│    Break reference down into isolated generative tasks:                     │
│    • Asset A: Screen texture / OS wallpaper                                 │
│    • Asset B: Foreground sticker badges / retro logos                       │
│    • Asset C: Photographic plate / polaroid frame                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. PROMPT COMPILATION & GENERATION (DALL-E 3)                               │
│    Formulate hyper-specific prompts with style anchors, lighting, and       │
│    compositional framing.                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. VISION CRITIC EVALUATION (The Comparison Step)                           │
│    Compare generated asset against the reference crop:                      │
│    • Color tone drift (Too warm / too cold?)                                │
│    • Texture fidelity (Needs more grain, halftones, or glossy reflection?)   │
│    • Geometric alignment (Angle and aspect ratio)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. CORRECTIVE RE-PROMPTING LOOP                                             │
│    If fidelity < 95%, apply corrective delta prompts and regenerate until   │
│    the asset matches the reference perfectly.                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Vision Deconstruction Prompt Template

When the user supplies a reference image, pass this prompt to GPT-4o Vision:

```markdown
Analyze this reference image for a 3D website asset cloning workflow.
Break it down into an actionable Asset Manifest:

1. Color DNA: Extract dominant background, accent, and ambient light hex codes.
2. Lighting & Atmosphere: Key light direction, shadow softness, volumetric haze, or film grain.
3. Asset Inventory: List all distinct 2D and 3D visual assets visible:
   - For each asset: name, intended role (e.g. screen wallpaper, polaroid photo, sticker), 
     exact visual description, and aspect ratio.
4. DALL-E 3 Generation Prompts: Write a production-grade prompt for each asset that precisely 
   replicates the style, materials, and mood of the reference without watermarks or artifacts.
```

---

## 3. The Iterative Refinement & Critic Formula

If the first generated image does not match the reference image closely enough:

### A. Delta Analysis:
Identify the exact divergence vector:
- **Tone Drift**: `generated.temp` is too warm $\rightarrow$ Add: `"cool blue tungsten color grade, muted earth tones, desaturated highlights"`.
- **Style Drift**: Looks too CGI/plastic $\rightarrow$ Add: `"authentic 1990s 35mm film photography, natural grain, subtle lens vignette, optical realism"`.
- **Complexity Drift**: Too cluttered $\rightarrow$ Add: `"minimalist graphic design, clean isolated subject on solid background, zero text clutter"`.

### B. Corrective Prompt Recipe:
```python
def build_refinement_prompt(original_prompt, critic_feedback):
    return (
        f"{original_prompt}. "
        f"CRITICAL REFINEMENT: Fix previous divergence. {critic_feedback}. "
        f"Match the exact lighting, texture, and aesthetic of the reference image."
    )
```

---

## 4. Code Implementation (Automated Deconstruction & Generation)

```python
import urllib.request
import json
import base64

def analyze_reference_image(image_path, api_key):
    """Uses GPT-4o Vision to extract the asset manifest from a reference image."""
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Deconstruct this website/3D reference image. Output a JSON list of assets needed (name, role, prompt, size) to recreate it 1:1."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }
    
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return json.loads(res["choices"][0]["message"]["content"])
```
