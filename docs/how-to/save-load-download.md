---
title: Save, load, download
type: how-to
audience: everyone
status: outline
---

# Save, load, download

Keep a project in the browser, download it as JSON, or replace the current project by uploading a file.

## Content to write

- Menu actions: save / download / upload / reset (labels from the Project menu).
- Browser storage vs downloaded `.json`: storage is convenient; the file is the copy you can share.
- Upload **replaces** the open project; warn before overwriting unsaved edits if the UI does so.
- Version migration toast: file format upgraded; what to tell the user (safe to continue; note the version range).
- Rename the project from the top bar so the downloaded filename matches.
