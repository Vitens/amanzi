---
lang: fr
title: Cascade
type: reference
audience: everyone
status: draft
---

# Cascade

Nom dans la bibliothèque : **Cascade**. Un escalier de marches. Pas de surpresseur.

## Quand le placer

L’absorption d’oxygène et une certaine élimination du CO₂ suffisent, et l’élimination du méthane peut rester modeste.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `units` | — | 1 | Remplace la valeur par défaut partagée |
| `number_of_steps` | — | 3 | 1–8 |
| `step_height` | m | 0.5 | 0.1–2 |
| `cascade_length` | m | 3 | 1–10 |

Le bloc n’est pas sous pression. La perte de charge du modèle est le nombre de marches multiplié par la hauteur de marche.

## Ce qu’il rapporte

La vue de conception répète le transfert de gaz pour 1 à 8 marches : pH, CO₂, oxygène et méthane.

## Science

[Aération](../../explanation/aeration.md).
