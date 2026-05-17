# clipshort

**clipshort** is a minimal Python script that runs in the background, detects URLs copied to the clipboard, shortens them with the public TinyURL service, and puts the shortened URL back onto the clipboard.

## Features
- Zero‑config, just run the script.
- Works on Windows, macOS, and Linux.
- Uses only the standard library plus `requests` and `pyperclip` (both pure‑Python).

## Installation
```bash
pip install requests pyperclip
```

## Usage
```bash
python clipshort.py &   # Unix‑like (run in background)
clipshort.exe          # Windows (double‑click or from cmd)
```
Copy any URL to the clipboard and watch it turn into a TinyURL instantly.

## How it works
1. Poll the clipboard every 0.5 s.
2. If the content matches a URL pattern and hasn't been processed before, send a GET request to `https://api.tinyurl.com/create` (via TinyURL’s public endpoint).
3. Replace the clipboard with the shortened link.

## License
MIT – see the LICENSE file in the repository.
