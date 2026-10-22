---
lang: en
title: Save, load, download
type: how-to
audience: everyone
status: draft
---

# Save, load, download

Amanzi keeps the project you are working on in this browser. **Download** writes a `.json` file you can send to someone else. **Open** reads that file back and replaces the project on screen.

## Save in this browser

Edit something, for example a note under **Scenario**. The title gains an asterisk, and the bar turns yellow: **Unsaved changes, click here to save.**

Click that bar, or choose **Project → Save**. On a Mac the shortcut is ⌘S. Elsewhere it is Ctrl+S. The bar then says **All changes saved**.

That copy stays in this browser on this computer. Leave the page and come back, and the saved project is still there. It is not a file you can attach to an email.

<video controls preload="metadata" src="../media/SaveInBrowser.mp4" style="max-width: 100%; height: auto;" aria-label="Type a scenario note and save the project from the Project menu">
Type a note, open Project, and click Save. The bar changes from Unsaved changes to All changes saved.
</video>

## Name the project, then download it

Click the project name in the title bar. **Project → Rename project** opens the same dialog. Type the new name and click **Save**.

**Project → Download** writes a JSON file of the project on screen, including its scenarios and notes. The filename is the name in the title bar, so **North plant** is saved as `North plant.json`.

The yellow bar does not turn on when only the name changes. **Save** again if you want this browser to keep the new name.

<video controls preload="metadata" src="../media/RenameProject.mp4" style="max-width: 100%; height: auto;" aria-label="Rename Demo Project to North plant from the title bar">
Click the project name, type North plant, and click Save. The title bar shows the new name.
</video>

<video controls preload="metadata" src="../media/DownloadJson.mp4" style="max-width: 100%; height: auto;" aria-label="Download the project JSON from the Project menu">
Open the Project menu and click Download.
</video>

## Start a new project

**Project → New...** asks before it replaces the project on screen.

- **Download and overwrite** writes a JSON file first, then starts empty.
- **Overwrite** starts empty without writing a file.
- Close the question with the X and the current project stays.

The empty project is titled **New project**. The last **Save** in this browser is still there until you **Save** or **Open** something else. Refresh before that, and the last saved project comes back.

<video controls preload="metadata" src="../media/NewProject.mp4" style="max-width: 100%; height: auto;" aria-label="Create a new project and choose Overwrite">
Open Project, click New, and choose Overwrite. The canvas is empty and the title is New project.
</video>

## Open a file

**Project → Open** asks for a `.json` file. On a Mac the shortcut is ⌘O. Elsewhere it is Ctrl+O. The file window is the system one, so it is not in the clip.

Choosing a file replaces the project on screen straight away. Amanzi does not ask first. That file also becomes the copy stored in this browser.

<video controls preload="metadata" src="../media/OpenProject.mp4" style="max-width: 100%; height: auto;" aria-label="Open a project JSON over an empty new project">
From an empty New project, click Open. The file comes back as North plant, notes included.
</video>

## An older file

Opening a file written by an earlier Amanzi shows **Project file updated**, with the version it came from and the version it is now. In the clip that range is 1.0.0 → 1.0.5. Continue working.

When a model setting was rewritten, the notice lists that change. When only the file version moved forward, it says that no model-level change was applied. The updated project is already saved in this browser.

<video controls preload="metadata" src="../media/MigrationNotice.mp4" style="max-width: 100%; height: auto;" aria-label="Open an older project file and read the update notice">
Open an older file. The notice says Project file updated, 1.0.0 to 1.0.5.
</video>
