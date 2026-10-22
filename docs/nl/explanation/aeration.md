---
lang: nl
title: Beluchting
type: explanation
audience: keyuser
status: outline
---

# Beluchting

Gepakte toren, sproei, plaat en cascade in Amanzi: wat elk model doet en welke correlaties het gebruikt.

## Inhoud om te schrijven

- Waarom grondwaterwinningen beluchten: CH₄, CO₂, O₂, VOC.
- **Toren:** Onda *k_L a* / HTU → NTU-efficiency; Engel–Stichlmair holdup, ΔP, flooding; blower als isentropische compressie; Henry en diffusie uit `tower/compounds.py`; pakkingcatalogus (Raflux).
- **Sproei:** penetratietheorie *k = 2(A/V)√(D t / π)*; valtijd *√(2h/g)*; optioneel Sauter-diameterprobleem.
- **Plaat:** PHREEQC `interact` met optioneel gerecirculeerd afgas (enkele iteraties).
- **Cascade:** empirisch *k_eff*(log tredehoogte); ΔC = (C_sat − C_in)(1 − (1 − k)^steps); CH₄ C_sat uit Duan & Mao 2006.
- Wanneer welke kiezen (kwalitatief): gepakte toren vs goedkope sproei/cascade vs plaat; VOC-stripping begunstigt de toren.
- Membraan-/vacuumontgassing in één alinea vergeleken; details op [Membranen](membranes.md).
- Citaten volledig op [Literatuur](literature.md).

## Diagrammen

- Mermaid-vergelijking: vier beluchtingsblokken → gassen die ze aanpakken.
