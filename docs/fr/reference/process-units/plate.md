---
lang: fr
title: Aération à plateaux
type: reference
audience: everyone
status: draft
---

# Aération à plateaux

Nom dans la bibliothèque : **Aération à plateaux**. Un plateau perforé avec un ventilateur d’alimentation et un effluent gazeux recirculé en option.

## Quand le placer

La filière a besoin d’un premier contact avec l’air. La démo utilise ce bloc sous le nom **Aération à plateaux**.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `type` | — | Metal | Metal, Foil |
| `length` | m | 1 | 0.1–10 |
| `width` | m | 1 | 0.1–10 |
| `hole_diameter` | mm | 1.5 | 0.5–3 |
| `recirculation` | fraction | 0 | 0–0.8 |
| `RQ` | — | 50 | 0–100 |
| `contact_time` | s | 10 | 1–100 |
| ΔP des ventilateurs d’alimentation, d’extraction et de recirculation | Pa | 100 chacun | 10–2000 |
| Rendements de ces trois ventilateurs | fraction | 0.75 chacun | 0.5–1 |
| `efficiency` | — | 0.02 | 0.01–1 |

## Science

[Aération](../../explanation/aeration.md).
