---
lang: fr
title: Ouvrir en ligne ou en local
type: how-to
audience: everyone
status: draft
---

# Ouvrir en ligne ou en local

Ouvrez Amanzi dans votre navigateur. Utilisez le site, ou une copie que vous avez téléchargée.

Le projet que vous construisez reste sur l'ordinateur où Amanzi est ouvert. Amanzi le calcule là, et n'envoie pas ce projet à un serveur. **Enregistrer** dans le menu **Projet** le conserve dans ce navigateur. **Télécharger** écrit un fichier que vous pouvez stocker ou déplacer vers un autre ordinateur. Aucune copie n'attend sur un serveur : ce fichier est celui que vous gardez. Comment l'enregistrer, le télécharger et le rouvrir est dans [Enregistrer, charger, télécharger](save-load-download.md).

La première fois que vous ouvrez Amanzi, une fenêtre intitulée **Démarrage d'AMANZI...** télécharge le programme de calcul. Gardez une connexion internet jusqu'à ce que cette fenêtre se ferme. Elle peut afficher des noms techniques pendant le chargement. Attendez qu'elle se ferme toute seule.

## Ouvrir le site

Utilisez le site quand vous voulez la version en cours.

1. Ouvrez [https://demo.amanzi.app](https://demo.amanzi.app).
2. Attendez que **Démarrage d'AMANZI...** se ferme.

Le canevas est prêt. Un court tutoriel peut proposer de démarrer. Suivez-le, ou fermez-le et continuez avec [Ouvrir Amanzi](../tutorials/open-amanzi.md).

<video controls preload="metadata" src="../media/StartingAmanzi.mp4" style="max-width: 100%; height: auto;" aria-label="Maintenez Maj en glissant une unité sur le canevas pour la placer et la relier">
Écran de chargement à l'ouverture d'Amanzi dans le navigateur. Une connexion internet est nécessaire pour terminer.
</video>

## Ouvrir une copie téléchargée

Utilisez une copie téléchargée quand vous voulez rester sur une version. Le site passe à une nouvelle version dès qu'elle est publiée. La copie sur votre ordinateur reste telle que vous l'avez décompressée.

Vous avez encore besoin d'une connexion internet la première fois, pour que **Démarrage d'AMANZI...** puisse télécharger le programme de calcul.

1. Ouvrez les [téléchargements Amanzi](https://github.com/Vitens/amanzi/releases/latest).
2. Sous **Assets**, téléchargez `dist.zip`.
3. Décompressez `dist.zip`. Travaillez dans le dossier qui contient `index.html`. Laissez les autres fichiers à côté.
4. Ouvrez un terminal dans ce dossier.
    - **Mac :** ouvrez Terminal. Tapez `cd` puis un espace, glissez le dossier sur la fenêtre Terminal, et appuyez sur Retour.
    - **Windows :** ouvrez le dossier dans l'Explorateur de fichiers. Cliquez sur la barre d'adresse, tapez `cmd`, et appuyez sur Entrée.
5. Copiez cette commande dans le terminal et appuyez sur Entrée :

    ```bash
    python3 -m http.server 8000
    ```

    Si l'ordinateur dit qu'il ne trouve pas `python3`, lancez `python -m http.server 8000` à la place. Si aucune des deux commandes n'est trouvée, installez Python depuis [python.org](https://www.python.org/downloads/) et relancez la commande. Cette commande permet à votre navigateur d'ouvrir le dossier. Le calcul s'exécute toujours dans le navigateur.

6. Dans la barre d'adresse du navigateur, ouvrez [http://localhost:8000](http://localhost:8000). Cette adresse est votre propre ordinateur.
7. Attendez que **Démarrage d'AMANZI...** se ferme.

Laissez la fenêtre du terminal ouverte pendant que vous travaillez. La fermer arrête cette copie d'Amanzi. Pour la réutiliser, relancez la commande, puis ouvrez [http://localhost:8000](http://localhost:8000). Amanzi se charge depuis cette adresse. Ouvrir `index.html` directement depuis le dossier saute l'adresse, et la page reste blanche.
