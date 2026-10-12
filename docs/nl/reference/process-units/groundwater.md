---
lang: nl
title: Winning
type: reference
audience: everyone
status: outline
---

# Winning

Bibliotheeknaam: **Winning**. Rekentype: `groundwater`. De bron van ruwwater en de samenstelling ervan.

## Wanneer plaatsen

Je hebt een startpunt voor de installatie nodig: putten, debiet en de analyse van het grondwater.

## Stromen

- Uit: productstroom (ruwwater de trein in).
- Emitter: definieert de initiële PHREEQC-oplossing voor downstream-units.

## Invoer (UI-groepen)

- **Algemeen:** jaarproductie (Mm³), min/nominale/max-capaciteit (m³/h).
- **Putontwerp:** aantal putten, gemiddelde putcapaciteit, hoogte, grondwaterstand, verlaging, kleine verliezen.
- **Samenstelling:** pH, temperatuur; opgeloste gassen (O₂, N₂, CH₄, H₂S); kationen/anionen (Fe, Mn, NH₄, Ca, Mg, Na, Cl, HCO₃, NO₃, …) in mg/L.
- **Microverontreinigingen:** PFAS-, VOC-, Overig-concentraties (zie [Werken met microverontreinigingen](../../how-to/work-with-micropollutants.md)).

## Uitvoer / ontwerptabellen

- Geïnstalleerde capaciteit en productie.
- Hydraulisch: drukhoogte bij put, bij behandeling, benodigde pompdrukhoogte, totale headloss.
- Ontwerpcontroles: ladingsbalans, zuurstofvraag, SI(Calcite), sc20.
- Energie van putpompen.

## Wetenschap

[Waterkwaliteit lezen](../../explanation/reading-water-quality.md), [Hoe Amanzi rekent](../../explanation/how-amanzi-calculates.md).
