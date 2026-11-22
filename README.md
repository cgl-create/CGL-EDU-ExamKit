# CGL+ ExamKit

CGL+ ExamKit is a browser-based examination workspace with an OS-style startup and desktop experience. The main application is based on `LegacyOS.html`.

## Run

Open `index.html` in a modern browser, or publish the repository with GitHub Pages. No Python, Node.js, or build step is required.

## Current foundation

- Animated startup screen and first-run setup
- Local user accounts, password sign-in, lock screen, and desktop launcher
- Exam setup and MCQ question editor with answer-key selection
- Printable question paper, OMR answer sheet, and answer key
- Image upload scanner prototype with corner-marker detection, perspective mapping, bubble scoring, and result overlays
- Manual correction of detected roll numbers and CSV result export
- Browser-local storage for user accounts and exam data

## Important limitations

This is an early prototype, not yet a production-grade examination system. OMR recognition depends on clean, correctly framed photos and the printed sheet remaining at 100% scale. Review every detected answer before using scores. Student-name OCR, a full student database, multiple saved papers per account, robust scan calibration, PDF export, and cloud sync are not implemented in this LegacyOS foundation.

The current LegacyOS foundation does **not yet include the planned CGL+ `.cgl` backup and restore system**. That needs to be added back and tested before relying on it for data portability.

## Data and privacy

Accounts and exam data are stored in the browser's local storage on the current device. Clearing site data can erase them. This prototype does not provide server-side accounts or cloud backup.
