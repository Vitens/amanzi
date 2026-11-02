---
lang: fr
title: Littérature
type: explanation
audience: keyuser
status: draft
---

# Littérature

Voici les sources que nomment les modèles publics. Le dépôt n'inclut pas les articles. Lorsqu'un éditeur fournit un DOI, c'est l'adresse durable.

## Tour garnie

La corrélation d'Onda fournit le coefficient côté gaz, le coefficient côté liquide et l'aire mouillée qui deviennent la hauteur d'unité de transfert. L'implémentation est `tower/onda.py`.

- Onda, K., Takeuchi, H., and Okumoto, Y. (1968). Mass transfer coefficients between gas and liquid phases in packed columns. *Journal of Chemical Engineering of Japan*, 1(1), 56–62. https://doi.org/10.1252/jcej.1.56

Engel et Stichlmair fournissent l'hydraulique du garnissage. Le code désigne la rétention statique comme leur équation 2, la rétention dynamique comme l'équation 4, et la rétention d'engorgement ainsi que la perte de charge à sec comme l'équation 15 (`tower/engelstichlmair.py`).

Les constantes de Henry et les diffusivités dans l'eau et dans l'air sont les coefficients de [henrys-law.org](https://henrys-law.org/), convertis en une constante de Henry adimensionnelle à la température du liquide (`tower/compounds.py`).

La viscosité du liquide, pour les propriétés de l'eau côté tour, cite Viswanath, D.S. and Natarajan, G. (1989), *Data Book on the Viscosity of Liquids*. La même citation est utilisée pour la viscosité du dessableur. La géométrie du garnissage est le catalogue Raflux interne au modèle (Raflux 25, 50 et 90).

La soufflante est une compression isentropique idéale de l'air (rapport des capacités thermiques 1.4), depuis 101325 Pa à travers la perte de charge du garnissage, divisée par le rendement de la soufflante. Cette expression est écrite dans le modèle de tour. Elle n'est pas tirée d'un article distinct sur les soufflantes.

## Cascade et méthane

La saturation en méthane de la cascade est interpolée à 10 °C à partir du tableau 4 de Duan et Mao (2006). L'oxygène et le dioxyde de carbone utilisent des efficacités empiriques de la hauteur de marche, stockées dans le modèle de cascade.

- Duan, Z. and Mao, S. (2006). A thermodynamic model for calculating methane solubility, density and gas phase composition of methane-bearing aqueous fluids from 273 to 523 K and from 1 to 2000 bar. *Geochimica et Cosmochimica Acta*, 70, 3369–3386. https://doi.org/10.1016/j.gca.2006.03.018

## Aspersion sur un filtre

L'efficacité d'aspersion sur un filtre à sable ou à marbre est un polynôme du quatrième ordre en hauteur de chute. Le commentaire dans la source y voit un ajustement à une courbe de buse TU Delft / Dresden, et le qualifie de contournement. La dérivation par le diamètre de Sauter, placée à côté, est mise en commentaire et ne s'exécute pas.

## Filtres

La perte de charge du lit propre est une expression de Kozeny–Carman. La perte de charge de lavage et l'expansion utilisent une viscosité dynamique fixe de 1.1375×10⁻³ Pa·s, notée dans le code comme 15 °C. Il n'y a pas d'autre clé bibliographique pour cette constante.

## Membranes

Kw est dérivé de la ligne d'essai du fabricant dans `membrane_database.csv` (rejet, flux, pression, taux de conversion, surface) et corrigé de 3 % par °C à partir de 25 °C. La pression osmotique utilise un coefficient chlorure de sodium sur le TDS. La perte de charge des espaceurs suit la relation citée dans le code sous le titre *Water Treatment — Nanofiltration and Reverse Osmosis*, p. 195 (TU Delft). La viscosité cinématique de cette perte de charge est un polynôme ajusté à la table de viscosité de l'eau d'Engineering Toolbox, et non au recueil de Viswanath.

## Moteur de chimie

Chaque parcours de qualité est PHREEQC, atteint par le PhreeqPython de Vitens.

- Parkhurst, D.L. and Appelo, C.A.J. (2013). *Description of input and examples for PHREEQC version 3 — A computer program for speciation, batch-reaction, one-dimensional transport, and inverse geochemical calculations*. U.S. Geological Survey Techniques and Methods, book 6, chap. A43. https://doi.org/10.3133/tm6A43

PhreeqPython est un logiciel de Vitens. Il est nommé dans la boîte de dialogue À propos, avec PHREEQC.

## Citer Amanzi

La boîte de dialogue À propos construit une entrée BibTeX de cette forme, avec la version et l'année de la copie que vous avez ouverte :

```
@software{amanzi_YEAR,
  author = {Vitens},
  title = {Amanzi},
  version = {VERSION},
  year = {YEAR},
  url = {https://github.com/Vitens/Amanzi}
}
```
