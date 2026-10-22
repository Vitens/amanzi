---
lang: en
title: Open hosted or local
type: how-to
audience: everyone
status: draft
---

# Open hosted or local

Open Amanzi in your web browser. Use the website, or a copy you have downloaded.

The project you build stays on the computer where Amanzi is open. Amanzi calculates it there and does not send that project to a server. **Save** in the **Project** menu keeps it in this browser. **Download** writes a file you can store or move to another computer. There is no copy waiting on a server, so that file is the one you keep. How to save, download, and open it again is in [Save, load, download](save-load-download.md).

The first time you open Amanzi, a window titled **Starting AMANZI...** downloads the calculation program. Keep an internet connection until that window closes. It may show technical names while it loads. Wait until it closes by itself.

## Open the website

Use the website when you want the current version.

1. Open [https://demo.amanzi.app](https://demo.amanzi.app).
2. Wait until **Starting AMANZI...** closes.

The canvas is ready. A short tutorial may ask to start. Follow it, or close it and continue with [Open Amanzi](../tutorials/open-amanzi.md).

<video controls preload="metadata" src="../media/StartingAmanzi.mp4" style="max-width: 100%; height: auto;" aria-label="Hold Shift while dragging a unit onto the canvas to place it and connect it">
Loading Screen when openening Amanzi in the webbrowser. Internet connection required to finish
</video>

## Open a downloaded copy

Use a downloaded copy when you want to stay on one version. The website moves to a new version when one is published. The copy on your computer stays as you unpacked it.

You still need an internet connection the first time, so **Starting AMANZI...** can download the calculation program.

1. Open the [Amanzi downloads](https://github.com/Vitens/amanzi/releases/latest).
2. Under **Assets**, download `dist.zip`.
3. Unzip `dist.zip`. Work in the folder that contains `index.html`. Leave the other files next to it.
4. Open a terminal in that folder.
    - **Mac:** open Terminal. Type `cd` and a space, drag the folder onto the Terminal window, and press Return.
    - **Windows:** open the folder in File Explorer. Click the address bar, type `cmd`, and press Enter.
5. Copy this command into the terminal and press Enter:

    ```bash
    python3 -m http.server 8000
    ```

    When the computer says it cannot find `python3`, run `python -m http.server 8000` instead. When neither command is found, install Python from [python.org](https://www.python.org/downloads/) and run the command again. The command lets your browser open the folder. The calculation still runs in the browser.

6. In the browser address bar, open [http://localhost:8000](http://localhost:8000). That address is your own computer.
7. Wait until **Starting AMANZI...** closes.

Leave the terminal window open while you work. Closing it stops this copy of Amanzi. To use it again, run the command, then open [http://localhost:8000](http://localhost:8000). Amanzi loads from that address. Opening `index.html` straight from the folder skips the address, and the page stays blank.
