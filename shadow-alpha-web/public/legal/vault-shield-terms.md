# Conditions Spécifiques — Shadow Vault & Shadow Shield

**Dernière mise à jour : 14 mars 2026**

Ces conditions complètent les Conditions Générales d'Utilisation de Shadow Alpha.

---

## PARTIE A : Shadow Vault — Conditions de Dépôt

### A.1 Nature du Service

Le Shadow Vault est un service de dépôt rémunéré où les fonds déposés sont alloués par le moteur quantitatif Shadow Alpha pour générer du rendement. **Les dépôts ne constituent pas un compte d'épargne bancaire** et ne bénéficient pas de la garantie des dépôts.

### A.2 Rendement

- Le rendement affiché (APY) est une estimation basée sur les performances récentes du moteur.
- **Le rendement n'est pas garanti.** Les performances passées ne préjugent pas des performances futures.
- Le rendement est calculé quotidiennement et crédité sur le solde du Vault.

### A.3 Commission de Performance

- Shadow Alpha prélève une commission de **35% sur les gains nets** générés par le Vault.
- La commission est calculée uniquement sur les gains positifs (high-water mark).
- Aucune commission n'est prélevée en cas de perte.

### A.4 Dépôts et Retraits

- **Dépôt minimum** : 5 000 FCFA
- **Dépôt maximum** : 10 000 000 FCFA par utilisateur
- **Retrait** : Les fonds sont disponibles sous 24 heures ouvrées. En période de forte demande, le délai peut être étendu à 72 heures.
- Aucun frais de retrait n'est appliqué.

### A.5 Risques Spécifiques

- Risque de perte en capital : le moteur quantitatif peut générer des pertes.
- Risque de liquidité : en cas de retrait massif simultané, des délais supplémentaires peuvent s'appliquer.
- Risque opérationnel : défaillance technique pouvant affecter les opérations.

---

## PARTIE B : Shadow Shield — Conditions d'Assurance

### B.1 Nature du Contrat

Shadow Shield est un contrat de couverture actuarielle (et non un contrat d'assurance au sens réglementaire). Il protège l'Utilisateur contre la perte d'une position active en échange d'une prime.

### B.2 Calcul de la Prime

- La prime est calculée par un modèle actuariel (Black-Scholes put adapté).
- Facteurs pris en compte : probabilité actuelle, volatilité du sport, temps restant, couverture demandée.
- La prime minimum est de **3% de la mise**.
- La prime maximum est de **30% de la mise**.

### B.3 Couverture

- **Couverture standard** : 70% de la mise initiale.
- **Couverture maximale** : 80% de la mise initiale (disponible pour les plans Premier et Black Card).
- La couverture ne s'applique qu'en cas de perte totale de la position (statut LOST).

### B.4 Activation

- Le Shield doit être activé **avant** le début de l'événement sportif.
- Une fois activé, le Shield ne peut être annulé ni remboursé.
- Un seul Shield peut être actif par position.

### B.5 Indemnisation

- En cas de perte de la position protégée, l'indemnité est versée automatiquement dans les 24 heures suivant le dénouement.
- L'indemnité = mise initiale × couverture_pct.
- Aucune indemnité n'est versée si la position est gagnante ou annulée.

### B.6 Exclusions

Le Shield ne couvre pas :
- Les positions liquidées pour appel de marge.
- Les événements annulés ou reportés indéfiniment.
- Les cas de fraude ou de manipulation avérée.

---

## PARTIE C : Position Loans — Accord de Prêt

### C.1 Nature du Prêt

L'Utilisateur peut emprunter des fonds en mettant en collatéral une position active. Le prêt est remboursable avec intérêts.

### C.2 Conditions

- **Ratio prêt/valeur (LTV)** : Maximum 60% de la valeur estimée de la position.
- **Taux d'intérêt** : 0.1% par jour (36.5% APR).
- **Frais d'origination** : 2% du montant emprunté.
- **Durée maximale** : 30 jours.

### C.3 Collatéral

- La position mise en collatéral est verrouillée (statut LOCKED) pendant la durée du prêt.
- L'Utilisateur ne peut pas vendre, échanger ou cacher la position verrouillée.
- Si la valeur de la position baisse en dessous du seuil de liquidation (LTV > 85%), le collatéral peut être liquidé.

### C.4 Remboursement

- Le remboursement inclut le principal + les intérêts + les frais d'origination.
- Après remboursement complet, la position est déverrouillée (statut ACTIVE).
- Le remboursement anticipé est autorisé sans pénalité.

### C.5 Défaut de Paiement

En cas de non-remboursement à l'échéance :
1. Une pénalité de retard de 0.5% par jour est appliquée.
2. Après 7 jours de retard, le collatéral est liquidé automatiquement.
3. Le produit de la liquidation est affecté au remboursement du prêt.

---

**En utilisant ces services, vous reconnaissez avoir lu et accepté ces conditions.**

Shadow Alpha SAS — support@shadow-alpha.com
