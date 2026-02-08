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

PV = Σ [ Cₖ / (1 + y/f)^(f × tₖ) ] + N / (1 + y/f)^(f × T)

où :  
- `Cₖ` = coupon à la période k  
- `y` = yield annuel (YTM)  
- `f` = fréquence par an (1, 2, 4…)  
- `tₖ` = temps en années jusqu’au paiement k (via day-count)  
- `T` = maturité restante en années  
- `N` = nominal (principal)

- **Régime de compounding** :  
- Pour le YTM : convention standard → compounding à la fréquence des coupons  
- Possibilité future d’ajouter : continuous compounding, annual compounding forcé

### Structure des classes / fonctions principales

| Élément                        | Emplacement                        | Responsabilité principale                                                                 |
|--------------------------------|------------------------------------|--------------------------------------------------------------------------------------------|
| `Bond` (classe abstraite ou base) | `instruments/bond.py`              | Stocke les caractéristiques fixes (nominal, coupon rate, maturité, fréquence, day-count, dates clés) |
| `.cash_flows(settlement_date)` | `instruments/bond.py`              | Retourne la liste des cash-flows restants après la date de règlement (list[dict] ou pd.DataFrame) |
| `.price(discount_curve, settlement_date)` | `instruments/bond.py` ou `pricing/pricers.py` | Calcule la valeur actuelle nette (dirty price) via actualisation des cash-flows |
| `.ytm(market_price, settlement_date, guess=0.05)` | `instruments/bond.py` ou `pricing/pricers.py` | Résout numériquement le YTM (via scipy.optimize.brentq ou newton) |
| Discount factors / curve       | `market/yield_curve.py` + `market/discounting.py` | Fournit `df(t)` ou `df(date)` pour une actualisation cohérente et réaliste |

### Décisions de design importantes

1. **Prix dirty vs clean**  
- La méthode `.price()` retourne systématiquement le **dirty price** (prix facturé, incluant accrued interest).  
- Une propriété ou méthode `.clean_price()` peut être ajoutée si nécessaire.

2. **Gestion des dates ex-coupon**  
- Les cash-flows sont générés en respectant strictement les dates de paiement théoriques et la règle ex-coupon (paiement non inclus si settlement ≥ ex-date).

3. **Résolution du YTM**  
- Utilisation préférentielle de `scipy.optimize.brentq` (robuste, intervalle-borné)  
- Plage de recherche typique : [-0.99, 10.0] pour tolérer des obligations distressed ou très haut rendement  
- Sensibilité au guess initial → valeur par défaut raisonnable (0.04–0.06 selon marché)

4. **Extensibilité future**  
- Le design permet d’ajouter facilement : obligations à taux variable (FRN), callable/putable, inflation-linked, amortissables  
- Possibilité d’intégrer des pricers vectorisés (numpy) ou GPU (torch) plus tard

5. **Performance vs lisibilité**  
- Priorité à la lisibilité et à la maintenabilité (code clair, typage, docstrings)  
- Optimisations (vectorisation) reportées après validation fonctionnelle

### Exemple d’utilisation typique

```python
from datetime import date
from quant_rates.instruments.bond import FixedRateBond
from quant_rates.market.discounting import FlatYieldDiscounting

bond = FixedRateBond(
face_value=100_000,
coupon_rate=0.035,          # 3.5%
maturity_date=date(2035, 5, 15),
issue_date=date(2025, 5, 15),
frequency=2,                # semestriel
day_count="ACT/ACT"
)

settlement = date(2026, 2, 8)
price = bond.price(flat_yield=0.042, settlement_date=settlement)   # ou via une courbe
ytm = bond.ytm(market_price=98_750, settlement_date=settlement)