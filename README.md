# 📡 WiFi File Server

A lightweight, cross-platform file server that lets you browse and download files from any device on the same WiFi network — just open a link in your browser.

## ✨ Features

- **Zero config** — run one command, get a URL
- **Works everywhere** — PC (Windows/Mac/Linux) and mobile (Termux/Pydroid)
- **Beautiful web UI** — browse files with icons, previews, and one-tap downloads
- **Dark mode** — auto-detects your system theme
- **Mobile friendly** — responsive design works great on phones
- **Secure** — only accessible on your local network, no internet exposure

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python app.py

# 3. Open the Network URL shown in the terminal on any device
```

### Serve a specific folder

```bash
# Windows
set WIFI_FTP_ROOT=C:\Users\YourName\Documents
python app.py

# Mac/Linux
WIFI_FTP_ROOT=/path/to/folder python app.py
```

### Change the port

```bash
PORT=8080 python app.py
```

## 📱 Mobile Usage

### Android (Termux)
```bash
pkg install python
pip install flask
python app.py
```

### iOS (Pythonista / Pyto)
Run `app.py` and open the URL in Safari.

## 🖥️ How It Works

1. The app starts a Flask web server on your machine
2. It detects your local IP address
3. Any device on the same WiFi can open that IP:port in a browser
4. Browse folders, view files, and download with one click

## 🔒 Security

- Only accessible on your local network (not the internet)
- Directory traversal protection
- Hidden files excluded by default

## 📄 License

MIT
