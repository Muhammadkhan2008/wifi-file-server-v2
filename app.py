#!/usr/bin/env python3
"""
WiFi File Server - A lightweight file sharing server accessible from any device on the same network.
Run this on your PC or mobile (via Termux/Pydroid) and access files from any browser.
"""

import os
import sys
import socket
import mimetypes
import urllib.parse
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, abort, jsonify

app = Flask(__name__)

ROOT_DIR = os.path.abspath(os.environ.get("WIFI_FTP_ROOT", os.path.expanduser("~")))
EXCLUDED = {'.DS_Store', 'Thumbs.db', '.git', '__pycache__', '.venv', 'node_modules', '.Trash'}

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_file_info(path):
    stat = path.stat()
    return {
        "name": path.name,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "is_dir": path.is_dir(),
        "extension": path.suffix.lower() if path.is_file() else "",
    }

def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def is_safe_path(base, target):
    base = os.path.realpath(base)
    target = os.path.realpath(target)
    return os.path.commonpath([base, target]) == base

@app.route('/')
@app.route('/<path:subpath>')
def browse(subpath=''):
    current_path = os.path.join(ROOT_DIR, subpath)
    current_path = os.path.abspath(current_path)
    if not is_safe_path(ROOT_DIR, current_path):
        abort(403)
    if not os.path.exists(current_path):
        abort(404)
    if os.path.isfile(current_path):
        return send_file(current_path, as_attachment=False)
    items = []
    try:
        for entry in sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name.lower())):
            if entry.name.startswith('.') or entry.name in EXCLUDED:
                continue
            info = get_file_info(Path(entry.path))
            info["url"] = urllib.parse.quote(os.path.join(subpath, entry.name)) if subpath else urllib.parse.quote(entry.name)
            items.append(info)
    except PermissionError:
        abort(403)
    parts = subpath.strip('/').split('/') if subpath else []
    breadcrumbs = [{"name": "🏠 Home", "url": "/"}]
    accumulated = ""
    for part in parts:
        if part:
            accumulated = os.path.join(accumulated, part) if accumulated else part
            breadcrumbs.append({"name": part, "url": "/" + urllib.parse.quote(accumulated)})
    return render_template('browse.html', items=items, breadcrumbs=breadcrumbs, current_path=subpath, root_name=os.path.basename(ROOT_DIR) or "Root", human_size=human_size)

@app.route('/download/<path:filepath>')
def download_file(filepath):
    full_path = os.path.join(ROOT_DIR, filepath)
    full_path = os.path.abspath(full_path)
    if not is_safe_path(ROOT_DIR, full_path):
        abort(403)
    if not os.path.isfile(full_path):
        abort(404)
    return send_file(full_path, as_attachment=True)

@app.route('/api/info')
def server_info():
    return jsonify({"ip": get_local_ip(), "port": PORT, "root": ROOT_DIR, "url": f"http://{get_local_ip()}:{PORT}"})

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    print("=" * 55)
    print("  📡 WiFi File Server")
    print("=" * 55)
    print(f"  Serving: {ROOT_DIR}")
    print(f"  Local:   http://127.0.0.1:{PORT}")
    print(f"  Network: http://{local_ip}:{PORT}")
    print("=" * 55)
    print("  Open the Network URL on any device on the same WiFi.")
    print("  Press Ctrl+C to stop.")
    print("=" * 55)
    app.run(host='0.0.0.0', port=PORT, debug=False)
