---
lang: fr
title: Résultats
type: reference
audience: everyone
status: draft
---

# Résultats

Le panneau de droite est le scénario ouvert, après la dernière résolution réussie. **Calculer le projet** ouvre le rapport de ce scénario. **Comparaison** dans le rapport dessine chaque scénario. La quantité n'apparaît dans le rapport que dans cette comparaison. Les titres de la comparaison restent en néerlandais : **Kwantiteit**, **Waterkwaliteit**, **Energie**, **Duurzaamheid**.

Un scénario non résolu ou déconnecté laisse le panneau sans résultat à jour. Le message en cas de connexion manquante est décrit dans [Flux](streams.md) et [Limites](limitations.md).

## Quantité

| Ligne | Signification | Unité |
|---|---|---|
| Captage | Débit produit sortant des unités sans rien en amont | Mm³/y |
| Distribution | Débit produit entrant dans les unités sans rien en aval | Mm³/y |
| Pertes | Captage moins distribution, également en pourcentage | Mm³/y et % |

## Qualité

L'eau en sortie d'usine. Libellés sur le panneau : pH, EGV, O₂, HCO₃, TAC, Dureté, TDS, TACC₉₀, AggCO₂, SI, Fe, Mn, NH₄, Na et Cl. Les concentrations sont en mg/l, sauf la dureté (mmol/l), l'EGV (mS/m) et les indices, qui n'ont pas d'unité. La signification de ces mots est dans [Lire la qualité de l'eau](../explanation/reading-water-quality.md).

## Énergie

| Ligne | Signification | Unité sur le panneau |
|---|---|---|
| Traitement | Consommation spécifique des unités de traitement | kWh/m³ |
| Distribution | Consommation spécifique de la sortie | kWh/m³ |
| Total | Ces deux ensemble, et la somme annuelle | kWh/m³ et MWh/y |

## Durabilité

| Ligne | Signification | Unité sur le panneau |
|---|---|---|
| Émissions spécifiques | Équivalent CO₂ par mètre cube délivré | gCO₂-eq/m³ |
| Émissions totales | Le même décompte sur l'année | ton CO₂-eq/y |

## Réactifs

Il n'y a pas de rubrique réactifs sur le panneau. Les masses de réactifs sont en g AS/m³ sur l'unité qui les dose, et elles entrent dans la durabilité par les facteurs des indicateurs. Voir [Quantité, énergie, réactifs, CO₂](../explanation/quantity-energy-chemicals-co2.md).
