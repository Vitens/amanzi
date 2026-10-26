---
lang: fr
title: Ce qu'est Amanzi
type: explanation
audience: novice
status: draft
---

# Ce qu'est Amanzi

Amanzi est un outil de conception pour le traitement de l'eau potable, réalisé par Vitens. Un scénario de traitement est le dessin d'une usine, plus les nombres que ce dessin implique : quelle quantité d'eau circule, ce qu'elle contient, combien d'énergie et de réactifs l'usine consomme, et le CO₂ qui découle de ces consommations. Comparer deux scénarios, c'est comparer deux dessins de ce genre. Le faire dans un tableur sépare le dessin du calcul. Amanzi les garde dans un seul projet.

Vous disposez d'un schéma de procédé, de plusieurs versions « et si », et de quatre familles de résultats sur l'usine : quantité, qualité, énergie et durabilité. La consommation de réactifs se trouve dans les unités et dans le bilan de CO₂. Les [tutoriels](../tutorials/index.md) parcourent la démo. Les [guides pratiques](../how-to/index.md) indiquent comment modifier une unité, un indicateur ou un fichier. La [référence](../reference/index.md) liste les champs. Cette section dit pourquoi les nombres sortent tels qu'ils sortent.

Amanzi est une calculatrice pour une conception que vous envisagez. Il n'exploite pas une usine, ne remplace pas une analyse de laboratoire, et ne tient pas lieu d'une autorisation ou d'un plan d'exécution. Il ne rejoue pas non plus une journée d'exploitation. Chaque scénario est un point de fonctionnement stationnaire.

Le calcul s'exécute dans le navigateur. La démo hébergée et une copie que vous servez vous-même reposent sur la même idée : le projet reste sur l'ordinateur où la page est ouverte, et le moteur de chimie s'y charge. Aucun modèle d'usine n'attend sur un serveur. L'ouverture de l'une ou de l'autre est décrite dans [Ouvrir en hébergé ou en local](../how-to/open-hosted-or-local.md).

Amanzi est sous licence GNU General Public License, version 3. La boîte de dialogue À propos, dans l'application, affiche cette mention et une entrée BibTeX du logiciel, avec Vitens comme auteur et l'adresse `https://github.com/Vitens/Amanzi`. L'année et la version de cette entrée suivent la copie que vous avez ouverte.
