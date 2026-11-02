---
lang: fr
title: Répartition
type: reference
audience: everyone
status: draft
---

# Répartition

Nom dans la bibliothèque : **Répartition**. Divise un flux produit en deux flux produit.

## Flux

Entrée : produit. Sortie : produit, à droite. Sortie : produit, en bas.

## Entrées

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `split` | fraction | 0.5 | 0.01–0.99 |
| `pressurized` | — | false | |

`split` est la fraction qui sort par l’une des deux sorties. 0.5 envoie la moitié de chaque côté. L’étiquette du champ indique %. La valeur stockée est la fraction.
