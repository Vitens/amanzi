---
lang: fr
title: Dosage
type: reference
audience: everyone
status: draft
---

# Dosage

Nom dans la bibliothèque : **Dosage**. Un seul produit chimique, soit une dose fixe, soit une recherche vers une cible.

## Quand le placer

L’eau a besoin d’un acide, d’une base, de CO₂, d’oxygène ou d’un sel métallique, et un réacteur à pellets n’est pas le bon bloc.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Valeur par défaut | Choix ou plage |
|---|---|---|
| `position` | influent | influent, effluent |
| `chemical` | co2 | co2, hcl, h2so4, lye, lime, calcite, oxygen, iron_chloride, manganese_chloride |
| `mode` | constant | constant, setpoint |
| `dosage` | 0.2 mmol/L | 0–5. Affiché en mode constant |
| `setpoint_parameter` | pH | pH, SI, AggCO2, CCPP90. Affiché en mode setpoint |
| `setpoint` | 7 | 0–14. Affiché en mode setpoint |

La dose constante est acceptée lorsque la touche Entrée est pressée. En mode setpoint, la recherche reste dans 0–5 mmol/L. En cas d’échec, la dose reste à 0 et l’unité émet un avertissement.

## Ce qu’il rapporte

Formule, masse formulaire (g AS/mol), dose (mmol/L) et dose massique (g AS/m³). La vue de conception trace le pH, l’oxygène, le CO₂ agressif, SI et TACC₉₀ en fonction de la dose, de 0 à 2 mmol/L.

## Science

[Adoucissement et dosage](../../explanation/softening-and-dosing.md).
