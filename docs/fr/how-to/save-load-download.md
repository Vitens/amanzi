---
lang: fr
title: Enregistrer, charger, télécharger
type: how-to
audience: everyone
status: draft
---

# Enregistrer, charger, télécharger

Amanzi conserve le projet en cours dans ce navigateur. **Télécharger** écrit un fichier `.json` que vous pouvez envoyer à quelqu'un d'autre. **Ouvrir** relit ce fichier et remplace le projet à l'écran.

## Enregistrer dans ce navigateur

Modifiez quelque chose, par exemple une note sous **Scénario**. Le titre gagne un astérisque, et la barre passe au jaune : **Modifications non enregistrées, cliquez ici pour enregistrer.**

Cliquez sur cette barre, ou choisissez **Projet → Enregistrer**. Sur un Mac, le raccourci est ⌘S. Ailleurs, c'est Ctrl+S. La barre indique alors **Toutes les modifications sont enregistrées**.

Cette copie reste dans ce navigateur, sur cet ordinateur. Quittez la page et revenez : le projet enregistré est toujours là. Ce n'est pas un fichier que vous pouvez joindre à un e-mail.

<video controls preload="metadata" src="../media/SaveInBrowser.mp4" style="max-width: 100%; height: auto;" aria-label="Saisissez une note de scénario et enregistrez le projet depuis le menu Projet">
Saisissez une note, ouvrez Projet et cliquez sur Enregistrer. La barre passe de Modifications non enregistrées à Toutes les modifications sont enregistrées.
</video>

## Nommer le projet, puis le télécharger

Cliquez sur le nom du projet dans la barre de titre. **Projet → Renommer le projet** ouvre la même fenêtre. Saisissez le nouveau nom et cliquez sur **Enregistrer**.

**Projet → Télécharger** écrit un fichier JSON du projet à l'écran, scénarios et notes compris. Le nom de fichier est celui de la barre de titre : **North plant** est donc enregistré comme `North plant.json`.

La barre jaune ne s'allume pas quand seul le nom change. **Enregistrer** de nouveau si vous voulez que ce navigateur garde le nouveau nom.

<video controls preload="metadata" src="../media/RenameProject.mp4" style="max-width: 100%; height: auto;" aria-label="Renommez Demo Project en North plant depuis la barre de titre">
Cliquez sur le nom du projet, tapez North plant et cliquez sur Enregistrer. La barre de titre affiche le nouveau nom.
</video>

<video controls preload="metadata" src="../media/DownloadJson.mp4" style="max-width: 100%; height: auto;" aria-label="Téléchargez le JSON du projet depuis le menu Projet">
Ouvrez le menu Projet et cliquez sur Télécharger.
</video>

## Démarrer un nouveau projet

**Projet → Nouveau...** demande confirmation avant de remplacer le projet à l'écran.

- **Télécharger et écraser** écrit d'abord un fichier JSON, puis démarre à vide.
- **Écraser** démarre à vide sans écrire de fichier.
- Fermez la question avec la croix : le projet en cours reste.

Le projet vide s'intitule **New project**. Le dernier **Enregistrer** de ce navigateur est toujours là, jusqu'à ce que vous cliquiez sur **Enregistrer** ou **Ouvrir** pour autre chose. Actualisez avant cela, et le dernier projet enregistré revient.

<video controls preload="metadata" src="../media/NewProject.mp4" style="max-width: 100%; height: auto;" aria-label="Créez un nouveau projet et choisissez Écraser">
Ouvrez Projet, cliquez sur Nouveau et choisissez Écraser. Le canevas est vide et le titre est New project.
</video>

## Ouvrir un fichier

**Projet → Ouvrir** demande un fichier `.json`. Sur un Mac, le raccourci est ⌘O. Ailleurs, c'est Ctrl+O. La fenêtre de fichier est celle du système, elle n'est donc pas dans la vidéo.

Choisir un fichier remplace tout de suite le projet à l'écran. Amanzi ne demande pas confirmation. Ce fichier devient aussi la copie stockée dans ce navigateur.

<video controls preload="metadata" src="../media/OpenProject.mp4" style="max-width: 100%; height: auto;" aria-label="Ouvrez un JSON de projet par-dessus un nouveau projet vide">
Depuis un New project vide, cliquez sur Ouvrir. Le fichier revient sous le nom North plant, notes comprises.
</video>

## Un fichier plus ancien

Ouvrir un fichier écrit par un Amanzi plus ancien affiche **Fichier de projet mis à jour**, avec la version d'origine et la version actuelle. Dans la vidéo, cette plage est 1.0.0 → 1.0.5. Continuez à travailler.

Quand un réglage de modèle a été réécrit, la notice liste ce changement. Quand seule la version du fichier a avancé, elle indique qu'aucune modification au niveau du modèle n'a été appliquée. Le projet mis à jour est déjà enregistré dans ce navigateur.

<video controls preload="metadata" src="../media/MigrationNotice.mp4" style="max-width: 100%; height: auto;" aria-label="Ouvrez un fichier de projet plus ancien et lisez la notice de mise à jour">
Ouvrez un fichier plus ancien. La notice indique Fichier de projet mis à jour, de 1.0.0 à 1.0.5.
</video>
