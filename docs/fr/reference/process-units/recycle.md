---
lang: fr
title: Réutilisation des eaux de lavage
type: reference
audience: everyone
status: draft
---

# Réutilisation des eaux de lavage

Nom dans la bibliothèque : **Réutilisation des eaux de lavage**. Renvoie une partie d’un flux de rejet ou de lavage vers la filière produit.

## Flux

Entrée : rejet. Sortie : produit. Sortie : rejet.

La sortie produit est l’eau récupérée. La sortie rejet est ce qui n’est pas récupéré.

## Entrées

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `recycle_efficiency` | fraction | 0.8 | 0.5–0.95 |

L’étiquette indique %. La valeur stockée est la fraction. 0.8 récupère 80 % du débit de rejet entrant vers la sortie produit.

## Énergie

Le total d’énergie paramétrique de ce bloc est la constante 0.5 kWh/m³. Ce n’est pas une courbe de pompe.
