---
lang: fr
title: Unités de procédé
type: reference
audience: everyone
status: draft
---

# Unités de procédé

Une page par bloc de la bibliothèque publique. La science est dans [Explications](../../explanation/index.md). Les couleurs des flux sont dans [Flux](../streams.md).

La plupart des blocs acceptent aussi les champs de conception partagés de `model.yml` :

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `units` | — | 1 | 1–40 |
| `minimal_capacity` | m³/h | 50 | 1–10000 |
| `nominal_capacity` | m³/h | 100 | à partir du minimum |
| `maximal_capacity` | m³/h | 150 | à partir du nominal |
| `inlet_elevation` | m | 5 | 0–25 |
| `influent_pressure_loss` | mH₂O | 0 | 0–10 |
| `pressurized` | — | false | |

Une page ci-dessous ne nomme un champ que lorsque ce bloc remplace la valeur par défaut partagée ou ajoute le sien. Des lignes d’électricité et de CO₂ chimique sont ajoutées pour chaque bloc qui déclare une consommation. Voir [Indicateurs](../key-figures.md).

Lorsqu’une étiquette d’unité indique `%` et que la plage est comprise entre 0 et 1, la valeur est une fraction. Voir [Unités de mesure](../units.md).

## Sources et stockage

- [Captage](groundwater.md)
- [Réservoir](reservoir.md)

## Aération et gaz

- [Aération en tour](toweraeration.md)
- [Aération par aspersion](sprayaerator.md) — masquée en tant que bloc distinct ; les champs sont sur les filtres
- [Aération à plateaux](plate.md)
- [Cascade](cascade.md)
- [Dégazage membranaire](membranedegassing.md)
- [Dégazage sous vide](vacuum.md)

## Filtration

- [Filtration sur sable](sandfiltration.md)
- [Filtration sur marbre](marblefiltration.md)

## Produits chimiques et membranes

- [Adoucissement sur pellets](softening.md)
- [Dosage](dosing.md)
- [Filtration membranaire](membrane.md)

## Transport et exutoires

- [Dessableur](sandtrap.md)
- [Conduite de transport](pipeline.md)
- [Répartition](splitter.md)
- [Réutilisation des eaux de lavage](recycle.md)
- [Distribution](output.md)
- [Flux de rejet](waste.md)

L’échange d’ions est omis. Le charbon actif n’est pas dans l’application publique. Les deux figurent dans [Limites](../limitations.md).
