---
lang: fr
title: Distribution
type: reference
audience: everyone
status: draft
---

# Distribution

Nom dans la bibliothèque : **Distribution**. L’exutoire du flux produit. L’eau livrée du scénario est le débit produit qui entre dans ce bloc. La démo le nomme souvent **Distribution**.

## Quand le placer

Tout scénario qui doit être résolu en a besoin d’un. Sans lui, le bilan de quantité n’a pas de distribution.

## Flux

Entrée : produit. Rien ne sort.

## Entrées

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `integrated_booster` | — | true | |
| `inlet_elevation` | m | 0 | −10–100 |
| `required_pressure` | mH₂O | 35 | 10–100 |

L’énergie de distribution sur le panneau de résultats est la part qui appartient à ce bloc, surpresseur compris lorsqu’il est activé. Le rendement du surpresseur est l’indicateur `booster_efficiency` (valeur par défaut 75 %).
