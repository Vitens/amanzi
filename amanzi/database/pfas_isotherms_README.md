# PFAS GAC Isotherm Literature Database

Standalone reference database of Freundlich and Langmuir isotherm parameters for **21 PFAS** (union of SUM20 + TFA), sourced from peer-reviewed literature. Each row stores **original published values** and **Amanzi-converted** parameters.

## Files

| File | Purpose |
|------|---------|
| `pfas_isotherms.csv` | Main database (semicolon-delimited) |
| `pfas_isotherms_build.py` | Regenerates CSV from curated literature data |
| `pfas_isotherms_viz.py` | Generates PNG figures in `pfas_isotherms_figures/` |
| `pfas_isotherms_figures/` | Output charts |

## Compounds (21)

**PFCAs:** TFA, PFBA, PFPeA, PFHxA, PFHpA, PFOA, PFNA, PFDA, PFUnDA, PFDoDA, PFTrDA, PFTeDA

**PFSAs:** PFBS, PFPeS, PFHxS, PFHpS, PFOS, PFDS

**Precursors:** PFOSA, N-MeFOSAA, N-EtFOSAA

Minimum **3 entries per compound** (distinct source × GAC × condition).

## Amanzi unit convention

Matches `amanzi/parametric/pfas.yml` and `activatedcarbon.py`:

| Parameter | Column | Units |
|-----------|--------|-------|
| Freundlich K | `amanzi_freundlich_k` | `(µg/g)·(L/µg)^(1/n)` |
| Freundlich exponent | `amanzi_freundlich_1n` | dimensionless (**1/n**, not n) |
| Langmuir qmax | `amanzi_langmuir_qmax` | µg/g |
| Langmuir KL | `amanzi_langmuir_kl` | L/µg (Ce in µg/L) |

Equation: `q = K × Ce^(1/n)` with Ce converted from ng/L to µg/L in the model (`/1000`).

UI label `µg/g/L/µg` in `micropollutants.vue` is shorthand for `(µg/g)·(L/µg)^(1/n)`.

## Unit conversion rules

| Source convention | Amanzi conversion |
|-------------------|-------------------|
| `(µg/g)(L/µg)^(1/n)` — Polanyi | `amanzi_k = orig_k` |
| `(µg/g)(L/ng)^(1/n)` — EPA WQTC | `amanzi_k = orig_k × 1000^(1/n)` |
| `(ng/mg)(ng/L)^(-1/n)` — Cantoni | `amanzi_k = orig_k × 1000^(1/n)` |
| `(ng/mg)/(ng/L)^n` — Chen 2024 | `amanzi_1n = n`; `amanzi_k = orig_k × 1000^n` |
| `(µg/g)/(µg/L)^n` — Hückstädt | `amanzi_k = orig_k`; `amanzi_1n = n` (Ce already µg/L) |
| Langmuir KL in L/ng | `amanzi_kl = orig_kl × 1000` |
| Langmuir qmax in ng/mg | `amanzi_qmax = orig_qmax` (numerically equal to µg/g) |

## Primary literature sources

1. **Burkhardt et al. 2020** — EPA WQTC batch isotherms (F400, Norit 400, UC1240LD)
2. **Cantoni et al. 2021** — [STOTEN](https://doi.org/10.1016/j.scitotenv.2021.150214) (4 Arkema GACs, tap water, 8-PFAS mixture)
3. **Burkhardt et al. 2023** — [Polanyi PMC10208310](https://pmc.ncbi.nlm.nih.gov/articles/PMC10208310/) (predicted; matches `pfas.yml` defaults)
4. **Pranić et al. 2024** — [Chemosphere](https://doi.org/10.1016/j.chemosphere.2024.143889) (SRD/CS GAC, 0.1–100 ng/L)
5. **Hückstädt et al. 2023** — [Environ Sci Eur](https://doi.org/10.1186/s12302-023-00716-5) (short-chain PFCAs, competitive)
6. **Appleman et al. 2014** — [Water Research](https://doi.org/10.1016/j.watres.2014.02.034) (long-chain PFAS, precursors)
7. **Belkouteb et al. 2020** — [Water Research](https://doi.org/10.1016/j.watres.2020.115913) (full-scale long-chain PFCAs)
8. **Chen & Cannon 2018** — [EES](https://doi.org/10.1089/ees.2018.0453) (TFA on modified AC)
9. **Eschauzier et al. 2012** — [Water Research](https://doi.org/10.1016/j.watres.2012.10.045) (precursors, PFSA)
10. **Sadia et al. 2024** — [Heliyon/KWR](https://doi.org/10.1016/j.heliyon.2024.e25130) (realistic 5 ng/L multi-PFAS)

## `pfas.yml` provenance

Default Freundlich K and 1/n values in `amanzi/parametric/pfas.yml` align with **Polanyi predicted** parameters from Burkhardt et al. 2023 (EPA dataset [10.23719/1528436](https://doi.org/10.23719/1528436)). Measured literature values often differ, especially under competitive/matrix conditions (e.g. Cantoni tap water) or at low ng/L (Pranić et al. 2024).

## Known gaps

- **Langmuir:** sparse for many compounds; Freundlich is the primary GAC equilibrium model in Amanzi.
- **PFDS `pfas.yml` default** (K=0.1): placeholder; measured values are orders of magnitude higher.
- **Long-chain PFCAs / precursors:** fewer measured batch isotherms; some entries use full-scale or estimated K.
- **TFA:** poorly adsorbed on unmodified GAC; modified/tailored carbons required for practical removal.

## Regenerate

```bash
python3 amanzi/database/pfas_isotherms_build.py
# Visualization requires matplotlib + pyyaml (e.g. project .test venv):
.test/bin/python amanzi/database/pfas_isotherms_viz.py
```
