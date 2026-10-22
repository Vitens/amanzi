---
lang: de
title: Membranen
type: explanation
audience: keyuser
status: outline
---

# Membranen

RO/NF-Stacks, Membrankontaktoren und Vakuum-Entgasung.

## Inhalt zum Schreiben

- **RO/NF:** Recovery-Aufteilung; Permeat vs Konzentrat (Abfall); *Kw* aus Hersteller-Testdaten und 3 %/°C-Korrektur; osmotischer Druck (NaCl-Koeffizient); Spacer-Druckverlust; Stufendrucklösung; Optiflux-Flag.
- Elementdatenbank (CSV) → auswählbare Typen (ESPA2-LD, AK-400H, …).
- Qualität über Rückhalt, nicht volle Ionenaustausch-Membranen.
- **Membranentgassung:** 1–2-stufiger Vakuumkontaktor; PHREEQC `interact` mit N₂/CO₂-Sweep bei gesetztem Vakuum; empirisches ΔP vs Last.
- **Vakuumstripper:** Gleichgewicht bei variablem Druck; Entwurfsdiagramme pH/SI/Gas vs Vakuum; H₂S muss H₂S sein, nicht Seaborgium (historischer Bug, behoben in 1.0.2).
- Wann RO vs Belüftung vs Vakuum für Gase vs Salze.

## Diagramme

- Mermaid: Zulauf → Stufen → Permeat (Produkt) + Konzentrat (Abfall).
