---
lang: fr
title: Comparer dans le rapport
type: how-to
audience: everyone
status: draft
---

# Comparer dans le rapport

Le panneau de droite se met à jour pendant que vous modifiez. Il montre la qualité, la quantité, l'énergie et la durabilité du scénario ouvert.

Le rapport est la vue détaillée de ce scénario, et l'endroit où chaque scénario du projet est dessiné côte à côte.

## Ouvrir le rapport

Cliquez sur **Calculer le projet** dans la barre du haut. La même commande est sous **Projet**.

Le rapport s'ouvre sur **Modèle unique**, pour le scénario sélectionné.

- **Qualité de l'eau** — des barres pour chaque unité de la filière. La liste choisit le paramètre (pH, dureté, et le reste). Les deux icônes à côté de la liste basculent entre des barres ordinaires et un graphique en escalier. La longue liste est le parcours à travers l'installation. Le tableau sous le graphique a les mêmes nombres. Laissez le pointeur sur une colonne pour voir en quoi cette étape diffère de la précédente. **Copier** place le tableau dans le presse-papiers.
- **Énergie** — par m³ traité, par m³ livré, et la consommation totale.
- **Durabilité** — le même type de graphique pour le CO₂.

La quantité (captage, distribution, pertes) reste dans le panneau de droite. Elle est dessinée dans le rapport quand vous activez **Comparaison**.

<video controls preload="metadata" src="../media/OpenReport.mp4" style="max-width: 100%; height: auto;" aria-label="Ouvrez le rapport, changez les paramètres de qualité de l'eau et copiez le tableau">
Cliquez sur Calculer le projet. Passez du pH à la dureté, basculez le graphique en escalier, ouvrez l'énergie et la durabilité, puis copiez le tableau de qualité de l'eau.
</video>

## Comparer deux scénarios

Une comparaison demande deux scénarios qui ne sont pas identiques.

1. Sur l'onglet de scénario en bas, cliquez sur **⋮** et choisissez **Dupliquer**. Nommez la copie et confirmez avec **Ajouter un scénario**.
2. Sur la copie, changez un choix de conception. Double-cliquez sur l'unité. Sous **Dosage**, réglez le nombre et appuyez sur Entrée. Dans la démo, **Adoucissement sur pellets** → **Dosage de base** est abaissé de 2 à 0.5. Les courbes de dosage bougent avec le nombre. Voir [Configurer une unité](configure-a-unit.md).
3. Cliquez sur **Calculer le projet**.
4. Activez **Comparaison**.

La liste des scénarios en haut est désactivée tant que **Comparaison** est activée, parce que chaque scénario est déjà sur la page.

La comparaison est regroupée sous quatre titres. À l'écran, ces titres sont **Kwantiteit**, **Waterkwaliteit**, **Energie** et **Duurzaamheid** (quantité, qualité de l'eau, énergie, durabilité). Chaque groupe a un graphique et un tableau. Les boutons ou la liste choisissent le nombre que vous comparez.

Un changement de dose apparaît dans la qualité de l'eau et la durabilité. La quantité reste la même quand vous ne changez qu'une dose de réactif.

**Compact** (le commutateur libellé **Uitgebreid** / **Compact**) garde les quatre graphiques et masque les tableaux.

<video controls preload="metadata" src="../media/DuplicateAndChange.mp4" style="max-width: 100%; height: auto;" aria-label="Dupliquez le scénario 1 sous le nom Lower dose et abaissez le dosage de base de l'adoucissement">
Ouvrez le menu de scénario, dupliquez le scénario 1 sous le nom Lower dose, double-cliquez sur Pelletontharding et réglez Dosage de base à 0.5.
</video>

<video controls preload="metadata" src="../media/CompareScenarios.mp4" style="max-width: 100%; height: auto;" aria-label="Activez Comparaison et Compact pour voir les deux scénarios">
Cliquez sur Calculer le projet, activez Comparaison, puis passez à Compact. La quantité correspond ; la dureté et le CO₂ non.
</video>

## Lire un scénario, puis revenir

Désactivez **Comparaison** pour revenir à **Modèle unique**. La liste en haut choisit les graphiques du scénario que vous lisez. Chaque scénario garde ses propres nombres.

Réactivez **Comparaison**. Les deux scénarios sont toujours là. Fermer le rapport ne les retire pas.

<video controls preload="metadata" src="../media/SwitchScenarioInReport.mp4" style="max-width: 100%; height: auto;" aria-label="Quittez la comparaison, changez la liste des scénarios, puis réactivez la comparaison">
Désactivez Comparaison, lisez le scénario 1, passez la liste à Lower dose, puis réactivez Comparaison. Les deux scénarios sont toujours listés.
</video>

## Ce que le rapport laisse de côté

Le rapport n'ouvre pas la fenêtre de conception d'une unité. Double-cliquez sur un bloc pour cela. La fenêtre contient le schéma de l'unité, le **Bilan massique**, la **Ligne hydraulique** et les **Tableaux de conception**. Cette fenêtre est détaillée dans [Utiliser la vue conception](use-design-view.md).

Les tableaux élément par élément d'une membrane sont dans cette fenêtre, pas dans le rapport. L'installation de démonstration n'a pas de membrane. La vidéo ouvre **Nafiltratie**, avec le même geste.

<video controls preload="metadata" src="../media/DesignNotInReport.mp4" style="max-width: 100%; height: auto;" aria-label="Fermez le rapport et ouvrez la vue conception de Nafiltratie">
Fermez le rapport, double-cliquez sur Nafiltratie, et ouvrez le schéma, les tableaux de conception et le bilan massique.
</video>

## Garder une copie des nombres

Le rapport n'a pas de commande d'impression ni d'export de fichier. **Copier** sur un tableau copie ce tableau (montré dans la première vidéo). **Projet → Télécharger** écrit le projet en JSON. Ce fichier, ce sont les données d'entrée. Le rouvrir est décrit dans [Enregistrer, charger, télécharger](save-load-download.md).

<video controls preload="metadata" src="../media/DownloadProject.mp4" style="max-width: 100%; height: auto;" aria-label="Téléchargez le JSON du projet depuis le menu Projet">
Ouvrez le menu Projet et cliquez sur Télécharger.
</video>
