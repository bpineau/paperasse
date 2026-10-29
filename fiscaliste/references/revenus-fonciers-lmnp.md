# Revenus fonciers, LMNP et SCI à l'IR

## Distinction fondamentale

| Type de location | Régime fiscal | Catégorie |
|------------------|---------------|-----------|
| Non meublée (location nue) | Revenus fonciers | Revenus fonciers (micro ou réel) |
| Meublée non professionnelle | **BIC** | LMNP (micro-BIC ou réel) |
| Meublée professionnelle | **BIC** | LMP (réel obligatoire) |
| SCI à l'IR | Revenus fonciers | Transparence fiscale |
| SCI à l'IS | IS | **Hors scope fiscaliste** — voir skill `comptable` |

**Erreur classique** : déclarer une location meublée en revenus fonciers. Non — le meublé relève des BIC. Conséquences fiscales très différentes (amortissements possibles en réel).

## Revenus fonciers (location nue)

### Micro-foncier (régime simplifié)

Voir `data/regimes-fonciers-lmnp.json` → `micro_foncier`.

- **Condition** : revenus fonciers bruts ≤ 15 000 €
- **Abattement** : 30% automatique
- **Exclusions** (brochure IR 2026, revenus fonciers) : monuments historiques, immeubles en nue-propriété, Loc'Avantages, amortissements Périssol, Besson neuf, Robien, Borloo neuf, déductions spécifiques (Anah, Borloo ancien, Cosse, Scellier intermédiaire, ZRR), et le cas où les seuls revenus fonciers du foyer viennent de parts de sociétés non soumises à l'IS (une SCI plus un immeuble en direct reste éligible). Le Pinel n'exclut pas du micro-foncier. Seuil apprécié sur l'ensemble du foyer, sans prorata temporis.
- **Avantage** : simplicité. Pas de comptabilité.
- **Inconvénient** : aucun déficit possible. Si vos charges réelles > 30%, vous payez trop d'impôt.

### Régime réel

Obligatoire au-delà de 15 000 € bruts ou sur option irrévocable pour 3 ans.

**Charges déductibles** :
- Intérêts d'emprunt (imputables uniquement sur les revenus fonciers)
- Travaux d'entretien, réparation, amélioration (pas construction, pas agrandissement)
- Taxe foncière (hors TEOM récupérable)
- Primes d'assurance (PNO, GLI)
- Frais de gestion (agence, syndic fraction non récupérable)
- Provisions pour charges de copropriété

**Piège travaux** : les travaux de construction, reconstruction, agrandissement **NE SONT PAS** déductibles des revenus fonciers — ils majorent seulement le prix d'acquisition pour la future plus-value.

### Déficit foncier

Voir `data/regimes-fonciers-lmnp.json` → `regime_reel_foncier.deficit_foncier`.

**Mécanisme** :
- Charges > recettes → déficit
- **Imputable sur le revenu global dans la limite de 10 700 €** par an (art. 156, I, 3° CGI ; BOI-RFPI-BASE-30-20, version du 16/09/2025)
- **Limite rehaussée à 21 400 €**, sur option à la 2044, du montant des dépenses de rénovation énergétique qui font passer le logement d'une classe E, F ou G à A, B, C ou D : devis accepté depuis le 05/11/2022, dépenses payées du 01/01/2023 au 31/12/2025, prorogé pour les dépenses payées jusqu'au 31/12/2027 (LFI 2026 art. 47) ; deux DPE à fournir. Ce n'est pas un « doublement » automatique.
- Au-delà : reportable sur les revenus fonciers des **10 années suivantes** ; si le revenu global ne suffit pas, l'excédent forme un déficit global reportable six ans
- **Intérêts d'emprunt** : la part du déficit qui provient des intérêts n'est jamais imputable sur le revenu global. Mais **les loyers sont réputés couvrir d'abord les intérêts** (§ 110) : seule la fraction des intérêts qui excède les loyers forme une part « intérêts ». Exemple : loyers 15 000 €, intérêts 6 000 €, autres charges 22 000 € : déficit de 13 000 € entièrement dû aux autres charges, 10 700 € sur le revenu global, 2 300 € reportés.
- Cases 2042 : 4BA (bénéfice), 4BB (déficit imputable sur les revenus fonciers), 4BC (déficit imputable sur le revenu global), 4BD (déficits antérieurs), annexe 2044.

