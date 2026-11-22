#!/bin/bash
set -e
APP="$HOME/Library/Application Support/CGL ExamKit/App"
mkdir -p "$APP"
BASE="https://raw.githubusercontent.com/cgl-create/CGL-EDU-ExamKit/main"
for f in index.html app.js server.py requirements.txt manifest.webmanifest sw.js icon.svg; do
  echo "Downloading $f..."
  curl -fL "$BASE/$f" -o "$APP/$f"
done
PYTHON="$(command -v python3 || true)"
if [ -z "$PYTHON" ]; then echo "Install Python 3 from https://www.python.org/downloads/macos/ and run this installer again."; read -r; exit 1; fi
"$PYTHON" -m venv "$APP/.venv"
"$APP/.venv/bin/python" -m pip install --upgrade pip
"$APP/.venv/bin/pip" install -r "$APP/requirements.txt"
mkdir -p "$HOME/Applications"
cat > "$HOME/Applications/ExamKit.command" <<EOF
#!/bin/bash
cd "$APP"
"$APP/.venv/bin/python" server.py
EOF
chmod +x "$HOME/Applications/ExamKit.command"
echo "Installed. Start ExamKit from ~/Applications/ExamKit.command"
echo "Open http://examkit.local:8765 (or the hostname printed by the server)."
read -r -p "Press Return to close..."
