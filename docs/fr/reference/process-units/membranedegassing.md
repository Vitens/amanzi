---
lang: fr
title: Dégazage membranaire
type: reference
audience: everyone
status: draft
---

# Dégazage membranaire

Nom dans la bibliothèque : **Dégazage membranaire**. Un ou deux contacteurs sous vide avec un balayage d’azote et de CO₂.

## Quand le placer

Les gaz doivent sortir sans qu’un aérateur ouvert charge l’eau en oxygène.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `num_stages` | — | double | single, double |
| `membranes_per_stage` | — | 4 | 1–10 |
| `membrane_type` | — | EXF14x40 | EXF14x40, EXF14x28 |
| `vacuum_type` | — | liquid-ring | liquid-ring, screw |
| `nitrogen_source` | — | cryogenic | cryogenic, PSA |
| `nitrogen_purity` | — | 4 | 4 ou 5 |
| `pressure_loss_cartridge_filter` | mH₂O | 2 | 0.01–20 |
| `n2_rq_stage_1` | Nm³/m³ | 0 | 0–1 |
| `co2_rq_stage_1` | Nm³/m³ | 0.02 | 0–1 |
| `vacuum_stage_1` | bara | 0.10 | 0.01–1 |
| Balayage et vide de l’étage 2 | mêmes unités | 0, 0, 0.10 | Affiché lorsque le contacteur est double |
| `vent_flare` | — | false | Lorsque le trajet d’évent s’applique |

La puissance PSA utilise les indicateurs `psa_purity_4_power_consumption` (0.61 kWh/Nm³) et `psa_purity_5_power_consumption` (0.82 kWh/Nm³), correspondant aux puretés 4 et 5.

## Science

[Membranes](../../explanation/membranes.md).
