#!/usr/bin/env python3
"""
Calculateur IR déterministe pour revenus 2025 (déclaration 2026).

Usage:
    # Calcul direct
    python fiscaliste/scripts/calc_ir.py --parts 1 --rni 45000

    # Via fichier foyer.json
    python fiscaliste/scripts/calc_ir.py --foyer foyer.example.json

    # Sortie JSON
    python fiscaliste/scripts/calc_ir.py --parts 2 --rni 90000 --json

    # Projection des encaissements 2026 (PS 18,6 % aussi sur dividendes et intérêts)
    python fiscaliste/scripts/calc_ir.py --foyer foyer.json --annee-revenus 2026

Couvre :
    - Abattement 10 % salaires (plancher et plafond par déclarant, salaires + ARE
      de chaque déclarant) et pensions (plancher par pensionné, plafond par foyer)
    - Barème progressif tranche par tranche
    - Quotient familial (avec plafonnement général par demi-part)
    - Décote célibataire / couple
    - Revenus du capital au PFU : IR 12,8 % + PS différenciés LFSS 2026
      (18,6 % revenus du patrimoine : PV mobilières, crypto, LMNP ; 17,2 % produits
      de placement encaissés en 2025, 18,6 % à partir de 2026 : dividendes, intérêts)
    - Option barème (options_fiscales.revenus_capital = "bareme") : dividendes après
      abattement de 40 %, intérêts et plus-values ajoutés au revenu global, PS inchangés,
      CSG déductible (6,8 %) des dividendes et intérêts à PS prélevés à la source
      déduite du revenu global de l'année même (ligne 2BH)
    - Crypto : option distincte pour le barème (options_fiscales.crypto = "bareme",
      case 3CN, art. 200 C CGI), indépendante de la 2OP
    - PS 17,2 % sur les revenus fonciers nets positifs (taux maintenu, L. 136-8 IV CSS)
    - RFR approché : RNI + cotisations PER réintégrées + revenus au PFU
      + abattement de 40 % si option barème (art. 1417, IV CGI)
    - CEHR

Ne couvre PAS :
    - Réductions / crédits d'impôt (à retrancher manuellement après)
    - CDHR (plancher de 20 %, voir references/cas-speciaux.md)
    - Régimes spéciaux : quotient des revenus exceptionnels, non-résidents
      (taux minimum, pas de décote, PS selon affiliation), DOM-TOM
    - Plafonds spécifiques du QF (parent isolé 4 262 €, veuf, case L)
    - Contrôle du plafond de déduction PER (le versement est déduit tel quel)
    - Champs equity_salarial, micro_bnc_recettes, bnc_regime_normal du foyer.json
    - CSG déductible de l'année suivante (plus-values, crypto, RCM sans PS à la
      source) en cas d'option barème
    - IFI (script distinct à créer si besoin)

Les valeurs viennent de data/bareme-ir-2025.json et data/pfu-prelevements-sociaux.json.
Pour une autre année de barème, exposer --bareme data/bareme-ir-XXXX.json.
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
DEFAULT_BAREME = DATA_DIR / "bareme-ir-2025.json"
DEFAULT_PFU = DATA_DIR / "pfu-prelevements-sociaux.json"
TAUX_PS_FONCIER = 0.172  # revenus fonciers : CSG maintenue à 9,2 % (L. 136-8, IV CSS)


def load_json(path):
    with open(path) as f:
        return json.load(f)


# ─────────────────────────────────────────────────────
# Abattement salaires / pensions
# ─────────────────────────────────────────────────────

def abattement_salaires(brut_1aj, bareme):
    """Revenu net d'un déclarant après la déduction forfaitaire de 10 %.

    Le plancher et le plafond s'appliquent séparément à chaque membre du foyer
    (art. 83-3° CGI) ; l'abattement ne peut pas dépasser le revenu lui-même.
    Passer ici salaires + ARE d'un même déclarant.
    """
    if brut_1aj <= 0:
        return 0
    cfg = bareme["abattement_salaires_10pct"]
    abatt = max(cfg["minimum"], min(cfg["maximum"], brut_1aj * cfg["taux"]))
    abatt = min(abatt, brut_1aj)
    return round(brut_1aj - abatt)


def abattement_pensions(pensions, bareme):
    """Revenu net de pensions du foyer après la déduction de 10 %.

    `pensions` : liste des pensions brutes imposables, une par pensionné.
    Le plancher s'apprécie par pensionné, le plafond sur l'ensemble des pensions
    du foyer (art. 158, 5-a CGI).
    """
    cfg = bareme["abattement_pensions_10pct"]
    total = sum(p for p in pensions if p > 0)
    if total <= 0:
        return 0
    abatt = 0.0
    for p in pensions:
        if p > 0:
            abatt += min(p, max(cfg["minimum"], p * cfg["taux"]))
    abatt = min(abatt, cfg["maximum"])
    return round(total - abatt)


# ─────────────────────────────────────────────────────
# Barème progressif (tranche par tranche, sur 1 part)
# ─────────────────────────────────────────────────────

def impot_par_part(quotient, tranches):
    """Calcule l'impôt sur un quotient (1 part) en appliquant les tranches."""
    impot = 0.0
    for t in tranches:
        taux = t["taux"]
        # cas "jusqu_a" (première tranche à 0%)
        if "jusqu_a" in t and "de" not in t:
            borne_basse = 0
            borne_haute = t["jusqu_a"]
        elif "au_dela" in t:
            borne_basse = t["au_dela"]
            borne_haute = float("inf")
        else:
            borne_basse = t["de"]
            borne_haute = t["a"]

        if quotient <= borne_basse:
            break
        base = min(quotient, borne_haute) - borne_basse
        impot += base * taux

    return impot


