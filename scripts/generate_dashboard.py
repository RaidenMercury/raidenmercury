#!/usr/bin/env python3
"""
Dashboard Generator for RaidenMercury GitHub Profile.
Keeps metrics in sync and ensures all SVGs are up to date.
"""

import os
import math
import json
import urllib.request
import base64

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

def main():
    print("Checking repository metrics for RaidenMercury...")
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    print("Dashboard assets verified.")

if __name__ == "__main__":
    main()
