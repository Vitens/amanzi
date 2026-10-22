---
lang: de
title: Gewinnen
type: reference
audience: everyone
status: outline
---

# Gewinnen

Bibliotheksname: **Gewinnen**. Berechnungstyp: `groundwater`. Die Quelle des Rohwassers und seiner Zusammensetzung.

## Wann platzieren

Sie brauchen einen Startpunkt für die Anlage: Brunnen, Durchfluss und die Analyse des Grundwassers.

## Ströme

- Aus: Produkt (Rohwasser in die Strecke).
- Emitter: definiert die anfängliche PHREEQC-Lösung für stromabwärtige Einheiten.

## Eingaben (UI-Gruppen)

- **Allgemein:** Jahresproduktion (Mm³), min/nominal/max Kapazität (m³/h).
- **Brunnenentwurf:** Anzahl Brunnen, mittlere Brunnenkapazität, Höhe, Grundwasserstand, Absenkung, Nebenverluste.
- **Zusammensetzung:** pH, Temperatur; gelöste Gase (O₂, N₂, CH₄, H₂S); Kationen/Anionen (Fe, Mn, NH₄, Ca, Mg, Na, Cl, HCO₃, NO₃, …) in mg/L.
- **Mikroschadstoffe:** PFAS-, VOC-, Sonstige-Konzentrationen (siehe [Mit Mikroschadstoffen arbeiten](../../how-to/work-with-micropollutants.md)).

## Ausgaben / Entwurfstabellen

- Installierte Kapazität und Produktion.
- Hydraulik: Druckhöhe am Brunnen, Druckhöhe an der Aufbereitung, erforderliche Pumpendruckhöhe, gesamter Druckverlust.
- Entwurfskontrollen: Ladungsbilanz, Sauerstoffbedarf, SI(Calcite), sc20.
- Energie der Brunnenpumpen.

## Wissenschaft

[Wasserqualität lesen](../../explanation/reading-water-quality.md), [Wie Amanzi berechnet](../../explanation/how-amanzi-calculates.md).
