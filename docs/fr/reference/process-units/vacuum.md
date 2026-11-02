---
lang: fr
title: Dégazage sous vide
type: reference
audience: everyone
status: draft
---

# Dégazage sous vide

Nom dans la bibliothèque : **Dégazage sous vide**. Une cuve sous vide. La phase gazeuse comprend le sulfure d’hydrogène sous la forme `H2Sg`.

## Quand le placer

Le méthane ou le sulfure d’hydrogène doit être extrait en abaissant la pression, plutôt qu’en soufflant de l’air à travers une tour.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `diameter` | m | 2 | 0.1–10 |
| `spray_height` | m | 1 | 0–5 |
| `bed_height` | m | 3 | 0–10 |
| `pressure_loss_nozzles` | mH₂O | 2 | 0.01–10 |
| `vacuum_pump` | — | liquid_ring | liquid_ring, screw |
| `vacuum_pressure` | bara | 0.2 | 0.05–0.5 |

Les mêmes commutateurs de traitement des gaz que pour la tour (torchère, production d’électricité, rendement et disponibilité du générateur) s’appliquent à l’effluent gazeux.

## Ce qu’il rapporte

La vue de conception balaie le vide et trace le pH, l’indice de saturation et les gaz.

## Science

[Membranes](../../explanation/membranes.md).
