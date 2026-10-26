---
lang: fr
title: Unités de mesure
type: reference
audience: everyone
status: draft
---

# Unités de mesure

Interprétation des grandeurs qu'Amanzi enregistre. Le libellé dans le formulaire est l'unité ci-dessous, sauf lorsqu'un champ est une fraction.

| Grandeur | Unité |
|---|---|
| Capacité, débit de conduite | m³/h |
| Production annuelle | Mm³ (le panneau Quantité affiche Mm³/y) |
| Charge, altitude, hauteur de lit | m |
| Perte de charge | mH₂O. Une pression d'étage membranaire en bar est la charge divisée par 9.81 là où la chaîne de calcul effectue cette conversion |
| Température | °C. Le champ de température ambiante de la tour est enregistré comme `C` |
| Ions et gaz dissous sur le Captage | mg/l |
| pH, indice de saturation | — |
| Dose constante, dose de base des pellets et dose d'acide | mmol/L |
| Masse de réactif | g AS/m³, et g AS/mol pour la masse de formule |
| Intensité énergétique | kWh/m³ |
| Énergie annuelle sur le panneau | MWh/y |
| Facteur du réseau | gCO₂/kWh |
| Facteur d'émission chimique | gCO₂/g AS |
| Facteur méthane | gCO₂/gCH₄ |
| CO₂ spécifique | gCO₂-eq/m³ |
| CO₂ annuel sur le panneau | ton CO₂-eq/y |
| Rapport d'air RQ sur une tour ou un plateau | — (m³ d'air par m³ d'eau) |
| Gaz de balayage sur un contacteur membranaire | Nm³/m³ |
| Vide | bara |
| Pression de soufflante | Pa |
| Perméabilité membranaire Kw | m³/(m²·bar·h) |
| Conductivité EGV | mS/m |
| Dureté | mmol/l |

## Fractions étiquetées %

Plusieurs champs utilisent le libellé d'unité `%` et une plage qui va de 0 à 1. Le nombre enregistré est une fraction. 0.8 correspond à 80 %. Cela s'applique à la fraction de répartition, au rendement de recyclage, au taux de conversion membranaire, à l'ouverture de la dérivation, aux rendements d'élimination, aux rendements d'aspersion, aux rendements d'aération du réservoir, aux rendements de soufflante et de ventilateur enregistrés sur une échelle 0–1, et à la capture du fer et du manganèse sur le réacteur à pellets.

Les rendements des puits et des pompes de surpression dans les indicateurs sont différents : ces valeurs par défaut sont 55 et 75, et le solveur hydraulique les divise par 100.
