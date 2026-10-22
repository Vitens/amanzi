---
lang: de
title: Wiederverwendung von Spülwasser
type: reference
audience: everyone
status: outline
---

# Wiederverwendung von Spülwasser

Bibliotheksname: **Wiederverwendung von Spülwasser**. Rückführung / Aufteilung, die eine Schleife stromaufwärts schließen kann.

## Wann platzieren

Sie führen Spülung oder einen Nebenstrom zu einer früheren Einheit zurück.

## Ströme

- Teilen-Stil: eingehender Durchfluss aufgeteilt Richtung Produkt/Rückführung gemäß dem Block.
- Qualität wird durchgereicht (keine Aufbereitung).

## Eingaben (UI-Gruppen)

- Aufteilungsanteile / Rückführungs-Entwurfsfelder wie im Formular.

## Ausgaben / Entwurfstabellen

- Durchflüsse auf jedem Zweig.
- Energie, wenn Pumpen enthalten sind.
- Hinweis: die Rückführungs-Massen-Hilfsfunktion liefert leer zurück, damit der Mengensolver konvergieren kann (Fakt für Schlüsselanwender, die diese Seite füllen).

## Wissenschaft

[Wie Amanzi berechnet](../../explanation/how-amanzi-calculates.md) (Rückführungsiteration).
