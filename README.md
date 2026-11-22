# CGL+ ExamKit

CGL+ ExamKit is a browser-based examination workspace for authoring papers, preparing answer sheets, managing students and recording grades.

## Run

Open `index.html` in a modern browser. No Python, Node.js or build step is required.

## Current build

- Overview dashboard and local workspace storage
- My Papers and MCQ Question Editor with answer-key selection
- Printable A4-style answer sheet generation
- Student Manager
- Manual Grade Checker and basic Analytics
- Versioned `.cgl` JSON backup export/import with SHA-256 integrity verification (requires a secure browser context that exposes Web Crypto for backup operations)

## Current limitations

Automatic OMR image recognition, perspective correction, bubble detection, multiple-mark detection, student-name OCR, cloud sync, and PDF/CSV export are not implemented in this initial foundation. The OMR Studio currently generates printable sheets and directs grading to the manual grade-entry workflow. Do not use this build as an automated examination scanner.

Workspace data is stored in the browser's local storage on the current device. Export backups before clearing browser data.

## Backup format

A `.cgl` file is a JSON envelope containing the product identifier, schema version, timestamp, workspace payload, and SHA-256 digest of the canonical payload. Restore verifies the digest before replacing current local data.