**Stratégie d'optimisation** :
- Concentrer les travaux importants sur une année → déficit imputable sur revenu global
- **Condition** : louer nu le bien jusqu'au 31 décembre de la troisième année qui suit l'année d'imputation (§ 20) ; une vente, une reprise pour soi ou un passage en meublé avant cette date fait réintégrer le déficit imputé

### Amortissement « bailleur privé » (acquisitions du 21/02/2026 au 31/12/2028)

Nouveau dispositif de la LFI 2026 (art. 47 ; art. 31, I, 1°, i et j CGI) : pour un logement dans un bâtiment d'habitation collectif acquis en vue d'une location nue (neuf, ou ancien avec des travaux d'au moins 30 % du prix), déduction des revenus fonciers d'un amortissement de 3,5 % (neuf) ou 3 % (ancien réhabilité), majoré pour les loyers sociaux, sur une base hors foncier forfaitaire de 20 %, plafonnée à 8 000 € par an et par foyer (majorée de 2 000 ou 4 000 € selon le loyer). Engagement de location nue en résidence principale pendant neuf ans, hors famille proche, sous plafonds de loyers et de ressources. À la revente, les amortissements déduits sont retranchés du prix d'acquisition (art. 150 VB, III). Interaction avec le micro-foncier et le déficit foncier, plafonds de loyers et de ressources : à vérifier au BOFiP (non commenté au 29/10/2026) avant tout calcul.

## LMNP (Location Meublée Non Professionnelle)

### Régime micro-BIC

Voir `data/regimes-fonciers-lmnp.json` → `micro_bic_lmnp`.

**Réforme loi Le Meur (nov. 2024), applicable revenus 2025** — la distinction clé est désormais **classé / non classé**, plus résidence principale.

| Type de location | Seuil revenus 2025 | Seuil revenus 2026 à 2028 | Abattement | Case 2042 C PRO (2026) |
|------------------|-------|-------|-----------|-----------|
| Autres locations meublées (longue durée, bail mobilité) | 77 700 € | 83 600 € | 50% | 5NI / 5OI / 5PI |
| Meublé de tourisme classé, chambres d'hôtes | 77 700 € | 83 600 € | 50% | 5NG / 5OG / 5PG |
| **Meublé de tourisme non classé** | **15 000 €** | **15 000 €** | **30%** | 5NH / 5OH / 5PH |

Seuils 2026-2028 : BOI-BAREME-000044 (version du 19/08/2026). Le micro reste applicable si le seuil n'est pas dépassé en N-1 ou en N-2 ; régime réel obligatoire après deux années consécutives de dépassement (brochure IR 2026, revenus non salariés). La case 5ND n'existe plus.

### Régime réel LMNP

**Principe** : résultat BIC = recettes − charges − **amortissements**.

**Amortissements** :
- Bien immobilier : 2-3%/an sur 25-40 ans (hors terrain, terrain non amortissable)
- Mobilier : 10-20%/an sur 5-10 ans
- Gros travaux : amortissables sur leur durée d'usage

**Résultat fiscal** : souvent nul grâce aux amortissements → pas d'IR sur les loyers pendant des années. Mais les amortissements ne peuvent ni créer ni augmenter un déficit (art. 39 C, II CGI ; BOI-BIC-CHAMP-40-20 § 57) : la part non déduite est reportée sans limite de durée, et un déficit LMNP ne peut provenir que des charges.

**Déficit LMNP** : NON imputable sur le revenu global (contrairement au LMP). Reportable sur les seuls bénéfices de location meublée non professionnelle des **10 années suivantes** (art. 156, I, 1° ter CGI), pas sur d'autres BIC.

**Reprise à la revente** : pour les cessions réalisées depuis le 15/02/2025, les amortissements déduits au réel sont **retranchés du prix d'acquisition** dans le calcul de la plus-value des particuliers (art. 150 VB, III CGI ; LF 2025 art. 84), sauf résidences étudiantes, seniors et médico-sociales. L'arbitrage micro / réel doit intégrer cette reprise : l'économie d'IR pendant la location est en partie reprise au taux de 19 % + 17,2 % (moins les abattements pour durée de détention).

**Formalités** : déclaration de début d'activité au guichet unique dans les 15 jours (numéro SIRET) ; au réel, liasse 2031 et annexes 2033 ; CFE possible (service-public F32744).

### Bascule LMP vs LMNP

Voir `data/regimes-fonciers-lmnp.json` → `lmp_vs_lmnp`. Source : art. 155, IV, 2 CGI ; BOI-BIC-CHAMP-40-10 ; brochure IR 2026, revenus non salariés.

**Conditions LMP (cumulatives)** :
1. Recettes meublées du foyer > 23 000 €
2. ET recettes meublées > **total** des autres revenus d'activité du foyer : traitements et salaires au sens de l'art. 79 CGI (**y compris pensions et rentes viagères**, et rémunérations de l'art. 62), BIC hors location meublée, BA, BNC. Ce n'est pas « 50 % » : avec 24 000 € de recettes et 40 000 € de salaires, on reste LMNP.

**Conséquences LMP** :
- Déficits imputables sur le revenu global sans limitation de montant
- Plus-values professionnelles : court terme à hauteur des amortissements déduits, long terme au-delà ; exonération art. 151 septies si activité exercée depuis au moins cinq ans et recettes < 90 000 € (totale) ou < 126 000 € (partielle)
- Cotisations sociales TNS sur le bénéfice (SSI), charge significative ; la location meublée de courte durée au-delà de 23 000 € de recettes y est soumise même en LMNP (art. L. 611-1, 6° CSS)
- IFI : exonération des locaux loués meublés sous des critères **propres** (art. 975, V, 1° CGI ; BOI-PAT-IFI-30-10-10-10 § 60) : recettes > 23 000 € ET bénéfice commercial net (après amortissements) > 50 % des revenus nets d'activité du foyer, ce bénéfice compris, et profession principale (exclu en général pour un salarié à plein temps, BOI-PAT-IFI-30-10-10-30 § 20). Le statut LMP à l'IR ne suffit pas.

**Attention bascule involontaire** : une baisse des autres revenus d'activité peut faire basculer en LMP malgré des loyers inchangés. Les pensions comptent parmi ces revenus : c'est l'arrêt de toute activité sans pension (par exemple une retraite anticipée financée par l'épargne, ou une année sans salaire ni ARE) qui fait basculer. À surveiller chaque année.

## SCI à l'IR

Voir `data/regimes-fonciers-lmnp.json` → `sci_ir`.

**Régime par défaut** : transparence fiscale.

- Les revenus et charges remontent directement dans la déclaration de chaque associé au prorata des parts
- Nature fiscale : revenus fonciers classiques (micro ou réel selon le total fonciers du foyer)
- Cession des parts ou du bien : régime des plus-values immobilières des particuliers
- L'amortissement **n'est PAS possible** (contrairement à la SCI à l'IS)

**Quand choisir SCI IR** :
- Transmission patrimoniale (démembrement, donation de parts)
- Location nue (meublé en SCI = risque de requalification IS)
- Détention longue (exonération PV immo à 22 ans IR / 30 ans PS)

**Quand choisir SCI IS (hors scope)** :
- Fort rendement locatif et réinvestissement
- Possibilité d'amortir le bien
- Piège : à la cession, PV calculée sur valeur nette comptable (après amortissements) → imposition forte

→ Pour SCI à l'IS, voir skill `comptable`.

## Formulaires

| Régime | Formulaire |
|--------|-----------|
| Micro-foncier | 2042 case 4BE |
| Régime réel foncier | 2044 (ou 2044 spéciale) |
| Micro-BIC LMNP | 2042 C-PRO (cases 5ND, 5NG, etc.) |
| Réel LMNP / LMP | 2031 + 2033 (liasse BIC) + 2042 C-PRO |
| SCI IR | Déclaration 2072 (SCI) + report sur 2044 (associés) |

## Références CGI / BOFiP

- Revenus fonciers : art. 14 à 33 quater CGI
- Déficit foncier : art. 156-I-3° CGI
- LMNP : art. 35-I-5° bis CGI
- LMP : art. 155-IV CGI
- SCI : art. 8 CGI (transparence)
- BOFiP : BOI-RFPI (fonciers) et BOI-BIC-CHAMP-40 (meublés)
