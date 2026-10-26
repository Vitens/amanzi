---
lang: fr
title: Captage
type: reference
audience: everyone
status: draft
---

# Captage

Nom dans la bibliothèque : **Captage**. Type de calcul : `groundwater`. La source de l’eau brute et de l’analyse dont part le reste de la filière.

## Quand le placer

Le scénario a besoin d’un champ captant : volume annuel, hydraulique des puits et analyse de l’eau souterraine.

## Flux

Sortie : produit. Cet ancrage est l’émetteur. Il construit la solution PHREEQC initiale.

## Puits et production

Ce bloc n’utilise pas les valeurs de capacité par défaut partagées. Les siennes sont :

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `yearly_production` | Mm³ | 10 | 0–100 |
| `minimal_capacity` | m³/h | 500 | 1–10000 |
| `nominal_capacity` | m³/h | 1000 | 1–10000 |
| `maximal_capacity` | m³/h | 1500 | 1–10000 |
| `number_of_wells` | — | 4 | 1–40 |
| `average_well_capacity` | m³/h | 100 | 1–500 |
| `average_elevation` | m | 0 | −10–50 |
| `average_groundwater_level` | m | −1 | −10–20 |
| `average_drawdown` | m | 3 | 0.1–10 |
| `minor_losses` | mH₂O | 1 | 0–3 |

La conduite de transport sur le même bloc : diamètre intérieur 450 mm (100–2500), longueur 1000 m (100–50000), matériau PE, PVC ou Steel.

## Composition

| Groupe | Champs | Unité | Notes |
|---|---|---|---|
| Communs | pH, température | —, °C | Valeurs par défaut 7 et 10 °C |
| Gaz dissous | oxygène, azote, méthane, sulfure d’hydrogène | mg/l | Valeurs par défaut 0, 15, 1, 0 |
| Cations | fer, manganèse, ammonium, calcium, magnésium, sodium, potassium, baryum, strontium | mg/l | Le fer vaut 5 par défaut, le calcium 60 |
| Anions | bicarbonate, chlorure, nitrite, nitrate, sulfate, phosphate, fluorure, silicate, bore | mg/l | Le bicarbonate vaut 140 par défaut |
| Autres | carbone organique total, couleur | mg/l | Valeur par défaut 0 |

## Ce qu’il rapporte

Capacité installée (nombre de puits × capacité moyenne d’un puits), production, charge au puits, charge au traitement, charge de pompe requise et perte de charge de la conduite. L’énergie des pompes de puits utilise `well_efficiency`.

## Science

[Lire la qualité de l’eau](../../explanation/reading-water-quality.md).
