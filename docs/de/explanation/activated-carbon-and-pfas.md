---
lang: de
title: Aktivkohle und PFAS
type: explanation
audience: keyuser
status: outline
---

# Aktivkohle und PFAS

GAC wie in Amanzi implementiert: kompetitive Isothermen, vereinfachter Durchbruch, Staffelung, regulatorische Summen und die Entwurf-vs-Laufzeit-Lücke.

## Inhalt zum Schreiben

- PFAS leben im **extraneous**-Strom (ng/L), nicht in PHREEQC.
- **SRS (Sheindorf–Rebhun–Sheintuch)** kompetitive Freundlich; *K* in `(µg/g)·(L/µg)^(1/n)`, Exponent **1/n**.
- DOC-Konkurrenz über TOC → DOC; Konkurrenzkoeffizienten.
- Vereinfachter Durchbruch (stationärer Fluss, keine Dispersion): *C/C₀ = 1 / (1 + exp(k · EBCT · (1 − BV · C_in / q)))*.
- PEQ-gewichtete Sum4 / Sum20 vs Kennzahlen-Grenzwerte.
- Gestaffelter Austausch: Mischen der Peak-Konzentrationen vor dem Austausch über Filter hinweg.
- Isothermen-Datenbank: 21 Verbindungen, Original- vs Amanzi-umgerechnete Spalten; Einheitenumrechnungsregeln (Polanyi, EPA WQTC, Cantoni, Chen, Hückstädt, Langmuir).
- Defaults in parametrischem PFAS-YAML (Polanyi vorhergesagt) vs Literaturzeilen.
- **Lücke:** `design()` führt diese Physik aus; `run_quality()` wendet keine PFAS-Entfernung an (nur optionale Spritzbelüftung).
- Mikroschadstoff-%-Entfernung aus Szenario-Metadaten für OMV-artige Organika.

## Diagramme

- Mermaid: Zulauf-PFAS → SRS-Kapazität → Durchbruch → Staffelungs-Mischung → Entwurfstabellen (nicht Anlagenlauf).
