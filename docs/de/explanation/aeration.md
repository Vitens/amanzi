---
lang: de
title: Belüftung
type: explanation
audience: keyuser
status: outline
---

# Belüftung

Füllkörper-Turm, Spritz-, Platten- und Kaskadenbelüftung in Amanzi: was jedes Modell tut und welche Korrelationen es nutzt.

## Inhalt zum Schreiben

- Warum Grundwasserwerke belüften: CH₄, CO₂, O₂, VOC.
- **Turm:** Onda *k_L a* / HTU → NTU-Effizienz; Engel–Stichlmair Holdup, ΔP, Flutung; Gebläse als isentrope Verdichtung; Henry und Diffusion aus `tower/compounds.py`; Füllkörperkatalog (Raflux).
- **Spray:** Penetrationstheorie *k = 2(A/V)√(D t / π)*; Fallzeit *√(2h/g)*; optionales Sauter-Durchmesser-Thema.
- **Platte:** PHREEQC `interact` mit optionalem rezirkuliertem Abgas (wenige Iterationen).
- **Kaskade:** empirisches *k_eff*(log Stufenhöhe); ΔC = (C_sat − C_in)(1 − (1 − k)^steps); CH₄ C_sat aus Duan & Mao 2006.
- Wann welches wählen (qualitativ): Füllkörper-Turm vs günstige Spritz-/Kaskadenbelüftung vs Platte; VOC-Strippung begünstigt den Turm.
- Membran-/Vakuum-Entgasung in einem Absatz verglichen; Details unter [Membranen](membranes.md).
- Zitate vollständig unter [Literatur](literature.md).

## Diagramme

- Mermaid-Vergleich: vier Belüftungsblöcke → Gase, die sie anvisieren.