# ─────────────────────────────────────────────────────
# Décote
# ─────────────────────────────────────────────────────

def decote(impot_brut, parts, bareme):
    """Applique la décote si éligible. Retourne le montant de décote."""
    cfg = bareme["decote"]
    if parts <= 1:
        seuil = cfg["seuil_celibataire"]
        plafond = cfg["plafond_celibataire"]
    else:
        seuil = cfg["seuil_couple"]
        plafond = cfg["plafond_couple"]

    if impot_brut >= seuil:
        return 0.0
    return max(0.0, plafond - 0.4525 * impot_brut)


# ─────────────────────────────────────────────────────
# Quotient familial avec plafonnement
# ─────────────────────────────────────────────────────

def impot_avec_qf(rni, parts_total, parts_base, bareme):
    """
    Applique le QF avec plafonnement.
    - parts_total : parts foyer (ex: couple + 2 enfants = 3)
    - parts_base : parts foyer sans enfants (ex: couple = 2, célib = 1)
    """
    tranches = bareme["bareme_ir"]["tranches"]
    plafond_demi = bareme["quotient_familial"]["plafond_gain_par_demi_part"]

    # Impôt avec toutes les parts
    impot_total = impot_par_part(rni / parts_total, tranches) * parts_total
    # Impôt sans les enfants (référence)
    impot_sans = impot_par_part(rni / parts_base, tranches) * parts_base

    gain_reel = impot_sans - impot_total
    nb_demi_parts = (parts_total - parts_base) * 2
    gain_max = nb_demi_parts * plafond_demi

    if gain_reel > gain_max:
        # Plafonné : impôt = impôt_sans_enfants − gain_max
        impot_brut = impot_sans - gain_max
        qf_plafonne = True
    else:
        impot_brut = impot_total
        qf_plafonne = False

    return {
        "impot_brut": round(impot_brut),
        "impot_total_parts": round(impot_total),
        "impot_base_parts": round(impot_sans),
        "gain_qf_reel": round(gain_reel),
        "gain_qf_max": round(gain_max),
        "qf_plafonne": qf_plafonne,
    }


# ─────────────────────────────────────────────────────
# CEHR
# ─────────────────────────────────────────────────────

def cehr(rfr, parts_base, bareme):
    cfg = bareme["cehr"]
    seuils = cfg["seuils_couple"] if parts_base >= 2 else cfg["seuils_celibataire"]
    total = 0.0
    for t in seuils:
        taux = t["taux"]
        if "au_dela" in t:
            if rfr > t["au_dela"]:
                total += (rfr - t["au_dela"]) * taux
        else:
            if rfr > t["de"]:
                base = min(rfr, t["a"]) - t["de"]
                total += base * taux
    return round(total)


# ─────────────────────────────────────────────────────
# Revenus du capital : IR au PFU et PS
# ─────────────────────────────────────────────────────

