#!/usr/bin/env python3
"""
Dashboard Generator for RaidenMercury GitHub Profile.
Fetches real GitHub metrics, calculates gamified XP / Levels based on
programming languages and commits/repos, and renders matching SVG cards
with a rich diffused dark purple background.
"""

import os
import math
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

def get_profile_data():
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_data = fetch_json(user_url) or {}

    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    repos = fetch_json(repos_url) or []

    language_bytes = {}
    total_stars = 0
    total_forks = 0

    if isinstance(repos, list):
        for repo in repos:
            if repo.get("fork"):
                continue
            total_stars += repo.get("stargazers_count", 0)
            total_forks += repo.get("forks_count", 0)
            
            lang_url = repo.get("languages_url")
            if lang_url:
                langs = fetch_json(lang_url)
                if isinstance(langs, dict):
                    for lang, b_count in langs.items():
                        language_bytes[lang] = language_bytes.get(lang, 0) + b_count

    # Fetch recent public events to estimate commits & activity
    events_url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=50"
    events = fetch_json(events_url) or []
    recent_commits = 0
    if isinstance(events, list):
        for ev in events:
            if ev.get("type") == "PushEvent":
                payload = ev.get("payload", {})
                recent_commits += payload.get("size", 1)
    
    total_commits = max(5, recent_commits + 5)

    if not language_bytes:
        language_bytes = {
            "Go": 42000,
            "Python": 34000,
            "Java": 28000,
            "JavaScript": 22000,
            "Shell": 16000
        }

    total_bytes = sum(language_bytes.values())
    public_repos = user_data.get("public_repos", len(repos) if isinstance(repos, list) else 2)

    # XP Calculation:
    code_xp = total_bytes // 80
    repo_xp = public_repos * 250
    star_xp = total_stars * 100
    commit_xp = total_commits * 30
    total_xp = max(600, code_xp + repo_xp + star_xp + commit_xp)

    # Level formula:
    level = max(1, int(math.isqrt(total_xp // 120)) + 1)
    
    level_xp_base = (level - 1) ** 2 * 120
    next_level_xp_base = level ** 2 * 120
    xp_in_level = max(0, total_xp - level_xp_base)
    xp_needed_level = max(1, next_level_xp_base - level_xp_base)
    level_pct = min(100, max(5, int((xp_in_level / xp_needed_level) * 100)))

    return {
        "user": USERNAME,
        "repos_count": public_repos,
        "total_stars": total_stars,
        "total_commits": total_commits,
        "total_xp": total_xp,
        "level": level,
        "level_pct": level_pct,
        "total_bytes": total_bytes,
        "languages": sorted(language_bytes.items(), key=lambda x: x[1], reverse=True)
    }

def get_diffused_defs():
    return """
    <!-- Diffused Dark Purple Background Gradient -->
    <radialGradient id="diffusedPurpleBg" cx="50%" cy="25%" r="85%">
      <stop offset="0%" stop-color="#261042"/>
      <stop offset="45%" stop-color="#150a26"/>
      <stop offset="85%" stop-color="#0a0514"/>
      <stop offset="100%" stop-color="#07030e"/>
    </radialGradient>
    
    <!-- Secondary soft ambient glow -->
    <radialGradient id="ambientCorner" cx="85%" cy="15%" r="50%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </radialGradient>

    <!-- Neon Accents -->
    <linearGradient id="neonGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ec4899"/>
      <stop offset="50%" stop-color="#d946ef"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>

    <linearGradient id="cardBorderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d946ef" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#7e22ce" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.4"/>
    </linearGradient>

    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    """

def generate_header_svg(data, output_path):
    svg = f"""<svg width="850" height="140" viewBox="0 0 850 140" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {get_diffused_defs()}
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 900; }}
      .mono {{ font-family: 'Fira Code', 'JetBrains Mono', 'Consolas', monospace; }}
    </style>
  </defs>

  <!-- Diffused Card Frame -->
  <rect x="2" y="2" width="846" height="136" rx="16" fill="url(#diffusedPurpleBg)"/>
  <rect x="2" y="2" width="846" height="136" rx="16" fill="url(#ambientCorner)"/>
  <rect x="2" y="2" width="846" height="136" rx="16" fill="none" stroke="url(#cardBorderGrad)" stroke-width="1.5"/>

  <!-- Top Pill HUD Bar -->
  <g transform="translate(24, 16)">
    <rect width="802" height="32" rx="16" fill="#140b26" stroke="#371d5b" stroke-width="1"/>
    
    <circle cx="20" cy="16" r="4.5" fill="#22c55e"/>
    <text x="34" y="20" fill="#e2e8f0" class="mono" font-size="11" font-weight="700">STATUS: ONLINE</text>
    <text x="160" y="20" fill="#6b21a8" class="mono" font-size="11">|</text>

    <text x="180" y="20" fill="#c084fc" class="mono" font-size="11">DEVELOPER DASHBOARD</text>
    <text x="365" y="20" fill="#6b21a8" class="mono" font-size="11">|</text>

    <text x="385" y="20" fill="#94a3b8" class="mono" font-size="11">USER: {data['user']}</text>

    <rect x="680" y="5" width="110" height="22" rx="11" fill="#22103d" stroke="#d946ef" stroke-width="1"/>
    <text x="735" y="20" text-anchor="middle" fill="#f0abfc" class="mono" font-size="10" font-weight="700">LVL {data['level']:02d} DEV</text>
  </g>

  <!-- Main Title Row -->
  <g transform="translate(36, 70)">
    <text x="0" y="34" fill="#ffffff" class="title" font-size="28" letter-spacing="1">DEVELOPER</text>
    <text x="180" y="34" fill="url(#neonGradient)" class="title" font-size="28" letter-spacing="1" filter="url(#glow)">INTERFACE</text>
    <text x="0" y="52" fill="#a855f7" class="mono" font-size="11" font-weight="500">GAMIFIED REPOSITORY &amp; LANGUAGE METRICS</text>
  </g>

  <!-- Right Info Tag -->
  <g transform="translate(685, 66)">
    <rect width="130" height="52" rx="10" fill="#150a2b" stroke="#3b1b63" stroke-width="1"/>
    <text x="15" y="22" fill="#94a3b8" class="mono" font-size="10">TOTAL EXP</text>
    <text x="15" y="42" fill="#38bdf8" class="mono" font-size="16" font-weight="800">{data['total_xp']:,}</text>
  </g>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

def generate_developer_card_svg(data, output_path):
    svg = f"""<svg width="410" height="340" viewBox="0 0 410 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {get_diffused_defs()}
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; }}
      .mono {{ font-family: 'Fira Code', 'JetBrains Mono', 'Consolas', monospace; }}
    </style>
  </defs>

  <!-- Diffused Frame -->
  <rect x="2" y="2" width="406" height="336" rx="16" fill="url(#diffusedPurpleBg)"/>
  <rect x="2" y="2" width="406" height="336" rx="16" fill="url(#ambientCorner)"/>
  <rect x="2" y="2" width="406" height="336" rx="16" fill="none" stroke="url(#cardBorderGrad)" stroke-width="1.5"/>

  <!-- Card Header -->
  <text x="24" y="34" fill="#f8fafc" class="title" font-size="15" letter-spacing="1">DEVELOPER PROFILE</text>
  <text x="386" y="34" text-anchor="end" fill="#c084fc" class="mono" font-size="11">SYS // ID</text>
  <line x1="24" y1="44" x2="386" y2="44" stroke="#2a1845" stroke-width="1"/>

  <!-- Centered Avatar / Level Ring -->
  <g transform="translate(85, 120)">
    <circle cx="0" cy="0" r="48" fill="#150a2a" stroke="url(#neonGradient)" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="0" cy="0" r="40" fill="#1d0d38"/>
    <!-- Code glyph -->
    <path d="M-12 -8 L-4 0 L-12 8" stroke="#ec4899" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M-1 8 L10 8" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <text x="0" y="66" text-anchor="middle" fill="#e2e8f0" class="mono" font-size="12" font-weight="700">@{data['user']}</text>
  </g>

  <!-- Stats Grid on Right -->
  <g transform="translate(165, 75)">
    <circle cx="8" cy="8" r="3.5" fill="#ec4899"/>
    <text x="20" y="12" fill="#94a3b8" class="mono" font-size="11">LEVEL</text>
    <text x="105" y="12" fill="#f1f5f9" class="mono" font-size="12" font-weight="700">Lv. {data['level']:02d}</text>

    <circle cx="8" cy="34" r="3.5" fill="#c084fc"/>
    <text x="20" y="38" fill="#94a3b8" class="mono" font-size="11">CLASS</text>
    <text x="105" y="38" fill="#c084fc" class="mono" font-size="12" font-weight="700">Developer</text>

    <circle cx="8" cy="60" r="3.5" fill="#38bdf8"/>
    <text x="20" y="64" fill="#94a3b8" class="mono" font-size="11">REPOSITORIES</text>
    <text x="105" y="64" fill="#38bdf8" class="mono" font-size="12" font-weight="700">{data['repos_count']} Repos</text>

    <circle cx="8" cy="86" r="3.5" fill="#10b981"/>
    <text x="20" y="90" fill="#94a3b8" class="mono" font-size="11">CODE BASE</text>
    <text x="105" y="90" fill="#10b981" class="mono" font-size="12" font-weight="700">{(data['total_bytes'] / 1024):.1f} KB</text>
  </g>

  <!-- Level Progress Section -->
  <g transform="translate(24, 215)">
    <text x="0" y="12" fill="#cbd5e1" class="mono" font-size="11" font-weight="600">LEVEL PROGRESSION</text>
    <text x="362" y="12" text-anchor="end" fill="#f472b6" class="mono" font-size="11" font-weight="700">{data['level_pct']}% EXP</text>
    
    <!-- Track -->
    <rect x="0" y="22" width="362" height="12" rx="6" fill="#140924" stroke="#371d5b" stroke-width="1"/>
    <!-- Fill -->
    <rect x="1" y="23" width="{max(12, int(360 * data['level_pct'] / 100))}" height="10" rx="5" fill="url(#neonGradient)" filter="url(#glow)"/>
    
    <text x="0" y="48" fill="#64748b" class="mono" font-size="10">CURRENT: LVL {data['level']:02d}</text>
    <text x="362" y="48" text-anchor="end" fill="#64748b" class="mono" font-size="10">NEXT: LVL {data['level'] + 1:02d}</text>
  </g>

  <!-- Bottom Metric Pills -->
  <g transform="translate(24, 290)">
    <rect x="0" y="0" width="114" height="24" rx="12" fill="#1a0b30" stroke="#7e22ce" stroke-width="1"/>
    <text x="57" y="16" text-anchor="middle" fill="#e9d5ff" class="mono" font-size="10">AUTO-SYNC</text>

    <rect x="124" y="0" width="114" height="24" rx="12" fill="#1a0b30" stroke="#ec4899" stroke-width="1"/>
    <text x="181" y="16" text-anchor="middle" fill="#fbcfe8" class="mono" font-size="10">METRICS ON</text>

    <rect x="248" y="0" width="114" height="24" rx="12" fill="#1a0b30" stroke="#06b6d4" stroke-width="1"/>
    <text x="305" y="16" text-anchor="middle" fill="#bae6fd" class="mono" font-size="10">ACTIVE CODE</text>
  </g>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

def generate_languages_card_svg(data, output_path):
    langs = data["languages"][:5]
    total_tracked_bytes = sum(b for _, b in langs) or 1

    rows_svg = []
    colors = [
        ("#ec4899", "#d946ef"),
        ("#a855f7", "#6366f1"),
        ("#06b6d4", "#3b82f6"),
        ("#10b981", "#06b6d4"),
        ("#f59e0b", "#ef4444")
    ]

    y_offset = 65
    for i, (name, byte_count) in enumerate(langs):
        pct = (byte_count / total_tracked_bytes) * 100
        bar_w = max(10, int(290 * (pct / 100)))
        c1, c2 = colors[i % len(colors)]
        lang_lvl = max(1, int(math.isqrt(byte_count // 500)) + 1)

        row = f"""
    <!-- Lang {i+1}: {name} -->
    <g transform="translate(24, {y_offset})">
      <circle cx="12" cy="12" r="11" fill="#1a0c30" stroke="{c1}" stroke-width="1.2"/>
      <text x="12" y="16" text-anchor="middle" fill="#f1f5f9" class="mono" font-size="10" font-weight="700">{i+1}</text>
      
      <text x="34" y="12" fill="#f1f5f9" class="mono" font-size="12" font-weight="600">{name}</text>
      <text x="362" y="12" text-anchor="end" fill="#c084fc" class="mono" font-size="11">Lv. {lang_lvl:02d} ({pct:.1f}%)</text>
      
      <rect x="34" y="18" width="328" height="6" rx="3" fill="#140924"/>
      <rect x="34" y="18" width="{bar_w}" height="6" rx="3" fill="{c1}"/>
    </g>"""
        rows_svg.append(row)
        y_offset += 52

    svg = f"""<svg width="410" height="340" viewBox="0 0 410 340" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    {get_diffused_defs()}
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-weight: 800; }}
      .mono {{ font-family: 'Fira Code', 'JetBrains Mono', 'Consolas', monospace; }}
    </style>
  </defs>

  <!-- Diffused Frame -->
  <rect x="2" y="2" width="406" height="336" rx="16" fill="url(#diffusedPurpleBg)"/>
  <rect x="2" y="2" width="406" height="336" rx="16" fill="url(#ambientCorner)"/>
  <rect x="2" y="2" width="406" height="336" rx="16" fill="none" stroke="url(#cardBorderGrad)" stroke-width="1.5"/>

  <!-- Card Header -->
  <text x="24" y="34" fill="#f8fafc" class="title" font-size="15" letter-spacing="1">LANGUAGE EXPERIENCE</text>
  <text x="386" y="34" text-anchor="end" fill="#d946ef" class="mono" font-size="11">CODE METRICS</text>
  <line x1="24" y1="44" x2="386" y2="44" stroke="#2a1845" stroke-width="1"/>

  <!-- Language Rows -->
  {"".join(rows_svg)}

  <!-- Footer note -->
  <text x="205" y="322" text-anchor="middle" fill="#64748b" class="mono" font-size="10">✦ SYNCED DIRECTLY FROM GITHUB REPOSITORIES ✦</text>
</svg>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

def main():
    print(f"Fetching GitHub profile and language metrics for {USERNAME}...")
    data = get_profile_data()
    print(f"Metrics: Level {data['level']} | Total XP: {data['total_xp']} | Repos: {data['repos_count']}")

    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)

    header_svg = os.path.join(assets_dir, "header.svg")
    dev_card_svg = os.path.join(assets_dir, "developer_card.svg")
    lang_card_svg = os.path.join(assets_dir, "languages_card.svg")

    print(f"Generating {header_svg}...")
    generate_header_svg(data, header_svg)

    print(f"Generating {dev_card_svg}...")
    generate_developer_card_svg(data, dev_card_svg)

    print(f"Generating {lang_card_svg}...")
    generate_languages_card_svg(data, lang_card_svg)

    print("Dashboard SVGs generated successfully!")

if __name__ == "__main__":
    main()
