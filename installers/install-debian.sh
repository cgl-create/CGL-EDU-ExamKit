#!/usr/bin/env bash
set -euo pipefail
APP="$HOME/.local/share/cgl-examkit-app"
mkdir -p "$APP"
BASE="https://raw.githubusercontent.com/cgl-create/CGL-EDU-ExamKit/main"
for f in index.html app.js server.py requirements.txt manifest.webmanifest sw.js icon.svg; do
  echo "Downloading $f..."
  curl -fL "$BASE/$f" -o "$APP/$f"
done
python3 -m venv "$APP/.venv"
"$APP/.venv/bin/python" -m pip install --upgrade pip
"$APP/.venv/bin/pip" install -r "$APP/requirements.txt"
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/examkit" <<EOF
#!/usr/bin/env bash
cd "$APP"
exec "$APP/.venv/bin/python" server.py "\$@"
EOF
chmod +x "$HOME/.local/bin/examkit"
echo ""
echo "Installed. Run: examkit"
echo "Then open http://examkit.local:8765 (or the hostname shown in the terminal)."
echo "If the command is not found, add ~/.local/bin to PATH or run the launcher by full path."
