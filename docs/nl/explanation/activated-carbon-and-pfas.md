---
lang: nl
title: Aktiefkool en PFAS
type: explanation
audience: keyuser
status: outline
---

# Aktiefkool en PFAS

GAC zoals geïmplementeerd in Amanzi: competitieve isothermen, vereenvoudigde doorbraak, staggered vervanging, wettelijke sommen, en de kloof ontwerp-vs-runtime.

## Inhoud om te schrijven

- PFAS leven in de **extraneous**-stroom (ng/L), niet in PHREEQC.
- **SRS (Sheindorf–Rebhun–Sheintuch)** competitieve Freundlich; *K* in `(µg/g)·(L/µg)^(1/n)`, exponent **1/n**.
- DOC-competitie via TOC → DOC; competitiecoëfficiënten.
- Vereenvoudigde doorbraak (stationaire stroming, geen dispersie): *C/C₀ = 1 / (1 + exp(k · EBCT · (1 − BV · C_in / q)))*.
- PEQ-gewogen Sum4 / Sum20 vs kengetallimieten.
- Staggered vervanging: piekconcentraties vóór vervanging mengen over filters.
- Isothermendatabase: 21 stoffen, originele vs Amanzi-omgezette kolommen; eenheidsconversieregels (Polanyi, EPA WQTC, Cantoni, Chen, Hückstädt, Langmuir).
- Standaarden in parametrisch PFAS-YAML (Polanyi-voorspeld) vs literatuurrijen.
- **Kloof:** `design()` draait deze fysica; `run_quality()` past geen PFAS-verwijdering toe (alleen optionele sproei).
- Microverontreiniging %-verwijdering uit scenariometadata voor OMV-achtige organics.

## Diagrammen

- Mermaid: influent-PFAS → SRS-capaciteit → doorbraak → staggered blend → ontwerptabellen (niet plantwandeling).