def taux_ps(pfu_data, annee_revenus=2025):
    """Taux de PS par nature de revenu pour une année d'encaissement donnée.

    - Revenus du patrimoine (PV mobilières CTO, crypto, LMNP) : 18,6 % dès
      les revenus 2025 (L. 136-6 CSS).
    - Produits de placement (dividendes, intérêts) : 17,2 % pour les
      encaissements 2025, 18,6 % à partir du 01/01/2026 (L. 136-7 CSS).
    - Revenus fonciers : 17,2 % maintenus.
    """
    ps = pfu_data["prelevements_sociaux"]
    cle_placement = ("taux_produits_de_placement_2026" if annee_revenus >= 2026
                     else "taux_produits_de_placement_2025")
    return {
        "patrimoine": ps["taux_revenus_du_patrimoine_2025"]["valeur"],
        "placement": ps[cle_placement]["valeur"],
        "foncier": ps.get("taux_inchanges_17_2", {}).get("valeur", TAUX_PS_FONCIER),
    }


def ps_capital(base_patrimoine, base_placement, pfu_data, base_foncier=0,
               annee_revenus=2025):
    """PS différenciés LFSS 2026, par nature de revenu."""
    taux = taux_ps(pfu_data, annee_revenus)
    m_patrimoine = round(base_patrimoine * taux["patrimoine"])
    m_placement = round(base_placement * taux["placement"])
    m_foncier = round(base_foncier * taux["foncier"])
    return {
        "patrimoine": {"base": base_patrimoine, "taux": taux["patrimoine"], "montant": m_patrimoine},
        "placement": {"base": base_placement, "taux": taux["placement"], "montant": m_placement},
        "foncier": {"base": base_foncier, "taux": taux["foncier"], "montant": m_foncier},
        "total": m_patrimoine + m_placement + m_foncier,
    }


def ir_pfu(base, pfu_data):
    """IR forfaitaire de 12,8 % sur les revenus du capital soumis au PFU (art. 200 A CGI)."""
    if not base or not pfu_data:
        return 0
    return round(base * pfu_data["pfu"]["taux_ir"])


# ─────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────

def calc(rni, parts, parts_base, bareme, rfr=None, base_ps_patrimoine=0,
         base_ps_placement=0, pfu_data=None, base_ps_foncier=0,
         option_capital="pfu", annee_revenus=2025, avertissements=None,
         base_ir_pfu=None):
    qf = impot_avec_qf(rni, parts, parts_base, bareme)
    dec = decote(qf["impot_brut"], parts_base, bareme)
    impot_apres_decote = max(0, qf["impot_brut"] - dec)

    if (base_ps_patrimoine or base_ps_placement or base_ps_foncier) and pfu_data:
        ps_detail = ps_capital(base_ps_patrimoine, base_ps_placement, pfu_data,
                               base_foncier=base_ps_foncier, annee_revenus=annee_revenus)
    else:
        ps_detail = None
    ps = ps_detail["total"] if ps_detail else 0

    # IR à 12,8 % sur les revenus du capital, sauf option barème (ils sont alors
    # déjà dans le RNI, dividendes après abattement de 40 %). La base IR peut
    # différer de la base PS : le LMNP est au barème (déjà dans le RNI) mais
    # supporte les PS des revenus du patrimoine ; la crypto a sa propre option.
    if base_ir_pfu is None:
        base_ir_pfu = (base_ps_patrimoine + base_ps_placement) if option_capital == "pfu" else 0
    ir_forfaitaire = ir_pfu(base_ir_pfu, pfu_data)

    cehr_montant = cehr(rfr, parts_base, bareme) if rfr else 0

    return {
        "rni": rni,
        "parts": parts,
        "parts_base": parts_base,
        "quotient_par_part": round(rni / parts),
        "impot_brut_apres_qf": qf["impot_brut"],
        "qf_details": {
            "gain_qf_reel": qf["gain_qf_reel"],
            "gain_qf_max": qf["gain_qf_max"],
            "plafonne": qf["qf_plafonne"],
        },
        "decote": round(dec),
        "impot_apres_decote": impot_apres_decote,
        "option_revenus_capital": option_capital,
        "ir_pfu_12_8": ir_forfaitaire,
        "prelevements_sociaux": ps,
        "ps_details": ps_detail,
        "rfr_approx": rfr,
        "cehr": cehr_montant,
        "total_a_payer": impot_apres_decote + ir_forfaitaire + ps + cehr_montant,
        "_note": "Avant réductions et crédits d'impôt. Les additionner manuellement. CDHR non calculée.",
        "_avertissements": avertissements or [],
    }


