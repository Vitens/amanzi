---
lang: fr
title: Aération en tour
type: reference
audience: everyone
status: draft
---

# Aération en tour

Nom dans la bibliothèque : **Aération en tour**. Colonne à garnissage avec un surpresseur.

## Quand le placer

Le méthane ou un autre gaz volatil doit être extrait par stripage, et une cascade ne suffit pas.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `pressure_loss_nozzles` | mH₂O | 1 | 0.01–10 |
| `fall_height` | m | 1 | 0.1–10 |
| `diameter` | m | 1 | 0.1–10 |
| `bed_height` | m | 2 | 0.1–10 |
| `packingmaterial` | — | Raflux50 | Raflux25, Raflux50, Raflux90 |
| `blowereficiency` | fraction | 0.75 | 0.01–1 |
| `rq` | — | 50 | 0.01–100 |
| `ambient_temperature` | °C | 20 | −30–40 |
| `air_system_pressure_loss` | Pa | 25 | 0–2000 |

Gestion des gaz sur l’effluent gazeux, à partir des champs partagés de traitement des gaz : torchère (activée par défaut), production d’électricité (activée par défaut), rendement du générateur 0.35 (0.1–0.6, fraction), disponibilité du générateur 0.9 (0.1–1, fraction). Les champs du générateur s’appliquent lorsque la production d’électricité est activée.

## Ce qu’il rapporte

Élimination par composé, perte de charge du garnissage, facteur d’engorgement et puissance du surpresseur. La vue de conception trace le point de fonctionnement par rapport à la ligne d’engorgement.

## Science

[Aération](../../explanation/aeration.md).
