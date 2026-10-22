---
lang: de
title: Ströme
type: reference
audience: everyone
status: outline
---

# Ströme

Verbindungen zwischen Prozesseinheiten. Drei Typen; jede Einheit stellt Anker bereit, die verdrahtet werden müssen, wenn sie nicht optional sind.

## Inhalt zum Schreiben

- **Produkt** (blau): aufbereitetes oder weitergeleitetes Wasser entlang der Hauptstrecke.
- **Abfall** (rot): Konzentrat, Sole oder verworfener Fluss zu einer Abfallsenke.
- **Spülung** (gepunktet blau): Rückspül- / Filterwaschwasser, oft Richtung Wiederverwendung oder Abfall.
- Erforderliche vs optionale Anker; die Meldung „not fully connected“.
- Rückführungsschleifen: Wiederverwendung/Teilen kann Wasser stromaufwärts senden; der Qualitätssolver iteriert, bis die Stoffbilanz konvergiert (nur Fakt; das Warum steht in [Wie Amanzi berechnet](../explanation/how-amanzi-calculates.md)).
- Ein Szenario ohne Quelle oder ohne Lieferung kann nicht gelöst werden.

## Diagramme

- Mermaid: Quelle → Einheit (Produkt) → Lieferung, mit Abfall- und Spül-Seitenkanten.
