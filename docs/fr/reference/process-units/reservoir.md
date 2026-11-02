---
lang: fr
title: Réservoir
type: reference
audience: everyone
status: draft
---

# Réservoir

Nom dans la bibliothèque : **Réservoir**. Un volume de stockage sur la ligne produit, avec un échange de gaz optionnel.

## Quand le placer

La filière a besoin d’un volume d’eau claire entre le traitement et la livraison.

## Flux

Entrée : produit. Sortie : produit. Sortie : lavage, et cet ancrage est optionnel.

## Entrées

Le nombre d’unités partagé est repris ici (valeur par défaut 1, plage 1–40). La forme est `rectangular` ou `cylindrical`.

| Champ | Unité | Valeur par défaut | Quand |
|---|---|---|---|
| `reservoir_width` | m | 10 | Rectangulaire. Plage 1–100 |
| `reservoir_length` | m | 20 | Rectangulaire. Plage 1–100 |
| `reservoir_diameter` | m | 10 | Cylindrique. Plage 1–50 |
| `reservoir_height` | m | 5 | Plage 1–20 |
| `inlet_elevation` | m | 2 | Plage 0–80. Remplace la valeur par défaut partagée |
| `influent_pressure_loss` | mH₂O | 0 | Plage 0–10 |
| `mean_water_level` | m | 3 | Jusqu’à la hauteur du réservoir |
| `integrated_aeration` | — | false | |
| `co2_removal` | fraction | 0.5 | Seulement si l’aération est activée. Plage 0–1 |
| `o2_saturation` | fraction | 0.8 | Seulement si l’aération est activée. Plage 0–1 |

## Science

[Aération](../../explanation/aeration.md) pour l’échange de gaz optionnel. Le réservoir lui-même est un stockage, pas une réaction de traitement.
