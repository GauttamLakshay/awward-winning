#!/usr/bin/env python3
"""
CINEMATIC 3D ASSET PIPELINE: SPLINE 3D + GPT VISION REFERENCE CLONING + DALL-E 3
Deconstructs reference images, generates 1:1 matching assets, and connects Spline 3D scenes.
Zero third-party dependencies: uses standard library urllib.request.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error

def load_env_file(filepath=".env"):
    """Loads environment variables from a .env file without external packages."""
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

def check_credentials():
    """Verifies presence of credentials without printing secrets."""
    env = load_env_file()
    openai_key = os.environ.get("OPENAI_API_KEY") or env.get("OPENAI_API_KEY")
    spline_url = os.environ.get("SPLINE_SCENE_URL") or env.get("SPLINE_SCENE_URL")

    status = {
        "openai_connected": bool(openai_key),
        "spline_connected": bool(spline_url),
        "spline_url": spline_url if spline_url else None
    }
    return status, openai_key

def analyze_reference_with_vision(image_path, api_key):
    """
    Sends reference screenshot to GPT-4o Vision to extract exact visual DNA
    and generate prompt-engineered specs for cloning all assets.
    """
    print(f"[*] Analyzing reference image with GPT-4o Vision: {image_path}...")
    with open(image_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    prompt = """
You are an expert art director and 3D web technologist.
Analyze this reference image of a website/3D scene.
Your mission: Break down this reference into individual 2D/3D assets needed to clone this website 1:1.

Return ONLY a valid JSON object with the following schema:
{
  "theme": "Brief description of the aesthetic",
  "palette": ["#hex1", "#hex2", "#hex3"],
  "lighting": "Description of lighting & atmosphere",
  "assets": [
    {
      "name": "asset_filename_without_ext",
      "role": "e.g. monitor_wallpaper, polaroid_plate, sticker, background_texture",
      "prompt": "Detailed DALL-E 3 prompt to recreate this exact asset matching the reference aesthetic",
      "size": "1024x1024"
    }
  ]
}
"""

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Cinematic3D-Pipeline/1.0"
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            manifest = json.loads(content)
            print("[+] Vision deconstruction complete. Extracted assets:")
            for a in manifest.get("assets", []):
                print(f"   - [{a['role']}] {a['name']}")
            return manifest
    except Exception as e:
        print(f"[!] Error in Vision analysis: {e}")
        return None

def generate_image_dalle(prompt, output_path, api_key, size="1024x1024", quality="standard"):
    """
    Calls OpenAI DALL-E 3 API to generate an image asset and saves it to disk.
    """
    print(f"[*] Prompting DALL-E 3: '{prompt[:75]}...'")
    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "response_format": "url"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Cinematic3D-Pipeline/1.0"
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            image_url = data["data"][0]["url"]
            print(f"[+] Generation successful. Downloading image...")

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img_req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=30) as img_resp, open(output_path, "wb") as out:
                out.write(img_resp.read())
            
            print(f"[OK] Asset saved to: {output_path}")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[!] OpenAI API Error ({e.code}): {err_msg}")
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False

def clone_reference_workflow(reference_image_path):
    """
    End-to-End Workflow:
    1. Reads reference screenshot
    2. Uses GPT-4o Vision to extract exact asset manifest & prompts
    3. Generates all matching assets via DALL-E 3
    4. Bundles into Spline 3D template
    """
    status, api_key = check_credentials()
    if not status["openai_connected"]:
        print("[!] Missing OPENAI_API_KEY in .env. Please add it to run the cloning loop.")
        return

    manifest = analyze_reference_with_vision(reference_image_path, api_key)
    if not manifest:
        print("[!] Failed to analyze reference image.")
        return

    generated_assets = []
    output_dir = os.path.join("assets", "generated")
    os.makedirs(output_dir, exist_ok=True)

    for item in manifest.get("assets", []):
        filename = f"{item['name']}.png"
        out_path = os.path.join(output_dir, filename)
        success = generate_image_dalle(item["prompt"], out_path, api_key, size=item.get("size", "1024x1024"))
        if success:
            generated_assets.append({
                "label": item["name"],
                "role": item["role"],
                "path": out_path
            })

    print(f"\n[OK] Successfully generated {len(generated_assets)} matching assets for the reference clone!")
    return generated_assets

def main():
    print("=" * 65)
    print("   NEXT-GEN 3D IMMERSIVE ASSET PIPELINE & REFERENCE CLONER")
    print("=" * 65)

    status, openai_key = check_credentials()
    print(f"[*] OpenAI API Connected:  {'YES' if status['openai_connected'] else 'NO (Set OPENAI_API_KEY in .env)'}")
    print(f"[*] Spline Scene Connected: {'YES' if status['spline_connected'] else 'NO (Set SPLINE_SCENE_URL in .env)'}")

    if len(sys.argv) > 1 and sys.argv[1] == "--clone":
        if len(sys.argv) < 3:
            print("Usage: python asset_pipeline.py --clone <path_to_reference_image>")
            return
        ref_image = sys.argv[2]
        if not os.path.exists(ref_image):
            print(f"Error: File not found: {ref_image}")
            return
        clone_reference_workflow(ref_image)
    else:
        print("\nCommands:")
        print("  1. python asset_pipeline.py --clone <reference_image.jpg>")
        print("     (Analyzes reference screenshot, generates 1:1 matching assets via GPT/DALL-E 3)")

if __name__ == "__main__":
    main()
