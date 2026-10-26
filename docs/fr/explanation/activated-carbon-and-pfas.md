---
lang: fr
title: Charbon actif et PFAS
type: explanation
audience: keyuser
status: outline
---

# Charbon actif et PFAS

Le charbon actif en grains (GAC) tel qu'il est implémenté dans Amanzi : isothermes compétitives, percée simplifiée, échelonnement, sommes réglementaires, et l'écart entre la conception et l'exécution.

## Contenu à rédiger

- Les PFAS vivent dans le flux **extraneous** (ng/L), pas dans PHREEQC.
- **SRS (Sheindorf–Rebhun–Sheintuch)**, Freundlich compétitive ; *K* en `(µg/g)·(L/µg)^(1/n)`, exposant **1/n**.
- Compétition du DOC via TOC → DOC ; coefficients de compétition.
- Percée simplifiée (écoulement stationnaire, sans dispersion) : *C/C₀ = 1 / (1 + exp(k · EBCT · (1 − BV · C_in / q)))*.
- Sum4 / Sum20 pondérées par le PEQ, face aux limites des indicateurs.
- Remplacement échelonné : mélange, d'un filtre à l'autre, des concentrations de pointe d'avant remplacement.
- Base d'isothermes : 21 composés, colonnes d'origine et colonnes converties par Amanzi ; règles de conversion d'unités (Polanyi, EPA WQTC, Cantoni, Chen, Hückstädt, Langmuir).
- Valeurs par défaut dans le YAML paramétrique des PFAS (prédites selon Polanyi) et lignes de la littérature.
- **Écart :** `design()` exécute cette physique ; `run_quality()` n'applique pas d'élimination des PFAS (aspersion optionnelle seulement).
- Pourcentage d'élimination des micropolluants, tiré des métadonnées du scénario, pour les organiques de type OMV.

## Diagrammes

- Mermaid : PFAS à l'entrée → capacité SRS → percée → mélange de l'échelonnement → tableaux de conception (pas le parcours de l'usine).
