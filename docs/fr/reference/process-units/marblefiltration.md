---
lang: fr
title: Filtration sur marbre
type: reference
audience: everyone
status: draft
---

# Filtration sur marbre

Nom dans la bibliothèque : **Filtration sur marbre**. La séquence d’oxydation du filtre à sable, avec saturation de la calcite après chaque oxydation, sur un lit de marbre. Une couche de chaux optionnelle peut s’y ajouter.

## Quand le placer

Le filtre doit tamponner le pH tout en oxydant le fer, le manganèse et l’ammonium.

## Flux

Entrée : produit. Sortie : produit. Entrée : lavage. Sortie : rejet.

## Lit

`spray` et `lime_pellets` valent tous les deux false par défaut. La forme est rectangulaire ou circulaire, avec les mêmes valeurs par défaut de longueur, de largeur et de diamètre que la filtration sur sable.

| Champ | Unité | Valeur par défaut | Plage | Quand |
|---|---|---|---|---|
| `height_lime` | m | 0.5 | 0.1–10 | Granulés de chaux activés |
| `diameter_lime` | mm | 1 | 0.0001–100 | Granulés de chaux activés |
| `porosity_lime` | — | 0.5 | 0.1–0.6 | Granulés de chaux activés |
| `porosity_lime_clogged` | — | 0.25 | 0.1–0.6 | Granulés de chaux activés |
| `height_marble` | m | 1 | 0.1–10 | |
| `diameter_marble` | mm | 1 | 0.0001–100 | |
| `porosity_marble` | — | 0.5 | 0.1–0.6 | |
| `porosity_marble_clogged` | — | 0.25 | 0.1–0.6 | |

La hauteur de chute, le fond du filtre, le surnageant et le lavage correspondent au filtre à sable, sauf la durée de marche, plafonnée à 72 h au lieu de 500 h. Les champs d’aspersion correspondent à [Aération par aspersion](sprayaerator.md).

## Élimination

Les trois mêmes interrupteurs de suppression que pour la filtration sur sable. Les efficacités sont des fractions, valeur par défaut 1, et elles n’apparaissent que lorsque l’interrupteur de suppression correspondant est activé.

## Ce qu’il rapporte

La vue de conception liste les mêmes étapes d’oxydation que le filtre à sable. Chaque oxydation sature aussi la calcite. Le fer de lavage est calculé de la même façon, et cette eau de rejet est elle aussi saturée vis-à-vis de la calcite.

## Science

[Filtration](../../explanation/filtration.md).
