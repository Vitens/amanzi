---
lang: fr
title: Régler les indicateurs
type: how-to
audience: everyone
status: draft
---

# Régler les indicateurs

Les indicateurs sont des nombres partagés : facteurs d'émission, rendements de pompe et limites de qualité. Laissez-les pendant que vous dessinez l'installation. Changez-en un quand l'hypothèse doit changer, par exemple le facteur d'émission de l'électricité, ou une limite de qualité à laquelle vous devez concevoir. Les réglages propres à une unité restent sur l'unité. Voir [Configurer une unité](configure-a-unit.md).

Le panneau de droite montre le résultat de ces nombres. La liste elle-même est une fenêtre. La base de données derrière la liste est décrite dans [Indicateurs](../reference/key-figures.md).

## Ouvrir la liste

Cliquez sur **Indicateurs** dans la barre du haut. La même commande est sous **Projet**.

Les colonnes restent **Name**, **Tag**, **Default**, **Project**, **Scenario** et **UOM**. **Default** est la valeur intégrée. Une cellule **Project** ou **Scenario** vide n'est pas une surcharge. Le nombre gris dans la case est cette valeur par défaut, affichée pour que vous sachiez ce que vous remplaceriez.

**Filter...** réduit la liste. La casse compte. `electricity` trouve **Facteur d'émission de l'électricité** (balise `carbon_intensity_grid`, 250 gCO₂/kWh). `hardness` trouve les limites de dureté sous **Normes de qualité**.

Les limites de qualité de cette liste sont des lignes telles que pH, dureté, fer et manganèse. Sum4, Sum20 et PEQ ne sont pas dans cette version de la liste.

<video controls preload="metadata" src="../media/SearchKeyFigures.mp4" style="max-width: 100%; height: auto;" aria-label="Ouvrez Indicateurs et filtrez sur electricity, puis sur hardness">
Cliquez sur Indicateurs. Filtrez sur electricity, puis sur hardness.
</video>

## Une valeur de projet s'applique à chaque scénario

Saisissez dans la cellule **Project**. La ligne passe au jaune. Le bouton de filtre indique combien d'indicateurs vous avez changés.

Dans la vidéo, le facteur électricité passe de 250 à 100 gCO₂/kWh. Fermez la fenêtre. À droite, les **Émissions spécifiques** descendent de 335 à 299 gCO₂-eq/m³, et les **Émissions totales** de 3177 à 2840 ton CO₂-eq/y. Chaque scénario utilise cette valeur de projet, sauf si sa propre cellule **Scenario** est remplie.

<video controls preload="metadata" src="../media/ProjectKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Réglez le facteur électricité du projet à 100 et regardez les émissions spécifiques baisser">
Tapez 100 dans la cellule Project du facteur électricité. Les émissions spécifiques passent de 335 à 299.
</video>

## Une valeur de scénario s'applique à un seul scénario

Dupliquez le scénario quand cette copie doit utiliser une autre hypothèse. Sur la copie, saisissez dans la cellule **Scenario**. Ce nombre l'emporte sur la valeur de projet, pour ce scénario seulement. Les autres scénarios gardent la valeur de projet.

Dans la vidéo, **High grid** règle le facteur électricité à 500. Ses émissions spécifiques sont de 394 gCO₂-eq/m³. **Scenario 1** a une cellule de scénario vide : il garde donc la valeur de projet de 100 et reste à 299.

<video controls preload="metadata" src="../media/ScenarioKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Dupliquez un scénario et réglez son facteur électricité à 500">
Dupliquez le scénario sous le nom High grid et tapez 500 dans la cellule Scenario. Les émissions spécifiques montent à 394.
</video>

## Voir seulement vos changements, puis vider une cellule

Le bouton à côté du filtre n'affiche que les lignes que vous avez changées. Le compteur indique combien.

L'icône orange dans une cellule vide cette cellule. La ligne utilise alors de nouveau la valeur par défaut de la base, sauf si l'autre colonne contient encore un nombre. Vider la cellule de scénario laisse le nombre de projet en vigueur. Vider aussi la cellule de projet ramène la valeur intégrée 250. Dans la vidéo, les émissions spécifiques reviennent à 335.

<video controls preload="metadata" src="../media/RestoreKeyFigure.mp4" style="max-width: 100%; height: auto;" aria-label="Filtrez sur les indicateurs modifiés et videz les cellules projet et scénario">
N'affichez que la ligne modifiée, videz la cellule de scénario, puis la cellule de projet. Les émissions spécifiques reviennent à 335.
</video>
