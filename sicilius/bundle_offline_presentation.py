#!/usr/bin/env python3
import os
import re
import base64
from pathlib import Path

def get_base64_image(image_path):
    if not image_path.exists():
        print(f"⚠️ Warning: Image not found at {image_path}")
        return ""
    with open(image_path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode("utf-8")
        if image_path.suffix.lower() == ".svg":
            return f"data:image/svg+xml;base64,{b64_str}"
        return f"data:image/png;base64,{b64_str}"

def bundle_standalone_html():
    print("🚀 Bundling 100% Self-Contained Offline HTML5 Presentation (Inlining Logo, CSS, JS & Base64 Images)...")

    project_root = Path(__file__).parent.parent
    pres_dir = project_root / "sicilius" / "frontend" / "public" / "presentation"
    output_dir = project_root / "sicilius" / "docs"
    
    assets_web = project_root / "sicilius" / "frontend" / "public" / "assets" / "web"
    assets_mobile = project_root / "sicilius" / "frontend" / "public" / "assets" / "mobile"
    logo_path = project_root / "sicilius" / "frontend" / "public" / "sicilius-logo.svg"

    html_path = pres_dir / "index.html"
    css_path = pres_dir / "style.css"
    js_path = pres_dir / "app.js"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # 1. Inline CSS into <style> tag
    html_content = html_content.replace(
        '<link rel="stylesheet" href="style.css" />',
        f'<style>\n{css_content}\n</style>'
    )

    # 2. Inline JS into <script> tag
    html_content = html_content.replace(
        '<script src="app.js"></script>',
        f'<script>\n{js_content}\n</script>'
    )

    # 3. Base64 Encode All Images (Including SVG Logo)
    img_map = {
        "../sicilius-logo.svg": logo_path,
        "../assets/web/web_search_dashboard.png": assets_web / "web_search_dashboard.png",
        "../assets/web/web_nexus_graph.png": assets_web / "web_nexus_graph.png",
        "../assets/mobile/mobile_gamification.png": assets_mobile / "mobile_gamification.png",
        "../assets/mobile/mobile_map_osm.png": assets_mobile / "mobile_map_osm.png",
    }

    for rel_path, abs_path in img_map.items():
        b64_uri = get_base64_image(abs_path)
        if b64_uri:
            html_content = html_content.replace(rel_path, b64_uri)
            print(f"  ✅ Embedded image {abs_path.name} as Base64 URI")

    # 4. Remove Download Buttons in Offline Version (Only Keep Controls & CTA)
    # Remove HTML blocks matching download <a> tags
    html_content = re.sub(
        r'<!-- 🌐 Direct Birebir Offline HTML5 Download.*?</a>\s*',
        '',
        html_content,
        flags=re.DOTALL
    )
    html_content = re.sub(
        r'<!-- 📊 Direct PowerPoint \(PPTX\) Download Button.*?</a>\s*',
        '',
        html_content,
        flags=re.DOTALL
    )
    html_content = re.sub(
        r'<!-- 📄 Direct PDF Download Button.*?</a>\s*',
        '',
        html_content,
        flags=re.DOTALL
    )

    # 5. Save to docs and public presentation directory
    offline_doc_path = output_dir / "Sicilius_Sunum_Offline.html"
    offline_public_path = pres_dir / "Sicilius_Sunum_Offline.html"

    with open(offline_doc_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(offline_public_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"🎉 100% Self-Contained Offline HTML5 Presentation bundled successfully (Download buttons removed from header)!")
    print(f"   📁 Doc Path: {offline_doc_path} ({offline_doc_path.stat().st_size // 1024} KB)")
    print(f"   📁 Public Path: {offline_public_path} ({offline_public_path.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    bundle_standalone_html()
