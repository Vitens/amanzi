---
lang: fr
title: Dessableur
type: reference
audience: everyone
status: draft
---

# Dessableur

Nom dans la bibliothèque : **Dessableur**. Un canal de décantation sur la ligne de rejet.

## Quand le placer

Un flux de rejet transporte des grains qui doivent se déposer avant que l’eau ne poursuive.

## Flux

Entrée : rejet. Sortie : rejet. Il ne se place pas sur la filière produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `nominal_capacity` | m³/h | 1000 | 10–5000 |
| `length` | m | 5 | 1–20 |
| `width` | m | 2 | 0.1–10 |
| `height_at_inlet` | m | 1 | 0.1–10 |
| `height_at_outlet` | m | 1.5 | 0.1–10 |
| `temperature` | °C | 10 | 0–40 |
| `particle_material` | — | quartz-sand | quartz-sand, anthracite, hydro-anthracite, garnet, pellets, basalt, marble, gravel, other |
| `other_particle_density` | kg/m³ | 2650 | 1000–5000, lorsque le matériau est other |
| `particle_size` | mm | 0.8 | 0.1–5 |

La viscosité de ce bloc cite le recueil de données de Viswanath et Natarajan. La citation est dans [Littérature](../../explanation/literature.md).
