---
lang: fr
title: Comparer des scénarios
type: tutorial
audience: novice
status: draft
---

# Comparer des scénarios

Un scénario est une version de l'installation, mais il y a toujours plusieurs façons de construire un traitement d'eau. Pour voir quel choix semble le meilleur, Amanzi compare les scénarios avec le bouton **Calculer le projet**, en haut à droite.
Les onglets sont en bas. Copiez la disposition, changez un chiffre, et lisez les deux versions dans le rapport.

## Copier la disposition

Sur l'onglet de scénario, cliquez sur le menu d'options (⋮) et choisissez **Dupliquer**. Nommez la copie (la vidéo utilise **Lower dose**) et confirmez avec **Ajouter un scénario**.

Le **+** à côté des onglets ouvre un scénario vide : un canevas vide.

Sur la copie, double-cliquez sur **Adoucissement sur pellets**. Sous **Dosage**, passez **Dosage de base** de 2 à 0.5 et appuyez sur Entrée. Un seul changement de conception suffit.

Les notes d'un scénario sont destinées au lecteur. Elles ne changent pas le calcul.

<video controls preload="metadata" src="../media/DuplicateAndChange.mp4" style="max-width: 100%; height: auto;" aria-label="Dupliquez le scénario 1 sous le nom Lower dose et réglez le dosage de base de Pelletontharding à 0.5">
Sur l'onglet de scénario, choisissez Dupliquer, nommez la copie Lower dose et confirmez avec Ajouter un scénario. Sur cette copie, double-cliquez sur Pelletontharding et passez Dosage de base de 2 à 0.5 sous Dosage.
</video>

## Lire les deux versions

Cliquez sur **Calculer le projet**. Le rapport s'ouvre sur **Modèle unique**, pour le scénario sélectionné. Les sections sont **Qualité de l'eau**, **Énergie** et **Durabilité**. La quantité reste dans le panneau de droite tant que vous n'activez pas **Comparaison**.

Activez **Comparaison** pour voir chaque scénario et choisir le paramètre à comparer.

Les graphiques, **Copier** et le commutateur **Compact** / **Détaillé** sont dans [Comparer dans le rapport](../how-to/compare-in-report.md). Le calcul du CO₂ pour les valeurs de durabilité est détaillé dans [Quantité, énergie, réactifs, CO₂](../explanation/quantity-energy-chemicals-co2.md).

<video controls preload="metadata" src="../media/CompareScenarios.mp4" style="max-width: 100%; height: auto;" aria-label="Activez Comparaison et Compact pour voir les deux scénarios">
Cliquez sur Calculer le projet, activez Comparaison, puis passez à Compact. La quantité correspond ; la dureté et le CO₂ non.
</video>
