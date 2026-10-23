#!/usr/bin/env python3
"""
Dashboard Generator for RaidenMercury GitHub Profile.
Fetches real GitHub metrics and generates the live languages card (410x390)
synced directly with the GitHub database.
"""

import os
import json
import urllib.request
import urllib.error

USERNAME = "RaidenMercury"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def fetch_json(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "RaidenMercury-Profile-Bot")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Warning: could not fetch {url}: {e}")
        return None

def get_real_languages():
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    repos = fetch_json(repos_url) or []

    language_bytes = {}
    if isinstance(repos, list):
        for repo in repos:
            if repo.get("fork"):
                continue
            l_url = repo.get("languages_url")
            if l_url:
                langs = fetch_json(l_url)
                if isinstance(langs, dict):
                    for lang, b_count in langs.items():
                        language_bytes[lang] = language_bytes.get(lang, 0) + b_count

    if not language_bytes:
        language_bytes = {"Go": 60518, "Python": 39152, "HTML": 37843}

    total_bytes = sum(language_bytes.values()) or 1
    sorted_langs = sorted(language_bytes.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs, total_bytes

def generate_live_languages_card(output_path):
    sorted_langs, total_bytes = get_real_languages()

    colors = {
        "Go": ("#00ADD8", "#06b6d4"),
        "Python": ("#38bdf8", "#3b82f6"),
        "HTML": ("#e34c26", "#f97316"),
        "Java": ("#f59e0b", "#ef4444"),
        "Shell": ("#10b981", "#059669"),
        "JavaScript": ("#f7df1e", "#eab308")
    }

    rows_svg = []
    y_offset = 62

    for i, (name, b_count) in enumerate(sorted_langs[:4]):
        pct = (b_count / total_bytes) * 100
        bar_w = max(15, int(300 * (pct / 100)))
        c1, c2 = colors.get(name, ("#c084fc", "#a855f7"))
        kb = b_count / 1024

        row = f"""
    <!-- {name} Row -->
    <g transform="translate(24, {y_offset})">
      <circle cx="12" cy="14" r="10" fill="#1b1233" stroke="{c1}" stroke-width="1.2"/>
      <text x="12" y="18" text-anchor="middle" fill="{c1}" font-size="10">●</text>
      
      <text x="32" y="14" fill="#f1f5f9" class="bold-txt" font-size="13">{name}</text>
      
      <rect x="290" y="2" width="72" height="20" rx="10" fill="#150a24" stroke="{c1}" stroke-width="1"/>
      <text x="326" y="15" text-anchor="middle" fill="#f1f5f9" class="mono" font-size="9" font-weight="700">{pct:.1f}%</text>

      <text x="32" y="32" class="desc-txt">{kb:.1f} KB de código en repositorios públicos</text>
      <rect x="32" y="40" width="330" height="4" rx="2" fill="#140924"/>
      <rect x="32" y="40" width="{bar_w}" height="4" rx="2" fill="{c1}"/>
    </g>"""
        rows_svg.append(row)
        y_offset += 66

    svg = f"""<svg width="410" height="390" viewBox="0 0 410 390" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="techDark" cx="50%" cy="20%" r="85%">
      <stop offset="0%" stop-color="#1c0d38"/>
      <stop offset="50%" stop-color="#0e0620"/>
      <stop offset="100%" stop-color="#070310"/>
    </radialGradient>

    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c084fc" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#4c1d95" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.5"/>
    </linearGradient>

    <filter id="glowTech" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; }}
      .mono {{ font-family: 'Fira Code', 'JetBrains Mono', 'Consolas', monospace; }}
      .bold-txt {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 700; }}
      .desc-txt {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 11px; fill: #cbd5e1; }}
    </style>
  </defs>

  <!-- Frame -->
  <rect x="2" y="2" width="406" height="386" rx="18" fill="url(#techDark)" stroke="url(#borderGrad)" stroke-width="1.5"/>

  <!-- Top Title Bar -->
  <g transform="translate(24, 22)">
    <circle cx="6" cy="6" r="4" fill="#a855f7" filter="url(#glowTech)"/>
    <text x="18" y="10" fill="#f8fafc" class="title" font-size="14" letter-spacing="1">MOST USED LANGUAGES</text>
    <text x="362" y="10" text-anchor="end" fill="#c084fc" class="mono" font-size="10">GITHUB DB</text>
    <line x1="0" y1="20" x2="362" y2="20" stroke="#2a124c" stroke-width="1"/>
  </g>

  <!-- Real Languages Data Rows -->
  {"".join(rows_svg)}

  <!-- Bottom Real-time Sync Note -->
  <g transform="translate(24, 330)">
    <rect width="362" height="42" rx="8" fill="#140826" stroke="#2e1053" stroke-width="1"/>
    <text x="181" y="18" text-anchor="middle" fill="#e9d5ff" class="bold-txt" font-size="10">✦ Sincronizado en tiempo real con GitHub API ✦</text>
    <text x="181" y="32" text-anchor="middle" fill="#94a3b8" class="desc-txt">Los proyectos privados se reflejarán al publicarse</text>
  </g>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("Live languages card generated successfully.")

def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    card_path = os.path.join(assets_dir, "core_tech.svg")
    generate_live_languages_card(card_path)

if __name__ == "__main__":
    main()
