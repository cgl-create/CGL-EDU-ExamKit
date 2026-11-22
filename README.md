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

Exam data is stored locally in the browser, separately for each local ExamKit account. It is not uploaded to a CGL+ server. Use **Full OS backup .cgl** to download the complete local OS state to the computer. Use **Restore .cgl** to replace the current browser's ExamKit OS data and accounts with the backup. After restore, sign in using an account contained in that backup. Backup and restore require a secure browser context with Web Crypto support (for example, GitHub Pages over HTTPS). Keep backups somewhere safe before clearing browser data.

The current `.cgl` file is a versioned JSON envelope containing all `os:` and `examkit:` browser-storage entries (including the local account database and all users' data), plus a SHA-256 integrity digest. It is not a ZIP archive. Restoring replaces the ExamKit OS data namespaces in the current browser; it does not restore browser extensions, browser settings, or data outside ExamKit.

## Important limitations

This is an early prototype, not a production-grade examination system. OMR recognition depends on clean, correctly framed photos and the printed sheet remaining at 100% scale. Roll numbers use six digit columns; check the roll value and correct it in the Grade Checker when any digit is uncertain. Review every detected answer before relying on scores. Name OCR is best-effort and may misread handwriting, low-resolution images or unusual scripts. The OCR tool currently reads a user-selected name image; it does not yet automatically extract the name from the OMR sheet during scanning.

Accounts are browser-local, not server-authenticated. Clearing site data can erase accounts and exam data. Export full OS backups regularly. Keep the `.cgl` file private because it contains local account records and all included exam data.
