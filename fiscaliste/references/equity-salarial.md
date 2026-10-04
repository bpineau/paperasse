# Equity salarial (RSU, BSPCE, stock-options, PEE/PERCO)

Voir `data/equity-salarial.json` pour les taux et seuils.

## RSU / AGA (Restricted Stock Units / Actions Gratuites)

**Terminologie** : "RSU" est le terme anglo-saxon ; "AGA" (Actions Gratuites d'Actions) est le terme juridique français (art. L. 225-197-1 C. com., art. 80 quaterdecies CGI). Les deux désignent le même dispositif : attribution d'actions gratuites aux salariés, avec période d'acquisition (vesting) puis détention éventuelle.

### Deux événements fiscaux distincts, imposés la même année (celle de la cession)

Source : [BOI-RSA-ES-20-20-20](https://bofip.impots.gouv.fr/bofip/5654-PGP.html/identifiant=BOI-RSA-ES-20-20-20-20260521) (régime fiscal au regard des bénéficiaires, version du 21/05/2026) et [BOI-RSA-ES-20-30](https://bofip.impots.gouv.fr/bofip/2389-PGP.html/identifiant=BOI-RSA-ES-20-30-20260521) (contribution salariale). Le régime dépend de la **date de la décision d'AGE** qui a autorisé l'attribution et du caractère **qualifiant** du plan (C. com. art. L. 225-197-1 et s. ; plans de sociétés étrangères : [BOI-RSA-ES-20-20-10-20](https://bofip.impots.gouv.fr/bofip/9665-PGP.html/identifiant=BOI-RSA-ES-20-20-10-20-20170724)).

**1. Gain d'acquisition** = valeur des actions à la date d'acquisition définitive (vesting) × nombre d'actions
- Valeur retenue : **premier cours coté du jour de l'attribution définitive** ; cotation en devise convertie au taux de change de ce jour (§ 120 et 130)
- **Fait générateur : la cession** (ou disposition, conversion au porteur, mise en location), pas le vesting (art. 80 quaterdecies CGI ; § 150). Un gain acquis en N et cédé en N+3 se déclare en N+3.
- Une **moins-value de cession** (vente sous la valeur d'acquisition) s'impute sur le gain d'acquisition correspondant, dans la limite de ce montant, avant tout abattement (art. 80 quaterdecies V ; § 190). Les moins-values sur d'autres titres ne s'imputent jamais sur le gain d'acquisition.

**2. Plus-value de cession** = prix de cession − valeur à la date d'acquisition définitive
- **PV mobilière** : PFU à **31,4 % pour les cessions réalisées dès 2025** (12,8 % IR + 18,6 % PS, LFSS 2026), ou barème sur option globale
- Les PV mobilières sont des "revenus du patrimoine" (art. L. 136-6 CSS), donc soumises au taux PS 18,6 % dès les revenus 2025

### Régime du gain d'acquisition selon la date de l'AGE (plans qualifiants)

| Décision d'AGE | Fraction annuelle ≤ 300 000 € | Fraction > 300 000 € |
|---|---|---|
| **Après le 31/12/2017** (LF 2018 art. 28, régime courant) | Barème **après abattement de 50 %** (art. 200 A, 3 CGI), le cas échéant abattement fixe 150-0 D ter ; **PS revenus du patrimoine** 18,6 % sans abattement (L. 136-6 I e CSS, § 50) ; **pas de contribution salariale** ; CSG non déductible | Traitements et salaires de droit commun : barème sans abattement, CSG/CRDS d'activité 9,7 %, **contribution salariale 10 %** (L. 137-14 CSS) |
| Du 31/12/2016 au 31/12/2017 | Barème après abattements pour durée de détention (ancien 150-0 D) ou abattement fixe, non cumulables ; PS patrimoine | Idem ci-dessus (salaire + contribution 10 %) |
| Du 08/08/2015 au 30/12/2016 (loi Macron) | Intégralité du gain : barème après abattements pour durée de détention, PS patrimoine, pas de contribution salariale | sans objet |
| Du 28/09/2012 au 07/08/2015 | Salaire (barème), CSG/CRDS d'activité, contribution salariale 10 % | sans objet |

La limite de 300 000 € s'apprécie par contribuable et par année de cession, sur l'ensemble des gains d'acquisition, **après** imputation d'une éventuelle moins-value de cession.

**Plans non qualifiants** (hors conditions du C. com.) : le gain d'acquisition est un salaire ordinaire, imposé l'année de l'acquisition définitive avec les cotisations de droit commun (§ 14).

### Pièges classiques

Deux erreurs symétriques :
1. **Traiter le gain d'acquisition d'un plan qualifiant comme un salaire** (cotisations, contribution 10 %, cases salaires) : faux sous 300 000 € depuis la loi Macron, c'est le régime des plans non qualifiants ou de la fraction excédentaire.
2. **Le traiter comme une simple PV mobilière** au PFU : faux, il est au barème après abattement de 50 %, avec PS patrimoine, l'année de la cession.

Seule la plus-value ultérieure (valeur au vesting → cession) est une PV mobilière. Les cases de la 2042 C (gain avec abattement 50 %, fraction > 300 000 €) sont à vérifier chaque année sur la notice.

### Stratégie : quotient pour revenus exceptionnels

Une cession massive d'actions gratuites (ex: 150 000 € de gain d'acquisition imposable la même année) fait franchir plusieurs tranches. Le **quotient pour revenus exceptionnels** (coefficient 4) peut lisser l'imposition.

Mécanisme : impôt = [IR(RNI_hors_RSU + gain/4) − IR(RNI_hors_RSU)] × 4. Utile si le gain seul fait franchir une tranche. **Nuance** : inutile si le foyer est déjà au TMI 45% — le taux marginal ne change pas avec la division. Détail et exemples chiffrés dans la section cas-speciaux listée depuis SKILL.md.

## Stock-options

### Rabais excédentaire

Différence entre prix du marché à l'attribution et prix d'exercice, au-delà de 5%.
→ **Imposition comme salaire à l'acquisition**.

### Gain de levée

Selon date d'attribution :

| Plan | Régime |
|------|--------|
| Avant 2012 | Barème de faveur (selon durée détention) |
| 2012-2016 | Salaire (barème IR + cotisations sociales spécifiques) |
| Après 2017 | Salaire (barème) + contribution salariale 10% sur plans qualifiants |

Toujours consulter le plan pour déterminer le régime applicable.

## BSPCE (Bons de Souscription de Parts de Créateur d'Entreprise)

**Différence clé vs RSU** : pas de gain d'acquisition imposable comme salaire. Le gain n'est réalisé et imposé **qu'à la cession des actions**.

### Imposition du gain de cession

Voir `data/equity-salarial.json` → `bspce.gain_cession`.

| Ancienneté dans la société à la date de cession | Taux global pour cessions 2025 |
|--------------------------------------------------|-------------|
| **≥ 3 ans** | **31,4 %** (12,8 % IR + 18,6 % PS) — PV mobilière |
| **< 3 ans** | 50 % (30 % IR + 20 % PS — contribution salariale spécifique) |

Note : pour les cessions ≥ 3 ans, le PS suit le taux applicable aux PV mobilières (revenus du patrimoine, L. 136-6 CSS), soit 18,6 % dès 2025. Pour les cessions < 3 ans, la part PS reste à 20 % (contribution salariale spécifique, distincte du PS de droit commun).

La pénalité pour départ précoce (< 3 ans) est forte. À intégrer dans les décisions de départ.

### Conditions d'éligibilité de la société

À vérifier avant attribution :
- SA ou SAS française
- Immatriculée depuis moins de 15 ans
- Non cotée OU cotée sur compartiment dédié aux PME
- Soumise à l'IS
- Capital détenu à 25% minimum par des personnes physiques
- Non issue d'une restructuration (fusion, scission, reprise d'activité)

**Si conditions non remplies** : requalification en salaires → barème IR + cotisations sociales → traitement beaucoup plus défavorable.

### Vérification préalable recommandée

Demander à la société :
- Date d'immatriculation au RCS
- Capital social et répartition (tableau des associés)
- Régime fiscal (IS obligatoire)
- Historique des restructurations éventuelles

## Épargne salariale (PEE / PERCO / PERO)

### PEE (Plan d'Épargne Entreprise)

Enveloppe collective distincte du PER individuel.

- **Abondement employeur** : exonéré IR et PS dans les plafonds — **AVANTAGE MAJEUR**
- **Plafond abondement** : ~3 709 € par bénéficiaire (8% PASS — vérifier annuellement)
- **Blocage** : 5 ans sauf cas de déblocage anticipé (mariage, naissance 3e enfant, achat RP, divorce avec enfant, fin contrat travail, surendettement, invalidité, décès, violences conjugales)
- **Sortie après 5 ans** : exonération IR, seuls PS 17,2% sur les gains
- **Dividendes réinvestis** : exonérés IR tant qu'ils restent dans l'enveloppe

### PERCO / PERO (PER d'entreprise)

- **Sortie à la retraite** : rente ou capital
- **Fiscalité sortie** : même que PER individuel (versements à barème, gains au PFU)
- **Abondement employeur** : exonéré dans plafonds (~7 418 €, distinct du plafond PEE)

### Arbitrage PEE/PERCO vs PER individuel

| Enveloppe | Avantage unique | Quand privilégier |
|-----------|----------------|-------------------|
| PEE | Abondement employeur (levier +30% à +300%) | D'abord, toujours — tant qu'il y a abondement |
| PERCO / PERO | Abondement employeur sur épargne retraite | En second après PEE max |
| PER individuel | Déduction RNI (pas de plafond d'abondement) | En complément, après saturation PEE/PERCO |

**Règle d'or** : ne jamais abonder un PER individuel avant d'avoir saturé l'abondement employeur PEE + PERCO. L'abondement est de l'argent gratuit.

## Quotient pour revenus exceptionnels

Vesting massif, cession d'entreprise, indemnité de départ → à activer.

**Mécanisme** :
1. Revenu exceptionnel ÷ coefficient (généralement 4)
2. Ajouter au revenu ordinaire
3. Calculer l'impôt supplémentaire
4. × coefficient

**À mentionner systématiquement** pour :
- Vesting RSU > 1,5 × salaire annuel
- Cession de parts de société
- Indemnité de départ importante
- Prime exceptionnelle massive

**Inutile si** : foyer déjà à TMI 45% (taux marginal identique quelle que soit la division).

## Formulaires

| Revenu | Formulaire / case |
|--------|-------------------|
| Gain acquisition RSU (salaire) | 2042 case 1TT / 1UT |
| Plus-value cession RSU | 2042 C case 3VG (PFU) ou 2074 (détail) |
| Gain cession BSPCE | 2042 C case 3VG ou 3WB selon ancienneté |
| Abondement PEE (information) | Déclaration employeur — exonéré |
| Stock-options | Variable selon plan — consulter le plan |

## Références CGI / BOFiP

- RSU : art. 80 quaterdecies CGI
- Stock-options : art. 80 bis CGI
- BSPCE : art. 163 bis G CGI
- PEE : art. L. 3332-1 et s. Code du travail
- PER : art. 163 quatervicies CGI
- BOFiP : BOI-RSA-ES (actionnariat salarié)