def from_foyer(foyer, bareme, pfu_data, annee_revenus=None):
    """Déduit les paramètres à partir d'un foyer.json."""
    f = foyer["foyer"]
    r = foyer["revenus"]
    d = foyer.get("deductions", {})
    opt = foyer.get("options_fiscales", {})
    meta = foyer.get("_meta", {})
    if annee_revenus is None:
        annee_revenus = int(meta.get("annee_revenus", 2025))
    avertissements = []

    non_resident = f.get("residence_fiscale", "FR") != "FR" or "non_resident" in foyer
    if non_resident:
        avertissements.append(
            "Foyer non résident : le script applique les règles des résidents "
            "(décote). Taux minimum de l'art. 197 A CGI non géré. PS sur les revenus "
            "fonciers non calculés : 17,2 % en principe, mais seul le prélèvement de "
            "solidarité de 7,5 % est dû en cas d'affiliation à un régime de sécurité "
            "sociale de l'EEE, de Suisse ou du Royaume-Uni (art. 235 ter CGI ; "
            "art. L. 136-6, I ter CSS)."
        )

    # Parts
    situation = f.get("situation", "celibataire")
    parts_base = 2 if situation in ("marie", "pacse") else 1
    enfants = f.get("nb_enfants_charge", 0)
    enfants_alternee = f.get("nb_enfants_alternee", 0)
    # Les 2 premiers enfants = 0,5 part chacun ; à partir du 3e = 1 part
    demi_parts_enfants = 0.5 * min(enfants, 2) + 1.0 * max(0, enfants - 2)
    demi_parts_alt = 0.25 * min(enfants_alternee, 2) + 0.5 * max(0, enfants_alternee - 2)
    parts = parts_base + demi_parts_enfants + demi_parts_alt

    # Revenu net catégoriel traitements et salaires, déclarant par déclarant.
    # L'ARE est un revenu de remplacement imposé selon les règles des T&S
    # (BOI-RSA-BASE-30-50-20) : même abattement de 10 %, même plancher et même
    # plafond que les salaires, appréciés sur salaires + ARE de chaque déclarant
    # (art. 83-3° CGI : « séparément aux rémunérations perçues par chaque membre
    # du foyer fiscal »). Le champ historique `revenus_chomage` est attribué au
    # déclarant 1 quand les champs par déclarant sont absents.
    chomage1 = r.get("revenus_chomage_declarant1", r.get("revenus_chomage", 0))
    chomage2 = r.get("revenus_chomage_declarant2", 0)
    net_salaires = (abattement_salaires(r.get("salaires_declarant1", 0) + chomage1, bareme)
                    + abattement_salaires(r.get("salaires_declarant2", 0) + chomage2, bareme))

    net_pensions = abattement_pensions(
        [r.get("pensions_declarant1", 0), r.get("pensions_declarant2", 0)], bareme)

    # Revenus fonciers : déjà au net (micro post-abattement / réel post-charges).
    fonciers = r.get("revenus_fonciers_reels", 0) + r.get("revenus_fonciers_micro", 0)
    # LMNP au réel : résultat BIC non professionnel, positif seulement (revenu du patrimoine pour les PS).
    lmnp = max(0, r.get("lmnp_reel_resultat", 0))

    # Revenus du capital
    dividendes = r.get("dividendes_bruts", 0)
    interets = r.get("interets_rcm", 0)
    pv_mobilieres = r.get("plus_values_mobilieres", 0)
    crypto = r.get("crypto_plus_values", 0)
    option_capital = opt.get("revenus_capital", "pfu")
    if option_capital not in ("pfu", "bareme"):
        avertissements.append(f"options_fiscales.revenus_capital = {option_capital!r} inconnu, PFU appliqué.")
        option_capital = "pfu"
    # Les actifs numériques ont leur propre option pour le barème (art. 200 C CGI,
    # case 3CN), indépendante de la 2OP qui ne couvre que les RCM et les PV mobilières.
    option_crypto = opt.get("crypto", "pfu")
    if option_crypto not in ("pfu", "bareme"):
        avertissements.append(f"options_fiscales.crypto = {option_crypto!r} inconnu, PFU appliqué.")
        option_crypto = "pfu"
    rcm_sans_ps_source = bool(r.get("rcm_sans_ps_a_la_source", False))

    # Revenus imposables au barème
    revenu_global = net_salaires + net_pensions + fonciers + lmnp
    abattement_40 = 0
    csg_ded_annee = 0
    if option_capital == "bareme":
        abattement_40 = round(dividendes * pfu_data["dividendes_option_bareme"]["abattement"]) if pfu_data else 0
        revenu_global += (dividendes - abattement_40) + interets + pv_mobilieres
        # CSG déductible (6,8 %) des dividendes et intérêts dont les PS ont été
        # prélevés à la source en 2025 (ligne 2BH) : déduite du revenu global de
        # l'année même, automatiquement (brochure IR 2026, RCM). Pour les PS
        # établis par voie de rôle (plus-values, RCM d'un courtier étranger sans
        # 2778), la CSG n'est déductible que l'année suivante.
        if pfu_data and not rcm_sans_ps_source:
            taux_csg_ded = pfu_data["prelevements_sociaux"]["dont_csg_deductible_si_bareme"]
            csg_ded_annee = round((dividendes + interets) * taux_csg_ded)
        if pv_mobilieres or (rcm_sans_ps_source and (dividendes or interets)):
            avertissements.append(
                "Option barème : la CSG déductible (6,8 %) des plus-values mobilières "
                "et des RCM sans PS à la source s'imputera sur le revenu global de "
                "l'année suivante, non modélisée."
            )
    if option_crypto == "bareme":
        revenu_global += crypto
        avertissements.append(
            "Crypto au barème (case 3CN) : la CSG déductible (6,8 %) s'imputera sur le "
            "revenu global de l'année suivante, non modélisée."
        )

    # Déductions (PER + pension alimentaire + CSG déductible)
    per = d.get("per_declarant1", 0) + d.get("per_declarant2", 0)
    pension_alim = d.get("pension_alimentaire_enfant_majeur", 0)
    csg_ded = d.get("csg_deductible_n1", 0)
    rni = max(0, revenu_global - per - pension_alim - csg_ded - csg_ded_annee)
    if per:
        avertissements.append("Le versement PER est déduit sans contrôle du plafond (voir l'avis d'imposition N-1).")

    # Base PS sur revenus du capital, séparée par nature (LFSS 2026)
    base_ps_placement = dividendes + interets
    base_ps_patrimoine = pv_mobilieres + crypto + lmnp
    # Dividendes et intérêts non soumis aux PS à l'encaissement (établissement payeur
    # hors de France sans 2778) : PS établis par voie de rôle au titre des revenus du
    # patrimoine, 18,6 % dès les revenus 2025 (impots.gouv.fr, « Les revenus mobiliers »).
    if rcm_sans_ps_source:
        base_ps_patrimoine += base_ps_placement
        base_ps_placement = 0
    base_ps_foncier = 0 if non_resident else max(0, fonciers)

    # Base de l'IR forfaitaire de 12,8 % : revenus du capital restés au PFU.
    # Le LMNP n'en fait jamais partie (barème, déjà dans le RNI).
    base_ir_pfu = 0
    if option_capital == "pfu":
        base_ir_pfu += dividendes + interets + pv_mobilieres
    if option_crypto == "pfu":
        base_ir_pfu += crypto

    # RFR approché (art. 1417, IV CGI) : RNI + cotisations PER réintégrées
    # + revenus imposés au PFU + abattement de 40 % réintégré si option barème.
    rfr_approx = rni + per + abattement_40 + base_ir_pfu

    return calc(
        rni=rni,
        parts=parts,
        parts_base=parts_base,
        bareme=bareme,
        rfr=rfr_approx,
        base_ps_patrimoine=base_ps_patrimoine,
        base_ps_placement=base_ps_placement,
        pfu_data=pfu_data,
        base_ps_foncier=base_ps_foncier,
        option_capital=option_capital,
        annee_revenus=annee_revenus,
        avertissements=avertissements,
        base_ir_pfu=base_ir_pfu,
    )


