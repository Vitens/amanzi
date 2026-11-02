---
lang: fr
title: Aération par aspersion
type: reference
audience: everyone
status: draft
---

# Aération par aspersion

Nom dans la bibliothèque : **Aération par aspersion**. Le bloc est masqué. Il n’est pas dans la bibliothèque. Les mêmes champs apparaissent sur la [filtration sur sable](sandfiltration.md) et la [filtration sur marbre](marblefiltration.md) lorsque `spray` est activé.

## Entrées

Tous s’appliquent seulement lorsque l’aspersion est activée.

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `area_per_nozzle` | m² | 1 | 0.1–10 |
| `co2_removal_efficiency` | fraction | 0.50 | 0.01–1 |
| `ch4_removal_efficiency` | fraction | 0.30 | 0.01–1 |
| `o2_saturation` | fraction | 0.80 | 0.01–1 |

La perte de charge des buses et la hauteur de chute jusqu’au média sont sur le filtre, pas sur ce bloc masqué. La hauteur de chute jusqu’au média vaut 0.5 m par défaut (0.1–2).

## Science

[Aération](../../explanation/aeration.md). Le calcul qui s’exécute est le polynôme de hauteur de chute, pas un diamètre de Sauter.
