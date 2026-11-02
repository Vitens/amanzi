---
lang: fr
title: Conduite de transport
type: reference
audience: everyone
status: draft
---

# Conduite de transport

Nom dans la bibliothèque : **Conduite de transport**. Une conduite sur la ligne produit. La perte de charge est le frottement de Darcy. Elle ne modifie pas la chimie de l’eau.

## Flux

Entrée : produit. Sortie : produit.

## Entrées

| Champ | Unité | Valeur par défaut | Plage ou choix |
|---|---|---|---|
| `pipe_inner_diameter` | mm | 450 | 100–2500 |
| `pipe_length` | m | 1000 | 100–50000 |
| `pipe_material` | — | PE | PE, PVC, Steel |

La rugosité utilisée dans le facteur de frottement est de 0.003 mm pour le PE, 0.0015 mm pour le PVC et 0.045 mm pour l’acier. La viscosité cinématique dans ce calcul est la constante 1.308 mm²/s. Le résultat de perte de charge comporte un contrôle : la perte par mètre reste inférieure à 0.005.

Le captage a sa propre copie de ces champs de conduite. Ce bloc est celui que vous placez entre les autres unités.
