# Design Documentation

## High-Level Architecture

`quant-rates-lib` est une bibliothèque Python modulaire dédiée au pricing et à l’analyse des instruments de taux d’intérêt (obligations, swaps, courbes de taux, etc.).

L’architecture suit une séparation claire des responsabilités :

- `market/` : gestion des données de marché (courbes de taux, facteurs d’actualisation)
- `instruments/` : définition des contrats financiers (obligations, swaps, …)
- `pricing/` : moteurs de valorisation réutilisables
- `utils/` : outils transverses (conventions de comptage de jours, calendriers, etc.)

## Pricing des Obligations (Bonds)

### Objectifs de conception

Le module d’obligations vise à offrir :

- Une représentation fidèle des cash-flows réels (coupons + principal)
- Une valorisation flexible : flat yield, courbe de taux spot, multi-courbe si besoin futur
- Un calcul robuste du **Yield to Maturity (YTM)** par résolution numérique
- Une compatibilité avec les conventions de marché les plus courantes (day-count, fréquence, ex-coupon, etc.)
- Une API simple et lisible pour les utilisateurs (notebook, scripts, futures applications)

### Conventions mathématiques et de marché adoptées

- **Day count conventions** : déléguées à `utils/day_count.py`  
  → Principales supportées : ACT/ACT (ICMA), 30/360, ACT/360, ACT/365, BUS/252

- **Fréquence des coupons** : annuelle, semestrielle, trimestrielle (1, 2, 4 paiements par an)

- **Base de calcul du coupon** :  
  Coupon brut = Nominal × Coupon rate × (Day count fraction entre deux dates)

- **Actualisation** :  
  - Par défaut : actualisation composée selon la fréquence des coupons (semi-annuelle le plus souvent)  
  - Formule de base pour un yield constant (YTM) :  