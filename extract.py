import os
import pdfplumber
import json
from dotenv import load_dotenv
from anthropic import Anthropic

# Note: Le client Anthropic sera initialisé dynamiquement


def get_anthropic_client():
    """Obtient le client Anthropic avec la clé API depuis Streamlit secrets ou environnement"""
    try:
        import streamlit as st
        api_key = st.secrets.get("CLAUDE_API_KEY")
    except:
        api_key = os.getenv("CLAUDE_API_KEY")
    
    if not api_key:
        raise ValueError("CLAUDE_API_KEY non trouvée dans secrets ou environnement")
    
    return Anthropic(api_key=api_key)


def lire_pdf(path):
    """Extrait le texte brut d'un PDF"""
    texte = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                texte += page.extract_text() + "\n"
    return texte


def extraire_donnees_ia(texte_pdf, nom_fichier=""):
    """Envoie le texte PDF à Claude AI et récupère un JSON structuré selon la structure Excel"""

    prompt = f"""Tu es un assistant spécialisé dans les formulaires énergétiques du canton du Valais.
Analyse le texte fourni et extrait TOUTES les données disponibles selon la structure complète ci-dessous.

IMPORTANT : Renvoie UNIQUEMENT un JSON valide, sans texte explicatif.

INSTRUCTIONS D'EXTRACTION :

1. NUMÉRO DE DOSSIER :
   - Cherche dans le nom du fichier : {nom_fichier}
   - Format attendu : "YYYY-XXXX" (ex: 2023-425, 2025-1234)
   - Peut aussi être mentionné dans le document

2. IDENTIFICATION DES FORMULAIRES :
   - Les formulaires sont identifiés par leur code : EN-VS, EN-VS-101a, EN-VS-101b, EN-VS-102a, EN-VS-102b, EN-VS-103, EN-VS-104, EN-VS-105, EN-VS-110
   - Extrait les données de CHAQUE formulaire présent dans le document
   - IMPORTANT : Il ne peut y avoir qu'UN SEUL des formulaires 102 (soit 102a, soit 102b, pas les deux)

3. SOLUTION STANDARD EN-VS-101a (TRÈS IMPORTANT) :
   Le formulaire EN-VS-101a contient un tableau de solutions standards.

   STRUCTURE DU TABLEAU :
   - En-tête : Lettres A, B, C, D, E (de gauche à droite)
   - Lignes : Numéros 1, 2, 3, 4 (de haut en bas)
   - Une seule case est cochée avec le symbole ●

   MÉTHODE D'EXTRACTION PRÉCISE :

   ÉTAPE 1 - IDENTIFIER LA LIGNE (facile) :
   Cherche la case cochée, va tout à gauche du tableau et monte légèrement pour trouver un chiffre

   ÉTAPE 2 - IDENTIFIER LA COLONNE (attention aux détails) :
   Cherche la case cochée, va tout eu haut du tableau et, puis légèrement à droite pour trouver une lettre.

   RÉSULTAT : Combine ligne + colonne (exemple: "3C" = ligne 3, colonne C)
   
   ASTUCE IMPORTANTE : 
   - Il n'y a pas de solutions standards 1E, 3D, 3E, 4E.


4. ÉLÉMENTS D'ENVELOPPE (TRÈS IMPORTANT) :
   - Les éléments doivent être séparés en DEUX listes distinctes

   A) ÉLÉMENTS OPAQUES (elements_enveloppe_opaques) :
      - Types : mur, toit, plafond, sol, dalle, caisson de store
      - Champs à extraire :
        * element : nom/description de l'élément
        * valeur_u : valeur U en W/m²K
        * valeur_u_limite : valeur U limite en W/m²K
        * couches_isolation : string décrivant toutes les couches d'isolation
          Format : "épaisseur cm de TYPE (λ = valeur W/mK) + épaisseur cm de TYPE (λ = valeur W/mK)"
          Exemples :
            - Une seule couche : "10 cm de laine minérale (λ = 0.035 W/mK)"
            - Plusieurs couches : "2 cm d'EPS 30 (λ = 0.033 W/mK) + 4 cm d'EPS 150 (λ = 0.035 W/mK) + 10 cm d'XPS (λ = 0.032 W/mK)"
          Si pas d'info : null

   B) ÉLÉMENTS VITRÉS (elements_enveloppe_vitres) :
      - Types : fenêtre, porte-fenêtre, velux, porte, baie vitrée
      - Champs à extraire :
        * element : nom/description de l'élément
        * valeur_ug : Ug du vitrage (coefficient U du vitrage seul) en W/m²K - aussi noté Us
        * valeur_uf : Uf du cadre (coefficient U du cadre) en W/m²K - si disponible, sinon null
        * valeur_uw : Uw de la fenêtre complète (vitrage + cadre) en W/m²K
        * valeur_u_limite : valeur U limite en W/m²K
        * facteur_g : facteur g (transmission énergétique solaire) - aussi noté Gp - valeur entre 0 et 1 - si disponible, sinon null


4. CASES COCHÉES ET OPTIONS :
   - Symboles : ☑, ✓, ✔, X, ●, ○ (rempli), [X], case cochée
   - "Oui/Non" → boolean (true/false)
   - Si case non cochée ou vide → null

5. VALEURS NUMÉRIQUES :
   - Extraire UNIQUEMENT le nombre (pas l'unité)
   - Surfaces (SRE) en m²
   - Puissances en kW, kWc ou W
   - Débits en m³/h
   - Rendements en %

Structure JSON complète attendue :

{{
  "numero_dossier": "string ou null",

  "EN-VS": {{
    "nature_des_travaux": "string ou null",
    "type_de_construction": "string ou null",
    "sre_neuf": "number ou null",
    "sre_existant": "number ou null",
    "categorie_sia": "string ou null",
    "type_de_chauffage": "string ou null",
    "couverture_des_besoins_de_chaleur": "string ou null",
    "formulaires_necessaires_ou_annexes": []
  }},

  "EN-VS-101a": {{
    "rafraichissement_humidification_ou_deshumidification": "boolean ou null",
    "pac_reversible_projetee": "boolean ou null",
    "solution_standard_choisie": "string (format: '1A', '2B', '3C', '4D', etc.) ou null"
  }},

  "EN-VS-102a": {{
    "hygiene_air_interieur_concept_ventilation": "string ou null",
    "protection_thermique_ete_valeur_g": "string ou null",
    "commande_automatique_protections_solaires": "boolean ou null",
    "protection_thermique_ete_rafraichissement": "boolean ou null",
    "elements_enveloppe_opaques": [
      {{
        "element": "string (mur, toit, sol, caisson de store)",
        "valeur_u": "number ou null",
        "valeur_u_limite": "number ou null",
        "couches_isolation": "string décrivant toutes les couches ou null"
      }}
    ],

    "elements_enveloppe_vitres": [
      {{
        "element": "string (fenêtre, porte-fenêtre, velux, porte)",
        "valeur_ug": "number ou null",
        "valeur_uf": "number ou null",
        "valeur_uw": "number ou null",
        "valeur_u_limite": "number ou null",
        "facteur_g": "number ou null"
      }}
    ],

    "valeurs_u_respectees_par_tous_elements": "boolean ou null",
    "justificatif_ponts_thermiques_respecte": "boolean ou null",
    "enveloppe_thermique_completement_fermee": "boolean ou null",
    "tous_locaux_chauffes_interieur_enveloppe": "boolean ou null",
    "check_list_ponts_thermiques_neuf": "string ou null"
  }},

  "EN-VS-103": {{
    "rafraichissement_humidification_ou_deshumidification": "boolean ou null",
    "pac_reversible_projetee": "boolean ou null",
    "type_de_generateur_de_chaleur": "string ou null",
    "puissance_thermique_kw": "number ou null",
    "dispositif_comptage_energie": "boolean ou null",
    "emission_chaleur_locaux_isoles": "boolean ou null",
    "emission_de_chaleur": "string ou null (si doute, mettre 'Surfaces chauffantes')",
    "temperature_emission_chaleur": "string ou null",
    "regulation_temperature_par_local": "string ou null (si doute, mettre 'Electronique avec sonde d'ambiance par local')",
    "temperature_ecs_inferieure_60": "boolean ou null",
    "nombre_unites_occupation": "number ou null",
    "systeme_mesure_installe_chauffage": "boolean ou null",
    "systeme_mesure_installe_ecs": "boolean ou null"
  }},

  "EN-VS-104": {{
    "puissance_production_propre_electricite_annuelle": "number ou null",
    "puissance_production_propre_electricite_requise": "number ou null",
    "nbre_de_panneaux": "number ou null",
    "punitaire_des_panneaux_wc": "number ou null"
  }},

  "EN-VS-110": {{
    "surface_nette_plancher_rafraichi_deshumidifie": "number ou null",
    "total_puissances_thermiques_frigorifiques": "number ou null",
    "puissances_electriques_total_kw": "number ou null",
    "puissances_electriques_puissance_specifique_w_m2": "number ou null"
  }},

  "EN-VS-105": {{
    "genre_type_installation": "string ou null",
    "air_recycle": "boolean ou null",
    "debits_maximums_air_fourni_fou": "number ou null",
    "debits_maximums_air_repris_rep": "number ou null",
    "chauffage_de_air": "boolean ou null",
    "rafraichissement_deshumidification": "boolean ou null",
    "dispositif_comptage_energie": "boolean ou null",
    "recuperation_chaleur_rc_technique_rc": "string ou null",
    "rendement_rc_solution_standard": "number ou null"
  }},

  "EN-VS-102b": {{
    "besoins_chaleur_chauffage_projet_qh": "number ou null",
    "besoins_chaleur_chauffage_projet_qh_li": "number ou null",
    "puissance_chauffage_specifique_ph": "number ou null",
    "puissance_chauffage_specifique_ph_li": "number ou null",
    "hygiene_air_interieur_concept_ventilation": "string ou null",
    "protection_thermique_ete_valeur_g": "string ou null",
    "commande_automatique_protections_solaires": "boolean ou null",
    "protection_thermique_ete_rafraichissement": "boolean ou null",
    "elements_enveloppe_opaques": [
      {{
        "element": "string (mur, toit, sol, caisson de store)",
        "valeur_u": "number ou null",
        "valeur_u_limite": "number ou null",
        "couches_isolation": "string décrivant toutes les couches ou null"
      }}
    ],

    "elements_enveloppe_vitres": [
      {{
        "element": "string (fenêtre, porte-fenêtre, velux, porte)",
        "valeur_ug": "number ou null",
        "valeur_uf": "number ou null",
        "valeur_uw": "number ou null",
        "valeur_u_limite": "number ou null",
        "facteur_g": "number ou null"
      }}
    ]
  }},

  "EN-VS-101b": {{
    "valeur_limite_ehwlk_exigences": "number ou null",
    "valeur_limite_ehwlk_valeur_calculee": "number ou null",
    "valeur_limite_ehwlk_respectee": "boolean ou null"
  }}
}}

RÈGLES D'EXTRACTION :
- Si un formulaire n'est PAS présent dans le document, ne pas inclure sa section dans le JSON
- Si une donnée n'est pas trouvée dans un formulaire présent, mettre null
- Pour les booléens : "Oui"/"✓"/"☑" = true, "Non"/"✗" = false, non trouvé = null
- Toutes les valeurs numériques doivent être des nombres (pas de strings, pas d'unités)
- Les listes vides sont acceptées si aucun élément trouvé
- Ne pas inventer de données : si absent = null
- IMPORTANT : Ne jamais inclure les deux formulaires EN-VS-102a ET EN-VS-102b. Un seul peut être présent.

EXEMPLE POUR EN-VS-101a :
Si dans le tableau tu trouves :
- Une coche (●) à la ligne 3 (celle avec "0,15" et "1,00")
- Sous l'en-tête "Chauffage à distance d'UIOM, STEP..." (colonne C - la colonne du MILIEU)

Alors le résultat doit être :
{{
  "EN-VS-101a": {{
    "rafraichissement_humidification_ou_deshumidification": false,
    "pac_reversible_projetee": false,
    "solution_standard_choisie": "3C"
  }}
}}

VÉRIFICATION : 
- "3C" signifie : ligne 3 (0,15 W/m²K + Uw 1,00) + colonne C (chauffage à distance)
- Si tu vois "UIOM" ou "STEP" dans le texte, c'est FORCÉMENT la colonne C
- Ne confonds pas avec la colonne A (sol-eau) ou D (air-eau)

ATTENTION : La solution standard doit être au format "chiffre+lettre" (exemples : "1A", "2B", "3C", "4D")
Ne pas écrire des phrases longues, juste le code "XY" où X = numéro ligne (1-4) et Y = lettre colonne (A-E).

EXTRACTION SPÉCIFIQUE POUR EN-VS-101b :
- "valeur_limite_ehwlk_exigences" : Cherche "EHWLK,li" ou "limite" dans le tableau
- "valeur_limite_ehwlk_valeur_calculee" : Cherche "EHWLK" calculé ou projet dans le tableau
- "valeur_limite_ehwlk_respectee" : Vérifie si case cochée pour "respectée"

EXTRACTION COMMANDE AUTOMATIQUE DES PROTECTIONS SOLAIRES (EN-VS-102a et EN-VS-102b) :
- Cherche dans la section "Protection thermique été"
- Ligne "Commande automatique des protections solaires" ou similaire
- Peut être formulé comme "Stores à commande automatique" ou "Protections solaires commandées automatiquement"
- Si case cochée = true, sinon = false, si absent = null
- IMPORTANT : Ce champ doit TOUJOURS être présent dans EN-VS-102a et EN-VS-102b, même s'il est null

EXTRACTION FORMULAIRES ANNEXÉS (EN-VS) :
- Cherche dans la section "Formulaires nécessaires ou annexes"
- Liste TOUS les formulaires mentionnés (EN-VS-101a, EN-VS-101b, EN-VS-102a, EN-VS-102b, EN-VS-103, EN-VS-104, EN-VS-105, EN-VS-110)
- Vérifie que les formulaires listés sont effectivement présents dans le document
- Ne liste que les formulaires dont tu peux confirmer la présence
- Format : liste de strings ["EN-VS-101a", "EN-VS-103", etc.]

EXTRACTION EN-VS-103 - VALEURS PAR DÉFAUT SI DOUTE :
- "emission_de_chaleur" : Si le texte n'est pas clair ou absent, mettre "Surfaces chauffantes"
- "regulation_temperature_par_local" : Si le texte n'est pas clair ou absent, mettre "Electronique avec sonde d'ambiance par local"
- Ces valeurs par défaut ne doivent être utilisées QUE si le formulaire EN-VS-103 est présent mais que ces champs spécifiques sont flous ou absents

Nom du fichier : {nom_fichier}

Texte du PDF :
{texte_pdf}

Réponds UNIQUEMENT avec le JSON complet, sans markdown ni commentaires."""

    try:
        response = get_anthropic_client().messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        texte_reponse = response.content[0].text.strip()

        # Nettoyer le markdown si présent
        if texte_reponse.startswith("```"):
            lignes = texte_reponse.split("\n")
            texte_reponse = "\n".join(lignes[1:-1]) if len(lignes) > 2 else texte_reponse

        # Valider le JSON
        json.loads(texte_reponse)
        return texte_reponse

    except json.JSONDecodeError as e:
        return json.dumps({
            "erreur": "Réponse JSON invalide",
            "details": str(e),
            "reponse_brute": texte_reponse if 'texte_reponse' in locals() else "N/A"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "erreur": "Erreur API",
            "details": str(e)
        }, ensure_ascii=False)


