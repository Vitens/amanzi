---
lang: fr
title: Adoucissement sur pellets
type: reference
audience: everyone
status: draft
---

# Adoucissement sur pellets

Nom dans la bibliothèque : **Adoucissement sur pellets**. Un réacteur à pellets de calcite avec une dérivation et un acide optionnel.

## Quand le placer

La dureté doit diminuer par dosage d’une base et précipitation de calcite, tandis qu’une partie du débit peut contourner le réacteur.

## Flux

Entrée : produit. Sortie : produit. La dérivation est une fraction à l’intérieur du bloc, pas un second ancrage.

## Réacteur et débits

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `nominal_capacity` | m³/h | 300 | 0–1000. Remplace la valeur par défaut partagée |
| `bypass_capacity` | m³/h | 100 | 0–1000 |
| `inlet_elevation` | m | 1 | −10–20 |
| `reactor_shape` | — | funnel | cylindrical, funnel |
| `height_cylindrical` | m | 5 | 1–10 |
| `diameter_cylindrical` | m | 2 | 0.1–10 |
| `height_funnel` | m | 2 | 1–10, entonnoir seulement |
| `diameter_funnel` | m | 3 | Du diamètre cylindrique jusqu’à 10, entonnoir seulement |
| `bypass_open` | fraction | 0.2 | 0–1 |
| `base_dosage` | mmol/L | 1 | 0–5 |
| `acid_dosage` | mmol/L | 0.1 | 0–5 |
| `soften_to_si` | — | 0.6 | 0–2 |
| `fe_capture` | fraction | 0.9 | 0–0.99 |
| `mn_capture` | fraction | 0.9 | 0–0.99 |

## Produits chimiques et germe

| Champ | Valeur par défaut | Choix |
|---|---|---|
| `seed_material` | quartz_sand | quartz_sand, garnet_sand, calcite |
| `base_chemical` | NaOH | NaOH, Ca(OH)2 |
| `acid_chemical` | CO2 | CO2, HCl |
| `acid_position` | reactor-outlet | reactor-outlet, bypass, after-bypass |
| `lime_type` | quicklime | quicklime, hydrated_lime, milk_of_lime, lorsque la base est de la chaux |

Lit de pellets : hauteur statique 3 m (0.1–10), porosité statique 0.4 (0.1–0.9), diamètre de germe 0.1 mm, diamètre de pellet 0.5 mm. Chaque diamètre reste du côté valide de l’autre.

## Ce qu’il rapporte

La vue de conception balaie la dose de base et trace le pH, la dureté, HCO₃ et la conductivité. Le résultat d’usine est le mélange du réacteur et de la dérivation.

## Science

[Adoucissement et dosage](../../explanation/softening-and-dosing.md).
