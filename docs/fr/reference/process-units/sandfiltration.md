---
lang: fr
title: Filtration sur sable
type: reference
audience: everyone
status: draft
---

# Filtration sur sable

Nom dans la bibliothèque : **Filtration sur sable**. Filtre rapide. Double média optionnel, aspersion optionnelle, puis la séquence d’oxydation.

## Quand le placer

Le fer, le manganèse, l’ammonium, le méthane ou le sulfure d’hydrogène doivent être éliminés sur un lit de sable, avec ou sans couche d’anthracite.

## Flux

Entrée : produit. Sortie : produit. Entrée : lavage. Sortie : rejet.

## Lit

`dual_media` vaut false par défaut. Les champs anthracite n’apparaissent que lorsqu’il est activé.

| Champ | Unité | Valeur par défaut | Plage |
|---|---|---|---|
| `height_anthracite` | m | 0.5 | 0.1–2 |
| `diameter_anthracite` | mm | 1.3 | 0.1–3 |
| `porosity_anthracite` | — | 0.45 | 0.1–0.6 |
| `porosity_anthracite_clogged` | — | 0.25 | 0.1–0.6 |
| `height_sand` | m | 1.0 | 0.5–3 |
| `diameter_sand` | mm | 1.3 | 0.1–3 |
| `porosity_sand` | — | 0.45 | 0.1–0.6 |
| `porosity_sand_clogged` | — | 0.25 | 0.1–0.6 |

## Géométrie du filtre et lavage

Repris des champs de filtration partagés. `spray` vaut false par défaut. La forme est rectangulaire (longueur 10 m, largeur 2.5 m) ou circulaire (diamètre 3 m). La hauteur de chute jusqu’au média est de 0.5 m (0.1–2). Le fond du filtre est de 0.5 m (0.1–1). Le niveau de surnageant est de 0.2 m, jusqu’à la hauteur de chute.

Rendement de la pompe de lavage 0.6 (0.4–0.8, fraction). Charge de lavage 5 mH₂O (1–10). La commande est `time` (durée de marche 24 h, plage 1–500) ou `volume` (volume de marche 5000 m³, plage 10–100000).

La surface de buse d’aspersion et les trois efficacités gazeuses sont dans [Aération par aspersion](sprayaerator.md). La perte de charge des buses est de 1 mH₂O lorsque l’aspersion est activée.

## Élimination

Le fer, l’ammonium et le manganèse ont chacun un interrupteur de suppression, désactivé par défaut. Lorsqu’un interrupteur est activé, l’efficacité d’élimination correspondante est une fraction, valeur par défaut 1, plage 0–1. Sinon, l’élimination va aussi loin que l’oxygène le permet.

## Ce qu’il rapporte

La vue de conception liste les étapes d’oxydation. La perte de charge du lit propre est Kozeny–Carman. La perte de charge de lavage et l’expansion utilisent une viscosité à 15 °C. Le flux de rejet reçoit le fer capté.

## Science

[Filtration](../../explanation/filtration.md).
