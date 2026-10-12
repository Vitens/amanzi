---
lang: nl
title: Aktiefkool
type: reference
audience: everyone
status: outline
---

# Aktiefkool

Bibliotheeknaam: **Aktiefkool**. GAC-contactors voor PFAS en organische microverontreinigingen (TOC, kleur), inclusief vervanging en staggered bedrijf in **ontwerpweergave**.

## Wanneer plaatsen

Je dimensionneert of vergelijkt GAC voor PFAS- of organische-microverontreinigingverwijdering.

## Stromen

- In: productstroom.
- Uit: productstroom; spoeling als filtratie-/spoelankers worden gebruikt.

## Invoer (UI-groepen)

- **Filtergeometrie:** rechthoekig/rond, lengte/breedte of diameter, bedhoogte.
- **Kool:** pakkingtype (NORIT-Supra-opties), schijnbare dichtheid, deeltjesdiameter, porositeit (schoon/verstopt).
- **PFAS / microverontreinigingen:** Freundlich *K* en *1/n* per stof, competitiecoëfficiënten, PEQ, ontwerplimiet, massatransfercoëfficiënt, verwijdering % uit metadata.
- **Vervanging / staggered:** interval en aantal filters in rotatie.
- Optionele Sproeibeluchting-velden indien ingeschakeld.

## Uitvoer / ontwerptabellen

- Doorbraakcurven, regeneratie-interval (dagen of BV), EBCT, influent/effluent OMV, competitiecoëfficiënten.
- Energie / chemicaliën / sustainability voor koolvervanging.

## Beperking

Plantbrede `run_quality` past momenteel geen PFAS-verwijdering toe; gebruik ontwerpweergave. Zie [Beperkingen](../limitations.md).

## Wetenschap

[Aktiefkool en PFAS](../../explanation/activated-carbon-and-pfas.md).
