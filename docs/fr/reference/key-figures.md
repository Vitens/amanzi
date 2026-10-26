---
lang: fr
title: Indicateurs
type: reference
audience: everyone
status: draft
---

# Indicateurs

Valeurs de consultation partagées. Le fichier est `amanzi/database/key_figures.csv`. Colonnes : name (la balise), category, type, default, UOM, remarks.

La boîte de dialogue les groupe en **Général** et **Chimique**. Sous Général, les types sont opérationnel, **Durabilité et émissions** et **Normes de qualité**. Sous Chimique, les lignes sont des facteurs d'émission.

| Balise | Défaut | Unité | Rôle |
|---|---|---|---|
| `max_hour` | 1.2 | — | Facteur de pointe journalier |
| `well_efficiency` | 55 | % | Pompes de puits |
| `booster_efficiency` | 75 | % | Pompes de surpression |
| `carbon_intensity_grid` | 250 | gCO₂/kWh | Électricité |
| `methane_emission_factor` | 28 | gCO₂/gCH₄ | Méthane |
| `ph_lower_limit` | 7 | — | Norme de qualité, l'un d'une paire limite inférieure/supérieure et seuil |
| `hardness_upper_limit` | 2 | mmol/l | Norme de qualité |
| `lye_emission` | 1.27 | gCO₂/g AS | Facteur chimique |

Le même schéma couvre les autres lignes de qualité (pH, conductivité, SI, oxygène, dureté, CO₂ agressif, TACC₉₀, fer, manganèse, ammonium, sodium, chlorure) et les autres facteurs chimiques (chaux, CO₂, acides, oxygène, sable filtrant, matériaux d'ensemencement, et le reste du bloc chimique).

Une redéfinition de projet remplace la valeur par défaut pour chaque scénario. Une redéfinition de scénario la remplace pour ce scénario seulement. Une cellule vide signifie que la colonne n'est pas une surcharge. Une balise manquante au moment du calcul est une erreur.

Le CSV du dépôt contient aussi `sum4PFAS_limit` (20 ng/l), `sum20PFAS_limit` (100 ng/l) et `PEQ_limit` (4.4 ng/l). La liste des indicateurs de l'application publique n'affiche pas ces trois lignes. La modification d'un indicateur qui figure dans la liste est dans [Régler les indicateurs](../how-to/set-key-figures.md).