def sauvegarder_json(json_data, chemin_sortie=None):
    """Sauvegarde le JSON dans un fichier"""
    if chemin_sortie is None:
        chemin_sortie = "extraction_formulaire.json"

    with open(chemin_sortie, 'w', encoding='utf-8') as f:
        json.dump(json.loads(json_data), f, ensure_ascii=False, indent=2)

    print(f"💾 Données sauvegardées dans : {chemin_sortie}")
    return chemin_sortie


def analyser_completude(json_data):
    """Analyse la complétude des données extraites"""
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    def compter_non_null(obj, chemin=""):
        count = 0
        total = 0
        details = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                sous_count, sous_total, sous_details = compter_non_null(value, f"{chemin}.{key}" if chemin else key)
                count += sous_count
                total += sous_total
                details.extend(sous_details)
        elif isinstance(obj, list):
            if len(obj) > 0:
                count = 1
                total = 1
                details.append((chemin, True))
            else:
                total = 1
                details.append((chemin, False))
        else:
            total = 1
            if obj is not None:
                count = 1
                details.append((chemin, True))
            else:
                details.append((chemin, False))

        return count, total, details

    remplis, total, details = compter_non_null(data)

    print("\n=== ANALYSE DE COMPLÉTUDE ===")
    print(f"Champs remplis : {remplis}/{total} ({100 * remplis / total:.1f}%)")

    print("\n=== CHAMPS NON REMPLIS ===")
    for chemin, rempli in details:
        if not rempli:
            print(f"  ❌ {chemin}")

    print("\n=== CHAMPS REMPLIS ===")
    for chemin, rempli in details:
        if rempli:
            print(f"  ✅ {chemin}")

    return remplis, total


# Exemple d'utilisation
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        chemin_pdf = sys.argv[1]
    else:
        chemin_pdf = "exemple_formulaire.pdf"

    if not os.path.exists(chemin_pdf):
        print(f"❌ Fichier non trouvé : {chemin_pdf}")
        sys.exit(1)

    print(f"📄 Traitement du fichier : {chemin_pdf}")
    nom_fichier = os.path.basename(chemin_pdf)

    print("📖 Lecture du PDF...")
    texte = lire_pdf(chemin_pdf)
    print(f"   → {len(texte)} caractères extraits")

    print("🤖 Extraction des données avec Claude AI...")
    json_resultat = extraire_donnees_ia(texte, nom_fichier)

    try:
        data = json.loads(json_resultat)
        if "erreur" in data:
            print(f"❌ Erreur : {data['erreur']}")
            print(f"   Détails : {data.get('details', 'N/A')}")
        else:
            print("✅ Extraction réussie")
            nom_sortie = chemin_pdf.replace('.pdf', '_extraction.json')
            sauvegarder_json(json_resultat, nom_sortie)
            analyser_completude(json_resultat)

    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON : {e}")
        print("Réponse brute :", json_resultat[:500])
