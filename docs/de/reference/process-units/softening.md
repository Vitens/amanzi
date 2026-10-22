---
lang: de
title: Pelletontharding
type: reference
audience: everyone
status: outline
---

# Pelletontharding

Bibliotheksname: **Pelletontharding** (pellet softening). Kalk-/Soda-Pelletreaktor mit Bypass und optionaler Säure.

## Wann platzieren

Sie reduzieren die Härte durch Kristallisation von Calcit in einem Pelletreaktor, mit optionaler Bypass-Mischung.

## Ströme

- Ein/Aus: Produkt (Bypass ist intern).

## Eingaben (UI-Gruppen)

- **Kapazitäten:** Nominal- und Bypass-Durchfluss (m³/h).
- **Reaktor:** Trichter vs zylindrisch; Höhen und Durchmesser.
- **Chemikalien:** Base- und Säurespezies und Dosierungen; Säureeinspeisepunkt.
- **Betrieb / Modell:** `soften_to_si`, Fe/Mn-Einfangraten, Saatgutmaterial.

## Ausgaben / Entwurfstabellen

- Schrittprofile: pH, Härte, CCPP, sc.
- Dosiersweep-Diagramme.
- Chemikalienverbrauch und CO₂ aus Chemikalien.
- Fluidisierungs- / Porositäts-Hilfsfunktion.

## Wissenschaft

[Enthärtung und Dosierung](../../explanation/softening-and-dosing.md).