def main():
    p = argparse.ArgumentParser(description="Calculateur IR déterministe — revenus 2025")
    p.add_argument("--rni", type=float, help="Revenu net imposable (après abattements et déductions)")
    p.add_argument("--parts", type=float, help="Nombre de parts fiscales")
    p.add_argument("--parts-base", type=float, help="Parts hors enfants (1 célib, 2 couple)")
    p.add_argument("--rfr", type=float, help="RFR pour CEHR (optionnel)")
    p.add_argument("--base-ps-patrimoine", type=float, default=0,
                   help="Revenus du patrimoine au PFU (PV mobilières, crypto) : IR 12,8 %% + PS 18,6 %% dès 2025")
    p.add_argument("--base-ps-placement", type=float, default=0,
                   help="Produits de placement au PFU (dividendes, intérêts) : IR 12,8 %% + PS 17,2 %% en 2025, 18,6 %% dès 2026")
    p.add_argument("--base-ps-foncier", type=float, default=0,
                   help="Revenus fonciers nets positifs : PS 17,2 %% (déjà inclus dans le RNI pour l'IR)")
    p.add_argument("--base-ps", type=float, default=0,
                   help="(déprécié) alias de --base-ps-placement")
    p.add_argument("--annee-revenus", type=int, default=None,
                   help="Année d'encaissement des revenus du capital (2025 par défaut ; 2026 : PS 18,6 %% sur dividendes et intérêts)")
    p.add_argument("--foyer", type=str, help="Chemin vers un foyer.json")
    p.add_argument("--bareme", type=str, default=str(DEFAULT_BAREME))
    p.add_argument("--pfu", type=str, default=str(DEFAULT_PFU))
    p.add_argument("--json", action="store_true", help="Sortie JSON")
    args = p.parse_args()

    bareme = load_json(args.bareme)
    pfu_data = load_json(args.pfu) if Path(args.pfu).exists() else None

    if args.foyer:
        foyer = load_json(args.foyer)
        result = from_foyer(foyer, bareme, pfu_data, annee_revenus=args.annee_revenus)
    else:
        if args.rni is None or args.parts is None:
            p.error("--rni et --parts requis sauf si --foyer est utilisé")
        parts_base = args.parts_base if args.parts_base else (2.0 if args.parts >= 2 else 1.0)
        result = calc(
            rni=args.rni,
            parts=args.parts,
            parts_base=parts_base,
            bareme=bareme,
            rfr=args.rfr,
            base_ps_patrimoine=args.base_ps_patrimoine,
            base_ps_placement=args.base_ps_placement + args.base_ps,
            pfu_data=pfu_data,
            base_ps_foncier=args.base_ps_foncier,
            annee_revenus=args.annee_revenus or 2025,
        )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print()
        print(f"  RNI ............................. {result['rni']:>10} €")
        print(f"  Parts ........................... {result['parts']:>10}")
        print(f"  Quotient par part ............... {result['quotient_par_part']:>10} €")
        print(f"  Impôt brut (après QF) ........... {result['impot_brut_apres_qf']:>10} €")
        qf = result["qf_details"]
        if qf["gain_qf_reel"]:
            status = "PLAFONNE" if qf["plafonne"] else "non plafonné"
            print(f"    └ gain QF réel / max .......... {qf['gain_qf_reel']:>6} / {qf['gain_qf_max']} € ({status})")
        print(f"  Décote .......................... {-result['decote']:>10} €")
        print(f"  Impôt après décote .............. {result['impot_apres_decote']:>10} €")
        if result["ir_pfu_12_8"]:
            print(f"  IR PFU 12,8 % revenus capital ... {result['ir_pfu_12_8']:>10} €")
        if result["prelevements_sociaux"]:
            det = result.get("ps_details") or {}
            for cle, libelle in (("patrimoine", "revenus patrimoine"),
                                 ("placement", "produits placement"),
                                 ("foncier", "revenus fonciers")):
                bloc = det.get(cle, {})
                if bloc.get("base"):
                    print(f"  PS {bloc['taux']*100:.1f}% {libelle:<20} {bloc['montant']:>10} €")
            print(f"  PS total ........................ {result['prelevements_sociaux']:>10} €")
        if result["cehr"]:
            print(f"  CEHR ............................ {result['cehr']:>10} €")
        print(f"  ─────────────────────────────────────────────────")
        print(f"  TOTAL (avant réductions/crédits)  {result['total_a_payer']:>10} €")
        for a in result.get("_avertissements", []):
            print(f"  ! {a}")
        print()


if __name__ == "__main__":
    main()
