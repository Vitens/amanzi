---
title: Literature
type: explanation
audience: keyuser
status: outline
---

# Literature

Bibliography for models and data in Amanzi. Prefer DOIs. Do not host paywalled PDFs.

## Content to write

Group entries and state *where Amanzi uses them*:

- **PFAS GAC isotherms:** Cantoni et al. 2021 (STOTEN, doi:10.1016/j.scitotenv.2021.150214); Pranić et al. 2024 (Chemosphere, doi:10.1016/j.chemosphere.2024.143889); Hückstädt et al. 2023 (Environ Sci Eur, doi:10.1186/s12302-023-00716-5); Appleman et al. 2014 (Water Research, doi:10.1016/j.watres.2014.02.034); Belkouteb et al. 2020 (Water Research, doi:10.1016/j.watres.2020.115913); Chen & Cannon 2018 (EES, doi:10.1089/ees.2018.0453); Eschauzier 2012; Sadia 2024; Burkhardt et al. 2020 (EPA WQTC); Burkhardt / Polanyi EPA dataset 2023 (PMC10208310).
- **Competitive adsorption:** Sheindorf–Rebhun–Sheintuch (SRS) Freundlich — cite the original SRS paper when writing.
- **Packed tower:** Onda mass-transfer correlation; Engel & Stichlmair hydraulics (Eq. 2, 4, 15 as used in code).
- **CH₄ solubility:** Duan & Mao 2006, Table 4.
- **Viscosity:** Viswanath & Natarajan 1989.
- **RO *Kw* and headloss:** manufacturer data; ResearchGate pub. 351606477; TU Delft NF/RO notes (as cited in `membranestack.py`).
- **Henry / diffusion:** henrys-law.org coefficients as used in `tower/compounds.py`.
- **Spray nozzle curve:** TU Delft / Dresden polynomial fit (sand and marble filtration).
- **PHREEQC / PhreeqPython:** Parkhurst & Appelo; Vitens PhreeqPython — acknowledgements.

Also: software citation text from the About dialog (BibTeX).
