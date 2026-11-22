# CGL+ ExamKit

CGL+ ExamKit is a browser-based examination workspace with an OS-style startup and desktop experience. The main application is based on `LegacyOS.html`.

## Run

Open `index.html` in a modern browser, or publish the repository with GitHub Pages. No Python, Node.js, or build step is required.

## Current features

- ExamKit OS startup, first-run account setup, local sign-in, lock screen and a TrueNAS-inspired administration dashboard with sidebar navigation and workspace metrics
- **My Papers**: create new papers, save them, reopen and continue editing, duplicate, and delete saved papers
- Exam setup, MCQ question editor, options and answer-key selection
- Printable question paper, OMR answer sheet and answer key
- Image-based OMR prototype with corner-marker detection, perspective mapping, bubble scoring and review overlays
- Grade Checker with right/wrong/blank counts, score calculation, editable roll numbers, CSV export and improved OMR digit sampling
- **Image to text for student names** using Tesseract.js loaded from a public CDN on demand; internet access is required for the first OCR load, and OCR output must be checked and corrected
- Browser-local persistence for account workspace, saved papers and scan results
- **Full OS backup and restore** as a `.cgl` file, including every local account and each account's workspace, saved papers and grade records, protected by SHA-256 integrity verification

## Data storage and backups

On the GitHub Pages web version, exam data is stored in browser localStorage, separately for each local ExamKit account. On an installed local-host setup, the browser first asks for the host access key printed in the server terminal, then synchronizes changes to a SQLite database on that same host PC. No CGL+ cloud server is involved. Use **Full OS backup .cgl** to download the complete local OS state to the computer. Use **Restore .cgl** to replace the current browser's ExamKit OS data and accounts with the backup. The Save current paper control is available only inside My Papers, not as a floating button across the application. After restore, sign in using an account contained in that backup. Backup and restore require a secure browser context with Web Crypto support (for example, GitHub Pages over HTTPS). Keep backups somewhere safe before clearing browser data.

The current `.cgl` file is a versioned JSON envelope containing all `os:` and `examkit:` browser-storage entries (including the local account database and all users' data), plus a SHA-256 integrity digest. It is not a ZIP archive. Restoring replaces the ExamKit OS data namespaces in the current browser; it does not restore browser extensions, browser settings, or data outside ExamKit.

## Important limitations

This is an early prototype, not a production-grade examination system. OMR recognition depends on clean, correctly framed photos and the printed sheet remaining at 100% scale. Roll numbers use six digit columns; check the roll value and correct it in the Grade Checker when any digit is uncertain. Review every detected answer before relying on scores. Name OCR is best-effort and may misread handwriting, low-resolution images or unusual scripts. The OCR tool currently reads a user-selected name image; it does not yet automatically extract the name from the OMR sheet during scanning.

Accounts are browser-local, not server-authenticated. On the static web version, clearing site data can erase accounts and exam data. On the installed version, the host SQLite database remains outside the browser profile. Export full OS backups regularly. Keep the `.cgl` file private because it contains local account records and all included exam data.


## Installable Web App (PWA)

ExamKit includes a web app manifest, app icon, and service worker. On a supported browser, open the GitHub Pages site over HTTPS or the local host and choose **Install Web App** from the dashboard (or use the browser's Install app / Add to Home Screen menu). The shell can be cached for offline opening. OCR still needs its first Tesseract.js download unless that library has already been cached by the browser.

## Run ExamKit on your own computer

The desktop installers are available from the dashboard and in `installers/`:

- Debian / Linux: download `installers/install-debian.sh`, then run `bash install-debian.sh`. It installs the app under `~/.local/share/cgl-examkit-app`, creates the `examkit` launcher in `~/.local/bin`, and installs the Python dependencies in a virtual environment.
- Windows: download `installers/install-windows.ps1` and run it in PowerShell. It creates a Desktop shortcut named **CGL+ ExamKit OS**.
- macOS: download `installers/install-macos.command` and run `bash install-macos.command` in Terminal. It creates `~/Applications/ExamKit.command`.

Python 3.9+ is required. On Debian, install the Python venv package if your distribution does not include it (for example, `sudo apt install python3-venv`). On Windows, run PowerShell as Administrator if you want the installer to add the optional private-network firewall rule; if script execution is blocked, use `Set-ExecutionPolicy -Scope Process Bypass` for that PowerShell session. The installers download the current application bundle and server files from this repository and install the small `zeroconf` dependency for mDNS discovery. To start the local service, run `examkit` on Debian, use the Windows Desktop shortcut, or open `~/Applications/ExamKit.command` on macOS.

The local host serves ExamKit on port **8765**. The server prints a random host access key at startup; enter it when a browser first connects. It is held in that browser tab's session storage. It prints both a localhost URL and a network URL such as `http://<computer-hostname>.local:8765`. The exact hostname depends on the installed computer's hostname. mDNS support and firewall rules vary by operating system and network; if the .local address does not resolve, use the computer's LAN IP address with port 8765. Keep the computer awake and the ExamKit server running while other devices use it. Devices must be on the same trusted local network.

## Local PC database

When opened from the installed local host, ExamKit synchronizes its `os:` and `examkit:` browser data to a local SQLite database. The database is stored outside the browser profile:

- Debian / Linux: `~/.local/share/cgl-examkit/examkit.sqlite3`
- Windows: `%LOCALAPPDATA%\\CGL\\ExamKit\\examkit.sqlite3`
- macOS: `~/Library/Application Support/CGL ExamKit/examkit.sqlite3`

The browser's localStorage is used as the app's live cache; the SQLite database is the durable local-host copy. The full OS `.cgl` backup remains available as a portable backup/export. The local server listens on the LAN so other devices can reach the .local address. The host access key protects the database API, but traffic is plain HTTP; use it only on a trusted private network and do not expose port 8765 to the public internet. The app's local account screen is not a replacement for a hardened multi-user server.

## Notes and limitations

This is a local web application hosted by a small Python service, not a bootable operating system or a native compiled desktop application. The computer hosting it must remain powered on. The installers are scripts, not signed packages; review them before running. GitHub Pages remains a static web version and keeps data in that browser unless the app is opened through the installed local host.
