#!/usr/bin/env python3
"""clipshort – auto‑shorten URLs from the clipboard.

Run this script and keep it alive. It polls the system clipboard, detects new URLs,
shortens them using TinyURL's public API, and writes the short link back to the
clipboard.
"""

import re
import sys
import time
import json
import urllib.parse
from hashlib import md5

import requests
import pyperclip

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
POLL_INTERVAL = 0.5  # seconds
URL_REGEX = re.compile(r"https?://[^\s]+", re.IGNORECASE)

# TinyURL public endpoint (no API key required for basic usage)
TINYURL_ENDPOINT = "https://api.tinyurl.com/create"

# Simple in‑memory cache to avoid re‑processing the same URL repeatedly
_processed_cache = set()


def shorten(url: str) -> str:
    """Return a TinyURL shortened version of *url*.
    Uses the public endpoint; if the request fails, returns the original URL.
    """
    try:
        # TinyURL accepts JSON payload: {"url": "..."}
        resp = requests.post(
            TINYURL_ENDPOINT,
            json={"url": url},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        # Response format: {"data": {"tiny_url": "..."}, ...}
        return data.get("data", {}).get("tiny_url", url)
    except Exception as e:
        print(f"[clipshort] warning: could not shorten {url}: {e}", file=sys.stderr)
        return url


def main() -> None:
    print("[clipshort] started – monitoring clipboard for URLs (Ctrl‑C to stop)")
    last_text = ""
    while True:
        try:
            cur_text = pyperclip.paste()
        except Exception:
            cur_text = ""
        if cur_text != last_text:
            # New clipboard content detected
            match = URL_REGEX.search(cur_text)
            if match:
                url = match.group(0)
                # Use a deterministic hash to avoid re‑shortening the same string
                url_hash = md5(url.encode()).hexdigest()
                if url_hash not in _processed_cache:
                    short = shorten(url)
                    if short != url:
                        pyperclip.copy(short)
                        print(f"[clipshort] {url} → {short}")
                    _processed_cache.add(url_hash)
            last_text = cur_text
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[clipshort] stopped.")
        sys.exit(0)
