---
lang: en
title: Literature
type: explanation
audience: keyuser
status: draft
---

# Literature

These are the sources the public models name. The repository does not include the papers. Where a publisher offers a DOI, that is the durable address.

## Packed tower

Onda’s correlation supplies the gas-side coefficient, the liquid-side coefficient, and the wetted area that become the height of a transfer unit. The implementation is `tower/onda.py`.

- Onda, K., Takeuchi, H., and Okumoto, Y. (1968). Mass transfer coefficients between gas and liquid phases in packed columns. *Journal of Chemical Engineering of Japan*, 1(1), 56–62. https://doi.org/10.1252/jcej.1.56

Engel and Stichlmair supply the packing hydraulics. The code labels static holdup as their equation 2, dynamic holdup as equation 4, and the flooding holdup and dry pressure drop as equation 15 (`tower/engelstichlmair.py`).

Henry constants and diffusivities in water and air are the coefficients from [henrys-law.org](https://henrys-law.org/), converted to a dimensionless Henry constant at the liquid temperature (`tower/compounds.py`).

Liquid viscosity for the tower-side water properties cites Viswanath, D.S. and Natarajan, G. (1989), *Data Book on the Viscosity of Liquids*. The same citation is used for the sand-trap viscosity. Packing geometry is the Raflux catalogue inside the model (Raflux 25, 50, and 90).

The blower is an ideal isentropic compression of air (heat-capacity ratio 1.4) from 101325 Pa across the packing pressure drop, divided by blower efficiency. That expression is written in the tower model. It is not taken from a separate blower paper.

## Cascade and methane

Methane saturation in the cascade is interpolated at 10 °C from Table 4 of Duan and Mao (2006). Oxygen and carbon dioxide use empirical efficiencies of step height stored in the cascade model.

- Duan, Z. and Mao, S. (2006). A thermodynamic model for calculating methane solubility, density and gas phase composition of methane-bearing aqueous fluids from 273 to 523 K and from 1 to 2000 bar. *Geochimica et Cosmochimica Acta*, 70, 3369–3386. https://doi.org/10.1016/j.gca.2006.03.018

## Spray on a filter

The spray efficiency on a sand or marble filter is a fourth-order polynomial in fall height. The source comment calls it a fit to a TU Delft / Dresden nozzle curve, and calls it a workaround. The Sauter-diameter derivation next to it is commented out and does not run.

## Filters

Clean-bed head loss is a Kozeny–Carman expression. Backwash head loss and expansion use a fixed dynamic viscosity of 1.1375×10⁻³ Pa·s, noted in the code as 15 °C. There is no further literature key on that constant.

## Membranes

Kw is derived from the manufacturer test row in `membrane_database.csv` (rejection, flux, pressure, recovery, area) and corrected by 3 % per °C from 25 °C. Osmotic pressure uses a sodium-chloride coefficient on TDS. Spacer head loss follows the relation cited in the code as *Water Treatment — Nanofiltration and Reverse Osmosis*, p. 195 (TU Delft). Kinematic viscosity for that head loss is a polynomial fitted to the Engineering Toolbox water-viscosity table, not the Viswanath data book.

## Chemistry engine

Every quality walk is PHREEQC, reached through Vitens PhreeqPython.

- Parkhurst, D.L. and Appelo, C.A.J. (2013). *Description of input and examples for PHREEQC version 3 — A computer program for speciation, batch-reaction, one-dimensional transport, and inverse geochemical calculations*. U.S. Geological Survey Techniques and Methods, book 6, chap. A43. https://doi.org/10.3133/tm6A43

PhreeqPython is Vitens software and is named in the About dialog together with PHREEQC.

## Citing Amanzi

The About dialog builds a BibTeX entry of this shape, with the version and year of the copy you have open:

```
@software{amanzi_YEAR,
  author = {Vitens},
  title = {Amanzi},
  version = {VERSION},
  year = {YEAR},
  url = {https://github.com/Vitens/Amanzi}
}
```
