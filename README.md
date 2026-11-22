# CGL+ ExamKit

CGL+ ExamKit is a browser-based examination workspace with an OS-style startup and desktop experience. The main application is based on `LegacyOS.html`.

## Run

Open `index.html` in a modern browser, or publish the repository with GitHub Pages. No Python, Node.js, or build step is required.

## Current features

- ExamKit OS startup, first-run account setup, local sign-in, lock screen and desktop launcher
- **My Papers**: create new papers, save them, reopen and continue editing, duplicate, and delete saved papers
- Exam setup, MCQ question editor, options and answer-key selection
- Printable question paper, OMR answer sheet and answer key
- Image-based OMR prototype with corner-marker detection, perspective mapping, bubble scoring and review overlays
- Grade Checker with right/wrong/blank counts, score calculation, roll-number correction and CSV export
- **Image to text for student names** using Tesseract.js loaded from a public CDN on demand; internet access is required for the first OCR load, and OCR output must be checked and corrected
- Browser-local persistence for account workspace, saved papers and scan results
- **Save backup to PC** as a `.cgl` file and restore it later with SHA-256 integrity verification

## Data storage and backups

Exam data is stored locally in the browser, separately for each local ExamKit account. It is not uploaded to a CGL+ server. Use **Save backup .cgl** to download a backup to the computer. Use **Restore .cgl** to import it again. Backup and restore require a secure browser context with Web Crypto support (for example, GitHub Pages over HTTPS). Keep backups somewhere safe before clearing browser data.

The current `.cgl` file is a versioned JSON envelope with the ExamKit workspace, saved paper library, grade results and a SHA-256 integrity digest. It is not a ZIP archive.

## Important limitations

This is an early prototype, not a production-grade examination system. OMR recognition depends on clean, correctly framed photos and the printed sheet remaining at 100% scale. Review every detected answer before relying on scores. Name OCR is best-effort and may misread handwriting, low-resolution images or unusual scripts. The OCR tool currently reads a user-selected name image; it does not yet automatically extract the name from the OMR sheet during scanning.

Accounts are browser-local, not server-authenticated. Clearing site data can erase accounts and exam data. Export backups regularly.
