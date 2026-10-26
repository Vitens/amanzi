---
lang: fr
title: Filtration membranaire
type: reference
audience: everyone
status: draft
---

# Filtration membranaire

Nom dans la bibliothèque : **Filtration membranaire**. Un empilement RO ou NF. Le perméat continue. Le concentrat part en rejet.

## Quand le placer

Les solides dissous doivent être retenus. Le taux de conversion est la part de l’alimentation qui devient perméat.

## Flux

Entrée : produit. Sortie : produit (perméat). Sortie : rejet (concentrat).

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `inlet_elevation` | m | 1 | −10–12. Remplace la valeur par défaut partagée |
| `pressure_loss_cartridge_filter` | mH₂O | 2 | 0.01–20 |
| `pressure_loss_between_stages` | mH₂O | 2 | 0.01–20 |
| `membrane_type` | — | ESPA2-LD | ESPA2-LD, ESPA2-LD-MAX, ESPA4-LD, ESPA4-MAX, AK-400H, AK-440H |
| `number_of_stages` | — | 3 | 1–3 |
| `modules_per_vessel` | — | 6 | 1–10 |
| `optiflux` | — | false | Lorsqu’il est activé, les tubes de pression doublent et les modules par tube sont divisés par deux |
| `stage1_vessels` | — | 12 | 1–20 |
| `stage2_vessels` | — | 6 | 1–20. Affiché à partir de 2 étages |
| `stage3_vessels` | — | 3 | 1–20. Affiché à 3 étages |
| `recovery` | fraction | 0.8 | 0.5–0.95 |

Les capacités minimale et maximale de ce bloc sont des sentinelles masquées (−1), pas des champs que vous réglez. La capacité nominale reste le champ partagé.

## Ce qu’il rapporte

Pression d’alimentation, flux par étage, TDS du perméat et du concentrat, et sursaturation du concentrat. Le passage de sel utilise la réjection de l’élément issue de la ligne du fabricant. Kw est en m³/(m²·bar·h).

## Science

[Membranes](../../explanation/membranes.md).
